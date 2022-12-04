import chess_lib
import pygame
import sys
size=80
w_size=size*8
def start():
    global func,board,w_timer,b_timer,status_message
    func=chess_lib.ChessEngine()
    board=func.board
    status_message="White to play"
    set_timer()
func=chess_lib.ChessEngine()
board=func.board
status_message="White to play"
pygame.init()
screen=pygame.display.set_mode([w_size,w_size+150])
font1 = pygame.font.SysFont(None, 25)
font2 = pygame.font.SysFont(None, 25)
font3 = pygame.font.SysFont(None, 100)
font4 = pygame.font.SysFont(None, 75)
font5= pygame.font.SysFont(None, 35)
w_timer,b_timer=0,0
dt=0
clock = pygame.time.Clock()
def set_timer():
    global w_timer,b_timer,dt
    screen.fill((0,0,0))
    timer=""
    dt=0
    timer_set=False
    while timer_set==False:
        text = font5.render("How many minutes of time do you want?", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (50, (w_size // 2) - 50 + 75, w_size - 100, 100))
        #pygame.draw.rect(screen, (0, 0, 0), ((w_size // 2) - 50, (w_size // 2) + 60 + 75, 100, 50))
        screen.blit(text, (90, (w_size//2)-50+75+25))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys=[pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_PERIOD,pygame.K_RETURN]
                if event.key in keys:
                    if event.key!=pygame.K_RETURN:
                        timer += event.unicode
                        text2=font1.render(timer, True, (255, 255, 255))
                        screen.blit(text2, ((w_size // 2) - 50 + 20, (w_size // 2) + 60 + 75 + 20))
                    else:
                        timer=float(timer)
                        timer_set=True
        pygame.display.flip()
    w_timer,b_timer=timer*60,timer*60
    pygame.display.flip()
    clock.tick()
set_timer()
images=[]
def load_images():
    global images
    images=[x for x in range(33)]
    images[chess_lib.WQ]=pygame.image.load("chess_pieces\white_queen.png")
    images[chess_lib.WK]=pygame.image.load("chess_pieces\white_king.png")
    images[chess_lib.WN1]=images[chess_lib.WN2]=pygame.image.load("chess_pieces\white_knight.png")
    images[chess_lib.WB1] = images[chess_lib.WB2] = pygame.image.load("chess_pieces\white_bishop.png")
    images[chess_lib.WR1] = images[chess_lib.WR2] = pygame.image.load("chess_pieces\white_rook.png")
    for x in range(chess_lib.WP1,chess_lib.WP8+1):
        images[x]=pygame.image.load("chess_pieces\white_pawn.png")
    images[chess_lib.BQ] = pygame.image.load("chess_pieces\\black_queen.png")
    images[chess_lib.BK] = pygame.image.load("chess_pieces\\black_king.png")
    images[chess_lib.BN1] = images[chess_lib.BN2] = pygame.image.load("chess_pieces\\black_knight.png")
    images[chess_lib.BB1] = images[chess_lib.BB2] = pygame.image.load("chess_pieces\\black_bishop.png")
    images[chess_lib.BR1] = images[chess_lib.BR2] = pygame.image.load("chess_pieces\\black_rook.png")
    for x in range(chess_lib.BP1, chess_lib.BP8 + 1):
        images[x] = pygame.image.load("chess_pieces\\black_pawn.png")

load_images()
def display_board(board,highlight,is_check):
    global cells
    y=75
    king_pos=[]
    if highlight:
        legal_moves=func.check_legal_moves(cells[0],func.get_colour())
    for row in range(8):
        x=0
        for col in range(8):
            if (row*7+col)%2==0:
                pygame.draw.rect(screen,(255, 233, 197),(x,y,size,size))
            else:
                pygame.draw.rect(screen, (164,116,73), (x, y, size, size))
            if highlight and (row,col)==cells[0]:
                if (row*7+col)%2==0:
                    pygame.draw.rect(screen,(102,215,102), (x, y, size, size))
                else:
                    pygame.draw.rect(screen, (102, 195, 102), (x, y, size, size))
            if board[row][col]!=0:
                screen.blit(images[board[row][col]], (x + 5, y + 5))
                if board[row][col] in func.kings and is_check:
                    if func.get_colour() == "w" and board[row][col] in func.white_pieces:
                        pygame.draw.circle(screen, (255, 0, 0), (x + size / 2, y + size / 2), size / 5)
                    elif func.get_colour() == "b" and board[row][col] in func.black_pieces:
                        pygame.draw.circle(screen, (255, 0, 0), (x + size / 2, y + size / 2), size / 5)
            if highlight and (row,col) in legal_moves:
                pygame.draw.circle(screen,(102, 235, 102),(x+size/2,y+size/2),size/5)

            x=x+size
        y=y+size
    x=4*size
    y=0

    pygame.display.flip()

pygame.draw.rect(screen,(0,0,0),(0,w_size+75,w_size,75))
pygame.draw.rect(screen, (0, 0, 0), (0, 0, w_size, 75))

def message():
    global status_message,w_timer,b_timer
    pygame.draw.rect(screen, (0, 0, 0), (0, w_size + 75, w_size, 75))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, w_size, 75))
    if func.status["checkmate"]:
        text2 = font3.render("Checkmate!", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (50, (w_size//2)-50+75, w_size-100, 100))
        screen.blit(text2, (115, (w_size//2)-50+75+25))
    if func.status["stalemate"]:
        text2 = font3.render("Stalemate!", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (50, (w_size//2)-50+75, w_size-100, 100))
        screen.blit(text2, (115, (w_size//2)-50+75+25))
    if status_message=="White to play":
        text2 = font2.render(status_message, True, (255,255,255))
        screen.blit(text2, (5, 55))
    elif status_message=="Black to play":
        text2 = font2.render(status_message, True, (255, 255, 255))
        screen.blit(text2, (5, w_size+80))
    min1 = w_timer // 60
    sec1 = w_timer % 60
    ms1 = w_timer - int(w_timer)
    text11 = font2.render(str(int(min1)) + ":" + str(int(sec1) + round(ms1, 1)), True, (255, 255, 255))
    screen.blit(text11, (w_size - 75, 55))
    min = b_timer // 60
    sec = b_timer % 60
    ms = b_timer - int(b_timer)
    text12 = font2.render(str(int(min)) + ":" + str(int(sec) + round(ms, 1)), True, (255, 255, 255))
    screen.blit(text12, (w_size - 75, w_size + 80))
    if w_timer<=0:
        text2 = font4.render("White timeout!", True, (255, 255, 255))
        func.status["game_end"]=True
        pygame.draw.rect(screen, (0, 0, 0), (50, (w_size // 2) - 50 + 75, w_size - 100, 100))
        screen.blit(text2, (115, (w_size // 2) - 50 + 75 + 25))
    elif b_timer<=0:
        text2 = font4.render("Black timeout!", True, (255, 255, 255))
        func.status["game_end"] = True
        pygame.draw.rect(screen, (0, 0, 0), (50, (w_size // 2) - 50 + 75, w_size - 100, 100))
        screen.blit(text2, (115, (w_size // 2) - 50 + 75 + 25))
    pygame.display.flip()


def get_cellClicked(xpos, ypos):
    ypos-=75
    row = ypos // size
    col = xpos // size
    return (row, col)

display_board(board,False,False)
cells = []
clock=pygame.time.Clock()
while True:
    if func.status["game_end"]:
        text = font1.render("Restart", True, (255, 255, 255))
        #pygame.draw.rect(screen, (0, 0, 0), (50, (w_size // 2) - 50 + 75, w_size - 100, 100))
        pygame.draw.rect(screen, (0, 0, 0), ((w_size // 2) - 50, (w_size // 2) + 60 + 75, 100, 50))
        screen.blit(text, ((w_size // 2) - 50+20, (w_size // 2) + 60 + 75+20))
        message()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                recx=(w_size // 2) - 50
                recy=(w_size // 2) + 60 + 75
                if (event.pos[0]>=recx and event.pos[0]<= recx+100) and (event.pos[1]>=recy and event.pos[1]<= recy+50):
                    start()
                    display_board(board,False,False)
        continue
    turn = func.get_colour()
    dt=clock.tick()/1000
    if dt >= 1:
        print("This system seems to be slow")
    if turn=="w":
        w_timer-=dt
        status_message="White to play"
    else:
        b_timer-=dt
        status_message = "Black to play"
    message()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_cellClicked(event.pos[0], event.pos[1])
            if len(cells)==0:
                if func.get_piece_colour(cell)==func.get_colour():
                    cells.append(cell)
                    print(cells)
                    if func.status["is_check"]:
                        display_board(board,True, True)
                    else:
                        display_board(board, True,False)

            elif len(cells)==1:
                cells.append(cell)
                print(cells)
                func.move(cells[0], cells[1])
                display_board(board, False,False)
                if turn=="w" and func.status["checkmate"]==False:
                    status_message="White to play"
                elif turn=="b" and func.status["checkmate"]==False:
                    status_message = "Black to play"
                cells.clear()
                print(func.status["is_check"])
                print(f"Game end {func.status['game_end']}")
                if func.status["is_check"]:
                    display_board(board, False, True)
                print(f'{func.status["checkmate"]} checkmate')
                """if func.status["checkmate"]:
                    message("Checkmate")
                elif func.status["stalemate"]:
                    message("Stalemate")"""