#Importing required libraries
import pygame
from queue import PriorityQueue

#Not hardcoding these variables to add some flexibilty to the program
YLENGTH=700
XLENGTH=700
ROWS=50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
YELLOW = (255, 255, 0)
DARKBLUE=(44, 62, 80)
DARKGREEN=(39, 174, 96)
LIGHTBLUE=(0,255,255)

#Setting up the screen along with its length and breadth
SCREEN=pygame.display.set_mode((YLENGTH,XLENGTH))
pygame.display.set_caption("Shortest path Finder")

#Each box in our grid is a node and operations on each of these can be performed using this class
class Node:
    def __init__(self,rowno,colno,boxwidth,totalrows,totalcols):
        self.rowno=rowno
        self.colno=colno
        self.boxwidth=boxwidth
        self.totalrows=totalrows
        self.totalcols = totalcols
        self.x=rowno*boxwidth
        self.y=colno*boxwidth
        self.color=DARKBLUE
        self.nbhs=[]
    def get_pos(self):
        return self.rowno,self.colno

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.boxwidth, self.boxwidth))

    def check_reset(self):
        return self.color==DARKBLUE

    def is_closed(self):
        return self.color == LIGHTBLUE

    def is_open(self):
        return self.color == DARKGREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == WHITE

    def is_end(self):
        return self.color == ORANGE

    def reset(self):
        self.color = DARKBLUE

    def make_start(self):
        self.color = WHITE

    def make_closed(self):
        self.color = LIGHTBLUE

    def make_open(self):
        self.color = DARKGREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = YELLOW

    def neighbours(self,grid):
        self.nbhs=[]
        if self.rowno<self.totalrows - 1:
            if not grid[self.rowno + 1][self.colno].is_barrier():
                self.nbhs.append(grid[self.rowno + 1][self.colno])
        if self.rowno>0:
            if not grid[self.rowno - 1][self.colno].is_barrier():
                self.nbhs.append(grid[self.rowno - 1][self.colno])
        if self.colno<self.totalcols - 1:
            if not grid[self.rowno][self.colno + 1].is_barrier():
                self.nbhs.append(grid[self.rowno][self.colno + 1])
        if self.colno>0:
            if not grid[self.rowno][self.colno - 1].is_barrier():
                self.nbhs.append(grid[self.rowno][self.colno - 1])


    def __lt__(self, other):
        return False

#Function for making the grid and it uses the class defined earlier to set all the nodes
def create_grid(rows,ylength,xlength):
    grid=[]
    YXwidth=ylength//rows
    cols=xlength//YXwidth
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            node=Node(r,c,YXwidth,rows,cols)
            grid[r].append(node)
    return grid

#Function for drawing the grid lines onto the screen
def draw_lines(screen,rows,ylength,xlength):
    YXwidth = ylength // rows
    cols = xlength // YXwidth
    for r in range(rows):
        pygame.draw.line(screen, BLACK, (0, r*YXwidth), (ylength, r*YXwidth))
    for c in range(cols):
        pygame.draw.line(screen, BLACK, (c*YXwidth, 0), (c*YXwidth, xlength))

"""This function is called after each iteration and every step in the algorithm 
to update any changes occuring in the program that is colors of each node"""
def draw_main(screen,grid,rows,ylength,xlength):
    screen.fill(WHITE)
    for r in grid:
        for n in r:
            n.draw(screen)
    draw_lines(screen,rows,ylength,xlength)
    pygame.display.update()


#Function for getting row and col no. of the mouse click point
def mouse_click_pos(pos,rows,ylength,xlength):
    YXwidth = ylength // rows
    cols = xlength // YXwidth
    y,x=pos
    rownum=y//YXwidth
    colnum = x // YXwidth
    return rownum,colnum


#Fscore=Gscore + Hscore
#Heuristic function H for finding F score
def H(xy1,xy2): #Uses manhattan distance
    x1,y1=xy1
    x2,y2=xy2
    return(abs(x1-x2)+abs(y1-y2))

#Astar algorithm
def Astar(grid,startnode,endnode):
    open=PriorityQueue()
    openiteratable={startnode}
    count=0
    prevnode={}
    open.put((0,count,startnode))
    gscore={n:float("inf") for r in grid for n in r}
    gscore[startnode]=0
    fscore={n:float("inf") for r in grid for n in r}
    fscore[startnode]= H(startnode.get_pos(),endnode.get_pos())

    while(not open.empty()):
        current=open.get()[2]
        if current!=startnode:
            current.make_closed()
        openiteratable.remove(current)

        if current==endnode:
            while(True):
                if prevnode[current]!=startnode:
                    prevnode[current].make_path()
                    current=prevnode[current]
                else:
                    break
            draw_main(SCREEN, grid, ROWS, YLENGTH, XLENGTH)
            endnode.make_end()
            return(True)



        for nbh in current.nbhs:
            gscoredash=gscore[current]+1
            if gscoredash<gscore[nbh]:
                prevnode[nbh]=current
                gscore[nbh]=gscoredash
                fscore[nbh]=gscoredash+H(nbh.get_pos(),endnode.get_pos())
                if nbh not in openiteratable:
                    count+=1
                    open.put((fscore[nbh],count,nbh))
                    openiteratable.add(nbh)
                    nbh.make_open()

        draw_main(SCREEN,grid,ROWS,YLENGTH,XLENGTH)


#This is the main function which uses all the previously defined functions to execute the program
def main(screen,ylength,xlength):
    grid=create_grid(ROWS,YLENGTH,XLENGTH)

    startnode=None
    endnode=None
    run=True
    started=False #Used to prevent interference by user once algo has started
    reset=True
    flag=0


    #This while loop runs infinitely until the close button of the window is clicked
    while(run):
        draw_main(SCREEN,grid,ROWS,YLENGTH,XLENGTH)
        #Checking if close button is clicked
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if started:
                continue
            #Checking for left click and performing required operations
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                rownum,colnum=mouse_click_pos(pos,ROWS,YLENGTH,XLENGTH)
                node=grid[rownum][colnum]
                if not startnode and node!=endnode:
                    startnode=node
                    startnode.make_start()
                elif not endnode and node!=startnode:
                    endnode=node
                    endnode.make_end()
                elif node!= startnode and node!= endnode:
                    node.make_barrier()

            # Checking for right click and performing required operations
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                rownum, colnum = mouse_click_pos(pos, ROWS, YLENGTH, XLENGTH)
                node = grid[rownum][colnum]
                node.reset()
                if node==startnode:
                    startnode=None
                elif node==endnode:
                    endnode=None

            # Checking if any key on keyboard is pressed
            if event.type == pygame.KEYDOWN:
                # Checking for pressing of enter button and performing required operations(For starting the algorithm)
                if event.key == pygame.K_RETURN and startnode and endnode and reset:
                    for r in grid:
                        for n in r:
                            n.neighbours(grid)
                    Astar(grid,startnode,endnode)

                # Checking for pressing of space button and performing required operations(For resetting screen)
                if event.key == pygame.K_SPACE and startnode and endnode:
                    for r in grid:
                        for n in r:
                            if not n.check_reset():
                                n.reset()
                                startnode=None
                                endnode=None

            for r in grid:
                for n in r:
                    if n.is_open():
                        reset = False
                        flag = 1
                        break
                    reset = True
                    flag=0
                if flag == 1:
                    break





    pygame.quit()

main(SCREEN,YLENGTH,XLENGTH)