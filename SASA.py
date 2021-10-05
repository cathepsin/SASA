import math

import CustomExceptions

class SASA:
    def __init__(self):
        self.SASA = 0
        self.RADIUS_MAP = {
            "N": 1.55,
            "O": 1.52,
            "S": 1.85,
            "nonArC": 1.7,
            "ArC": 1.7,
            "OthC": 1.7,
            "Zn": 0.74
        }

    def SetSASA(self, sasa):
        self.SASA = sasa
    class FibonacciSphere:
        def __init__(self):
            print("wow")

    def GetSASA(self, structure, n, solvent_radius):
        self.n = n
        self.solvent_radius = solvent_radius
        #Create Fibonacci sphere around each atom
        cf = list()
        allAtoms = list()
        for res in [residue.atoms for residue in structure]:
            for atom in res:
                if not atom.hetatm:
                    allAtoms.append(atom)
        SASA = 0
        for atom in allAtoms:
            #x = self.GetClassifications(atom)
            #print(self.RADIUS_MAP[self.GetClassifications(atom)])
            sphere = self.GenerateSphere(n, atom, self.RADIUS_MAP[self.GetClassifications(atom)] + solvent_radius)
            dotsToKeep = list()
            closeAtoms = self.GetCloseAtoms(atom, allAtoms, solvent_radius)
            # manager = multiprocessing.Manage()
            # SASAlist = manager.list()
            for dot in sphere:
                addFlag = True
                for otherAtom in closeAtoms:
                #for otherAtom in [otherAtom for otherAtom in allAtoms if otherAtom != atom]:
                    if self.dist(atom.location, dot) > self.dist(otherAtom.location, dot):
                        addFlag = False
                        break
                if addFlag:
                    dotsToKeep.append(dot)
            cf.append(dotsToKeep)
            dotSA = self.SphereSA(self.RADIUS_MAP[self.GetClassifications(atom)] + (solvent_radius)) / n
            SASA += dotSA * len(dotsToKeep)
        #print(SASA)
        return SASA

    def SASASection(self, section, structure, n, solvent_radius):
        # Create Fibonacci sphere around each atom
        cf = list()
        allSectionAtoms = list()
        for res in [residue.atoms for residue in section]:
            for atom in res:
                if not atom.hetatm:
                    allSectionAtoms.append(atom)

        allAtoms = list()
        for res in [residue.atoms for residue in structure]:
            for atom in res:
                if not atom.hetatm:
                    allAtoms.append(atom)

        SASA = 0
        for atom in allSectionAtoms:
            #TODO Kill hydrogen atoms!

            # x = self.GetClassifications(atom)
            # print(self.RADIUS_MAP[self.GetClassifications(atom)])
            sphere = self.GenerateSphere(n, atom, self.RADIUS_MAP[self.GetClassifications(atom)] + solvent_radius)
            dotsToKeep = list()
            closeAtoms = self.GetCloseAtoms(atom, allAtoms, solvent_radius)
            # manager = multiprocessing.Manage()
            # SASAlist = manager.list()
            for dot in sphere:
                addFlag = True
                for otherAtom in closeAtoms:
                    # for otherAtom in [otherAtom for otherAtom in allAtoms if otherAtom != atom]:
                    if self.dist(atom.location, dot) > self.dist(otherAtom.location, dot):
                        addFlag = False
                        break
                if addFlag:
                    dotsToKeep.append(dot)
            cf.append(dotsToKeep)
            dotSA = self.SphereSA(self.RADIUS_MAP[self.GetClassifications(atom)] + (solvent_radius)) / n
            SASA += dotSA * len(dotsToKeep)
        #print(SASA / self.SASA)
        return SASA, SASA / self.SASA


        #Remove dot if dist(parentAtom, dot) < dist(otherAtom, dot)
    #Get atoms +-2 residues in the list. These are most likely to interfere
    def GetNearAtoms(self, atom, structure):
        retList = list()
        resiList = list()
        # for res in structure:
        #     try:
        #         resiList.append(structure[atom.])

    def SphereSA(self, radius):
        x = 4 * math.pi * (radius **2)
        return 4 * math.pi * (radius **2)

    def dist(self, coor1, coor2):
        return math.sqrt((coor1[0] - coor2[0])**2 + (coor1[1] - coor2[1])**2 + (coor1[2] - coor2[2])**2)

    def GenerateSphere(self, n, atom, radius):
        #TODO Make work with variable radius
        # Thanks to user 'CR Drost' from https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
        from numpy import pi, cos, sin, arccos, arange
        indices = arange(0, n, dtype=float)
        phi = arccos(1 - 2 * indices / n)
        theta = pi * (1 + 5 ** 0.5) * indices
        x, y, z = radius * cos(theta) * sin(phi), radius * sin(theta) * sin(phi), radius * cos(phi);
        points = list()
        for val in range(len(x)):
            points.append([x[val] + atom.location[0], y[val] + atom.location[1], z[val] + atom.location[2]])
        return points

    def GetCloseAtoms(self, atom, atomList, solvent_radius):
        retlist = list()
        for a in [a for a in atomList if a != atom]:
            if self.GetClassifications(atom) == "Placeholder":
                continue
            if self.dist(atom.location, a.location) < self.RADIUS_MAP[self.GetClassifications(atom)] + self.RADIUS_MAP[self.GetClassifications(a)] + 2.5 * solvent_radius:
                retlist.append(a)
        return retlist

    def GetClassifications(self, atom):
        retList = list()
        # retList.append(atom)
        if atom.element == "N" or atom.id.find("N") != -1:
            retList.append('N')
        elif atom.element == "O" or atom.id.find("O") != -1:
            retList.append('O')
        elif atom.element == "S" or atom.id.find("S") != -1:
            retList.append('S')
        elif atom.element.upper() == "ZN" or atom.id.upper().find("ZN") != -1:
            retList.append('Zn')
        elif atom.id == "C":
            retList.append('OthC')
        elif atom.id == "CA" and not atom.residue == "PRO":
            retList.append('OthC')

        else:
            if atom.residue == "HIS": #DONE
                if atom.id == "CB":
                    retList.append('nonArC')
                else:
                    retList.append('ArC')

            elif atom.residue == "ARG":#DONE
                if atom.id == "CZ" or atom.id == "CD":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "LYS":#DONE
                if atom.id == "CE":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "ILE":#DONE
                retList.append('nonArC')

            elif atom.residue == "PHE":#DONE
                if atom.id == "CB":
                    retList.append('nonArC')
                else:
                    retList.append('ArC')

            elif atom.residue == "LEU":#DONE
                retList.append('nonArC')

            elif atom.residue == "TRP":#Done
                if atom.id == "CB":
                    retList.append('nonArC')
                else:
                    retList.append('ArC')

            elif atom.residue == "ALA":#Done
                retList.append('nonArC')

            elif atom.residue == "MET":#DONE
                if atom.id == "CG" or atom.id == "CE":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "PRO":#DONE
                if atom.id == "CA" or atom.id == "CD":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "CYS":#DONE
                retList.append('OthC')

            elif atom.residue == "ASN":#DONE
                if atom.id == "CG":
                    retList.append("OthC")
                else:
                    retList.append('nonArC')

            elif atom.residue == "VAL":#DONE
                retList.append("nonArC")

            elif atom.residue == "SER":#DONE
                retList.append('OthC')

            elif atom.residue == "GLN":#DONE
                if atom.id == "CD":
                    retList.append("OthC")
                else:
                    retList.append('nonArC')

            elif atom.residue == "TYR":#DONE
                if atom.id == "CB":
                    retList.append("nonArC")
                else:
                    retList.append("ArC")

            elif atom.residue == "ASP":#DONE
                if atom.id == "CG":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "GLU":#DONE
                if atom.id == "CD":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')

            elif atom.residue == "THR":#DONE
                if atom.id == "CB":
                    retList.append('OthC')
                else:
                    retList.append('nonArC')
            else:
                retList.append("Placeholder")
                raise CustomExceptions.UnknownAtom
        #TODO Check that all atoms have a label

        return retList[0]