# Developed by George F. Alkhoury, Computer Science Engineering, University of Miskolc, 2020
# Graphics Programming Course
# For Educational Purposes
# Importing the required libraries
import pygame
import sys
import random
import pandas
# --------------------------------------------------------------------------------------------
# Initiating the Pygame and defining multiple required variables
pygame.init()
pygame.display.set_caption("Need For Speed -- Pre-History Edition")
pygame.mixer.music.load("1.mp3")
pygame.mixer.music.play(0)
Width = 500
Height = 700
Black = (0,0,0)
Blue = (0, 0, 250)
Red = (250, 0, 0)
Yellow = (255, 255, 0)
Grass = (0, 247, 111)
White = (255, 255, 255)
Brown = (212, 82, 13)
Back_Ground = (71, 79, 73)
Player_Size_W = 40
Player_Size_L = 60
Block_Size = 50
Block_Pos = [random.randint(60,Width-60-Block_Size),0]
Block_list = [Block_Pos]
Coin_Size = 15
Coin_Pos = [random.randint(60,Width-60-Coin_Size),0]
Coin_list = [Coin_Pos]

Window = pygame.display.set_mode((Width,Height))
game_over = False

Clock = pygame.time.Clock()
My_Font = pygame.font.SysFont("arial", 35, bold=True)
My_Font1 = pygame.font.SysFont("arial", 40, bold=True)
My_Font2 = pygame.font.SysFont("arial", 30, bold=True)
My_Font3 = pygame.font.SysFont("arial", 30, bold=True)
My_Font4 = pygame.font.SysFont("arial", 20, bold=True)
base_font = pygame.font.Font(None,32)
# --------------------------------------------------------------------------------------------
# Defining the functions of the game
# Level increasing function
def set_level(score,Speed):
    Speed = score/5 + 5
    return Speed

# Blocks Generation Function
def drop_Blocks(Block_list):
    delay = random.random()
    if len(Block_list) < 5 and delay < 0.1:
        X_Pos = random.randint(60,Width-60-Block_Size)
        Y_Pos = 0
        Block_list.append([X_Pos,Y_Pos])

# Coin Generation Function
def drop_Coin(Coin_list):
    delay = random.random()
    if len(Coin_list) < 1 and delay < 0.1:
        X_Pos = random.randint(60,Width-60-Coin_Size)
        Y_Pos = 0
        Coin_list.append([X_Pos,Y_Pos])

# Blocks Drawing Function
def draw_Blocks(Block_list):
    for Block_Pos in Block_list:
        pygame.draw.rect(Window, Brown, (Block_Pos[0], Block_Pos[1], Block_Size, Block_Size))

# Coins Drawing Function
def draw_Coin(Coin_list):
    for Coin_Pos in Coin_list:
        pygame.draw.circle(Window, Yellow, (Coin_Pos[0], Coin_Pos[1]), Coin_Size)

# Block Moving Function
def update_Block_pos(Block_list,score, Speed):
    for idx, Block_Pos in enumerate(Block_list):
      if Block_Pos[1] >= 0 and Block_Pos[1] < Height:
         Block_Pos[1] += Speed
      else:
          Block_list.pop(idx)
          score += 1
    return score

# Collision Check Function
def collsion_check(Block_list, Player_Pos):
    for Block_Pos in Block_list:
        if detect_collision(Block_Pos,Player_Pos):
            return True
    return False

# Coin Collision Check Function
def coin_collsion_check(Coin_list, Player_Pos):
    for Coin_Pos in Coin_list:
        if coin_detect_collision(Coin_Pos,Player_Pos):

            return True
    return False
# Coin Collision detect Function
def coin_detect_collision(Player_Pos, Coin_Pos):
    P_X = Player_Pos[0]
    P_Y = Player_Pos[1]
    C_X = Coin_Pos[0]
    C_Y = Coin_Pos[1]
    if (C_X >= P_X and C_X < (P_X + Player_Size_W)) or (P_X >= C_X and P_X < (C_X + Coin_Size)):
        if (C_Y >= P_Y and C_Y < (P_Y + Player_Size_L)) or (P_Y >= C_Y and P_Y < (C_Y + Coin_Size)):
             return True
    return False

# Coin Moving Function
def update_Coin_pos(Coin_list):
    for idx, Coin_Pos in enumerate(Coin_list):
      if Coin_Pos[1] >= 0 and Coin_Pos[1] < Height:
         Coin_Pos[1] += 10
      else:
          Coin_list.pop(idx)

# Collision Detection Function
def detect_collision(Player_Pos, Block_Pos):
    P_X = Player_Pos[0]
    P_Y = Player_Pos[1]
    E_X = Block_Pos[0]
    E_Y = Block_Pos[1]
    if (E_X >= P_X and E_X <= (P_X + Player_Size_W))or(P_X >= E_X and P_X <= (E_X + Block_Size)):
        if (E_Y >= P_Y and E_Y <= (P_Y + Player_Size_L)) or (P_Y >= E_Y and P_Y <= (E_Y + Block_Size)):
             return True
    return False

# Records of Players Saving Function
def save_record(data):
    df1 = pandas.read_csv("Scores.csv")
    df2 = pandas.DataFrame(data)
    df1 = df1.append(df2,ignore_index=True)
    df1 = df1.sort_values(by=['Score'],ascending=False)
    df1.to_csv("Scores.csv",index=False)

# High Scores Option Handling Function
def High_Scores():
    while True:
        click = False
        Window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(110, 600, 250, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                Main_Menu()
        pygame.draw.rect(Window, Red, button_1)
        text = "Back"
        label = My_Font.render(text, 0, White)
        Window.blit(label, (200, 600))
        text = "High Scores"
        label = My_Font1.render(text, 0, Red)
        Window.blit(label, (150, 0))
        PW = 100
        PH = 100
        df = pandas.read_csv("Scores.csv")
        df1 = df.head(10)
        df_list = df1.values.tolist()
        for i in df_list:
           text_surface = base_font.render(str(i), True, White)
           Window.blit(text_surface, (PW, PH))
           PH += 30

        pygame.display.update()
        Clock.tick(30)

# Game Over Handling Function
def Game_Over(score,coin):
    user_text = ''
    while True:
        click = False
        Window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode
        Record = score + coin*10
        text = "Your Score : " + str(Record)
        label = My_Font.render(text, 1, White)
        Window.blit(label, (150, 250))

        text = "Type your name and click Save"
        label = My_Font2.render(text, 0, White)
        Window.blit(label, (60, 350))
        Input_Rect = pygame.Rect(80, 390, 300, 50)
        pygame.draw.rect(Window, White, Input_Rect)
        text_surface = base_font.render(user_text,True,Black)
        Window.blit(text_surface,(100,400))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(110, 600, 250, 50)
        button_2 = pygame.Rect(180, 500, 100, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                Main_Menu()
        if button_2.collidepoint((mx, my)):
            if click:
                data = {'Player': [user_text], 'Score': [Record]}
                save_record(data)

        pygame.draw.rect(Window, Red, button_1)
        pygame.draw.rect(Window, Red, button_2)
        text = "Main Menu"
        label = My_Font.render(text, 0, White)
        Window.blit(label, (150, 600))
        text2 = "Save"
        label2 = My_Font.render(text2, 0, White)
        Window.blit(label2, (200, 500))
        image = pygame.image.load("Game-over.png").convert()
        Window.blit(image, (Width/8, Height/8))

        pygame.display.update()
        Clock.tick(30)

# Game Handling Function
def game():
    game_over = False
    Player_Pos = [Width / 2, Height - 2 * Player_Size_L]
    Speed = 30
    score = 0
    coin = 0
    Coin_Sound = pygame.mixer.Sound("coin.wav")
    pygame.mixer.music.load("2.mp3")
    pygame.mixer.music.play(-1)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                x = Player_Pos[0]
                y = Player_Pos[1]
                if event.key == pygame.K_LEFT:
                    x -= Player_Size_W
                elif event.key == pygame.K_RIGHT:
                    x += Player_Size_W
                Player_Pos = [x, y]
        Window.fill(Back_Ground)
        drop_Coin(Coin_list)
        drop_Blocks(Block_list)
        score = update_Block_pos(Block_list, score, Speed)
        update_Coin_pos(Coin_list)
        Speed = set_level(score, Speed)

        text = "Score" + str(score)
        label = My_Font.render(text, 1, White)
        Window.blit(label, (Width - 200, Height - 40))
        if collsion_check(Block_list, Player_Pos):
            pygame.mixer.music.stop()
            pygame.mixer.music.load("3.mp3")
            pygame.mixer.music.play(0)
            pygame.time.delay(100)
            Game_Over(score, coin)
            game_over = True
            Main_Menu()
        if coin_collsion_check(Coin_list, Player_Pos):
           Coin_list.pop(0)
           pygame.mixer.Sound.play(Coin_Sound)
           coin += 1

        text_coin = "Coins" + str(coin)
        label_coin = My_Font.render(text_coin, 1, White)
        Window.blit(label_coin, (Width - 400, Height - 40))

        pygame.draw.line(Window, White, (Width / 2, 0), (Width / 2, Height), 10)
        draw_Blocks(Block_list)
        draw_Coin(Coin_list)
        pygame.draw.line(Window, Yellow, (50, 0), (50, Height), 10)
        pygame.draw.line(Window, Yellow, (Width - 50, 0), (Width - 50, Height), 10)
        pygame.draw.line(Window, Grass, (0, 0), (0, Height), 50)
        pygame.draw.line(Window, Grass, (Width, 0), (Width, Height), 50)
        pygame.draw.rect(Window, Blue, (Player_Pos[0], Player_Pos[1], Player_Size_W, Player_Size_L))
        image = pygame.image.load("Car.png").convert()
        Window.blit(image, (Player_Pos[0], Player_Pos[1]))

        Clock.tick(30)
        pygame.display.update()

# Game Main Menu Handling Function
def Main_Menu():
    while True:
        click = False
        Window.fill((0, 0, 0))
        Block_list.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        text = "Simple Car Racing Game"
        label = My_Font1.render(text, 0, Red)
        Window.blit(label, (60, 0))
        text = "-- Version 0.0 --"
        label = My_Font2.render(text, 0, Red)
        Window.blit(label, (150, 40))
        text = "Buckle Up and Get Ready"
        label = My_Font3.render(text, 0, Red)
        Window.blit(label, (90, 130))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(110, 200, 250, 50)
        button_2 = pygame.Rect(110, 300, 250, 50)
        button_3 = pygame.Rect(110, 400, 250, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
             if click:
                 High_Scores()
        if button_3.collidepoint((mx, my)):
             if click:
                 sys.exit()
        pygame.draw.rect(Window, (255, 0, 0), button_1)
        pygame.draw.rect(Window, (255, 0, 0), button_2)
        pygame.draw.rect(Window, (255, 0, 0), button_3)
        text2 = "Start"
        label2 = My_Font.render(text2, 0, White)
        Window.blit(label2, (200, 200))
        text3 = "High Scores"
        label3 = My_Font.render(text3, 0, White)
        Window.blit(label3, (150, 300))
        text5 = "Quit"
        label5 = My_Font.render(text5, 0, White)
        Window.blit(label5, (200, 400))
        text4 = "Developed by George F. Alkhoury  2020"
        label4 = My_Font4.render(text4, 1, White)
        Window.blit(label4, (10, 660))
        pygame.display.update()
        Clock.tick(30)
# --------------------------------------------------------------------------------------------
# Game instantiation by calling Game Main Menu handling function
Main_Menu()
