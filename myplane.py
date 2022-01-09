# 控制我方飞机
import pygame

# 我方飞机
class MyPlane(pygame.sprite.Sprite):
    # 我方飞机初始化，bg_size为背景
    def __init__(self, bg_size) -> None:
        pygame.sprite.Sprite.__init__(self)
        # 飞机图片
        self.image1 = pygame.image.load('images/me1.png').convert_alpha()
        self.image2 = pygame.image.load('images/me2.png').convert_alpha()
        # 我方飞机死亡图片
        self.destroy_img = [
            pygame.image.load('images/me_destroy_1.png').convert_alpha(),
            pygame.image.load('images/me_destroy_2.png').convert_alpha(),
            pygame.image.load('images/me_destroy_3.png').convert_alpha(),
            pygame.image.load('images/me_destroy_4.png').convert_alpha()
        ]
        self.rect = self.image1.get_rect()
        # 背景宽高
        self.width, self.height = bg_size
        # 飞机初始位置
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = self.height - self.rect.height - 60
        # 飞机速度
        self.speed = 10
        # 我方飞机是否存活
        self.active = True
        # 标志位，判断碰撞使用
        self.mask = pygame.mask.from_surface(self.image1)
        # 统计得分
        self.score = 0
        # 生命图片
        self.life_img = pygame.image.load('images/life.png').convert_alpha()
        self.life_rect = self.life_img.get_rect()
        # 生命数量
        self.life_num = 3
        # 我方飞机是否无敌
        self.invincible = False

    # 根据不同的按键移动到不同的位置
    def move(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.moveUp()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.moveRight()

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.moveDown()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.moveLeft()

    # 向上移动
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    # 向下移动
    def moveDown(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height

    # 向左移动
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    # 向右移动
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    # 重置我方飞机
    def reset(self):
        # 飞机初始位置
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = self.height - self.rect.height - 60
        # 重新活着
        self.active = True
        # 复活有一定的无敌时间
        self.invincible = True
