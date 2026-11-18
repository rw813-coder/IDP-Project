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
Depot (will eventually be DGL, DGR, DUL, DUR for depot ground left , ..., ..., depot upper left)
The depots consist of 6 bays each.
Yard (YL0, YL1, YR0, YR1)
Junction

0 is by default the state closest to the junction, with numbers increasing going away from the junction. 
Currently 0 is in the junction, 1 is up to the first yard (YL0/ YR0), 2 is in between the yards, 3 is between the second yard the depot, including the first bay. Bays 0 to 5 are then locations 3 to 8.

All measurements in global data are in millimetres. All time measurements are in milliseconds.
