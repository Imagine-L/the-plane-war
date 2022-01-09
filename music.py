import pygame

pygame.mixer.init()
# 导入音乐函数
def load_sound(fileName: str, set_volume: float) -> pygame.mixer.Sound:
    res = pygame.mixer.Sound(fileName)
    res.set_volume(set_volume)
    return res


# 全局
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)

# 子弹
bullet_sound = load_sound('sound/bullet.wav', 0.2)
# 爆炸效果
bomb_sound = load_sound('sound/use_bomb.wav', 0.2)
# 补给
supply_sound = load_sound('sound/supply.wav', 0.2)
# 子弹击中后
get_bomb_sound = load_sound('sound/get_bomb.wav', 0.2)
get_bullet_sound = load_sound('sound/get_bullet.wav', 0.2)
# 升级
upgrade_sound = load_sound('sound/upgrade.wav', 0.2)
# 敌人音效
enemy3_fly_sound = load_sound('sound/enemy3_flying.wav', 0.2)
enemy1_down_sound = load_sound('sound/enemy1_down.wav', 0.1)
enemy2_down_sound = load_sound('sound/enemy2_down.wav', 0.2)
enemy3_down_sound = load_sound('sound/enemy3_down.wav', 0.5)
# 本机死亡
me_down_sound = load_sound('sound/me_down.wav', 0.2)
