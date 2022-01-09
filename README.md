# 飞机大战

#### 介绍
来自小甲鱼视频P91-P97，原视频地址：https://www.bilibili.com/video/BV1Fs411A7HZ?p=91。
仓库中有视频中的全部素材，但是由于全部本人手敲，可能部分代码不一致，导致有些bug...

#### 软件架构
- main.py：程序主配置文件，直接执行该文件即可启动程序

- bullet.py：飞机子弹文件，配置子弹的类

- enemy.py：敌机文件，配置三种类型的敌机

- music.py：导入所有音乐

- myplane.py：我方飞机文件，配置我方飞机类

- supply.py：补给品文件，两种补给品的类

- record.txt：历史最高记录


#### 安装教程

1.  需要python3的运行环境，下载地址：https://www.python.org/。
2.  下载好python3之后需要pygame模块，Windows系统打开终端，输入：` pip3 install pygame` 即可。
3.  如果下载pygame的速度过慢，可以自行百度，换到国内的镜像源即可提升速度。

#### 使用说明

执行main.py即可运行整个程序，进入项目目录，打开终端输入：` python main.py ` 即可。