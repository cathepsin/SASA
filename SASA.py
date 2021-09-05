import CustomExceptions

class SASA:
    def __init__(self):
        self.SASA = 0
        self.RADIUS_MAP = {
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
        cf = list()
        for residue in structure:
            for atom in residue.atoms:
                cf.append(dict())
                cf[-1]['Classification'] = (self.GetClassifications(atom))
                cf[-1]['Radius'] = (self.RADIUS_MAP[cf[-1][1]] + solvent_radius)
                cf[-1]['Sphere'] = (self.DrawSphere(n, atom))
        print("stub!")

    def DefineSphere(self):
        print("stub")

    def DrawSphere(self, n, atom):
        #TODO Make work with variable radius
        # Thanks to user 'CR Drost' from https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
        from numpy import pi, cos, sin, arccos, arange
        indices = arange(0, n, dtype=float)
        phi = arccos(1 - 2 * indices / n)
        theta = pi * (1 + 5 ** 0.5) * indices
        x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi);
        points = list()
        for val in range(len(x)):
            points.append([x[val] + atom.location[0], y[val] + atom.location[1], z[val] + atom.location[2]])
        return points

    def RemoveClosePoints(self):
        print("stub")

    def GetCloseAtoms(self):
        print("stub")

    def GetClassifications(self, atom):
        retList = list()
        retList.append(atom)
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

        return retList