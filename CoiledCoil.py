class CoiledCoil:
    def __init__(self, chains, sock_info):
        self.ccAtoms = list()
        self.monomers = list()
        for info in sock_info:
            self.GetIncludedResidues(chains, info)

    def GetccAtoms(self):
        return self.ccAtoms

    def GetMonomers(self):
        return self.monomers

    def GetIncludedResidues(self, chains, sock_info):
        chain = chains.chains[sock_info[0]]
        currMonomer = list()
        for i in range(sock_info[1][0], sock_info[1][1] + 1):
            try:
                if chain[i] not in set(self.ccAtoms) and sock_info[3][i - sock_info[1][0]] != '-':
                    self.ccAtoms.append(chain[i])
                    currMonomer.append(chain[i])
            except IndexError:
                continue
            except KeyError:
                continue
        self.monomers.append(currMonomer)

