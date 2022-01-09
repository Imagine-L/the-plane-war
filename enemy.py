# 控制敌人飞机
import random

import pygame


# 所有敌机的父类
class Enemy(pygame.sprite.Sprite):
    # 初始化，bg_size：背景，image：敌机图片，hit_img：被击中图片，speed：速度
    def __init__(self, bg_size: tuple, image: str, hit_img: str, speed: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        # 敌机图片
        self.image = pygame.image.load(image).convert_alpha()
        # 被击中后图片
        if hit_img is not None:
            self.img_hit = pygame.image.load(hit_img).convert_alpha()
        else:
            self.image = self.image
        self.rect = self.image.get_rect()
        # 背景的宽高
        self.width, self.height = bg_size
        # 敌机的速度
        self.speed = speed
        # 标志位，判断碰撞使用
        self.mask = pygame.mask.from_surface(self.image)

    # 敌机向下移动
    def moveDown(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    # 重新初始化敌机的位置(敌机死亡后/初始化)
    def reset(self, left_pos: int, top_pos: int):
        self.rect.left = left_pos
        self.rect.top = top_pos
        # 敌机是否存活(默认为True)
        self.active = True
        # 敌机是否被击中(默认没有)
        self.hit = False


# 普通敌人
class EasyEnemy(Enemy):
    def __init__(self, bg_size) -> None:
        # 父类执行初始化
        super().__init__(bg_size, 'images/enemy1.png', None, 2)
        # 普通敌人死亡图片
        self.destroy_img = [
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),
            pygame.image.load('images/enemy1_down4.png').convert_alpha()
        ]
        # 初始化敌机位置
        self.reset()

    # 重新初始化敌机的位置(敌机死亡后/初始化)
    def reset(self):
        # 随机位置
        left_pos = random.randint(0, self.width - self.rect.left - 100)
        top_pos = random.randint(-5 * self.height, 0)
        super().reset(left_pos, top_pos)


# 中等的敌人
class MidEnemy(Enemy):
    # 类变量，表示满状态的血量
    energy = 8

    def __init__(self, bg_size) -> None:
        super().__init__(bg_size, 'images/enemy2.png', 'images/enemy2_hit.png', 1)
        # 中等敌人死亡图片
        self.destroy_img = [
            pygame.image.load('images/enemy2_down1.png').convert_alpha(),
            pygame.image.load('images/enemy2_down2.png').convert_alpha(),
            pygame.image.load('images/enemy2_down3.png').convert_alpha(),
            pygame.image.load('images/enemy2_down4.png').convert_alpha()
        ]
        # 初始化敌机位置
        self.reset()

    def reset(self):
        left_pos = random.randint(0, self.width - self.rect.width)
        top_pos = random.randint(-10 * self.height, -self.height)
        self.energy = MidEnemy.energy
        super().reset(left_pos, top_pos)


# Boss敌人
class BossEnemy(Enemy):
    # 类变量，表示满状态的血量
    energy = 20

    def __init__(self, bg_size) -> None:
        super().__init__(bg_size, 'images/enemy3_n1.png', 'images/enemy3_hit.png', 1)
        self.image2 = pygame.image.load('images/enemy3_n2.png')
        # boss敌人死亡图片
        self.destroy_img = [
            pygame.image.load('images/enemy3_down1.png').convert_alpha(),
            pygame.image.load('images/enemy3_down2.png').convert_alpha(),
            pygame.image.load('images/enemy3_down3.png').convert_alpha(),
            pygame.image.load('images/enemy3_down4.png').convert_alpha(),
            pygame.image.load('images/enemy3_down5.png').convert_alpha(),
            pygame.image.load('images/enemy3_down6.png').convert_alpha()
        ]
        # 初始化敌机位置
        self.reset()

    def reset(self):
        left_pos = random.randint(0, self.width - self.rect.width)
        top_pos = random.randint(-15 * self.height, -5 * self.height)
        self.energy = BossEnemy.energy
        super().reset(left_pos, top_pos)
