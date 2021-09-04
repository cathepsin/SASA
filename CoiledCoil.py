class CoiledCoil:
    def __init__(self, chains, sock_info):
        self.ccAtoms = list()
        for info in sock_info.sock_info:
            self.GetIncludedResidues(chains, info)

    def GetIncludedResidues(self, chains, sock_info):
        chain = chains.chains[sock_info[0]]
        for i in range(sock_info[1][0], sock_info[1][1] + 1):
            try:
                self.ccAtoms.append(chain[i])
            except IndexError:
                continue
