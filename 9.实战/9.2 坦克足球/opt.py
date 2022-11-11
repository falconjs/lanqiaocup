"""
Fake opt class

"""

import opt

GROUND_WIDTH = 0 # 场地宽
GROUND_HEIGHT = 0 # 场地高
TANK_WIDTH = 0 # 机器人宽
TANK_LENGTH = 0 # 机器人长
DOOR_WIDTH = 0 # 球门宽
MY_DOOR_LEFT = 0 # 我的球门左顶点坐标
MY_DOOR_RIGHT = 0 # 我的球门右顶点坐标
ENEMY_DOOR_RIGHT = opt.Pos(0,0) # 敌方球门右顶点坐标
ENEMY_DOOR_LEFT = opt.Pos(0,0) # 敌方球门左顶点坐标
BALL_RADIUS = 0 # 球半径
BULLET_VELOCITY = 0 # 炮弹的速度，160m/s，或者可以理解为2m/帧
BULLET_RADIUS = 0 # 炮弹的半径
BALL_LINEAR_DAMPING = 0 # 足球的线速度阻力系数
BALL_ANGULAR_DAMPING = 0 # 足球的角速度阻力系数

class Tank: 

    def __init__(data_list, i):
        return

    def angle_to(x, y):
        # 获取物体与某坐标（x, y) 的角度
        angle = None
        return angle
    
    def distance_to(x, y):
        # 获取物体与某坐标 (x, y) 距离
        distance = None
        return distance

class Pos:

    x = 0
    y = 0

    def __init___(x, y):
        return

class Sprite:
    def __init___(i, x, y, vx, vy, r, vr):
        return


class Ball:
    def __init___(data_list):
        return


class Bullet:
    def __init___(data_list):
        return

