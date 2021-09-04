import CoiledCoil
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
        #Get ranges of each helix
        cCoil = CoiledCoil.CoiledCoil(seqChains, socket_info)
        print(os.environ['SOLVENTRADIUS'])

        #Output information to write file
        outfile = open(ntpath.basename(f_p.name) + ".csv", "w")
        filewriter.SetWriteFile(outfile)
        filewriter.writeFile()
        outfile.close()
        os.chdir("..")

finally:
    #Return to original directory
    print("Done")
    os.chdir(currdir)
    filewriter.WriteMaster(len(filelist))