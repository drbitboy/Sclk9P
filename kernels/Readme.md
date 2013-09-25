kernels/ subdirectory of Deep Impact Spacecraft Characterization project
========================================================================

This directory contains SPICE files.  Spacecraft Clock (SCLK) and
LEAPSECOND kernels are provided in the repository; ephemeris kernels must
be obtained from JPL/NAIF as described below.


Manifest of kernels/ subdirectory
=================================


Documentation
=============

00readme.txt - this file


LEAPSECOND and SCLK kernels
===========================

naif0010.tls - Leapsecond kernel

dif_sclkscet_00015_science.tsc - DIF SCLK-kernel for science

dii_sclkscet_00008.tsc - DII operations SCLK

dii_sclkscet_00008_science.tsc - DII SCLK-kernel adjusted for TOI

dii_sclkscet_00008_science_btc.tsc - DII SCLK-ernel adjusted for TOI


Ephemeris (trajectory) kernels
==============================

dif_preenc174_nav_v1.bsp

dii_preenc174_nav_v1.bsp

- those ephemerides are not provided in this Git repository;
  they may be downloaded from

  http://naif.jpl.nasa.gov/pub/naif/pds/data/di-c-spice-6-v1.0/disp_1000/data/spk/

Note that those files are not the most recent versions of the final
navigation ephemerides, but they are sufficient for calculating the
light (and telemetry) transmission time to Earth from the DI spacecraft.


Abbreviations
=============

JPL - Jet Propulsion Laboratory

NAIF - Navigation and Ancillary Information Facility a division of JPL
       that provides SPICE products

SPICE - Toolkit (code) and kernel files (data) for describing ancillary
        info about spacecraft observations; see http://naif.jpl.nasa.gov/

