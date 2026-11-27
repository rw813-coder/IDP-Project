# IDP-Project
The Repository for the Integrated Design Project Coursework

Naming conventions:
Sensors:
Front/back goes before left/right, hence:
FR
FL
BL
BR
Which are sensors 1, 2, 3 and 4 respectively.

Locations:
Depot (will eventually be DGN, DGS, DUN, DUS for depot ground north , ..., ..., depot upper south)
The depots consist of 6 bays each.
Yard (YN0, YN1, YS0, YS1)
Junction

0 is by default the state closest to the junction, with numbers increasing going away from the junction. 
Currently 0 is in the junction, 1 is up to the first yard (YN0/ YS0), 2 is in between the yards, 3 is between the second yard the depot, including the start of the depot. Bays 0 to 5 are the bays of the upper and lower depots, with 0 being the closest to the junction.

"north", "south" and "neither" are the descriptions of the magnetic field sensor states. The left hand side, when viewed from the junction looking towards the traffic light, is described as "north" as it contains the yards for the north pole boxes, with "south" being the right hand side, hence the names YS and YN.

All time measurements are in milliseconds.
