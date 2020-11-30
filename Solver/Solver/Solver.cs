
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Text;

/// <summary>
/// Sokoban solver (algorithm: brute force, not parallelized)
/// Syntax for map (thanks to Pavel Klavik):
/// “#” is a wall,
/// “ ” is a free space,
/// “$” is a box,
/// “.” is a goal place,
/// “*” is a boxes placed on a goal,
/// “@” is for Sokoban and
/// “+” is for Sokoban on a goal.
/// </summary>
public class SokobanSolver
{
    //private HashSet<int> knownPositions;
    private Dictionary<int, SokobanSingleStep> knownPositions;
    private char[][] targetLocation;
    private Direction startDirection = Direction.l;
    /// <summary>
    /// Create new instance of Sokoban solver
    /// </summary>
    public SokobanSolver()
    {
        knownPositions = new Dictionary<int, SokobanSingleStep>();
    }

    internal class SokobanSingleStep
    {
        internal int Cost { get; set; }
        internal int HashKey { get; set; }
        internal Direction? Direction { get; set; }
        internal char[][] Map { get; set; }
    }

    public void Go(string filePath)
    {
        if (!SolveSokoban(filePath))
            throw new Exception("Could not find solution for the map...");
    }


    /// <summary>
    /// /// Run this function after the solution was found. This function does save the result to text files
    /// </summary>
    /// <param name="solutionFilePath">File path where content for robot get stored</param>
    /// <param name="debugOutputPath">File path where debug output get's stored (each map iteration, number of steps)</param>
    public void ExportResults(string solutionFilePath, string debugOutputPath = null)
    {
        ExportResults(targetLocation, solutionFilePath, debugOutputPath);
    }

    private bool SolveSokoban(string pathToMap)
    {
        var prev_states = new List<object>();
        var directions = new List<Direction> {
                Direction.u,
                Direction.d,
                Direction.l,
                Direction.r

            };
        // directions = ["left", "right"]
        char[][] map = Parse(pathToMap);
        AddMapToHashList(map, null, startDirection);
        List<char[][]> openList = new List<char[][]>(10000000);

        openList.Add(map);
        var watch = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < openList.Count; i++)
        {
            if (i % 10000 == 0)
                Console.WriteLine("Iteration: " + i + "       Seconds: " + watch.Elapsed.TotalSeconds);

            foreach (var directionToGo in directions)
            {
                //required to pass as reference parameter
                Direction d = directionToGo;
                char[][] newMap = openList[i].Select(a => a.ToArray()).ToArray();
                if (!WalkSokobanSingleStep(newMap, ref d))
                {
                    if (newMap != null && AddMapToHashList(newMap, openList[i], d))
                        openList.Add(newMap);
                }
                else
                {
                    //we solved it...
                    AddMapToHashList(newMap, openList[i], d);
                    targetLocation = newMap;
                    return true;
                }
            }
        }
            return false;
    }


    /// <summary>
    /// Helper class to find the position on map
    /// </summary>
    internal struct Point
    {
        internal byte x { get; set; }
        internal byte y { get; set; }
        internal Point(byte x, byte y)
        {
            this.x = x;
            this.y = y;
        }
        internal Point(int x, int y)
        {
            this.x = (byte)x;
            this.y = (byte)y;
        }
    }

    /// <summary>
    /// Contains all 4 directions.
    /// Direction+=10 if a can get's pushed (capital)
    /// </summary>
    internal enum Direction
    {
        u = 0,
        l = 1,
        d = 2,
        r = 3,
        //Direction+=10 if a can get's pushed  
        U = 10,
        L = 11,
        D = 12,
        R = 13
    }


    private static char[][] Parse(string filePath)
    {
        List<char[]> lines = new List<char[]>();
        foreach (string line in File.ReadLines(filePath))
        {
            lines.Add(line.ToCharArray());
        }
        var char_array = lines.ToArray();
        return char_array;
    }

    /// <summary>
    /// Check where Sokoban is
    /// </summary>
    /// <param name="map"></param>
    /// <returns>Point of Sokoban (x, y)</returns>
    internal static Point? FindSokobanOnMap(char[][] map)
    {
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                if (map[i][k].Equals('@') || map[i][k].Equals('+'))
                {
                    return new Point(k, i);
                }
            }
        }
        return null;
    }

    /// <summary>
    /// Return character of position map
    /// </summary>
    /// <param name="map"></param>
    /// <param name="position"></param>
    /// <returns></returns>
    private static object PositionOnMap(char[][] map, Point position)
    {
        char pos = map[position.y][position.x];
        return pos;
    }

    /// <summary>
    /// Set character to given positino on map
    /// </summary>
    /// <param name="map"></param>
    /// <param name="position">location on map</param>
    /// <param name="positionValue">Char value to be set</param>
    private static void SetPositionOnMap(char[][] map, Point position, char positionValue)
    {
        map[position.y][position.x] = positionValue;
    }


    /// <summary>
    /// Single step on sokoban
    /// </summary>
    /// <param name="map"></param>
    /// <param name="oldPosition">currentPositon of Sokoban</param>
    /// <param name="newPosition">next Position of Sokoban</param>
    /// <param name="newPositionValue">Sokoban's position, has to be @ or +</param>
    private static void WalkSokoban(char[][] map, Point oldPosition, Point newPosition, char newPositionValue)
    {
        if (!(newPosition.Equals('+') || newPosition.Equals('@')))
            map[newPosition.y][newPosition.x] = newPositionValue;
        if (PositionOnMap(map, oldPosition).Equals('+'))
        {
            SetPositionOnMap(map, oldPosition, '.');
        }
        else
        {
            SetPositionOnMap(map, oldPosition, ' ');
        }
    }


    /// <summary>
    /// Check if point is valid
    /// </summary>
    /// <param name="map"></param>
    /// <param name="p"></param>
    /// <returns></returns>
    private static bool PointInRange(char[][] map, Point p)
    {
        if (p.y > map.Length || p.x > map[0].Length)
            return false;
        else
            return true;
    }

    /// <summary>
    /// Move the can, this function does NOT move Sokoban
    /// </summary>
    /// <param name="map"></param>
    /// <param name="boxPosition">Curreont Position of box</param>
    /// <param name="direction">direction to move</param>
    /// <returns>If the can was moved or not (if it's not possible)</returns>
    private static bool MoveBox(char[][] map, Point boxPosition, Direction direction)
    {
        Point nextPosition;
        switch (direction)
        {
            case Direction.d: nextPosition = new Point(boxPosition.x, boxPosition.y + 1); break;
            case Direction.u: nextPosition = new Point(boxPosition.x, boxPosition.y - 1); break;
            case Direction.r: nextPosition = new Point(boxPosition.x + 1, boxPosition.y); break;
            case Direction.l: nextPosition = new Point(boxPosition.x - 1, boxPosition.y); break;
            default: nextPosition = new Point(char.MaxValue, char.MaxValue); break;
        }
        if (!PointInRange(map, nextPosition))
            return false;
        //free, let's go
        if (PositionOnMap(map, nextPosition).Equals(' '))
        {
            SetPositionOnMap(map, nextPosition, '$');
        }
        else if (PositionOnMap(map, nextPosition).Equals('.'))
        {
            SetPositionOnMap(map, nextPosition, '*');
        }
        else
        {
            return false;
        }
        return true;
    }

    /// <summary>
    /// This function does move Sokoban on step into the selected direction (if possible).
    /// It moves the can and checks if the move is possible
    /// </summary>
    /// <param name="map"></param>
    /// <param name="direction"></param>
    /// <returns></returns>
    private static bool WalkSokobanSingleStep(char[][] map, ref Direction direction)
    {
        Point? currentPosition = FindSokobanOnMap(map);
        if (currentPosition == null)
            return false;
        Point nextPosition;
        switch (direction)
        {
            case Direction.d: nextPosition = new Point(currentPosition.Value.x, currentPosition.Value.y + 1); break;
            case Direction.u: nextPosition = new Point(currentPosition.Value.x, currentPosition.Value.y - 1); break;
            case Direction.r: nextPosition = new Point(currentPosition.Value.x + 1, currentPosition.Value.y); break;
            case Direction.l: nextPosition = new Point(currentPosition.Value.x - 1, currentPosition.Value.y); break;
            default: nextPosition = new Point(char.MaxValue, char.MaxValue); break;
        }
        if (!PointInRange(map, nextPosition))
            return false;

        if (PositionOnMap(map, nextPosition).Equals(' '))
        {
            //free spot, let's go
            WalkSokoban(map, currentPosition.Value, nextPosition, '@');
        }
        else if (PositionOnMap(map, nextPosition).Equals('#'))
        {
            //wall, we can't go here, so here is a dead end...
            return false;
        }
        else if (PositionOnMap(map, nextPosition).Equals('$'))
        {
            //let's move the box
            if (MoveBox(map, nextPosition, direction))
            {
                //We moved the box, let's make the direction capital (box moved)
                direction = (Direction)(((int)direction) + 10);
                WalkSokoban(map, currentPosition.Value, nextPosition, '@');
                if (CheckIfSolved(map))
                    return true;
            }
            else
            {
                return false;
            }
        }
        else if (PositionOnMap(map, nextPosition).Equals('.'))
        {
            WalkSokoban(map, currentPosition.Value, nextPosition, '+');
        }
        else if (PositionOnMap(map, nextPosition).Equals('*'))
        {
            if (MoveBox(map, nextPosition, direction))
            {
                //We moved the box, let's make the direction capital (box moved)
                direction = (Direction)(((int)direction) + 10);
                WalkSokoban(map, currentPosition.Value, nextPosition, '+');
            }
            else
            {
                return false;
            }
        }
        return false;
    }


    /// <summary>
    /// Add the current Map to the Hash list (including debug data)
    /// </summary>
    /// <param name="map">current map</param>
    /// <param name="oldMap">map from previous step (required to build Tree</param>
    /// <param name="d">Direction</param>
    /// <returns>Add was successful</returns>
    private bool AddMapToHashList(char[][] map, char[][] oldMap, Direction? d)
    {
        if (map == null)
        {
            return false;
        }
        int mapHash = GetHashFromMap(map);
        int oldMapHash = GetHashFromMap(oldMap);
        if (knownPositions.ContainsKey(mapHash))
        {
            var oldWaypoint = knownPositions[oldMapHash];
            var thisWaypoint = knownPositions[mapHash];
            var cost = CalculateWaypointCost(oldWaypoint.Direction, d);
            if (oldWaypoint.Cost + cost < thisWaypoint.Cost)
            {
                knownPositions[mapHash].Cost = oldWaypoint.Cost + cost;
                knownPositions[mapHash].Direction = d;
                knownPositions[mapHash].HashKey = oldMapHash;
                knownPositions[mapHash].Map = oldMap;
                return false;
            }
            else
                return false;

        }
        else
        {
            if (oldMapHash != 0)
            {

                var oldWaypoint = knownPositions[oldMapHash];
                knownPositions.Add(mapHash, new SokobanSingleStep()
                {
                    Cost = oldWaypoint.Cost + CalculateWaypointCost(oldWaypoint.Direction, d),
                    HashKey = oldMapHash,
                    Direction = d,
                    Map = oldMap
                });
                return true;
            }
            else
            {
                knownPositions.Add(mapHash, new SokobanSingleStep()
                {
                    Cost = CalculateWaypointCost(null, d),
                    HashKey = oldMapHash,
                    Direction = d,
                    Map = oldMap
                });
                return true;
            }
        }
    }

    enum WaypointCost
    {
        Straight = 10,
        Corner = 13,
        Push = 70,
        TurnAround = 15
    }
    private int CalculateWaypointCost(Direction? d1, Direction? d2)
    {
        if (!d1.HasValue || !d2.HasValue)
        {
            return 0;
        }
        int cost = 0;
        if ((int)d2 > 10)
        {
            cost += (int)WaypointCost.Push;
        }
        if ((int)d1 > 10)
            d1 -= 10;
        if ((int)d2 > 10)
            d2 -= 10;
        if (d1 == d2)
            cost += (int)WaypointCost.Straight;
        else if (((int)d1 - (int)d2) % 2 == 0)
            cost += (int)WaypointCost.TurnAround;
        else if (d1 != d2)
            cost += (int)WaypointCost.Corner;
        return cost;


    }

    /// <summary>
    /// /// Run this function after the solution was found. This function does save the result to text files
    /// </summary>
    /// <param name="targetMap">map where solution got found</param>
    /// <param name="solutionFilePath">File path where content for robot get stored</param>
    /// <param name="debugOutputPath">File path where debug output get's stored (each map iteration, number of steps)</param>
    private void ExportResults(char[][] targetMap, string solutionFilePath, string debugOutputPath = "")
    {
        List<SokobanSingleStep> path = new List<SokobanSingleStep>(300);
        path.Add(new SokobanSingleStep()
        {
            Map = targetMap,
        });
        string str = "";
        int hash = GetHashFromMap(targetMap);
        SokobanSingleStep outVal;
        TextWriter solutionWriter = new StreamWriter(solutionFilePath);
        TextWriter mapWriter = null;

        while (knownPositions.TryGetValue(hash, out outVal) && outVal.HashKey != 0)
        {
            hash = outVal.HashKey;
            if (outVal.Direction.HasValue)
                path.Add(outVal);
        }

        if (!string.IsNullOrEmpty(debugOutputPath))
        {
            mapWriter = new StreamWriter(debugOutputPath);
            mapWriter.WriteLine("Steps: " + (path.Count - 1));
            mapWriter.WriteLine("Costs: " + (knownPositions[GetHashFromMap(targetMap)].Cost));
            mapWriter.WriteLine("");
        }

        path.Reverse();

        for (int i = 0; i < path.Count; i++)
        {
            solutionWriter.Write(path[i].Direction);
            for (int j = 0; j < path[i].Map.Length; j++)
            {
                for (int k = 0; k < path[i].Map[j].Length; k++)
                {
                    str += path[i].Map[j][k];
                }
                if (mapWriter != null)
                    mapWriter.WriteLine(str);
                str = "";
            }
            if (mapWriter != null)
                mapWriter.WriteLine(str + "\n\n");
        }
        solutionWriter.Close();
        if (mapWriter != null)
            mapWriter.Close();
    }

    /// <summary>
    /// Get the hash value from Map array to string -> Hash of string
    /// </summary>
    /// <param name="map"></param>
    /// <returns>hash value</returns>
    private int GetHashFromMap(char[][] map)
    {
        StringBuilder sb = new StringBuilder();
        if (map == null)
            return 0;
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                sb.Append(map[i][k]);
            }
        }
        return sb.ToString().GetHashCode();
    }

    /// <summary>
    /// Check if the quiz was solved. This is the case when no can is on the field.
    /// </summary>
    /// <param name="map"></param>
    /// <returns>Solved?</returns>
    private static bool CheckIfSolved(char[][] map)
    {
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                if (map[i][k].Equals('$'))
                {
                    return false;
                }
            }
        }
        return true;
        //throw new Exception("We did it, it's solved!!!");
    }
}
