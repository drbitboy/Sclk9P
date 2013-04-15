Characterization and Improvement of the SPICE Kernels
from the Deep Impact Encounter with Comet Tempel 1
==================================================

Brian Carcich, Latchmoor Services LLC, working for Dr. Tony Farnham of UMd


Understanding what the DI SpaceCraft cLocKs (SCLKs) were doing
around encounter.



Manifest
========

check_00.py - Initial test comparing DII and DIF SCLKs at TOI

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

