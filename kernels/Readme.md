kernels/ subdirectory of Deep Impact Spacecraft Characterization project
========================================================================

This directory contains SPICE files.  Spacecraft Clock (SCLK) and
LEAPSECOND kernels are provided in the repository; ephemeris kernels must
be obtained from elsewhere as described below.


=================================
Manifest of kernels/ subdirectory
=================================


==================================
naif0010.tls
dif_sclkscet_00015_science.tsc
dii_sclkscet_00008_science.tsc
dii_sclkscet_00008_science_btc.tsc
==================================

SCLK and LEAPSECOND kernels


========================
dif_preenc174_nav_v1.bsp
dii_preenc174_nav_v1.bsp
========================

Ephemeris (trajectory) kernels; these are not provided in the Git
repository; they may be obtained from

  http://naif.jpl.nasa.gov/pub/naif/pds/data/di-c-spice-6-v1.0/disp_1000/data/spk/

Note that these files are not the most recent versions of the final
navigation solution, but they are sufficient for calculating the light (and
telemetry) transmission time to Earth from the DI spacecraft


============
00readme.txt - this file
============
