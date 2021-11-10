import CoiledCoil
import SASA
import Sequence
import Chain
import CCSocket
import filemanager
import CustomExceptions
import writefile
import sys
import os
import ntpath
import signal
import FPTools as fpt
import writerhelper

if __name__ == '__main__':

    #Establish solvent radius
    if "SOLVENTRADIUS" not in os.environ:
        userSelection = input("Solvent radius is not set. "
                                            "Use radius of water? (1.4Å) [y/n]")
        if userSelection == "y":
            sRadius = 1.4
        else:
            sRadius = "a"
            while sRadius == "a":
                try:
                    num = float(input("Input solvent radius (Å)"))
                    sRadius = num
                except ValueError:
                    print("Invalid input. Must input a numerical value")
            userSelection = input("Set " + str(sRadius) + " as environment variable SOLVENTRADIUS? [y/n]")
            if userSelection == "y":
                os.environ['SOLVENTRADIUS'] = str(sRadius)
    else:
        try:
            sRadius = float(os.environ['SOLVENTRADIUS'])
        except ValueError:
            print("Environment variable SOLVENTRADIUS is not set to a numerical value.")
            sRadius = "a"
            while sRadius == "a":
                try:
                    num = float(input("Input solvent radius (Å)"))
                    sRadius = num
                    userSelection = input("Set " + str(sRadius) + " as environment variable SOLVENTRADIUS? [y/n]")
                    if userSelection == "y":
                        os.environ['SOLVENTRADIUS'] = str(sRadius)
                except ValueError:
                    print("Invalid input. Must input a numerical value")

    #Establish solvent radius
    if "NUMFIBPOINTS" not in os.environ:
        userSelection = input("Number of Fibonacci points is not set. Please input desired number of points.")
        while True:
            try:
                numPoints = int(userSelection)
                break
            except ValueError:
                userSelection = input("Invalid input. Must input a numerical value")

        userSelection = input("Set " + str(numPoints) + " as environment variable NUMFIBPOINTS? [y/n]")
        if userSelection == "y":
            os.environ['NUMFIBPOINTS'] = str(numPoints)
    else:
        try:
            numPoints = int(os.environ['NUMFIBPOINTS'])
        except ValueError:
            print("Environment variable NUMFIBPOINTS is not set to a numerical value.")
            numPoints = "a"
            while numPoints == "a":
                try:
                    num = int(input("Input desired number of points"))
                    numPoints = num
                    userSelection = input("Set " + str(numPoints) + " as environment variable NUMFIBPOINTS? [y/n]")
                    if userSelection == "y":
                        os.environ['NUMFIBPOINTS'] = str(sRadius)
                except ValueError:
                    print("Invalid input. Must input a numerical value")

    #Check file. Return true if correct file extension
    ACCEPTED_EXTENSIONS = [".mmol", ".ent", "pdb", ".short.socket"]
    def CheckExtensions(val):
        for ext in ACCEPTED_EXTENSIONS:
            loc = val.endswith(ext)
            if loc:
                return True
        return False

    #Set current directory. Override SIGINT to first return to the original directory and then continue with SIGINT
    currdir = os.getcwd()
    def signal_handler(signal, frame):
        os.chdir(currdir)
        sys.exit(-1)
    signal.signal(signal.SIGINT, signal_handler)

    #Some constants
    ##Accepted protein files
    ACCEPTED_FILES = [
        ('Molecular Topology', '*.mmol')
        , ('Protein Database File (old) (Not yet supported)', '*.ent')
        , ( 'Protein Database File (Not yet supported)', '*.pdb')
    ]
    ##Accepted socket formats
    ACCEPTED_SOCKET = [('Socket File', '*.short.socket')]

    ##Messages
    ERROR_MESSAGE = "Must select a file"
    PDB_PROMPT = "Select a .pdb file"

    filewriter = writefile.FileWriter()
    wHelper = writerhelper.WriterHelper()

    try:
        #If no command line arguments, prompt user to choose two files
        if len(sys.argv) == 1:
            from tkinter.filedialog import askopenfilename
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            f_pdb = askopenfilename(title=PDB_PROMPT, filetypes=ACCEPTED_FILES)
            pmt = "Select associated .socket file for " + fpt.CutPath(f_pdb)
            f_sock = askopenfilename(title=pmt, filetypes=ACCEPTED_SOCKET)
            filelist = [filemanager.TwoFiles(f_pdb, f_sock)]
        #Provide an entire directory to iterate through
        elif sys.argv[1] == "-dir":
            if not os.path.isdir(sys.argv[2]):
                raise CustomExceptions.NotDirectory
            filemanager.GetFileList(sys.argv[2])
            filemanager.Organize()
            filelist = [file for file in os.listdir() if os.path.isdir(file)]

        #This loop is where everything happens

        for file in filelist:
            try:
                #Navigate to protein directory and get pdb and socket files
                os.chdir(os.path.join(os.getcwd(), file))
                print("Checking: ", os.path.basename(file))
                for ptr in os.listdir():
                    if CheckExtensions(ptr) and not ptr.endswith(".short.socket"):
                        f_pdb = ptr
                    elif ptr.endswith(".short.socket"):
                        f_sock = ptr

                #Open found files and ensure correct encoding
                try:
                    f_p = open(f_pdb, encoding="utf8")
                except FileNotFoundError:
                    continue
                    sys.exit(ERROR_MESSAGE)
                try:
                    f_s = open(f_sock, encoding="utf8")
                except FileNotFoundError:
                    continue
                    sys.exit(ERROR_MESSAGE)
                #Parse pdb file
                protSeq = Sequence.ProteinSequence()
                protSeq.parsePDB(f_p)
                #Split into chains
                seqChains = Chain.Chain(protSeq)
                f_p.seek(0)
                #Check for symmatries.
                seqChains.Symmetry(f_p, protSeq)
                for key in seqChains.matrix:
                    protSeq.GeneratePair(seqChains.copyChains, seqChains.matrix[key])
                #Get socket file and make heptad assignings
                socket_info = CCSocket.CCSocket()
                socket_info.ParseSocket(f_s)
                socket_info.GroupSockInfo()
                #Get ranges of each helix
                # Output information to write file
                outfile = open(ntpath.basename(f_p.name) + ".csv", "w")
                outfile.write(f"SASA Data from {ntpath.basename(f_p.name)} and {ntpath.basename(f_s.name)}\n")
                outfile.write(f"This protein contains {len(socket_info.groupData)} coiled coils\n")
                index = 1
                for si in socket_info.groupData:
                    outfile.write(f"Coiled coil {index}: contains {len(si)} monomers,{len(si)}\n")
                    cCoil = CoiledCoil.CoiledCoil(seqChains, si)
                    sasa = SASA.SASA()
                    #pSASA = sasa.GetSASA(protSeq.sequence, numPoints, sRadius)
                    cCoilSASA = sasa.GetSASA(cCoil.GetccAtoms(), numPoints, sRadius)
                    outfile.write(f"\n ,SASA,% of struture,# of residues\nCoiled-coil SASA, {cCoilSASA},{len(cCoil.GetccAtoms())}\n")
                    sasa.SetSASA(cCoilSASA)
                    monomerSASAs = list()
                    monomerPcnt = list()
                    monRes = list()
                    outofcontext = list()
                    monIndex = 1
                    for monomer in cCoil.monomers:
                        monSASA, monPct = sasa.SASASection(monomer, cCoil.GetccAtoms(), numPoints, sRadius)
                        monomerSASAs.append(monSASA)
                        monomerPcnt.append(monPct)
                        monRes.append(len(monomer))
                        outofcontext.append(sasa.GetSASA(monomer, numPoints, sRadius))
                        outfile.write(f"Monomer {monIndex}, {monomerSASAs[-1]}, {monomerPcnt[-1] * 100}%, {len(monomer)}\n")
                        #print(f"Monomer {monIndex}: {monomerSASAs[-1]}A {monomerPcnt[-1] * 100}% of the structure")
                        monIndex += 1
                    print(len(si))
                    wHelper.insertMonomers(f"{os.path.basename(file)} coil {index}", len(si), sasa.SASA, monomerSASAs, monomerPcnt, len(cCoil.GetccAtoms()), monRes, outofcontext)
                    index += 1
                #filewriter.writeFile()
            except:
                print("An error in calculating the SASA for this protein")
            finally:
                outfile.close()
                os.chdir("..")

    finally:
        #Return to original directory
        print("Done")
        os.chdir(currdir)
        filewriter.WriteMaster(len(filelist), wHelper)