#Blocks

#Constants
height = 20
width = 10

reward = [40, 100, 300, 1200]
deleted_lines = 0

#Stack Of Blocks (To find which line had been filled)
stack = dict(map(lambda x : (x, []), [t for t in range(width)]))

#Initializing
point = 0
level = 0

special = None

class Block:
    '''Blocks'''
    def __init__(self, positions, pivot = 0):
        self.pos = positions #Position
        self.pivot = pivot #Pivot for rotating

    def is_ground(self):
        '''
        is_ground
            check if block is on ground
        '''
        check = False
        for pos in self.pos:
            if pos[1] + 1 in stack[pos[0]]:
                check = True
            elif pos[1] + 1 == height:
                check = True
        return check

    def is_movable(self, direction):
        '''
        is_movable
            check if block is movable (to left or right)
        params:
            direction : 0 for left, 1 for right
        '''
        if direction == 0: #Left side
            movable = True
            for pos in self.pos:
                if pos[0] == 0:
                    movable = False
                elif pos[1] in stack[pos[0] - 1]:
                    movable = False
            return movable
        elif direction == 1: #Right side
            movable = True
            for pos in self.pos:
                if pos[0] == width - 1:
                    movable = False
                elif pos[1] in stack[pos[0] + 1]:
                    movable = False
            return movable

    def move(self, direction):
        '''
        move
            move the block (to left or right)

        params:
            direction : 0 for left, 1 for right
        '''
        if self.is_movable(direction):
            if direction == 0: #Left side
                for pos in self.pos:
                    pos[0] -= 1
            else:
                for pos in self.pos:
                    pos[0] += 1

    def is_rotatable(self, direction):
        '''
        is_rotatable
            check if the block is rotatable
        params:
            direction : 0 for clockwise, 1 for counterclockwise
        '''
        if direction == 0: #Clockwise
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - self.pos[self.pivot][0] #Relative x according to pivot point
                ry = pos[1] - self.pos[self.pivot][1] #Relative y according to pivot point
                arx = self.pos[self.pivot][0] - ry
                ary = self.pos[self.pivot][1] + rx
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
        else:
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - self.pos[self.pivot][0] #Relative x according to pivot point
                ry = pos[1] - self.pos[self.pivot][1] #Relative y according to pivot point
                arx = self.pos[self.pivot][0] + ry
                ary = self.pos[self.pivot][1] - rx
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
        
    def rotate(self, direction):
        '''
        rotate
            rotate the block according to the given direction
        params:
            direction : 0 for clockwise, 1 for counterclockwise
        '''
        if self.is_rotatable(direction):
            if direction == 0: #Clockwise:
                new = []
                for pos in self.pos:
                    rx = pos[0] - self.pos[self.pivot][0] #Relative x according to pivot point
                    ry = pos[1] - self.pos[self.pivot][1] #Relative y according to pivot point
                    arx = self.pos[self.pivot][0] - ry
                    ary = self.pos[self.pivot][1] + rx
                    new.append([arx, ary])
                self.pos = new
            else:
                new = []
                for pos in self.pos:
                    rx = pos[0] - self.pos[self.pivot][0] #Relative x according to pivot point
                    ry = pos[1] - self.pos[self.pivot][1] #Relative y according to pivot point
                    arx = self.pos[self.pivot][0] + ry
                    ary = self.pos[self.pivot][1] - rx
                    new.append([arx, ary])
                self.pos = new

    def stack(self):
        '''
        stack
            stack the block and make the block static
        '''
        global point, deleted_lines, level
        for pos in self.pos:
            stack[pos[0]].append(pos[1])
        point += check_line()
        level = deleted_lines // 10

    def fall(self):
        '''
        fall
            make block fall for 1 block if it is not on the ground
        '''
        if not self.is_ground():
            for pos in self.pos:
                pos[1] += 1

def check_line():
    '''
    check_line
        check if there exist a filled line
    '''
    global stack, width, reward, deleted_lines, level, special
    line = [n for n in range(height) if sum(stack.values(), []).count(n) == 10] # Find filled line. The width should be 10
    if len(line) == 0: # If there is no line filled
        point = 0
    else:
        if len(line) == 4: # If 4 lines were filled with one block
            special = "Tetris"
        deleted_lines += len(line) # For calculating level
        point = reward[len(line) - 1]*(level + 1)
        stack = dict(map(lambda x : (x, [y if y > max(line) else y + sum(l > y for l in line) for y in stack[x] if y not in line]), [t for t in range(width)]))
        # Make a new stack for the board
    return point
