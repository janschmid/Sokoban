
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class Module
{
    //public HashSet<int> knownPositions;
    Dictionary<int, KeyValuePair<int, Direction?>> knownPositions;
    public Module()
    {
        knownPositions = new Dictionary<int, KeyValuePair<int, Direction?>>();
    }

    public void Go()
    {
        var prev_states = new List<object>();
        var directions = new List<Direction> {
                Direction.u,
                Direction.d,
                Direction.l,
                Direction.r
            };
        // directions = ["left", "right"]
        char[][] map = Parse();
        AddMapToHashList(map, null, null);
        List<char[][]> openList = new List<char[][]>(10000000);

        openList.Add(map);
        var watch = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < openList.Count; i++)
        {
            if (i % 10000 == 0)
                Console.WriteLine("Step: " + i + "       Seconds: " + watch.Elapsed.TotalSeconds);
            foreach (var d in directions)
            {
                char[][] newMap = openList[i].Select(a => a.ToArray()).ToArray();
                if (!MoveSokoban(newMap, d))
                {
                    if (newMap != null && AddMapToHashList(newMap, openList[i], d))
                        openList.Add(newMap);
                }
                else
                {
                    //we solved it...
                    AddMapToHashList(newMap, openList[i], d);
                    FindPath(newMap);
                    return;
                }
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
        u = 0,
        d = 1,
        l = 2,
        r = 3
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
                    return new Point(k, i);
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
                    cans.Add(new Point(k, i));
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
        char pos = map[position.y][position.x];
        return pos;
    }

    public static void SetPositionOnMap(char[][] map, Point position, char positionValue)
    {
        map[position.y][position.x] = positionValue;
    }

    public static void WalkSokoban(char[][] map, Point oldPosition, Point newPosition, char newPositionValue)
    {
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

    public static bool PointInRange(char[][] map, Point p)
    {
        if (p.y > map.Length || p.x > map[0].Length)
            return false;
        else
            return true;
    }

    public static bool MoveBox(char[][] map, Point boxPosition, Direction direction)
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

    public static bool MoveSokoban(char[][] map, Direction direction)
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
                WalkSokoban(map, currentPosition.Value, nextPosition, '+');
            }
            else
            {
                return false;
            }
        }
        return false;
    }


    public bool AddMapToHashList(char[][] map, char[][] oldMap, Direction? d)
    {
        if (map == null)
        {
            return false;
        }
        int hashCode = GetHashFromMap(map);
        if (knownPositions.ContainsKey(hashCode))
            return false;
        else
        {
            knownPositions.Add(hashCode, new KeyValuePair<int, Direction?>(GetHashFromMap(oldMap), d));
            return true;
        }
    }

    private void FindPath(char[][] targetMap)
    {
        List<Direction> path = new List<Direction>();
        int hash = GetHashFromMap(targetMap);
        KeyValuePair<int, Direction?> outVal;
        int count = 0;
        while (knownPositions.TryGetValue(hash, out outVal) && outVal.Key != 0)
        {
            hash = outVal.Key;
            if (outVal.Value.HasValue)
                path.Add(outVal.Value.Value);
            count++;
            Console.WriteLine(count);
        }
        path.Reverse();
        TextWriter tw = new StreamWriter("SavedList.txt");
        foreach (var d in path)
        {
            tw.Write(d);

        }
        tw.WriteLine("");
        tw.WriteLine("Steps: " + count);
        tw.Close();
        
    }

    private int GetHashFromMap(char[][] map)
    {
        string stringMap = "";
        if (map == null)
            return 0;
        for (int i = 0; i < map.Length; i++)
        {
            for (int k = 0; k < map[i].Length; k++)
            {
                stringMap += map[i][k];
            }
        }
        return stringMap.GetHashCode();

    }

    public static bool CheckIfSolved(char[][] map)
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
