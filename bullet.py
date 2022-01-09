# 控制子弹
import pygame


# 普通子弹
class Bullet(pygame.sprite.Sprite):
    # 初始化子弹，position为子弹的初始位置
    def __init__(self, position: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)
        # 子弹图片
        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        # 初始化子弹位置
        self.reset(position)
        # 速度
        self.speed = 12
        # 标志位，判断是否碰撞
        self.mask = pygame.mask.from_surface(self.image)

    # 射击子弹向上移动
    def moveUp(self):
        if self.rect.top < 0:
            self.active = False
        self.rect.top -= self.speed

    def reset(self, position):
        # 位置
        self.rect.left, self.rect.top = position
        # 是否存活
        self.active = True


class SuperBullet(Bullet):
    def __init__(self, position: tuple) -> None:
        super().__init__(position)
        self.active = False
        self.image = pygame.image.load('images/bullet2.png').convert_alpha()
        self.speed = 14
