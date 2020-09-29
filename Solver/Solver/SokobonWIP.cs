
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;

public class Module
{
    public HashSet<int> knownPositions;
    public Module()
    {
        knownPositions = new HashSet<int>();

    }

    public void Go()
    {
        var prev_states = new List<object>();
        var directions = new List<Direction> {
                Direction.up,
                Direction.down,
                Direction.left,
                Direction.right
            };
        // directions = ["left", "right"]
        char[][] map = Parse();
        AddMapToHashList(map);
        List<char[][]> openList = new List<char[][]>(10000000);

        openList.Add(map);
        var watch = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < openList.Count; i++)
        {
            if (i % 10000 == 0)
                Console.WriteLine("Step: " + i+ "       Seconds: "+ watch.Elapsed.TotalSeconds);
            foreach (var d in directions)
            {
                char[][] newMap = openList[i].Select(a => a.ToArray()).ToArray();
                MoveSokoban(newMap, d);
                if (newMap != null && AddMapToHashList(newMap))
                    openList.Add(newMap);
            }
        }
    }
    public struct Point
    {
        public byte x { get; set; }
        public byte y { get; set; }
        public Point(byte x, byte y)
        {
            this.x = x;
            this.y = y;
        }
        public Point(int x, int y)
        {
            this.x = (byte)x;
            this.y = (byte)y;
        }
    }

    public enum Direction
    {
        up = 0,
        down = 1,
        left = 2,
        right = 3
    }
    public static char[][] Parse(string textFile = "Sokoban_map2019.txt")
    {
        string fullPath = System.Reflection.Assembly.GetAssembly(typeof(Module)).Location;
        //get the folder that's in
        string dir = Path.GetDirectoryName(fullPath);
        List<char[]> lines = new List<char[]>();
        foreach (string line in File.ReadLines(Path.Combine(dir, textFile)))
        {
            lines.Add(line.ToCharArray());
        }
        var char_array = lines.ToArray();
        return char_array;
    }

    public static Point? FindSokobanOnMap(char[][] map)
    {
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                if (map[i][k].Equals('@') || map[i][k].Equals('+'))
                {
                    return new Point(i, k);
                }
            }
        }
        return null;
    }

    public static object FindCansOnMap(char[][] map)
    {
        var cans = new List<Point>();
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                if (map[i][k].Equals('$') || map[i][k].Equals('*'))
                {
                    cans.Add(new Point(i, k));
                }
            }
        }
        return cans;
    }

    //public static object closestCan(object soko_pos, object cans_pos)
    //{
    //    var dist = new List<object>();
    //    foreach (var i in Enumerable.Range(0, cans_pos.Count))
    //    {
    //        var soko_x = Convert.ToInt32(soko_pos["row"]);
    //        var soko_y = Convert.ToInt32(soko_pos["column"]);
    //        var can_x = Convert.ToInt32(cans_pos[i]["row"]);
    //        var can_y = Convert.ToInt32(cans_pos[i]["column"]);
    //        dist.append(np.sqrt(soko_x * can_x + soko_y * can_y));
    //    }
    //    var nearestcan = dist.index(min(dist));
    //    return nearestcan;
    //}

    public static object PositionOnMap(char[][] map, Point position)
    {
        char pos = map[position.x][position.y];
        return pos;
    }

    public static void SetPositionOnMap(char[][] map, Point position, char positionValue)
    {
        map[position.x][position.y] = positionValue;
    }

    public static void WalkSokoban(char[][] map, Point oldPosition, Point newPosition, char newPositionValue)
    {
        map[newPosition.x][newPosition.y] = newPositionValue;
        if (PositionOnMap(map, oldPosition).Equals('+'))
        {
            SetPositionOnMap(map, oldPosition, '.');
        }
        else
        {
            SetPositionOnMap(map, oldPosition, ' ');
        }
    }

    public static bool PointInRange(char[][] map, Point p)
    {
        if (p.x > map.Length || p.y > map[0].Length)
            return false;
        else
            return true;
    }

    public static bool MoveBox(char[][] map, Point boxPosition, Direction direction)
    {
        Point nextPosition;
        switch (direction)
        {
            case Direction.down: nextPosition = new Point(boxPosition.x, boxPosition.y + 1); break;
            case Direction.up: nextPosition = new Point(boxPosition.x, boxPosition.y - 1); break;
            case Direction.right: nextPosition = new Point(boxPosition.x + 1, boxPosition.y); break;
            case Direction.left: nextPosition = new Point(boxPosition.x - 1, boxPosition.y); break;
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

    public static object MoveSokoban(char[][] map, Direction direction)
    {
        Point? currentPosition = FindSokobanOnMap(map);
        if (currentPosition == null)
            return null;
        Point nextPosition;
        switch (direction)
        {
            case Direction.down: nextPosition = new Point(currentPosition.Value.x, currentPosition.Value.y + 1); break;
            case Direction.up: nextPosition = new Point(currentPosition.Value.x, currentPosition.Value.y - 1); break;
            case Direction.right: nextPosition = new Point(currentPosition.Value.x + 1, currentPosition.Value.y); break;
            case Direction.left: nextPosition = new Point(currentPosition.Value.x - 1, currentPosition.Value.y); break;
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
            return null;
        }
        else if (PositionOnMap(map, nextPosition).Equals('$'))
        {
            //let's move the box
            if (MoveBox(map, nextPosition, direction))
            {
                WalkSokoban(map, currentPosition.Value, nextPosition, '@');
                CheckIfSolved(map);
            }
            else
            {
                return null;
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
                WalkSokoban(map, currentPosition.Value, nextPosition, '+');
            }
            else
            {
                return null;
            }
        }
        return map;
    }


    public bool AddMapToHashList(char[][] map)
    {
        if (map == null)
        {
            return false;
        }
        string stringMap = "";
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                stringMap += map[i][k];
            }
        }
        int hashCode = stringMap.GetHashCode();
        if (knownPositions.Contains(hashCode))
            return false;
        else
        {
            knownPositions.Add(hashCode);
            return true;
        }
    }

    public static object CheckIfSolved(char[][] map)
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
        throw new Exception("We did it, it's solved!!!");
    }

    //public static object AddLeafsMap(object tree, object directions, object prev_states)
    //{
    //    var newStates = 0;
    //    var oldStates = 0;
    //    foreach (var leave in tree.leaves)
    //    {
    //        foreach (var d in directions)
    //        {
    //            var newMap = MoveSokoban(copy.deepcopy(leave.map), d);
    //            var hash = hashList(newMap, prev_states);
    //            if (hash != null)
    //            {
    //                Node(hash, parent: leave, map: newMap);
    //                newStates += 1;
    //            }
    //            else
    //            {
    //                oldStates += 1;
    //            }
    //        }
    //    }
    //    if (newStates == 0)
    //    {
    //        throw Exception("No solution found...");
    //    }
    //    Console.WriteLine("new States: {0}   old States: {1}".format(newStates, oldStates));
    //}

}
