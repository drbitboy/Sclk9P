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

doc/ - Directory containing documents related to this project

doc/00readme.txt - Descriptions of those documents

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

