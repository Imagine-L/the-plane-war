# 主函数，程序入口
import time

import pygame
import sys
import traceback
from music import *
from myplane import *
from enemy import *
from bullet import *
from supply import *

# pygame模块初始化
pygame.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')
# 背景
background = pygame.image.load('images/background.png').convert()
# 帧率
fps = 60


# 添加普通飞机，参数时简单飞机组，全部飞机组，数量
def add_easy_enemy(easy_enemies, enemies, num):
    for i in range(num):
        enemy = EasyEnemy(bg_size)
        easy_enemies.add(enemy)
        enemies.add(enemy)


# 添加中等飞机
def add_mid_enemy(mid_enemies, enemies, num):
    for i in range(num):
        enemy = MidEnemy(bg_size)
        mid_enemies.add(enemy)
        enemies.add(enemy)


# 添加boss飞机
def add_boss_enemy(boss_enemies, enemies, num):
    for i in range(num):
        enemy = BossEnemy(bg_size)
        boss_enemies.add(enemy)
        enemies.add(enemy)


# 添加速度
def add_speed(target: pygame.sprite.Group, speed: int):
    for each in target:
        each.speed += speed


# 创建所有飞机
def create_plane():
    pass


# 入口
def main():
    pygame.mixer.music.play(-1)
    running = True
    clock = pygame.time.Clock()
    # 生成我方飞机
    hero = MyPlane(bg_size)
    # 生成敌方飞机组
    enemies = pygame.sprite.Group()
    # 生成敌方普通飞机
    easy_enemies = pygame.sprite.Group()
    add_easy_enemy(easy_enemies, enemies, 15)
    # 生成敌方中等飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemy(mid_enemies, enemies, 4)
    # 生成boss
    boss_enemies = pygame.sprite.Group()
    add_boss_enemy(boss_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1.append(Bullet(hero.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num // 2):
        bullet2.append(SuperBullet((hero.rect.centerx - 33, hero.rect.centery)))
        bullet2.append(SuperBullet((hero.rect.centerx + 30, hero.rect.centery)))

    # 控制飞机的图片切换
    switch_img = True
    # 中弹图片索引
    easy_destroy_index = 0
    mid_destroy_index = 0
    boss_destroy_index = 0
    me_destroy_index = 0
    # 图片切换延时
    delay = 100
    # 显示得分的字体
    score_font = pygame.font.Font('font/font.ttf', 36)
    # 设置难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font.ttf', 48)
    bomb_num = 3

    # 每30s发放一个补给包
    bullet_supply = BulletSupply(bg_size)
    bomb_supply = BombSupply(bg_size)
    supply_time = pygame.USEREVENT
    pygame.time.set_timer(supply_time, 30 * 1000)

    # 超级子弹定时器
    double_bullet_time = pygame.USEREVENT + 1

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 解除我方飞机无敌计时器
    invincible_time = pygame.USEREVENT + 2

    # 用于阻止重复打开文件
    recorded = False

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_pressed_image  # 标志当前的按钮

    # 游戏结束画面
    gameover_font = pygame.font.Font('font/font.ttf', 48)
    again_img = pygame.image.load('images/again.png').convert_alpha()
    again_rect = again_img.get_rect()
    gameover_img = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_rect = gameover_img.get_rect()

    # 循环执行程序
    while running:
        for event in pygame.event.get():
            # 程序退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # 检测鼠标是否点击暂停/恢复按钮
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(supply_time, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            # 判断鼠标是否悬停在暂停/恢复按钮
            elif event.type == pygame.MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            # 当用户按下键盘处理事件
            elif event.type == pygame.KEYDOWN:
                # 用户如果按下空格，表示释放炸弹，清空所有敌人
                if event.key == pygame.K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            # 每间隔一段时间，就会发放补给，并随机选择发送哪个补给
            elif event.type == supply_time:
                supply_sound.play()
                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            # 监听超级子弹的定时器
            elif event.type == double_bullet_time:
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_time, 0)
            # 监听事件，解除我方飞机无敌
            elif event.type == invincible_time:
                hero.invincible = False
                pygame.time.set_timer(invincible_time, 0)

        # 更新画面
        screen.blit(background, (0, 0))

        # 绘制游戏结束(我方飞机阵亡)
        if not hero.life_num:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 停止全部音效
            pygame.mixer.stop()
            # 停止发放补给
            pygame.time.set_timer(supply_time, 0)
            if not recorded:
                recorded = not recorded
                # 读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())
                # 如果玩家得分高于历史最高分，存档
                if hero.score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(hero.score))
            # 绘制结束画面
            record_score_text = score_font.render("Best: %d" % record_score, True, 'white')
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score: ", True, 'white')
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 2
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(hero.score), True, 'white')
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_img, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_img, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

            # screen.blit(paused_image, paused_rect)
            pygame.display.flip()
            continue

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 绘制分数
        score_text = score_font.render(f'Score: {hero.score}', True, 'white')
        screen.blit(score_text, (10, 5))

        # 如果游戏暂停则不继续往下执行
        if paused:
            screen.blit(resume_nor_image, paused_rect)
            screen.blit(score_text, (10, 5))
            pygame.display.flip()
            continue

        # 检测用户的键盘操作进行移动，get_pressed获取到列表
        # 这个列表包含键盘所有类型的布尔类型值
        hero.move(pygame.key.get_pressed())

        # 绘制我方飞机
        if hero.active:
            if switch_img:
                screen.blit(hero.image1, hero.rect)
            else:
                screen.blit(hero.image2, hero.rect)
        else:
            if me_destroy_index == 0: me_down_sound.play()
            screen.blit(hero.destroy_img[me_destroy_index], hero.rect)
            me_destroy_index = (me_destroy_index + 1) % 4
            if me_destroy_index == 0:
                # 生命减少
                hero.life_num -= 1
                hero.reset()
                pygame.time.set_timer(invincible_time, 3 * 1000)

        # 绘制炸弹补给
        if bomb_supply.active:
            bomb_supply.move()
            screen.blit(bomb_supply.image, bomb_supply.rect)
            if pygame.sprite.collide_mask(bomb_supply, hero):
                get_bomb_sound.play()
                if bomb_num < 5:
                    bomb_num += 1
                bomb_supply.active = False

        # 绘制超级子弹补给
        if bullet_supply.active:
            bullet_supply.move()
            screen.blit(bullet_supply.image, bullet_supply.rect)
            if pygame.sprite.collide_mask(bullet_supply, hero):
                get_bullet_sound.play()
                # 发射超级子弹(设置可以使用，同时开启定时器)
                is_double_bullet = True
                pygame.time.set_timer(double_bullet_time, 18 * 1000)
                bullet_supply.active = False

        # 重置子弹，每间隔10帧就重置一次子弹(跟随我方飞机移动)
        if delay % 10 == 0:
            bullet_sound.play()
            if is_double_bullet:
                bullets = bullet2
                bullets[bullet2_index].reset((hero.rect.centerx - 33, hero.rect.centery))
                bullet2_index = (bullet2_index + 1) % bullet1_num
                bullets[bullet2_index].reset((hero.rect.centerx + 30, hero.rect.centery))
                bullet2_index = (bullet2_index + 1) % bullet1_num
            else:
                bullets = bullet1
                bullets[bullet1_index].reset(hero.rect.midtop)
                bullet1_index = (bullet1_index + 1) % bullet1_num

        # 绘制子弹，并检测子弹是否击中敌机
        for b in bullets:
            if b.active:
                b.moveUp()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in boss_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False

        # 绘制boss飞机
        for each in boss_enemies:
            # 首先判断是否存活
            if each.active:
                each.moveDown()
                # 如果被击中，就绘制被打到后的特效，否则绘制正常图片
                if each.hit:
                    screen.blit(each.img_hit, each.rect)
                    each.hit = False
                else:
                    if switch_img:
                        screen.blit(each.image, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)

                # 绘制血条
                pygame.draw.line(screen, 'black', (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5), 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / BossEnemy.energy
                if energy_remain > 0.2:
                    energy_color = 'green'
                else:
                    energy_color = 'red'
                pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
                # 即将出现时，播放boss音效
                if each.rect.bottom >= -50:
                    enemy3_fly_sound.play(-1)
            else:
                # 毁灭后，播放音效以及毁灭图片
                if not (delay % 3):
                    if boss_destroy_index == 0: enemy3_down_sound.play()
                    screen.blit(each.destroy_img[boss_destroy_index], each.rect)
                    boss_destroy_index = (boss_destroy_index + 1) % 6
                    # 毁灭后，重置飞机位置/关闭音效
                    if boss_destroy_index == 0:
                        enemy3_fly_sound.stop()
                        hero.score += 10000
                        each.reset()

        # 绘制中型飞机
        for each in mid_enemies:
            if each.active:
                each.moveDown()
                # 如果被击中，就绘制被打到后的特效，否则绘制正常图片
                if each.hit:
                    screen.blit(each.img_hit, each.rect)
                    each.hit = False
                else:
                    screen.blit(each.image, each.rect)
                # 绘制血条
                pygame.draw.line(screen, 'black', (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5), 2)
                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / BossEnemy.energy
                if energy_remain > 0.2:
                    energy_color = 'green'
                else:
                    energy_color = 'red'
                pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
            else:
                if not (delay % 3):
                    if mid_destroy_index == 0: enemy2_down_sound.play()
                    screen.blit(each.destroy_img[mid_destroy_index], each.rect)
                    mid_destroy_index = (mid_destroy_index + 1) % 4
                    if mid_destroy_index == 0:
                        hero.score += 6000
                        each.reset()

        # 绘制普通飞机
        for each in easy_enemies:
            if each.active:
                each.moveDown()
                screen.blit(each.image, each.rect)
            else:
                if not (delay % 3):
                    if easy_destroy_index == 0: enemy1_down_sound.play()
                    screen.blit(each.destroy_img[easy_destroy_index], each.rect)
                    easy_destroy_index = (easy_destroy_index + 1) % 4
                    if easy_destroy_index == 0:
                        hero.score += 1000
                        each.reset()

        # 检测我方飞机是否碰撞
        enemies_down = pygame.sprite.spritecollide(hero, enemies, False, pygame.sprite.collide_mask)
        if enemies_down and not hero.invincible:
            hero.active = False  # 我方飞机死亡
            for e in enemies_down:  # 敌方飞机死亡
                e.active = False

        # 绘制本机剩余生命
        if hero.life_num:
            for i in range(hero.life_num):
                screen.blit(hero.life_img,
                            (width - 10 - (i + 1) * hero.life_rect.width, height - 10 - hero.life_rect.height))

        # 绘制全屏炸弹数量
        bomb_text = bomb_font.render(f'x {bomb_num}', True, 'white')
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
        screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

        # 根据用户的得分增加难度
        if level == 1 and hero.score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加3架普通敌机、2架中型敌机、1架boss敌机
            add_easy_enemy(easy_enemies, enemies, 3)
            add_mid_enemy(mid_enemies, enemies, 2)
            add_boss_enemy(boss_enemies, enemies, 1)
            # 增加普通敌机的速度
            add_speed(easy_enemies, 1)
        elif level == 2 and hero.score > 300000:
            level = 3
            upgrade_sound.play()
            upgrade_sound.play()
            # 增加5架普通敌机、3架中型敌机、2架boss敌机
            add_easy_enemy(easy_enemies, enemies, 5)
            add_mid_enemy(mid_enemies, enemies, 3)
            add_boss_enemy(boss_enemies, enemies, 2)
            # 增加普通敌机的速度
            add_speed(easy_enemies, 1)
            add_speed(mid_enemies, 1)
        elif level == 3 and hero.score > 600000:
            level = 4
            upgrade_sound.play()
            # 增加5架普通敌机、3架中型敌机、2架boss敌机
            add_easy_enemy(easy_enemies, enemies, 5)
            add_mid_enemy(mid_enemies, enemies, 3)
            add_boss_enemy(boss_enemies, enemies, 2)
            # 增加普通敌机的速度
            add_speed(easy_enemies, 1)
            add_speed(mid_enemies, 1)
            add_speed(boss_enemies, 1)
        elif level == 4 and hero.score > 1000000:
            level = 5
            upgrade_sound.play()
            # 增加6架普通敌机、4架中型敌机、3架boss敌机
            add_easy_enemy(easy_enemies, enemies, 6)
            add_mid_enemy(mid_enemies, enemies, 4)
            add_boss_enemy(boss_enemies, enemies, 3)
            # 增加普通敌机的速度
            add_speed(easy_enemies, 1)
            add_speed(mid_enemies, 1)
            add_speed(boss_enemies, 2)
        elif level == 5 and hero.score > 1500000:
            level = 6
            upgrade_sound.play()
            # 增加6架普通敌机、4架中型敌机、3架boss敌机
            add_easy_enemy(easy_enemies, enemies, 6)
            add_mid_enemy(mid_enemies, enemies, 4)
            add_boss_enemy(boss_enemies, enemies, 3)
            # 增加普通敌机的速度
            add_speed(easy_enemies, 2)
            add_speed(mid_enemies, 2)
            add_speed(boss_enemies, 3)

        # 控制图片切换的延时
        if delay % 5 == 0:
            switch_img = not switch_img

        if delay < 0:
            delay = 100
        delay -= 1

        pygame.display.flip()
        # 控制帧率
        clock.tick(fps)


if __name__ == '__main__':
    try:
        main()
    except:
        print('游戏结束！')
        pygame.quit()
