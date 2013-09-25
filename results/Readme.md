Characterization and Improvement of the SPICE Kernels from the Deep Impact Encounter with Comet Tempel 1
==================================================

Brian Carcich, Latchmoor Services LLC, working for Dr. Tony Farnham of UMd


Understanding what the DI SpaceCraft cLocKs (SCLKs) were doing
around encounter.

Background
==========

The two Deep Impact (DI) spacecraft, the DI Flyby (DIF) and DI Impactor (DII), have independent SpaceCraft cLocKs (SCLKs).  The correlations of those SCLKs with each other, and with TDT (Terrestrial Dynamical Time, linear time), have been adjusted to fix the time of the DII Time Of Impact (TOI), with comet 9P/Tempel 1 during the prime mission, at UTC 2005-07-04T05:44:34.2; that time matches the ephemeris in the final ephemeris solution provided by Dan Kubitschek (JPL Optical Navigation Group).  Based on the appearance of the impact flash in DIF images at encounter, the TOI was 173727702:218 on the DIF clock (N.B. the :218 is not milliseconds).  Based on geometric analysis by Dennis Wellnitz(University of Maryland) of the DII final encounter images, TOI was 173727875:105 on the DII clock.  With the TOI point fixed, linear interpolation to the last formal correlation point three weeks earlier models the relationship between the DI SCLKs and TDT during the approach to 9P/Tempel 1, using the SPICE SCLK kernel format.

Further background on this issue is available in the [accompanying documentation](../doc/spacecraft_clock_correlation/) [[PDF]](https://github.com/drbitboy/Sclk9P/blob/master/doc/spacecraft_clock_correlation/sclk_correlation.pdf?raw=true), extracted from the [DI mission documentation data set](http://pdssbn.astro.umd.edu/holdings/di-c-hrii_hriv_mri_its-6-doc-set-v4.0/document/flight_data/di/spacecraft_clock_correlation/) archived with the Planetary Data System (PDS).  There are also some subtleties in the interpretation of the DI SCLK counters; those subleties, as well as details of the DI SCLK internals and digital representation, will not be described here and the reader is encouraged to browse the [document directory](../doc/) that is distributed on Github as part of this report as well as the [JPL/NAIF/SPICE SCLK required reading](http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/sclk.html) and associated documents.

After the end of the prime mission, limited efforts were made to improve the SCLK correlation.  Unresolved ambiguities in flight software and telemetry had limited the accuracy of the correlation to +/-1s; during the extended EPOXI mission, and an error was discovered in the way image timestamps were set.  During these efforts, Amy Walsh (Ball Aerospace) resolved many of these issues, fully characterized the DI SCLKs, and developed a method to improve the correlation accuracy by two orders of magnitude.  

Amy also provided flight thermal data for the DI SCUs (Spacecraft CPUs), vendor data describing the thermal performance of the SCLK oscillators, five other reliable time correlations within a fortnight of TOI, and one other suspect correlation a few days before TOI.  The available data are summarized in following figures:

![](https://github.com/drbitboy/Sclk9P/raw/master/results/ExistingKernelCorrelationWithExtension.png)

## Timing data; note especially the Good, Suspect and TOI points in the inset

![](https://github.com/drbitboy/Sclk9P/raw/master/doc/spacecraft_clock_correlation/fig2_sclk_temp_history.jpg)

## Thermal data

At the time, the mission focus was on delivering prime data sets to PDS, so further work applying these data to improving the SCLK correlations was postponed, and later became the current project:  Characterization and Improvement of the SPICE Kernels from the Deep Impact Encounter with Comet Tempel 1.

Project Scope and Cut To The Chase
==================================

The goals of this project are 

- to determine if the additional thermal data, and later SCLK correlation data, can facilitate significantly improving our knowledge of the timing of the DI TOI, perhaps tying it back to earth-based observations, and if so, 

- to provide an updated timing model, as well as updated trajectories, in the form of SPICE SCLK- and SP-Kernels

To cut to the chase, the answer is no, the additional data do not suggest a physically plausible model consistent with the available data that will improve the timing model in such a way as to significantly improve the science obtained from the mission.

Summary
=======

Refer to the following figure:

![](https://github.com/drbitboy/Sclk9P/raw/master/results/TwoParamModel_case0.png)



