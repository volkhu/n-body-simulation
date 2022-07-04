# n-body-simulation
A simulation of gravitationally bound particles with an interactable graphical user interface.

# Repository structure
* `/` - main components of the application like the viewport or input handling
* `/calculators/` - methods for calculating forces applying on simulation particles, currently just the O(n^2) strategy of comparing all particle pairs is implemented
* `/integrators/` - methods for translating calculated forces into particle movements over the timespan of the simulation, currently Euler with Leapfrog or its variants planned in the future
* `/models/` - objects for holding the state of various parts of the system like particles or camera 
