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
    def __init__(self, positions, color, pivot = 0):
        self.pos = positions #Position
        self.col = color
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
                for piv in self.pivot:
                    piv[0] -= 1
            else:
                for pos in self.pos:
                    pos[0] += 1
                for piv in self.pivot:
                    piv[0] += 1

    def _is_rotatable(self, direction, pivot):
        if direction == 0: #Clockwise
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1]
                arx = pivot[0] - ry #회전 후, 원래 좌표로 돌려 놓음
                ary = pivot[1] + rx
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
        else:
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1]
                arx = pivot[0] + ry #회전 후, 원래 좌표로 돌려 놓음
                ary = pivot[1] - rx
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
        
    def _rotate(self, direction, pivot):
        if direction == 0: #시계
            new = []
            newp = []
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1] 
                arx = pivot[0] - ry #회전 및, 원래 좌표 찾기
                ary = pivot[1] + rx
                new.append([arx, ary]) #좌표 등록
            self.pos = new
            for piv in self.pivot:
                rx = piv[0] - pivot[0]
                ry = piv[1] - pivot[1]
                arx = pivot[0] - ry
                ary = pivot[1] + rx
                newp.append([arx, ary, piv[2]])
            self.pivot = newp
        else:
            new = []
            newp = []
            for pos in self.pos:
                rx = pos[0] - pivot[0]
                ry = pos[1] - pivot[1] 
                arx = pivot[0] + ry
                ary = pivot[1] - rx
                new.append([arx, ary])
            self.pos = new
            for piv in self.pivot:
                rx = piv[0] - pivot[0]
                ry = piv[1] - pivot[1] 
                arx = pivot[0] + ry
                ary = pivot[1] - rx
                newp.append([arx, ary, piv[2]])
            self.pivot = newp

    def _is_rotatable_with_falling(self, direction, pivot):
        if direction == 0: #Clockwise
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1]
                arx = pivot[0] - ry #회전 후, 원래 좌표로 돌려 놓음
                ary = pivot[1] + rx + 1 #회전하면서 동시에 한 칸 떨어짐.
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
        else:
            rotatable = True
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1]
                arx = pivot[0] + ry #회전 후, 원래 좌표로 돌려 놓음
                ary = pivot[1] - rx + 1 #회전하면서 동시에 한 칸 떨어짐.
                if arx < 0 or arx >= width or ary >= height:
                    rotatable = False
                elif ary in stack[arx]:
                    rotatable = False
            return rotatable
    
    def _rotate_with_falling(self, direction, pivot):
        if direction == 0: #시계
            new = []
            newp = []
            for pos in self.pos:
                rx = pos[0] - pivot[0] #상대 좌표
                ry = pos[1] - pivot[1] 
                arx = pivot[0] - ry #회전 및, 원래 좌표 찾기
                ary = pivot[1] + rx + 1 #회전하고 y좌표 1 증가
                new.append([arx, ary]) #좌표 등록
            self.pos = new
            for piv in self.pivot:
                rx = piv[0] - pivot[0]
                ry = piv[1] - pivot[1] 
                arx = pivot[0] - ry
                ary = pivot[1] + rx + 1
                newp.append([arx, ary, piv[2]])
            self.pivot = newp
        else:
            new = []
            newp = []
            for pos in self.pos:
                rx = pos[0] - pivot[0] 
                ry = pos[1] - pivot[1] 
                arx = pivot[0] + ry
                ary = pivot[1] - rx + 1
                new.append([arx, ary])
            self.pos = new
            for piv in self.pivot:
                rx = piv[0] - pivot[0] 
                ry = piv[1] - pivot[1] 
                arx = pivot[0] + ry
                ary = pivot[1] - rx + 1
                newp.append([arx, ary, piv[2]])
            self.ivot = newp
            
    def rotate(self, direction):
        for piv in self.pivot:
            if piv[2] == 1:
                if self._is_rotatable(direction, (piv[0], piv[1])):
                    self._rotate(direction, (piv[0], piv[1]))
                    break
            else:
                if self._is_rotatable_with_falling(direction, (piv[0], piv[1])):
                    self._rotate_with_falling(direction, (piv[0], piv[1]))
                    break

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
            for piv in self.pivot:
                piv[1] += 1

def check_line():
    '''
    check_line
        check if there exist a filled line
    '''
    global stack, width, reward, deleted_lines, level, special
    line = [n for n in range(height) if sum(stack.values(), []).count(n) == width] # Find filled line. The width should be 10
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
