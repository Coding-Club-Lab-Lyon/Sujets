from tkinter import *

incr = 2
size = incr * 10
posX = 1
posY = 1
map = [[]] * 100

for value in range(0, 100):
    map[value] = [0] * 100

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x * (incr), 0, x * (incr), canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y * (incr), canvas_width, y * (incr), fill="#476042")

def right():
    global posX
    global posY
    if (map[posY][posX + 1] == 1):
        return
    setACaseXY(posX, posY, 'grey')
    map[posY][posX] = -1
    posX += 1
    setACaseXY(posX, posY, 'yellow')
    if (map[posY][posX] == 2):
        exit(0)

def left():
    global posX
    global posY
    if (map[posY][posX - 1] == 1):
        return
    setACaseXY(posX, posY, 'grey')
    map[posY][posX] = -1
    posX -= 1
    setACaseXY(posX, posY, 'yellow')
    if (map[posY][posX] == 2):
        exit(0)

def up():
    global posY
    global posX
    if (map[posY - 1][posX] == 1):
        return
    setACaseXY(posX, posY, 'grey')
    map[posY][posX] = -1
    posY -= 1

    setACaseXY(posX, posY, 'yellow')
    if (map[posY][posX] == 2):
        exit(0)

def down():
    global posY
    global posX
    if (map[posY + 1][posX] == 1):
        return
    setACaseXY(posX, posY, 'grey')
    map[posY][posX] = -1
    posY += 1
    setACaseXY(posX, posY, 'yellow')
    if (map[posY][posX] == 2):
        exit(0)


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


def setACaseXY(X, Y, color):
    points = [X * size, Y * size, size * (X + 1), Y * size, size * (X + 1), size * (Y + 1), X * size, size * (Y + 1)]
    w.create_polygon(points, outline="#476042", fill=color, width=4)


master = Tk()
master.title("Le Fil d'Ariane")
canvas_width = 1280
canvas_height = 620
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)




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
