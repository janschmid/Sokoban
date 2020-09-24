import numpy as np
import hashlib



def parse(map = 'Sokoban_map.txt'):
  ### Line Parser ###
  # Using readlines() 
  map_txt = open(map, 'r') 
  Lines = map_txt.readlines() 
  

  map_ls = []
  # Strips the newline character 
  for line in Lines: 
    line = line.strip("\n")
    temp = []
    for ch in line:
      temp.append(ch)
    map_ls.append(temp)
  return map_ls




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

def hashList(ls, Hash_ls):
  s = ' '.join([str(elem) for elem in ls]) 
  new_hash = hashlib.sha256(s.encode())
  new_hash = new_hash.hexdigest()

  if (ismember(Hash_ls,new_hash)):
    Hash_ls.append(new_hash)
  
  return Hash_ls


def ismember(ls, num):
    for i in range(np.size(ls)):
      if (i == num):
        return 0
    return 1
    

def main():
    prev_states = []
    map = parse()
    prev_states = hashList(map, prev_states)


if __name__ == "__main__":
  main()