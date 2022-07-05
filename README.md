# n-body-simulation
A simulation of gravitationally bound particles with an interactable graphical user interface.

# Screenshot
![User interface](/images/user_interface.png "User interface")

# Controls
* `LEFT MOUSE BUTTON` - hold and drag the cursor around to move the camera
* `RIGHT MOUSE BUTTON` - spawn a new particle at the location of the cursor
* `SCROLL WHEEL` - zoom in/out on the position of the cursor
* `LEFT SHIFT` - hold to increase zoom in/out speed
* `W` `A` `S` `D` or `↑` `←` `↓` `→` - move the camera using the keyboard
* `ESC` - exit the application

# Repository structure
* `/` - main components of the application like the viewport or input handling
* `/calculators/` - methods for calculating forces applying on simulation particles, currently just the O(n^2) strategy of comparing all particle pairs is implemented
* `/integrators/` - methods for translating calculated forces into particle movements over the timespan of the simulation, currently Euler with Leapfrog or its variants planned in the future
* `/models/` - objects for holding the state of various parts of the system like particles or camera 
