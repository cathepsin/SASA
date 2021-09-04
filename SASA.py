import CustomExceptions

class SASA:
    def __init__(self):
        self.SASA = 0
        self.RADIUS_MAP - {
            "N": 1.5,
            "O": 1.4,
            "S": 1.85,
            "nonArC": 2.0,
            "ArC": 1.85,
            "OthC": 1.5,
            "Zn": 0.74
        }

    class FibonacciSphere:
        def __init__(self):
            print("wow")

    def GetSASA(self, structure, n, solvent_radius):
        self.n = n
        self.solvent_radius = solvent_radius
        cf = self.GetClassifications()
        print("stub!")

    def DefineSphere(self):
        print("stub")

    def DrawSphere(self):
        print("stub")

    def RemoveClosePoints(self):
        print("stub")

    def GetCloseAtoms(self):
        print("stub")

    def GetClassifications(self, atom):
        retList = list()
        if atom.element == "N":
            retList.append('N')
        elif atom.element == "O":
            retList.append('O')
        elif atom.element == "S":
            retList.append('S')
        elif atom.element.upper() == "ZN":
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

        return retList