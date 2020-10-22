import pygame
import time
import random
import sys

#MUSIC##
from pygame.locals import *
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

#play background music
pygame.mixer.music.load("BigUniverse.mp3")
pygame.mixer.music.set_volume(0.2)  
pygame.mixer.music.play(-1) 



black=(0,0,0)
white=(255,165,0)
red=(255,0,0)
blue=(0,0,255)
green=(50,205,50)
gold=(255,215,0)
orange=(255,140,0)
boardw=7
boardh=6
disw=1000
dish=800
fps=30
spacesize=100
bgcolour=white
textcolour=black
Red='red'
Blue='blue'
player1='player1'
player2='player2'
xmargin=int((disw-boardw*spacesize)/2)
ymargin=int((dish-boardh*spacesize)/2)
bg=pygame.image.load('background5.jpg')
bg=pygame.transform.scale(bg,(1000,800))
fpsclock=pygame.time.Clock()
class Board():
    
    def __init__(self):
        self.M=[[]]
        self.turn=None 
        self.g=None
        self.bet=None
        self.long=None
        self.bal1=100
        self.bal2=100

    def acceptdetails(self):
        """NECESSARY DET FOR BOARD"""
        h=input("Should the game build from bottom to top only?(Y/N)")
        t=input("Should the game be alternate turn based(1) or bet-based(2)?")
        l=int(input("Enter the no of coins in a line required to win:"))
        m=6
        n=7
        
        self.M=[[0 for i in range(n)]for j in range(m)]
        if h=="y" or h=="Y":
            self.g=True
        elif h=="n" or h=="N":
            self.g=False
        if t=="1" :
            self.turn=1
        elif t=="2":
            self.bet=True
        
        self.long=l

    def bet_winner(self):
        print ("Player 1 Balance:",self.bal1)
        print ("Player 2 Balance:",self.bal2)

        a=b=101;counta=0;countb=0;count=0

        while a==b:
            while a>self.bal1:
                a=int(input("Player 1,Enter your bet(lesser than your balance):"))
                if counta>=1:
                    print("P1,Your bet must be lesser than your balance.Invalid bet.")
                counta +=1
            while b>self.bal2:
                b=int(input("Player 2,Enter your bet(lesser than your balance):"))
                if countb>=1:
                    print("P2,Your bet must be lesser than your balance.Invalid bet.")
                countb +=1
            if count>=1:
                print ("Your bets are equal.Bet again.")
                
        z=greater(a,b)
        if z==a:
            self.bal1-=a
            self.bal2+=a
            self.turn=1
        else: 
            self.bal1+=b
            self.bal2-=b
            self.turn=2
        
    
        
            
    def make_move(self,pr,pc):
        if valid_move(self.M,self.g,pr,pc)==True:
            self.M[pr][pc]=self.turn
           
        
    def check_for_victory(self,pr,pc):
        """Checks for victory of the player who played last
        -l in a row,where l is entered by user in acceptdetails.Returns tuple of
        flags in order in which checked-(v,h,d)"""
        m=len(self.M)
        n=len(self.M[0])
        l=self.long
        lim=l-1
        limit=lim-1
        hflag=vflag=dflag=False  
        ovrow1=pr-lim
        ovrow2=pr+lim   
        ovcol1=pc-lim
        ovcol2=pc+lim
        vrow2=ovrow2 if ovrow2<m else m-1    
        vcol2=ovcol2 if ovcol2<n else n-1
        vrow1=ovrow1 if ovrow1>=0 else 0    
        vcol1=ovcol1 if ovcol1>=0 else 0

        #Vertical Victory
        L1=[]
        for i in range(vrow2-vrow1 +1):
            L1.append(M[vrow1+i][pc])
            if x_in_row(L1)==True:
                vflag=flag=True
            
        #Horizontal Victory
        L2=[]
        if flag==False:     
            for i in range(vcol2-vcol1+1):
                L2.append(M[pr][vol1+i])
                if x_in_row(L2)==True:
                    hflag=flag=True
                          
        #Diagonal Victory
        if flag==False:
            orow1=vrow1-ovrow1    
            orow2=vrow2-ovrow2
            ocol1=vcol1-ovcol1
            ocol2=vcol2-ovcol2
            drow1=vrow1+ocol1  
            drow2=vrow2+ocol2
            dcol1=vcol1+orow1
            dcol2=vcol2+orow2
            Drow1=vrow1-ocol2
            Drow2=vrow2-ocol1
            Drow3=vcol1-orow2
            Drow4=vcol2-orow1
            D1=D2=[]
            for i in range(l):  
                D1.append(self.M[drow1+i][dcol1+i])  
                D2.append(self.M[Drow1+i][Dcol2-i])  
            if x_in_line(D1)==True or x_in_line(D2)==True:
                dflag=flag=True
        return flag   


def main():
    global clock,redpilerect,bluepilerect,gridimg,bg
    global coinb,coinr,gamedis,countr,countb
    pygame.init()
    
    clock=pygame.time.Clock()
    gamedis=pygame.display.set_mode((disw,dish))
    pygame.display.set_caption('FOUR IN A LINE')
    gridimg=pygame.image.load('grid.png')
    redpilerect=pygame.Rect(int(spacesize/2)-5,dish-int(3*spacesize/2),spacesize,spacesize)
    bluepilerect=pygame.Rect(disw-int(3*spacesize/2),dish-int(3*spacesize/2),spacesize,spacesize)
    bg=pygame.image.load('background5.jpg')
    bg=pygame.transform.scale(bg,(1000,800))
    coinb=pygame.image.load('BLUE COIN2.png')
    coinb = pygame.transform.scale(coinb, (spacesize, spacesize))
    coinr=pygame.image.load('RED COIN.png')
    coinr= pygame.transform.scale(coinr, (spacesize,spacesize))
    gameintro()
    font=pygame.font.SysFont(None,50)
    text=font.render('RED'+':'+str(0),True,black)
    gamedis.blit(text,(0,0))

    font=pygame.font.SysFont(None,50)
    text=font.render('BLUE'+':'+str(0),True,black)
    gamedis.blit(text,(850,0))
    


    

def rungame(isFirstgame,countr,countb):

    Turn=player1  # just for now
    mainboard=newboard()


    while True:
        if Turn==player1:
            player1move(mainboard,countr,countb)
            if check_for_victory(mainboard,Red)==True:
                countr+=1

                print(countr)
                message('RED WINS',countr,countb)
                font=pygame.font.SysFont(None,50)
                text=font.render('RED'+':'+str(countr),True,black)
                gamedis.blit(text,(0,0))

                break
            Turn=player2
        elif Turn==player2:
            player2move(mainboard,countr,countb)
            if check_for_victory(mainboard,Blue)==True:
                
                countb+=1
                print(countb)
                message('BLUE WINS',countr,countb)
                font=pygame.font.SysFont(None,50)
                text=font.render('BLUE'+':'+str(countb),True,black)
                gamedis.blit(text,(850,0))
                #score2(countb,'BLUE')
                break
            Turn=player1
        if isboardfull(mainboard)==True:
            message('TIE')#display message
            break
    while True:
        drawboard(mainboard,countr,countb)
        for event in pygame.event.get():   #event handling loop
            if event.type==pygame.QUIT or(event.type==pygame.KEYUP and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                return
                
            
def newboard():
    b=Board()
    b.M=[['empty' for i in range(boardh)]for j in range(boardw)]
    return b.M
def makemove(board,player,column):
    lowest=Lowestemptyspace(board,column)
    if lowest!=-1:
        board[column][lowest]=player
def drawboard(board,countr,countb,extratoken=None):

    gamedis.fill(white)
    gamedis.blit(bg,(0,0))
    font=pygame.font.SysFont(None,50)
    text=font.render('RED'+':'+str(countr),True,black)
    gamedis.blit(text,(0,0))

    font=pygame.font.SysFont(None,50)
    text=font.render('BLUE'+':'+str(countb),True,black)
    gamedis.blit(text,(850,0))
    

    spaceRect=pygame.Rect(0,0,spacesize,spacesize)
    for i in range(boardw):
        for j in range(boardh):
            spaceRect.topleft = (xmargin + (i * spacesize), ymargin + (j * spacesize))
            if board[i][j] == Red:
              gamedis.blit(coinr, spaceRect)
            elif board[i][j] == Blue:
                gamedis.blit(coinb, spaceRect)
    
    if extratoken != None:
        if extratoken['color'] == Red:
            gamedis.blit(coinr, (extratoken['x'], extratoken['y'], spacesize, spacesize))
        elif extratoken['color'] == Blue:
            gamedis.blit(coinb, (extratoken['x'], extratoken['y'], spacesize, spacesize))
    # draw board over the tokens
    for i in range(boardw):
        for j in range(boardh):
            spaceRect.topleft = (150, 100)
            gamedis.blit(gridimg, spaceRect)
   
    gamedis.blit(coinr, redpilerect) 
    gamedis.blit(coinb, bluepilerect) # blue on the right

def player1move(mainboard,countr,countb):
    draggingToken=False
    tokenx,tokeny=None,None
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and not draggingToken and redpilerect.collidepoint(event.pos):
                draggingToken=True
                tokenx,tokeny=event.pos
            elif event.type==pygame.MOUSEMOTION and draggingToken:
                tokenx,tokeny=event.pos
            elif event.type==pygame.MOUSEBUTTONUP and draggingToken:
                if tokeny < ymargin and tokenx > xmargin and tokenx<disw-xmargin:
                    column=int((tokenx-xmargin)/spacesize)
                    if isValidmove(mainboard,column):
                        animateDroppingToken(mainboard,column,Red)
                        mainboard[column][Lowestemptyspace(mainboard,column)]=Red
                        drawboard(mainboard,countr,countb)
                        pygame.display.update()
                        return
                tokenx,tokeny=None,None
                draggingToken=False
        if tokenx!=None and tokeny!=None:
            drawboard(mainboard,countr,countb, {'x':tokenx - int(spacesize / 2), 'y':tokeny - int(spacesize / 2), 'color':Red})
        else:
            drawboard(mainboard,countr,countb)
        pygame.display.update()
        fpsclock.tick()
def player2move(mainboard,countr,countb):
    draggingToken=False
    tokenx,tokeny=None,None
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and not draggingToken and bluepilerect.collidepoint(event.pos):
                draggingToken=True
                tokenx,tokeny=event.pos
            elif event.type==pygame.MOUSEMOTION and draggingToken:
                tokenx,tokeny=event.pos
            elif event.type==pygame.MOUSEBUTTONUP and draggingToken:
                if tokeny < ymargin and tokenx > xmargin and tokenx<disw-xmargin:
                    column=int((tokenx-xmargin)/spacesize)
                    if isValidmove(mainboard,column):
                        animateDroppingToken(mainboard,column,Blue)
                        mainboard[column][Lowestemptyspace(mainboard,column)]=Blue
                        drawboard(mainboard,countr,countb)
                        pygame.display.update()
                        return
                tokenx,tokeny=None,None
                draggingToken=False
        if tokenx!=None and tokeny!=None:
            drawboard(mainboard,countr,countb,{'x':tokenx - int(spacesize / 2), 'y':tokeny - int(spacesize / 2), 'color':Blue})
        else:
            drawboard(mainboard,countr,countb)
        pygame.display.update()
        fpsclock.tick()
        
def animateDroppingToken(board,column,color):

    x=xmargin+column*spacesize
    y=ymargin-spacesize
    dropSpeed=1.0
    lowestemptyspace=Lowestemptyspace(board,column)
    while True:
        y+=int(dropSpeed)
        dropSpeed+=0.5
        if int((y-ymargin)/spacesize)>=lowestemptyspace:
            return
    drawboard(board,{'x':x, 'y':y, 'color':color})
    pygame.display.update()
    fpsclock.tick()
    #not over
    
def Lowestemptyspace(board,column):
    
    # Return the row number of the lowest empty row in the given column.
    for j in range(boardh-1, -1, -1):
        if board[column][j] == 'empty':
           return j
    return -1
def isValidmove(board,column):
    if column<0 or column>=boardw or board[column][0]!='empty':
        return False
    return True          #this returns false if the condition is true else true
def isboardfull(board):
    for i in range(boardw):
        for j in range(boardh):
            if board[i][j]=='empty':
                return False
    return True
    

def check_for_victory(board, tile):
 # check horizontal spaces
    for x in range(boardw - 3):
        for y in range(boardh):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
# check vertical spaces
    for x in range(boardw):
        for y in range(boardh - 3):
             if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                 return True
# check / diagonal spaces
    for x in range(boardw - 3):
         for y in range(3, boardh):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                 return True
     # check \ diagonal spaces
    for x in range(boardw - 3):
         for y in range(boardh - 3):
             if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                 return True
    return False

def menu():
    print('1 Two Player')
    print('2  One Player')
    g=input('enter your choice      ')
def textobj(text,font):
    textsurf=font.render(text,True,black)
    return textsurf,textsurf.get_rect()
def message(text,countr,countb):#for  winner display
    text1=pygame.font.SysFont('comicsansms',100)
    textsur,textrect=textobj(text,text1)
    textrect.center=(500,400)
    gamedis.blit(textsur,textrect)
    pygame.display.update()
    time.sleep(2)
    isfirstgame=True
    while True:
        rungame(isfirstgame,countr,countb)
        isfirstgame=False
    

def button(text,x,y,w,h,gold,orange,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gamedis,gold,(x,y,w,h))
        if click[0]==1and action!=None:
            if action=='play':
                countr=0
                countb=0
                isfirstgame=True
                while True:
                    rungame(isfirstgame,countr,countb)
                    isfirstgame=False
            elif action=='exit':
                pygame.quit()
                quit()
            
    else:  
        pygame.draw.rect(gamedis,orange,(x,y,w,h))
    text2=pygame.font.SysFont('comicsansms',30)
    textsur,textrect=textobj(text,text2)
    textrect.center=((x+(w/2)),(y+(h/2)))
    gamedis.blit(textsur,textrect)
    
def gameintro():
    
    intro=True
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gamedis.fill(white)
        gamedis.blit(bg,(0,0))
        text1=pygame.font.SysFont('comicsansms',100)
        textsur,textrect=textobj('Four in a Line',text1)
        textrect.center=(500,400)
        gamedis.blit(textsur,textrect)

        button('PLAY',425,500,150,50,gold,orange,'play')
        button('EXIT',425,575,150,50,gold,orange,'exit')



        pygame.display.update()
        clock.tick(15)
        pygame.display.update()

     


    pygame.display.update()
    clock.tick(60)
print("HELLO!WELCOME TO CONNECT4!")
main()
pygame.quit()

quit()
