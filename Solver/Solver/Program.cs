using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Collections;
using System.Text;
using System.Threading.Tasks;

/// Solve the sokoban quiz with the A* algorithm, exports RobotCommands and StepDescription for robot, needs target map as input.
namespace Solver
{
    public class Program
    {
        static void Main(string[] args)
        {
            string fullPath = System.Reflection.Assembly.GetAssembly(typeof(SokobanSolver)).Location;
            string dir = Path.GetDirectoryName(Path.Combine(fullPath));
            SokobanSolver solver = new SokobanSolver();
            string targetPath = Path.Combine(dir, "../../../", "Tests//Map 2020");
            solver.Go(Path.Combine(targetPath, "Sokoban_map2020.txt"));
            //string targetPath = Path.Combine(dir, "../../../", "Tests//Map 2019");
            //solver.Go(Path.Combine(targetPath, "Sokoban_map2019_formatted.txt"));
            solver.ExportResults(Path.Combine(targetPath, "RobotCommands.txt"), Path.Combine(targetPath, "StepDescription.txt"));
        }

    }
}