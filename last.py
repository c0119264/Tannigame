#%%
import pygame
import sys

pygame.init() 

WINDOW_W=1200
WINDOW_H=600

FPS=20

BLACK = (0,0,0)
GREEN = (0,255,0)

ADD_NEW_FRAME_RATE=25
toge_img=pygame.image.load('toge.png')
toge_img_rect=toge_img.get_rect()
toge_img_rect.left=0

firewall_img=pygame.image.load('firewall.png')
firewall_img_rect=firewall_img.get_rect()
firewall_img_rect.left=0

CLOCK=pygame.time.Clock()
font=pygame.font.SysFont('forte',20)

canvas = pygame.display.set_mode((WINDOW_W,WINDOW_H))
pygame.display.set_caption("Tanni game")

class Topscore:
    def __init__(self):
        self.high_score=0
    def top_score(self,score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score
    
topscore = Topscore()

class Teki1:
    teki1_velocity = 10

    def __init__(self):
        self.teki1_img = pygame.image.load('teki1.png')
        self.teki1_img.rect = self.teki1_img.get_rect()
        self.teki1_img_rect.width -= 10
        self.teki1_img_rect.height -= 10
        self.teki1_img_rect.top = WINDOW_H/2
        self.teki1_img_rect.right =WINDOW_W
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.teki1_img,self.teki1_img_rect)
        if self.teki1_img_rect.top <= toge_img_rect.bottom:
            self.up=False
            self.down=True
        elif self.teki1_img_rect.bottom >= firewall_img_rect.top:
            self.up =True
            self.down = False

        if self.up:
            self.teki1_img_rect.top -= self.teki1_velocity
        elif self.down:
            self.teki1_img_rect.top += self.teki1_velocity

class Flames:
    flames_velocity=20

    def __init__(self):
        self.flames=pygame.image.load('tanni.png')
        self.flames_img = pygame.transform.scale(self.flames ,(20,20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = teki1.teki1_img_rect.pygame.sprite.get_layer_of_sprite()
        self.flames_img_rect.top=teki1.teki1_img_rect.top + 30

    def update(self):
        canvas.blit(self.flames_img,self.flames_img_rect)

        if self.flames_img_rect.left >0 :
            self.flames_img_rect.left -= self.flames_velocity

class Boku:
    velocity =10 

    def __init__(self):
        self.boku_img= pygame.image.load('boku.png')
        self.boku_img_rect=self.boku_img.get_rect()
        self.boku_img_rect.left=20
        self.boku_img_rect.top =WINDOW_H/2 -100
        self.down =True
        self.up =False

    def update(self):
        canvas.blit(self.boku_img_rect,self.boku_img_rect)
        if self.boku_img_rect.top <= toge_img_rect.bottom:
            gameover()

            if SCORE > self.boku_score:
                self.boku_score=SCORE  

        if self.boku_img_rect.bottom >= firewall_img_rect.top:
            gameover()
            if SCORE > self.boku_score:
                self.boku_score=SCORE

        if self.up:
            self.boku_img_rect.top -= 10

        if self.down:
            self.boku_img_rect.bottom +=10

def gameover():
    topscore.top_score(SCORE)
    game_over_img =pygame.image.load('game-over.png')
    game_over_img_rect=game_over_img.get_rect()
    game_over_img_rect.center=(WINDOW_W/2,WINDOW_H/2)
    canvas.blit(game_over_img_rect,game_over_img_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                game_loop()
        pygame.display.update()

def start_game():
    canvas.fill(BLACK)
    start_img=pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_W/2,WINDOW_H/2)
    canvas.blit(start_img,start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def check_level(SCOER):
    global LEVEL
    if score in range(0,10):
        toge_img_rect.bottom=50
        firewall_img_rect.top = WINDOW_H-50
        LEVEL=1
    elif SCORE in range(10,20):
        toge_img_rect.bottom = 100
        firewall_img_rect.top=WINDOW_H - 100
        LEVEL=2
    elif SCORE in range(20,30):
        toge_img_rect.bottom = 150
        firewall_img_rect.top =WINDOW_H - 150
        LEVEL = 3
    elif SCORE >30:
        toge_img_rect.bottom = 200 
        firewall_img_rect.top = WINDOW_H -200
        LEVEL = 4

def game_loop():
    while True:
        global teki1
        teki1 = Teki1
        teki1  = Teki1()
        flames = Flames()
        boku = Boku()
        add_new_flame_counter = 0
        global SCORE
        SCORE=0
        global HIGH_SCORE
        flames_list=[]
        
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            teki1.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FRAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE+=1
                f.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        boku.up = True
                        boku.down = False
                    elif event.key == pygame.K_DOWN:
                        boku.down = True
                        boku.up =False
                if event.type==pygame.KeyUP:
                    if event.key == pygame.K_UP:
                        boku.up = False
                        boku.down =True
                    elif event.key == pygame.K_DOWN:
                        boku.down = True
                        boku.up = False
            
            score_font = font.render('Score:'+str(SCORE), true,GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200,toge_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font,score_font_rect)
            
            level_font = font.render('Level:' + str(LEVEL),True,GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center= (500,toge_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font,level_font_rect)

            top_score_font = fonr.render('Top Score:'+str(topscore,high_score),True,GREEN)
            top_score_font_rect = top_score_font_.get_rect()
            top_score_font_rect.center = (800,toge_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font,top_score_font_rect)

            canvas.blit(toge_img_rect,toge_img_rect)
            canvas.blit(firewall_img,firewall_img_rect)
            boku.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(boku.boku_img_rect):
                    game_over()
                    if SCORE > boku.boku_score:
                        boku.boku_score=SCORE
            pygame.display.update()
            CLOCK.tick(FPS)

start_game()












# %%
