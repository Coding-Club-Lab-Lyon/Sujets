from cc_maze.maze import *

path = []

def algo(value):
    if (map[posY][posX + 1] == 0 or map[posY][posX + 1] == 2):
        right()
        path.append("right")
    elif (map[posY + 1][posX] == 0 or map[posY + 1][posX] == 2):
        down()
        path.append("down")
    elif (map[posY][posX - 1] == 0 or map[posY][posX - 1] == 2):
        left()
        path.append("left")
    elif (map[posY - 1][posX] == 0 or map[posY - 1][posX] == 2):
        up()
        path.append("up")
    else:
        if (path[-1] == "up"):
            down()
        elif (path[-1] == "left"):
            right()
        elif (path[-1] == "down"):
            up()
        elif (path[-1] == "right"):
            left()
        path.pop()
    print(path)



filepath = 'map.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 0
   while line:
       x = line.find('x')
       while x != -1:
           setACaseXY(x, cnt, 'red')
           map[cnt][x] = 1
           x = line.find('x', x + 1)
       x = line.find('o')
       if (x != -1):
           setACaseXY(x, cnt, 'green')
           map[cnt][x] = 2
       line = fp.readline()
       cnt += 1

w.pack()

for value in range(0, 1000):
    master.after(value * 100, algo, value)

checkered(w,10)

mainloop()

