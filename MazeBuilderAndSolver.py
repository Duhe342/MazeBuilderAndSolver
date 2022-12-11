from random import random, randint, choice
from copy import deepcopy
from time import perf_counter


print("Задание 7.1")
density = float
xy = int


def mazebuilder():
    global density, xy
    ############# Генерируем пустой лабиринт с обрамляющей стеной
    maze = []

    xy = 10

    # xy = randint(5,50) #  при xy > 20 мне потребуется супер компьютер
    exits = randint(1, int(xy))
    density = random()


    for i in range(xy):
        maze.append([' ' for _ in range(xy)])

    walls = []

    for i in range(xy):
        maze[0][i] = "#"
        walls.append([0, i])
    for i in range(xy):
        maze[i][xy - 1] = "#"
        walls.append([i, xy])
    for i in range(xy):
        maze[xy - 1][i] = "#"
        walls.append([xy, i])
    for i in range(xy):
        maze[i][0] = "#"
        walls.append([i, 0])

    ############# Вставляем выходы

    haveExits = 0

    while haveExits < exits:
        new = choice(walls)

        if maze[new[0] - 1][new[1] - 1] != " ":
            maze[new[0] - 1][new[1] - 1] = " "
            haveExits += 1

    allCords = []
    for i in range(xy - 1):
        for e in range(xy - 1):
            allCords.append([i, e])

    ########### Строим стены

    ro = density
    antiRo = 1 - ro
    times = 0
    changed = False

    if ro < 0.5:
        highRo = ro / 2
    else:
        highRo = antiRo / 2

    for i in range(1, xy - 1):
        for e in range(1, xy - 1):
            times = 0
            placed = False
            if maze[i + 1][e] == "#" and changed is False:
                ro += highRo
            if random() <= ro:
                maze[i][e] = "#"
                placed = True
                changed = True
            ro = density

            if placed is True:
                if ro < 0.5:
                    ro = ro / 2
                else:
                    ro -= antiRo

            times += 1
            if times == 2:
                times = 0
                changed = False
                ro = density

    return maze


print("Задание 7.2")


def print_maze(maze):
    y = len(maze)

    for i in range(y):
        print("".join(maze[i]).replace("#", "#"))


def validate_input(maze):
    try:
        x = int(input("Введите значение x "))
        y = int(input("Введите значение y "))
    except NameError:
        print("Вы ввели неприемломое значение координат")

    except ValueError:
        print("Вы не задали значение одной из координат")
        x = 0
        y = 0

    lnMaze = len(maze)
    cord = [y, x]

    emptSpaces = []

    for i in range(lnMaze - 1):
        for e in range(lnMaze - 1):
            if maze[i][e] == " ":
                emptSpaces.append([i, e])
    if y >= lnMaze or x >= lnMaze:
        cord = choice(emptSpaces)

    y = cord[0]
    x = cord[1]

    if maze[y][x] == "#":
        cord = choice(emptSpaces)

    return cord


myMaze = mazebuilder()
for i in myMaze:
    print(i)

myMazeCopy = deepcopy(myMaze)

lnMaze = len(myMaze)

print("3a")

y, x = validate_input(myMaze)
print(f"cord {[y, x]}")
print("3b")

exitCord = []

for i in range(1, lnMaze - 1):
    if myMaze[0][i] != "#":
        exitCord.append([0, i])

for i in range(1, lnMaze - 1):
    if myMaze[i][lnMaze - 1] != "#":
        exitCord.append([i, lnMaze - 1])

for i in range(1, lnMaze - 1):
    if myMaze[lnMaze - 1][i] != "#":
        exitCord.append([lnMaze - 1, i])

for i in range(1, lnMaze - 1):
    if myMaze[i][0] != "#":
        exitCord.append([i, 0])

auf = 0
while auf < len(exitCord):
    print(f"Выход {auf + 1} - {exitCord[auf]}")
    auf += 1

wave = {
    "Way": [[y, x]],
    "Steps": 0,
    "Direction": 2
}

waves = [wave]

turning = ['down', 'left', 'up', 'right']


def posibDirections(wave):
    bufX = wave["Way"][-1][1]
    bufY = wave["Way"][-1][0]

    try:
        prevCoor = wave["Way"][-2]
    except IndexError:
        prevCoor = wave["Way"][-1]

    rightCord = [bufY, bufX + 1]
    leftCord = [bufY, bufX - 1]
    upCord = [bufY - 1, bufX]
    downCord = [bufY + 1, bufX]

    positions = [rightCord, leftCord, upCord, downCord]
    possiblePosition = []

    for i in positions:
        if myMaze[i[0]][i[1]] == " " and i != prevCoor:
            possiblePosition.append(i)

    return possiblePosition


def chooseDirection(wave, way):
    position = wave["Way"][-1]

    if way[0] < position[0]:
        newDir = 2
    elif way[0] > position[0]:
        newDir = 0
    elif way[1] < position[1]:
        newDir = 1
    else:
        newDir = 3

    return newDir


def copyWave(dir, wave, waves_list):
    # newWave = wave.copy()
    newWave = deepcopy(wave)
    newWave["Direction"] = dir
    waves_list.append(newWave)


def step(wave):
    global turning

    bufX = wave["Way"][-1][1]
    bufY = wave["Way"][-1][0]

    if turning[wave["Direction"]] == "right":
        bufX += 1
    elif turning[wave["Direction"]] == "left":
        bufX -= 1
    elif turning[wave["Direction"]] == "up":
        bufY -= 1
    elif turning[wave["Direction"]] == "down":
        bufY += 1

    wave["Steps"] += 1
    new_coordinates = [bufY, bufX]
    wave["Way"].append(new_coordinates)


print("3c")
print("Ожидайте, идут расчеты...")
print()

finish = []


def start():
    global waves, finish, lnMaze, density, xy
    time = perf_counter()

    while True:
        waves_copy = []
        checker = 0
        for i in waves:
            try:
                possible_cords = posibDirections(i)
            except IndexError:
                continue
            for dir in possible_cords:
                new_direction = chooseDirection(i, dir)
                copyWave(new_direction, i, waves_copy)


        waves = deepcopy(waves_copy)

        for i in range(len(waves)):
            waves[i]["Way"] = deepcopy(waves[i]["Way"])

            step(waves[i])

            if waves[i]['Way'][-1] in exitCord:
                finish.append(waves[i])
                myMaze[waves[i]["Way"][-1][0]][waves[i]["Way"][-1][1]] = "#"
                waves = [wave]
                checker = 1
                break

        if checker == 1:
            start()
            break

        if len(finish) >= len(exitCord):
            break

        if perf_counter() - time > 1.3 / density:
            break


start()

Way = []
for i in finish:
    Way.append(i["Way"])

exitStep = []

for i in Way:
    exitStep.append(i[-1])


for i in range(len(exitCord)):

    for e in range(len(exitStep)):
        if exitCord[i] == exitStep[e]:
            print(f"Выход {i + 1} - да")
            break
        if e + 1 == len(exitStep):
            print(f"Выход {i + 1} - нет")

if len(exitStep) == 0:
    for i in range(len(exitCord)):
        print(f"Выход {i + 1} - нет")

print("3d")

noGood = 0

try:
    print(
        f'Кратчайший путь из начальной точки {[y, x]} – {finish[0]["Steps"]} шагов до выхода в {finish[0]["Way"][-1]}')
except IndexError:
    noGood = 1
    print("Нельзя достичь ни одного выхода")

print("3e")

if noGood == 1:
    print("Нельзя достичь ни одного выхода")

for i in finish:
    for e in i['Way']:
        xe = e[1]
        ye = e[0]
        myMazeCopy[ye][xe] = "+"

t = 1
for i in finish:
    print(f'Выход {i["Way"][-1]}')
    print(f'Кол-во шагов: {i["Steps"]}')

    print()
    t += 1

myMazeCopy[y][x] = "0"
for i in myMazeCopy:
    print(i)
