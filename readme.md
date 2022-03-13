# Overview
This work is based on the assignment during the AI01 course at the University of Southern Denmark, the full report can be see [here](Artificial_Intelligence_Sokoban.pdf).
The assignment given, is to create a robot out of Lego Mindstorms which is able to autonomously execute a Sokoban quiz. This includes a solver for the quiz, a design of the physical structure of the robot and to give it the ability to follow lines, push objects and turn on a given map.

# Syntax
The map is represented as following:
|Icon| Representation   |
|---|-------------------|
|’#’|wall               |
|’ ’| free space        |
|’$’| box               |
|’.’| goal              |
|’*’| box placed on goal|
|’@’| Sokoban           |
|’+’| Sokoban on goal   |

# Usage
First a valid map needs to be given to the Solver, which solves the map for the shortest path with an A* algorithm.
The ouput is a file which contains all commands for the robot, as well as a "Step Description", which prints a valid map after each step for debugging.
A map could look like [following](Solver/Tests/Map%202019/Sokoban_map2019_formatted.txt):
<pre>
XXXXXXXXXXXX
XX   X     X
XX   X ..  X
XX$$$ X..XXX
X $    @XXXX
X   X   XXXX
XXXXXXXXXXXX 
</pre>

Afterwards the step description needs to be copied to (robotfiles/Sokoban_Moves.txt)[robotfiles/Sokoban_Moves.txt]. The [main](robotfiles/main.py) program will parse the moves and execute it. 

# Tips and hints
Most likely the turn and line following parameters need to be fine tuned, dependent on the construction of the robot. Therefore it might be a good idea to reduce the speed significantly and start with the function "RunDebug" in main.py. The performance of the robot varies dependent on the battery level, so ensure to charge it frequently and tune the parameters only with a fully charged battery.