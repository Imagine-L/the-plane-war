# 控制补给品
import pygame
import random


# 所有补给物的父类
class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size, image) -> None:
        pygame.sprite.Sprite.__init__(self)
        # 加载图片
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.reset()
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        # 默认不存活
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        # 初始位置
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
        self.active = True


# 加强子弹
class BulletSupply(Supply):
    def __init__(self, bg_size) -> None:
        super().__init__(bg_size, 'images/bullet_supply.png')


# 增加炸弹
class BombSupply(Supply):
    def __init__(self, bg_size) -> None:
        super().__init__(bg_size, 'images/bomb_supply.png')
