Characterization and Improvement of the SPICE Kernels
from the Deep Impact Encounter with Comet Tempel 1
==================================================

Brian Carcich, Latchmoor Services LLC, working for Dr. Tony Farnham of UMd


Understanding what the DI SpaceCraft cLocKs (SCLKs) were doing
around encounter.



Manifest
========

check_00.py - Initial test comparing DII and DIF SCLKs at TOI

readtemps.py - Read DIF and DII clock temperatures

doc/ - documents related to this project

doc/zzOriginals/ - original versions of documents

spice/ - symlink to PySPICE/spice/
       - allows 'import spice' in Python code
       - not part of repo
       - see https://github.com/drbitboy/PySPICE

../kernels/ - SCLK and LEAPSECOND kernels
            - not part of repo


Abbreviations
=============

DI - Deep Impact (mission, project, spacecraft)
DII - Deep Impact Impactor spacecraft
DIF - Deep Impact Flyby spacecraft
TOI - Time Of Impact
SPICE - Toolkit (code) and kernel files (data) for describing ancillary
        info about spacecraft observations; see http://naif.jpl.nasa.gov/


Git cheat sheet
===============

git commit -a -m "..."
git push -u origin master

00readme.txt
all_scutemp.txt
check_00.py
check_01.py
check_02.py
dif_scutemp.txt
dii_dif_diffs.txt
dii_scutemp.txt
doc
fit2png.py
fit2png.pyc
mrivis
readtemps.py
readtemps.pyc
smoothtemps.py
smoothtemps.pyc
spice
timediffs.py
timediffs.pyc
ttmodel.py
TwoParamModel_case0.png
TwoParamModel_case1.png
VTCi_vs_VTCf.png
VTCi_vs_VTCf.xcf
x.x
y.y
z.z
