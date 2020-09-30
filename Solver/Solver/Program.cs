using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solver
{
    class Program
    {
        static void Main(string[] args)
        {
            string fullPath = System.Reflection.Assembly.GetAssembly(typeof(SokobanSolver)).Location;
            string dir = Path.GetDirectoryName(fullPath);
            SokobanSolver solver = new SokobanSolver();
            solver.Go(Path.Combine(dir, "Sokoban_map2019.txt"));
            solver.ExportResults(Path.Combine(dir, "../../RobotCommands.txt"), Path.Combine(dir, "../../StepDescription.txt"));
        }
    }
}
