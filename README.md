# AutoDewar
Automated system for filling liquid nitrogen dewars, for use with HPGe detectors 

## Overview
  During the course of the 2026 NURTURE (NUclear Recruitment Through Undergraduate REsearch) program at UMass Lowell, we were tasked with creating an automated fill system for the liquid nitrogen dewars located throughout the Umass Lowell radiation lab. These dewars are used to fill the many detectors used to take data in the nuclear reactor and particle accelerator in the lab. Commonly referred to as High Purity Germanium (HPGe) detectors, the germanium based semiconductor inside is in an excited state at room temperature, necessitating cooling with liquid nitrogen to achieve the needed operational temperature. 

## Methodology ##
  We were given several normally-closed ASGO valves that are rated for a LN2 tank as a starting point for the lab.  Each of these valves are rated for 120 VAC, and have a hot, neutral and ground lead. Our initial goals were to get the valve to open , get the valve to open with a switch, open the valve with a micro-controller, and to finally open the valve via computer command. 
  This allowed us to create a python scripts to open and close the valve initially with an arduino microcontroller, and subsequently a raspberry pi to allow networking capabilities. By this step, we were able to send a voltage through our control boards in order to trigger the solenoids in the valves,  with our first sensor based off an LED, then a thermistor. We were then able  design circuits for the low power section of our system, on bread boards , then on perf boards for the final product. After our low power control section was designed, we were able to create a high power section wiring harness to fully test the system. 

**

    
