import ntpath
import os


class FileWriter:
    def __init__(self, *argv):
        self.arg = argv
        self.summary = ""
        print("Putting master file in: ", os.getcwd())
        self.master = open("Master_Summary.csv", "w")

    def SetWriteFile(self, file):
        self.writefile = file
        self.writefile.write("Protein from " + ntpath.basename(file.name) + ",\n")
    def SetArgs(self, *argv):
        self.arg = argv

    #Write all data to a file from given argv. Fill summary
    def writeSummary(self, content):
        self.summary += content
        if not self.summary.endswith("\n"):
            self.summary += "\n"

    #Write to master csv file
    def WriteMaster(self, num, writer):
        self.master.write(writer.WriteData(num))
        print("")
