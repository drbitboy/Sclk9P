Characterization and Improvement of the SPICE Kernels from the Deep Impact Encounter with Comet Tempel 1
==================================================

Brian Carcich, Latchmoor Services LLC, working for Dr. Tony Farnham of UMd


Understanding what the DI SpaceCraft cLocKs (SCLKs) were doing
around encounter.

![](https://raw.github.com/drbitboy/Sclk9P/results/TwoParamModel_case0a.png)


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


Documentation
=============

00readme.txt, Readme.md - this file

doc/ - Directory containing documentation for this project

doc/00readme.txt - Descriptions of those documents


SPICE kernels
=============

kernels/ - SPICE kernels (SCLK, LSK, SPK)

kernels/00readme.txt - description of SPICE kernels


DII and DIF SCLK (time) and SCU temperature data
================================================

all_scutemp.txt, dif_scutemp.txt, dii_scutemp.txt - Temperature data

dii_dif_diffs.txt - DIF and DII SCLK summary clock correlation data



Python scripts
==============

ttmodel.py - Implements two-parameter time model for DI SCLKs

timediffs.py - Module with Classes to read and difference DII and DIF times

smoothtemps.py - Module with Classes to read and smooth DI temperatures

readtemps.py - Python module to read DIF and DII temperatures

spice/ - symlink to PySPICE/spice/
       - allows 'import spice' in Python code
       - not part of repo
       - see https://github.com/drbitboy/PySPICE

check_00.py - Test script comparing DII, DIF SCLKs and VTCs from kernels

check_01.py -  "

check_02.py -  "; also plots data


=============
Abbreviations
=============

DI - Deep Impact (mission, project, spacecraft)

DII - Deep Impact Impactor spacecraft

DIF - Deep Impact Flyby spacecraft

TOI - Time Of Impact

S/C - SpaceCraft

SCU - S/C CPU

SCLK - S/C clock representation e.g. '1/0123456789:012'; see SPICE

VTC - Vehicle TimeCode, Floating point representation of S/C seconds

SPICE - Toolkit (code) and kernel files (data) for describing ancillary
        info about spacecraft observations; see http://naif.jpl.nasa.gov/


===============
Git cheat sheet
===============

git commit -a -m "..."
git push -u origin master

