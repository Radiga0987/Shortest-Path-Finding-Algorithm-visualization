# Shortest-Path-Finding-Algorithm-visualization
In this project, the famous Astar algorithm has been implemented on python. The program creates a grid on which the user can set a start node and end node and place several obstacles in the way.Once executed, the program visualizes how the given algorithm is working and after execution , it shows the shortest path between these 2 nodes .
A few examples of what the code does have been shown below.
The white box is the start node whereas the orange box is the end/target node.The shortest path found by the algorithm is the yellow path linkin the 2 nodes.
The Light blue boxes are the boxes that the algorithm has gone through during code execution and the green boxes are the ones that were going to be used in the next iteration.
The Black box can be viewed as walls that blobk any possible paths through them and hence the algorithm has to find a way around them.


Image of a simple shortest path found:

![SPF_1](https://user-images.githubusercontent.com/70105902/126061926-21ad0b6e-b80a-43f6-9e9b-01d8fe469eee.JPG)

Image of a much more complex maze:

![SPF_2](https://user-images.githubusercontent.com/70105902/126062107-8bd77409-8756-4a4b-a70f-7a302a0b15e3.JPG)

## How to use:
1. Make sure required modules are installed(pip install pygame).
2. A grid will be generated on which one can click boxes to highlight them.
3. The first click will create the start node and the second click will create the end node.
4. Any subsequent clicks will result in the creation of walls in black.
5. To reset any of the individual colored boxes, just right click on them and they will be reset to a normal box.
6. If there is need to reset the whole grid, just click the space bar on your keyboard.Reset cannot be done during execution.
7. After setting up the start and end nodes and any required walls, just hit the enter key and algorithm will start working on finding the shortest path.
8. Once execution is complete, the shortest path will be highlighted in yellow(If such a path exists)
9. Feel free to mess around with the color coding if you dont like my current format.
