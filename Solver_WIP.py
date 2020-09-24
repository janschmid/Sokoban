import numpy as np




def parse(map = 'Sokoban_map.txt'):
  ### Line Parser ###
  # Using readlines() 
  map_txt = open(map, 'r') 
  Lines = map_txt.readlines() 
  
  count = 0
  map_ls = []
  # Strips the newline character 
  for line in Lines: 
    line = line.strip("\n")
    temp = []
    for ch in line:
      temp.append(ch)
    map_ls.append(temp)
  print(map_ls)





#
# def move_sokoban(map, direction):
#  switch (){
#  case 1: wall
#  case 2: can 
#  case 3: empty
#  case 4: goal
#  case 5: can_on_goal
#  }
#  check hash



def main():
    parse()


if __name__ == "__main__":
  main()