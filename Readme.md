Characterization and Improvement of the SPICE Kernels
from the Deep Impact Encounter with Comet Tempel 1
==================================================

Brian Carcich, Latchmoor Services LLC, working for Dr. Tony Farnham of UMd


Understanding what the DI SpaceCraft cLocKs (SCLKs) were doing
around encounter.


=====
Usage
=====

0) Prerequisites:

0.1) Python 2.7

0.1.1) Python modules:  numpy; scipy; pyfits; matplotlib; PySPICE.

0.1.2) PySPICE (misc.py, object.py, _spice.so, build from Git repo
       https://github.com/drbitboy/PySPICE) in spice/ subdirectory of
       this directory.


1) Read 00readme.txt (this file), doc/00readme.txt, kernels/00readme.txt,
   and follow recommendations and read additional materials referenced.


========
Manifest
========

check_0{0,1,2}.py - Initial test comparing DII and DIF SCLKs

readtemps.py - Read DIF and DII clock temperatures

kernels/ - SPICE kernels (SCLK, LSK, SPK)

kernels/00readme.txt - description of SPICE kernels


doc/ - Directory containing documents related to this project

doc/00readme.txt - Descriptions of those documents


spice/ - symlink to PySPICE/spice/
       - allows 'import spice' in Python code
       - not part of repo
       - see https://github.com/drbitboy/PySPICE


=============
Abbreviations
=============

DI - Deep Impact (mission, project, spacecraft)
DII - Deep Impact Impactor spacecraft
DIF - Deep Impact Flyby spacecraft
TOI - Time Of Impact
SPICE - Toolkit (code) and kernel files (data) for describing ancillary
        info about spacecraft observations; see http://naif.jpl.nasa.gov/


===============
Git cheat sheet
===============

git commit -a -m "..."
git push -u origin master

