#Coiled-Coil SASA
<hr>

#Introduction
This script was originally made to quickly estimate the surface area of each individual monomer within a coiled coil.
An updated and more general version of this script will be implemented in the
[***apalib***](https://pypi.org/project/apalib/) python module.<br><br>
This was designed with simplicity and efficiency in mind. Using a pdb file and an associated socket
file, the surface area of each monomer within a coiled-coil can be obtained


version 0.0.1
<hr>

#Installation
This script uses the following modules. Install them as you would normally install a python module:
- numpy
- ntpath
- shutil
- tkinter

Under special and extremely rare circumstances, the following may also need to be installed:
- math
- sys
- signal
- os
#Running Instructions
First, two environment variables must be set:<br>
**SOLVENTRADIUS**: Set this to be the radius of your desired solvent.<br>
**NUMFIBPOINTS**: Set this to be the number of fibonacci points to generate around each atom. A higher number
results in higher resolution/higher accuracy, but increases the time required for the script to run.<br><br>
If either or both environment variables are not set, then upon running the script, a prompt will ask for values to use.<br><br>
This script can be run as follows:<br>
`cmd: python3 main.py`<br>
This will prompt the user to select a .pdb, .mmol, or .ent file. Next, the user will be prompted to
select an associated socket file.<br><br>
Output data will be put into a file in the current working directory called **Master_Summary.csv**<br><br>
This script can also be run using the -dir flag as follows:<br>
`cmd: python3 main.py -dir /path/to/directory`<br>
The directory pointed to should contain nothing except for .pdb/.mmol/.ent files and their assocaited socket files.<br>
![ ](https://raw.githubusercontent.com/cathepsin/SASA/master/file.png) <br>
The provided directory will be scanned and file-pairs will be organized into sub-directories.
Each pair will produce an individual data sheet as well as a **Master_Summary.csv** compiling all data
for all provided files.<br><br>
Note that this script can take up to a few minutes to run ***per protein***.<br><br>

## License
[MIT](https://choosealicense.com/licenses/mit/)

##Note
This program has been tested only enough to produce data for a single project. It cannot handle every protein
(i.e. proteins containing a rotamer). A more robust form of this script will be included in the [***apalib***](https://pypi.org/project/apalib/)
python module.