import numpy as np
import copy
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
  


def FindSokobanOnMap(map):
  for i in range(len(map)):
    for k in range(len(map[0])):
      if(map[i][k] == '@' or map[i][k] == '+'):
        return {"row": i, "column":k}

def FindCansOnMap(map):
  cans = []
  for i in range(len(map)):
    for k in range(len(map[0])):
      if(map[i][k] == '$' or map[i][k] == '*'):
        cans.append({"row": i, "column":k})
  return cans

def closestCan(soko_pos,cans_pos):
  dist =[]
  count = 0
  for i in range(len(cans_pos)):
    soko_x = int(soko_pos["row"])
    soko_y = int(soko_pos["column"])
    can_x = int(cans_pos[i]["row"])
    can_y = int(cans_pos[i]["column"])
    dist.append(np.sqrt(soko_x*can_x+soko_y*can_y))
    
  nearestcan = dist.index(min(dist))
  return nearestcan

def PositionOnMap(map, position):
  pos= map[int(position["row"])][int(position["column"])]
  return pos

def SetPositionOnMap(map, position, positionValue):
  map[int(position["row"])][int(position["column"])] = positionValue

def WalkSokoban(map, oldPosition, newPosition, newPositionValue):
  map[int(newPosition["row"])][int(newPosition["column"])] = newPositionValue
  if(PositionOnMap(map, oldPosition) == '+'):
    SetPositionOnMap(map, oldPosition, '.')
  else:
    SetPositionOnMap(map, oldPosition, ' ')

def MoveBox(map, boxPosition, direction):
  nextPosition = copy.copy(boxPosition)
  
  if(direction=="down"): 
    nextPosition["row"] = boxPosition["row"]+1
  elif(direction=="up"): 
    nextPosition["row"] = boxPosition["row"]-1
  elif(direction=="left"): 
    nextPosition["column"] = boxPosition["column"]-1
  elif(direction=="right"): 
    nextPosition["column"] = boxPosition["column"]+1
  else:
    raise Exception("Sorry, i don't know where you want to go: {0}".format(direction))


  if(int(nextPosition["column"])<0 or int(nextPosition["row"])<0 or 
    int(nextPosition["column"]) > len(map) or int(nextPosition["column"])> len(map[0])):
    return False
  
  #free, let's go
  if(PositionOnMap(map, nextPosition) == ' '):
    SetPositionOnMap(map, nextPosition, '$')
  elif(PositionOnMap(map, nextPosition) == '.'):
    SetPositionOnMap(map, nextPosition, '*')
  else:
    return False
  return True
    

def MoveSokoban(map, direction):
  currentPosition = FindSokobanOnMap(map)  
  nextPosition = copy.copy(currentPosition)

  if(direction=="down"): 
    nextPosition["row"] = currentPosition["row"]+1
  elif(direction=="up"): 
    nextPosition["row"] = currentPosition["row"]-1
  elif(direction=="left"): 
    nextPosition["column"] = currentPosition["column"]-1
  elif(direction=="right"): 
    nextPosition["column"] = currentPosition["column"]+1
  else:
    raise Exception("Sorry, i don't know where you want to go: {0}".format(direction))

  #check if position is valid
  if(int(nextPosition["column"])<0 or int(nextPosition["row"])<0 or 
    int(nextPosition["column"]) > len(map) or int(nextPosition["column"])> len(map[0])):
    return None
  
  if(PositionOnMap(map, nextPosition) == ' '):
    #free spot, let's go
    WalkSokoban(map, currentPosition, nextPosition, '@')
  elif(PositionOnMap(map, nextPosition) == '#'):
    #wall, we can't go here, so here is a dead end...
    return None
  elif(PositionOnMap(map,nextPosition) == '$'):
    #let's move the box
    if(MoveBox(map, nextPosition, direction)):
      WalkSokoban(map, currentPosition, nextPosition, '@')
    else:
      return None
  elif(PositionOnMap(map, nextPosition) == '.'):
    WalkSokoban(map, currentPosition, nextPosition,'+')
  elif(PositionOnMap(map, nextPosition) == '*'):
    if(MoveBox(map, nextPosition, direction)):
      WalkSokoban(map, currentPosition, nextPosition, '+')
    else:
      return None
  CheckIfSolved(map)
  return (map)

def hashList(map,hList):
  if(map==None):
    return True
  s = ' '.join([str(elem) for elem in map]) 
  new_hash = hashlib.sha256(s.encode())
  new_hash = new_hash.hexdigest()

  if (ismember(hList,new_hash)):
    hList.append(new_hash)
    return False
  return True




def ismember(ls, num):
    for i in range(np.size(ls)):
      if (ls[i] == num):
        return 0
    return 1
  
def CheckIfSolved(map):
  for i in range(len(map)):
    for k in range(len(map[i])):
      if(map[i][k] == '$'):
        return False
  raise Exception("We did it, it's solved!!!")

def main():
    prev_states = []
    directions = ["up", "down", "left", "right"]
    # directions = ["left", "right"]
    map = parse()
    
    
    hashList(map, prev_states)
    openList=[]
    openList.append(map)
    count = 0
    while(count< len(openList)):
      #print (count)
      for d in directions:
        newMap = MoveSokoban(copy.deepcopy(openList[count]), d)
       
        if(hashList(newMap, prev_states) == False):
          openList.append(newMap)
      # newMapDown = MoveSokoban(openList[count], "down")
      # newMapLeft = MoveSokoban(openList[count], "left")
      # newMapRight = MoveSokoban(openList[count], "right")
      
      
      # if(hashList(newMapUp, prev_states) == False):
      #   openList.append(newMapUp)

      # if(hashList(newMapDown, prev_states) == False):
      #   openList.append(newMapDown)

      # if(hashList(newMapLeft, prev_states) == False):
      #   openList.append(newMapLeft)

      # if(hashList(newMapRight, prev_states) == False):
      #   openList.append(newMapRight)  
      count+=1




if __name__ == "__main__":
  main()