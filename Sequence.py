import numpy as np

class ProteinSequence:
    def __init__(self):
        self.sequence = []
        self.message = ""

    class Atom:#Class to store information about an individual atom
        def __init__(self, num, coord, tag, res, ch, occ, bf, ele):
            self.num = num
            self.location = coord
            self.id = tag
            self.occupancy = occ
            self.bfactor = bf
            self.element = ele
            self.residue = res
            self.chain = ch
            self.hetatm = False

        #If a HETRATM
        def het(self, bl):
            self.hetatm = bl

        #ATOM dunder methods
        def __repr__(self):
            return f"ATOM: NUMBER: {self.num}, TAG: {self.id}, RESIDUE: {self.residue}, CHAIN: {self.chain}, COORDINATES: {self.location}, OCCUPANCY: {self.occupancy}, B_FACTOR: {self.bfactor}, ELEMENT: {self.element}"
        def __str__(self):
            return f"{self.id} {self.residue} {self.location}"
        def __mul__(self, other):
            arr = np.array([self.location[0],self.location[1],self.location[2], 1.])
            return np.matmul(other, arr).tolist()[:3]

    class AminoAcid:#Class to store information about a whole residue
        def __init__(self, numb, atomList, cName, ch):
            self.num = numb
            self.atoms = atomList
            self.residue = cName
            if len(cName) == 4:
                self.residue = cName[1:]

            self.chain = ch
            self.rotation = dict()
            self.SetSpecials()
            self.assignment = 'none'


        #Organizes special atoms and residues with non-1 occupancy
        def SetSpecials(self):
            for atom in self.atoms:
                if atom.residue != self.residue:
                    if not atom.residue in self.rotation:
                        self.rotation[atom.residue] = list()
                    self.rotation[atom.residue].append(atom)
            for key in self.rotation:
                for atom in self.rotation[key]:
                    self.atoms.remove(atom)
            self.specialAtoms = list()
            for atom in self.atoms:
                if atom.id.upper().find('X') != -1:
                    self.specialAtoms.append(atom)
            for atom in self.specialAtoms:
                self.atoms.remove(atom)

        #Set the centroid and the centroidal vector (CA-->Cent) for a residue
        def SetCentroid(self, centr):
            self.centroid = centr
            for atom in self.atoms:
                if atom.id == 'CA':
                    try:
                        self.vector = [centr[0] - atom.location[0], centr[1] - atom.location[1], centr[2] - atom.location[2]]
                        break
                    except TypeError:
                        self.vector = "Bad"

        #AminoAcid dunder methods
        def __lt__(self, other):
            return self.num < other.num
        def __repr__(self):
            return f"RESIDUE: {self.residue}, NUMBER: {self.num}, CHAIN: {self.chain}"
        def __str__(self):
            return f"{self.residue} {self.num} {self.chain} {self.assignment}"

    #Parses a .pdb or .ent file. Returns an AA sequence.
    #Each residue is placed in the order they appear in the .pdb/.ent file
    def parsePDB(self, file):
        currResNum = -1
        atomGroup = []
        for line in file:
            if line.find("ENDMDL") == 0:
                self.message += "The selected file contains multiple model builds. Only the first will be considered for calculations.\n"
                break
            if line.find("ATOM") == 0 or line.find("HETATM") == 0 and line.find("HOH") == -1:
                resNum = int("".join(chr for chr in line[22:27] if chr.isdigit()))
                if currResNum == -1:
                    #Not all files start at residue 0 or 1. This ensures correct starting position
                    currResNum = resNum
                #Check if the current ATOM is on a new residue
                if resNum != currResNum:
                    #Found the next residue, so save previously recorded data as an AminoAcid
                    self.sequence.append(self.AminoAcid(currResNum, atomGroup.copy(), atomGroup[0].residue, chain))
                    currResNum = resNum
                    atomGroup.clear()
                #Parse ATOM data
                num = int(line[6:11])
                tag = line[11:16].strip()
                residue = line[16:20].strip()
                chain = line[20:22].strip()
                if chain == "": #A chain name is required for future logic. If no name is assigned, assign one
                    chain = "$"
                coordinates = [float(line[27:38]),float(line[38:46]),float(line[46:55])]
                occupancy = float(line[55:60])
                bfactor = float(line[60:67])
                element = line[77:].strip()
                #Save atom
                newAtom = self.Atom(num, coordinates, tag, residue, chain, occupancy, bfactor, element)
                if line.find("HETATM") == 0:
                    newAtom.het(True)
                atomGroup.append(newAtom)
        #Save the final AminoAcid instance
        self.sequence.append(self.AminoAcid(currResNum, atomGroup.copy(), atomGroup[0].residue, chain))

    #Generate symmatry pairs
    def GeneratePair(self, chainPairs, matrix):
        self.symmetryPairs = list()
        for key in chainPairs:
            for residue in self.sequence:
                if residue.chain == key:
                    atomGroup = []
                    for atom in residue.atoms:
                        newAtom = self.Atom(atom.num, atom * matrix, atom.id, atom.residue, atom.chain + atom.chain, atom.occupancy, atom.bfactor, atom.element)
                        atomGroup.append(newAtom)
                    newRes = self.AminoAcid(residue.num, atomGroup, residue.residue, residue.chain)
                    self.symmetryPairs.append(newRes)