# physics-sim
Physics simulation for MESA engineering

VERSION 1.0
There's no UI for changing variables, so changes have to be done directly in the code.

Changing num_of_objs (currently line 85 of main.py) could result in an error due to 
pygame.draw.circle(screen, (n * 10, 0, 0), (objects[n].position.x, objects[n].position.y), objects[n].shape.radius)
in lines 123 and 124. Lower the number multiplied by n (10, in this case) to fix this.
This was initially a way for me to tell each circle apart by color and has been kept
because it looks better.

Next version will focus on optimization. After that I hope to implement a UI and reset 
function so that you don't have to quit the program for each new simulation. Boxes will 
be added at some point after that.
