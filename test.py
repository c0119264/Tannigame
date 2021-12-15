#%%
import pygame   #pygameをインポートする。
import time #timeをインポートする。
from pygame import Color    #pygameからColorをインポートする。
import sys
import random

# 定数群
FPS = 60     # Frame per Second 毎秒のフレーム数
DURATION = 0.05        # 描画間隔

BOX_WIDTH = 1200        # ゲーム領域の幅
BOX_HEIGHT = 450       # ゲーム領域の高さ

TANK_WIDTH = 10      # タンクの幅
TANK_HEIGHT = 40     # タンクの高さ
TANK_COLOR = "pink" # タンクの色

BLOCK_WIDTH=200
BLOCK_HEIGHT=200


TARGET_WIDTH, TARGET_HEIGHT = (100, 100) # targetのサイズ
TARGET_COLOR = "red" # 色
TARGET_COLOR2 = "green"

BALL_VX=2
BALL_DIAMETER=10 # ボールの直径
LARGE_BALL_COLOR="blue"
SMALL_BALL_COLOR="yellow"

# ----------------------------------
# Tankは、spriteクラスを継承している。
class Tank(pygame.sprite.Sprite):
    def __init__(self,screen,x,y): # コンストラクタ
        super().__init__() # オーバーライド
        self.screen = screen
        self.x, self.y = (x, y)
        self.vx, self.vy = (10, 10)
        self.rect = pygame.Rect(x,y,TANK_WIDTH,TANK_HEIGHT)
        self.image = pygame.image.load("boku.png")
        self.screen.blit(self.image, (self.x, self.y))

    def draw(self): # 描画
        self.rect = self.screen.blit(self.image, (self.x, self.y))

    def up(self): # 上に移動
        y = self.y - self.vy
        if (y >= 0):
            self.y = y     # 移動量の設定は、独自メソッド
        
        
    def down(self): # 下に移動
        y = self.y + self.vy
        if (y <= 320-55):
            self.y = y

    def left(self): # 左に移動
        x = self.x - self.vx
        if (x >= 0):
            self.x = 0
    
    def right(self): # 右に移動
        x = self.x + self.vx
        if (x <= 640-70):
            self.x = 0
    
    def stop(self): # 停止
        self.vx = 0
        self.vy = 0

# Blockは、spriteクラスを継承している。
class Block(pygame.sprite.Sprite):
    #teki1_velocity=10

    def __init__(self,screen,x1,y1,z=1): # コンストラクタ、不必要に引数を増やさないように初期値を入れてあげる
        super().__init__() # オーバーライド
        self.image = pygame.image.load("teki1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = screen
        #self.rect = pygame.Rect(x1,y1,BLOCK_WIDTH,BLOCK_HEIGHT)
        self.rect.top = BOX_HEIGHT/2
        self.rect.right = BOX_WIDTH
        self.up = True
        self.down = False
        vy=10

    def draw(self):
        self.screen.blit(self.image, self.rect)

        
    def update(self):
        canvas.blit(self.image,self.image.rect)
        if self.iamge.rect.top <= 0:
            self.up=False
            self.down=True
        elif self.image.rect.bottom >= BOX_HEIGHT:
            self.up =True
        self.down = False

        if self.up:
            self.rect.top -= self.teki1_velocity
        elif self.down:
            self.rect.top += self.teki1_velocity


    

class Bullet(pygame.sprite.Sprite):
    def __init__(self,group,screen,x,y,radius,vx):
        super().__init__(group)
        self.radius = radius
        self.vx = -vx
        self.rect = pygame.Rect(x,y,radius,radius)
        self.screen = screen
        self.image = pygame.image.load("rakutan.png")

    def update(self):
        self.rect.move_ip(-self.vx, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, group, screen, LARGE_BALL_COLOR, x, y, d, BALL_VX):
        super().__init__()
        self.group = group
        self.screen = screen
        self.x, self.y = (x, y)
        self.vx, self.vy = (-10, 10)
        self.rect = pygame.Rect(x,y,TANK_WIDTH,TANK_HEIGHT)
        self.image = pygame.image.load("teki1.png")
        self.screen.blit(self.image, (self.x-40, self.y+5))
        self.bullet = Bullet(self.group, self.screen, self.x, self.y, 10, self.vx)

class LargeBall(Ball):
    def __init__(self, group, screen, x, y):
        d = BALL_DIAMETER * 2
        super().__init__(group, screen, LARGE_BALL_COLOR, x, y, d, BALL_VX/2)


backgrond= pygame.image.load("firewall.png")


# ----------------------------------
# Box(ゲーム領域)の定義
class Box:
    def __init__(self): # コンストラクタ
        self.tank = None
        self.block = None
        self.bullets = pygame.sprite.Group()     

    def set(self):   # 初期設定を一括して行う
        self.screen = pygame.display.set_mode((BOX_WIDTH, BOX_HEIGHT))
        self.clock = pygame.time.Clock()   # 時計オブジェクト
        self.tank = Tank(self.screen,0,100) # tankを準備する
        self.block = Block(self.screen,1000,100) # blockを準備する

    def fire(self):
        LargeBall(self.bullets, self.screen, self.block.rect.x+50, self.block.rect.y+60)
    
    def animate(self):
        LOOP = True
        fire_image = pygame.image.load("game-over.png")
        while LOOP: # メインループ
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: LOOP = False

            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延

            pressed_keys = pygame.key.get_pressed() # キー情報を取得
            if pressed_keys[pygame.K_UP]:    # 上が押されたら
                self.tank.up()       # y 座標を小さく
            if pressed_keys[pygame.K_DOWN]:  # 下が押されたら
                self.tank.down()        # y 座標を大きく
            if pressed_keys[pygame.K_LEFT]:    # 左が押されたら
                self.tank.left()       # x 座標を小さく
            if pressed_keys[pygame.K_RIGHT]:  # 右が押されたら
                self.tank.right()        # x 座標を大きく
            if pressed_keys[pygame.K_a]:
                self.fire()
            
        

            clock=pygame.time.Clock()
            min_time,max_time=500,2000 #0.5second up to  4seconds
            bullet_time=pygame.USEREVENT+1
            pygame.time.set_timer(bullet_time,random.randint(min_time,max_time))
    
            for event in pygame.event.get():
                if event.type==bullet_time:
                    pygame.time.set_timer(bullet_time,random.randint(min_time,max_time))
                    self.fire()


            self.bullets.update()
            self.tank.update()
            self.tank.draw() # tankの描画
            self.block.draw() # blockの描画、常時は赤
            if pygame.sprite.spritecollideany(self.tank, self.bullets):
                self.screen.blit(fire_image, (0,0))
            self.bullets.draw(self.screen)
            if pygame.sprite.collide_rect(self.tank,self.block): # 衝突判定
                self.tank.stop() # 停止

            pygame.display.flip() # 描画を画面に反映
            self.screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない


# ----------------------------------
# メインルーチン
box = Box()
box.set()       # ゲームの初期設定
box.animate()   # アニメーション
pygame.quit()   # 画面を閉じる
# %%

# %%
