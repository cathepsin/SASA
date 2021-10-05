class WriterHelper:
    def __init__(self):
        self.CC = dict()

    def insertMonomers(self, name, olig_state, totalSASA,  monomerSASAs, monomerPcts, totalRes, numRes, outOfContext):
        if olig_state not in self.CC:
            self.CC[olig_state] = list()
        self.CC[olig_state].append(f"{name}, {totalSASA}, {totalRes},")
        for i in range(len(monomerSASAs)):
            self.CC[olig_state][-1] += f"{outOfContext[i]}, {monomerSASAs[i]}, {monomerPcts[i]}, {numRes[i]},"
        self.CC[olig_state][-1] += "\n"
        print(self.CC[olig_state][-1])

    def WriteData(self, num):
        keys = list()
        for key in self.CC.keys():
            keys.append(key)
        retStr = f"SASA information for {num} proteins and their individual coiled coils and monomers\n\n"

        for state in keys:
            if state == 2:
                retStr += "Dimers,\n"
            elif state == 3:
                retStr += "Trimers,\n"
            elif state == 4:
                retStr += "Tetramers,\n"
            elif state == 5:
                retStr += "Pentamers,\n"
            elif state == 6:
                retStr += "Hexamers,\n"
            else:
                retStr += "Other,\n"
            retStr += "Name, Total SASA, Total # of Residues,"
            for i in range(state):
                retStr += f"Monomer SASA (standalone), Monomer {i + 1} SASA (in context), % of Whole Coil, # of Residues,"
            retStr += "\n"
            for info in self.CC[state]:
                retStr += info
            retStr += "\n\n"
        return retStr