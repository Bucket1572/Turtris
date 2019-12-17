# Tetris made out of turtle. Only used turtle for the graphics and used playsound for background music.
import blocks as bk
import random as r
import turtle as t
import threading as th
from playsound import playsound

# settings
fps = 60

grid = 32

creator = t.Turtle()
draw = t.Turtle()
screen = t.Screen()

frame_hold = 30
consolefont = ("BitOut", 35, "normal")
specialfont = ("BitOut", 45, "normal")
titlefont = ("BitOut", 30, "normal")

lv_factor = pow(1 / frame_hold, 1 / 20) 

now = False
types = ['L', 'T', 'S', 'Z', 'I', 'O', 'R']

frame_count = 0

next_blocks = []
holding = False

hold_cool = False

trigger = False
final_chance = False

def init():
    '''
    init
        initializing the game
    '''
    global creators, screen, fps, consolefont, score

    # Screen Settings
    screen.setup(624,672,400,100)
    screen.setworldcoordinates(0, 672, 624, 0)
    screen.tracer(0, 0)
    screen.title("Turtris")
    screen.ontimer(update, 1000//fps) # Update Function
    screen.bgcolor('#000000')

    # Key Settings
    screen.onkeypress(press_A, 'a')
    screen.onkeypress(press_S, 's')
    screen.onkeypress(press_D, 'd')
    screen.onkeypress(press_Q, 'q')
    screen.onkeypress(press_E, 'e')
    screen.onkeypress(hold, 'h')

    # Turtle settings
    creator.ht()
    creator.speed(0)
    creator.pu()

    draw.ht()
    draw.speed(0)
    draw.pu()

    # Block initializing
    for i in range(5):
        next_blocks.append(new_block())
        
    # Drawing default screen
    creator.pensize(4)
    creator.pencolor('white')
    
    # Default screen
    creator.goto(60, 48)
    creator.write("hold", move = False, align = "center", font = consolefont)
    creator.goto(-5, 48)
    creator.pd()
    creator.goto(120, 48)
    creator.goto(120, 48 + 125)
    creator.goto(-5, 48 + 125)
    creator.goto(-5, 48)
    creator.pu()

    creator.goto(456, 48)
    creator.pd()
    creator.goto(456 + 160, 48)
    creator.goto(456 + 160, 48 + 480)
    creator.goto(456, 48 + 480)
    creator.goto(456, 48)
    creator.pu()
    creator.goto(540, 48)
    creator.write("next", move = False, align = "center", font = consolefont)

    creator.pensize(1)
    creator.pencolor('#334433')
    creator.goto(128, 16)

    for i in range(1, 10):
        creator.goto(128 + grid * i, 16)
        creator.pd()
        creator.goto(128 + grid * i, 656)
        creator.pu()

    for i in range(1, 20):
        creator.goto(128, 16 + grid * i)
        creator.pd()
        creator.goto(448, 16 + grid * i)
        creator.pu()

    creator.pensize(4)
    creator.pencolor('white')        
    creator.goto(128, 16)
    creator.pd()
    creator.goto(128, 656)
    creator.goto(448, 656)
    creator.goto(448, 16)
    creator.goto(128, 16)
    creator.pu()

    creator.rt(30)
    creator.color('#FFFFFF', '#FFFFFF')
    creator.goto(40, 250)
    creator.shape('turtle')
    creator.turtlesize(5, 5)
    creator.stamp()
    creator.turtlesize(1, 1)
    creator.goto(57.5, 330)
    creator.write("turtris", move = False, align = "center", font = titlefont)
        
    screen.listen()

def new_block():
    '''
    new_block
        make a new block
    '''
    global tmp, now
    t = r.choice(types) #['L', 'T', 'S', 'Z', 'I', 'O', 'R']
    r.shuffle(types)
    if t == 'L':
        tmp = bk.Block([[4, 0], [5, 0], [6, 0], [4, 1]], 1)
        return (tmp, 'L')
    elif t == 'T':
        tmp = bk.Block([[4, 0], [5, 0], [6, 0], [5, 1]], 1)
        return (tmp, 'T')
    elif t == 'S':
        tmp = bk.Block([[4, 1], [5, 1], [5, 0], [6, 0]], 1)
        return (tmp, 'S')
    elif t == 'Z':
        tmp = bk.Block([[4, 0], [5, 0], [5, 1], [6, 1]], 2)
        return (tmp, 'Z')
    elif t == 'I':
        tmp = bk.Block([[4, 0], [5, 0], [6, 0], [7, 0]], 1)
        return (tmp, 'I')
    elif t == 'O':
        tmp = bk.Block([[6, 0], [5, 0], [5, 1], [6, 1]], 1)
        return (tmp, 'O')
    elif t == 'R':
        tmp = bk.Block([[4, 0], [5, 0], [6, 0], [6, 1]], 1)
        return (tmp, 'R')
    
def update():
    '''
    update
        updating game screen
    '''
    global draw, screen, now, frame_count, next_blocks, trigger, final_chance, holding, hold_cool, lv_factor, consolefont, specialfont

    draw.clear()
    draw.pensize(1)

    if 0 in sum(bk.stack.values(), []):
        screen.clear()
        screen.bye()
        print(f"Point : {bk.point}, Erased : {bk.deleted_lines}")
        
    # falling bk.Block
    #['L', 'T', 'S', 'Z', 'I', 'O', 'R']
    if now == False:
        frame_count = 0
        now = next_blocks.pop(0)
        next_blocks.append(new_block())
    else:
        # Last Chance (Sliding on the ground)
        frame_count += 1
        if frame_count >= frame_hold * (lv_factor ** (bk.level)):
            now[0].fall()
            frame_count = 0
            if final_chance == True:
                final_chance = False
                trigger = True
        if now[0].is_ground():
            if trigger:
                now[0].stack()
                del now
                now = False
                if hold_cool == True:
                    hold_cool = False
            else:
                final_chance = True
        # Drawing the block which is falling
        if trigger:
            trigger = False
        elif now[1] == 'L':
            draw.color('#FFFFFF','#FF9900')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'T':
            draw.color('#FFFFFF','#6600CC')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'S':
            draw.color('#FFFFFF','#33FF00')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'Z':
            draw.color('#FFFFFF','#FF0000')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'I':
            draw.color('#FFFFFF','#33FFFF')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'O':
            draw.color('#FFFFFF','#FFFF33')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()
        elif now[1] == 'R':
            draw.color('#FFFFFF','#0033FF')
            for pos in now[0].pos:
                if pos[1] < 0:
                    continue
                draw.pu()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1] + grid)
                draw.goto(128 + grid * pos[0] + grid, 16 + grid * pos[1])
                draw.goto(128 + grid * pos[0], 16 + grid * pos[1])
                draw.end_fill()

    # Next blocks
    j = 0
    for nextb in next_blocks:
        if nextb[1] == 'L':
            draw.color('#FFFFFF','#FF9900')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'T':
            draw.color('#FFFFFF','#6600CC')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'S':
            draw.color('#FFFFFF','#33FF00')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'Z':
            draw.color('#FFFFFF','#FF0000')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'I':
            draw.color('#FFFFFF','#33FFFF')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'O':
            draw.color('#FFFFFF','#FFFF33')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        elif nextb[1] == 'R':
            draw.color('#FFFFFF','#0033FF')
            for pos in nextb[0].pos:
                draw.pu()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.pd()
                draw.begin_fill()
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1] + 16)
                draw.goto(440 + 16 * pos[0] + 16, 96 * j + 64 + 16 * pos[1])
                draw.goto(440 + 16 * pos[0], 96 * j + 64 + 16 * pos[1])
                draw.end_fill()
        j += 1

    # Holding
    if holding == False:
        pass
    elif holding[1] == 'L':
        draw.color('#FFFFFF','#FF9900')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'T':
        draw.color('#FFFFFF','#6600CC')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'S':
        draw.color('#FFFFFF','#33FF00')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'Z':
        draw.color('#FFFFFF','#FF0000')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'I':
        draw.color('#FFFFFF','#33FFFF')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'O':
        draw.color('#FFFFFF','#FFFF33')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()
    elif holding[1] == 'R':
        draw.color('#FFFFFF','#0033FF')
        for pos in holding[0].pos:
            draw.pu()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.pd()
            draw.begin_fill()
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1] + 12.5)
            draw.goto(-17.5 + 12.5 * pos[0] + 12.5, 96 + 12.5 * pos[1])
            draw.goto(-17.5 + 12.5 * pos[0], 96 + 12.5 * pos[1])
            draw.end_fill()

    # Static blocks        
    draw.color('#FFFFFF', '#FFFFFF')
    for x, ys in bk.stack.items():
        for y in ys:
            draw.pu()
            draw.goto(128 + grid * x, 16 + grid * y)
            draw.pd()
            draw.begin_fill()
            draw.goto(128 + grid * x, 16 + grid * y + grid)
            draw.goto(128 + grid * x + grid, 16 + grid * y + grid)
            draw.goto(128 + grid * x + grid, 16 + grid * y)
            draw.goto(128 + grid * x, 16 + grid * y)
            draw.end_fill()

    # Scoreboard
    draw.pu()
    draw.goto(456, 650)
    draw.write(f"score\n{bk.point}", move = False, align = "left", font = specialfont)

    # TETRIS!
    if bk.special == 'Tetris':
        draw.goto(60, 640)
        draw.color('#FF0000','#FF0000')
        draw.write("Tetris!", move = False, align = "center", font = consolefont)

    bk.special = None
    
    screen.update()
    screen.ontimer(update, 1000//fps)

# Key Press
def press_A():
    global now
    if now != False:
        now[0].move(0)

def press_D():
    global now
    if now != False:
        now[0].move(1)

def press_S():
    global now
    if now != False:
        now[0].fall()
        if not now[0].is_ground():
            bk.point += 1

def press_Q():
    global now, final_chance, frame_count
    if now != False:
        now[0].rotate(1)
    if final_chance:
        frame_count = 0
    
def press_E():
    global now, final_chance, frame_count
    if now != False:
        now[0].rotate(0)
    if final_chance:
        frame_count = 0

def hold():
    '''
    hold
        Calculates for the holding block
    '''
    global now, holding, frame_count, next_blocks, hold_cool
    # Cannot use hold twice for one block
    if hold_cool == False:
        if holding == False: # First hold, holding new block
            if now[1] == 'L':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [4, 1]], 0)
                holding = (tmp, 'L')
            elif now[1] == 'T':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [5, 1]], 1)
                holding = (tmp, 'T')
            elif now[1] == 'S':
                tmp = bk.Block([[4, 1], [5, 1], [5, 0], [6, 0]], 1)
                holding = (tmp, 'S')
            elif now[1] == 'Z':
                tmp = bk.Block([[4, 0], [5, 0], [5, 1], [6, 1]], 2)
                holding = (tmp, 'Z')
            elif now[1] == 'I':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [7, 0]], 1)
                holding = (tmp, 'I')
            elif now[1] == 'O':
                tmp = bk.Block([[6, 0], [5, 0], [5, 1], [6, 1]], 1)
                holding = (tmp, 'O')
            elif now[1] == 'R':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [6, 1]], 2)
                holding = (tmp, 'R')
            frame_count = 0
            now = next_blocks.pop(0)
            next_blocks.append(new_block())
        else:
            temp = holding
            if now[1] == 'L':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [4, 1]], 0)
                holding = (tmp, 'L')
            elif now[1] == 'T':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [5, 1]], 1)
                holding = (tmp, 'T')
            elif now[1] == 'S':
                tmp = bk.Block([[4, 1], [5, 1], [5, 0], [6, 0]], 1)
                holding = (tmp, 'S')
            elif now[1] == 'Z':
                tmp = bk.Block([[4, 0], [5, 0], [5, 1], [6, 1]], 2)
                holding = (tmp, 'Z')
            elif now[1] == 'I':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [7, 0]], 1)
                holding = (tmp, 'I')
            elif now[1] == 'O':
                tmp = bk.Block([[6, 0], [5, 0], [5, 1], [6, 1]], 1)
                holding = (tmp, 'O')
            elif now[1] == 'R':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [6, 1]], 2)
                holding = (tmp, 'R')
            if temp[1] == 'L':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [4, 1]], 0)
                now = (tmp, 'L')
            elif temp[1] == 'T':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [5, 1]], 1)
                now = (tmp, 'T')
            elif temp[1] == 'S':
                tmp = bk.Block([[4, 1], [5, 1], [5, 0], [6, 0]], 1)
                now = (tmp, 'S')
            elif temp[1] == 'Z':
                tmp = bk.Block([[4, 0], [5, 0], [5, 1], [6, 1]], 2)
                now = (tmp, 'Z')
            elif temp[1] == 'I':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [7, 0]], 1)
                now = (tmp, 'I')
            elif temp[1] == 'O':
                tmp = bk.Block([[6, 0], [5, 0], [5, 1], [6, 1]], 1)
                now = (tmp, 'O')
            elif temp[1] == 'R':
                tmp = bk.Block([[4, 0], [5, 0], [6, 0], [6, 1]], 2)
                now = (tmp, 'R')
            frame_count = 0
        hold_cool = True

def sound_play(music):
    '''
    sound_play
        Infinitely play background music.
    '''
    while True:
        playsound(music)
        
if __name__=="__main__":
    init()
    # sound = th.Thread(target=sound_play,args=["BGM.mp3"]) # IF you have a file for bgm
    # sound.start()
    screen.mainloop()
