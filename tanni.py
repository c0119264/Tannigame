#%%
import math
import sys
import pygame
from pygame.locals import *
from random import randint
import random
import time

pygame.init()#pygameのモジュールを初期化
screen = pygame.display.set_mode((1200, 600)) #ウィンドウを1200×600に設定
pygame.display.set_caption("単位ほいほい")#ウィンドウの左上に”単位ほいほい”と表示する
sysfont = pygame.font.SysFont(None, 36)#フォントを設定する
FPSCLOCK = pygame.time.Clock()#時間を設定する
FPS = 15


class CanonGame():
    def __init__(self):
        bullet_image = pygame.image.load("tanni.png")#rakutan.pngを読み込む
        self.set_teacher()
        self.set_bullet()
        self.bullet_shot = False
        self.is_gakusei = False
        self.is_collision = False
        self.score = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:#×ボタンを押すと全て終了させる
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_a: #aボタンを押したとき
                        self.bullet_shot = True
                    elif event.key == K_UP and self.teacher_radian < 89:#teacherの角度が89度以下の処理
                        self.teacher_radian += 1
                    elif event.key == K_DOWN and self.teacher_radian > 0:#teacherの角度が0度以上の処理
                        self.teacher_radian -= 1
                    

            self.set_gakusei()
            self.bullet()

            screen.fill((255, 255, 255))#白の背景にする
            screen.blit(bullet_image, (self.bullet_x, self.bullet_y))#画像を更新する
            if not self.is_collision:#衝突が起きなかった場合、gakusei_imageを更新する
                screen.blit(self.gakusei_image, (self.gakusei_x, self.gakusei_y))
            elif self.is_collision:#衝突が起きた場合の処理
                screen.blit(self.pang_image, self.pang_rect)
            rotate_teacher = pygame.transform.rotate(self.teacher_image, self.teacher_radian - 45)#画像を回転させる
            teacher_rect = rotate_teacher.get_rect()
            teacher_rect.center = (84, 536) #teacherの中心画像を設定する
            screen.blit(rotate_teacher, teacher_rect)#画像更新
            score_image = sysfont.render("score : {}".format(self.score), True, (255, 0, 0))#score_imageの設定
            screen.blit(score_image, (10, 20))#score_imageの描画位置

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def set_bullet(self): #弾の設定
        self.bullet_x = 130  #弾のx座標
        self.bullet_y = 465 #弾のy座標
        a=random.randint(45,70)#45から70の数字をランダムに発生させる
        self.bullet_speed = a #弾の速度
        self.time = 0
   
    
    def set_teacher(self):
        self.teacher_image = pygame.image.load("teacher.png") #teacher.pngを読み込む
        self.teacher_radian = 45 #画像の角度を45度に設定

    def set_gakusei(self):
        now_time = time.time() #timeモジュールを設定
        if self.is_collision:
            if now_time - self.gakusei_break > 1: #学生が消えて1秒以上経ったら、次の学生を出現させる
                self.is_collision = False
        if self.is_collision is False:
            if self.is_gakusei:
                self.gakusei_y = self.gakusei_y - 12
                self.gakusei_alive = time.time()
                if self.gakusei_alive - self.gakusei_create > 4: #現在時刻を取得し,gakusei_aliveとの差が4秒以上になれば、再び学生を出現させる
                    self.is_gakusei = False
                else:
                    self.collision_check()
            else:
                self.gakusei_image = pygame.image.load("gakusei.png") #gakusei.pngを読み込む
                self.gakusei_x = randint(900, 1050) #x座標(900から1050の間)
                self.gakusei_y = 600 #y座標は600に学生を出現させる
                self.is_gakusei = True
                self.gakusei_create = time.time()

    def bullet(self):
        gravity = 9.8 #重力を9.8にする
        if self.bullet_shot:
            bullet_speed_x = self.bullet_speed * math.cos(math.radians(self.teacher_radian)) #弾のx方向のスピードを設定
            bullet_speed_y = (self.bullet_speed * math.sin(math.radians(self.teacher_radian))) #弾のy方向のスピードを設定
            self.bullet_x = self.bullet_x + bullet_speed_x #斜方投射
            self.bullet_y = self.bullet_y - bullet_speed_y + gravity * self.time #斜方投射
            self.time += 0.28

            if self.bullet_x > 1200 or self.bullet_y > 600: #弾がx座標1200、y座標600より大きくなったら
                self.bullet_shot = False #弾を消す
                self.set_bullet()

    def collision_check(self):
        distance_y = ((self.gakusei_y+100 ) - (self.bullet_y))**2 #画像の左上の座標からy座標を100px中心をずらした円
        distance_x = ((self.gakusei_x+50) - (self.bullet_x))**2 #画像の左上の座標からx座標を50px中心をずらした円
        distance = (distance_x + distance_y)**(1/2) #三平方の定理で距離を求める
        if distance < 100: #画像距離が100px以下なら
            self.pang_image = pygame.image.load("goukaku.png") #taigaku.pngを読み込む
            self.pang_rect = self.pang_image.get_rect() #画像の大きさを取得
            self.pang_rect.center = (600,300) #ウィンドウの中心(600,300)の位置に表示させる
            self.is_collision = True
            self.is_gakusei = False
            self.total_score(100)
            self.gakusei_break = time.time()

    def total_score(self, score): #スコアの設定
        self.score = self.score + score 

            


def main():
    CanonGame()


if __name__ == '__main__':
    main()
# %%
