import opt
import math

""" 
全局变量定义
"""

glb_env_var = {'totaltime': 180}
stuck_count = {"tank1": 0, "tank2": 0, "tank3": 0, "tank4": 0, "tank5": 0}
no_push_to_mydoor_count = {"tank1": 0, "tank2": 0, "tank3": 0, "tank4": 0, "tank5": 0}
run_direct = {"tank1": 1, "tank2": 1, "tank3": 1, "tank4": 1, "tank5": 1}
switch_keeper_pos = "CENTER"

"""
打印信息
"""

def print_start(tankname):
    global glb_env_var
    print(f"=================================  >>>>>>>>>>>>>>>  ===================================")
    print(f"----{tankname}---- 秒 = {glb_env_var['totaltime'] - opt.time_step()/80} -----------")


def print_status(me, ball, tankname):
    print(f"{tankname} 的位置 x={me.x}, y={me.y}, 速度 x={me.vx}, y={me.vy} r={opt.r2a(me.vr)} : stuck_count[{tankname}] = {stuck_count[tankname]}")
    print(f"Ball 的位置 x={ball.x}, y={ball.y}; 球的角度 = {ball.angle}; 球的速度 x={ball.vx}, y={ball.vy}")
    

def print_end(me, vs, hs, tankname):
    global run_direct
    # if get_speed(me) < 0.3: print(f"{tankname}速度慢了")
    print(f"<<<<<< {tankname}输出了 vs={vs}, hs={hs}, 行驶方向={run_direct[tankname]}=======")

"""
卡住处理
"""

def get_speed(sprite):
    """ 
    利用物体的vx，vy，计算v的量
    两直角边计算斜边
    """
    return math.sqrt(sprite.vx ** 2 + sprite.vy ** 2) + 0.000001

# def is_hit_edge(me, tankname):
#     # 在门里
#     if abs(me.x) > 50 : return True

#     if me.x >= 0 :
#         pos = opt.Pos(50, me.y)
#     elif me.x < 0 :
#         pos = opt.Pos(-50, me.y)
#     elif me.y >= 0 :
#         pos = opt.Pos(me.x, 25)
#     else :
#         pos = opt.Pos(me.x, -25)
    
#     return me.is_point_in_range(pos.x, pos.y, 0.2, opt.a2r(10), opt.a2r(-10))

def is_stuck(me, speed, tankname):
    global stuck_count
    stuck_duration = -30
    min_speed = 2

    # 必须先检查是否已经在倒计时中
    if stuck_count[tankname] < 0 : # 卡住中，倒计时
        stuck_count[tankname] = stuck_count[tankname] + 1
        return True

    # 上次状态没有卡住，检查是否卡住
    if me.is_stuck(speed): # 卡住了 系统函数
        stuck_count[tankname] = stuck_duration
        return True
    else:
        if (
            get_speed(me) < speed # 卡了 ， 连续卡 20帧，就是卡住了
            # and is_hit_edge(me, tankname)
        ): 
            stuck_count[tankname] = stuck_count[tankname] + 1 
        elif get_speed(me) >= min_speed : # 有点动了，重置
            stuck_count[tankname] = 0
    
        if stuck_count[tankname] >= 20: # 卡住了
            stuck_count[tankname] = stuck_duration
            return True
    
    return False

"""
定点跑动
"""
def get_distance_to_pos(sprite, pos, keep_distance):
    return get_distance_to(sprite, pos.x, pos.y, keep_distance)

def get_distance_to(sprite, posx, posy, keep_distance):
    distance = opt.distance(sprite.x, sprite.y, posx, posy) - keep_distance   
    # distance = sprite.distance_to(posx, posy) - keep_distance   
    return distance

def get_angle_to_pos(sprite, pos):
    return get_angle_to(sprite, pos.x, pos.y)

def get_angle_to(sprite, posx, posy):
    """
    获取sprite朝向与目标坐标的夹角：（左侧）180到-180 (右侧)
    """
    angle_s = sprite.angle_to(posx, posy)
    if 0 <= angle_s <= 180:
        angle = angle_s
    elif 180 < angle_s <= 360:
        angle = (angle_s - 360)
    else:
        angle = 9999 # This is error
    return angle

def generate_hs(angle, rundirect):
    if rundirect == 1:
        abs_angle = abs(angle)
    elif rundirect == -1:
        abs_angle = 180 - abs(angle)
    else:
        print(f"Error: 错误的 run direct")

    if 0 <= abs_angle <= 1 :
        hs = 0 - (0.1 - 0) * (abs_angle - 0) / (1 - 0)
    elif 1 < abs_angle <= 10 :
        hs = -0.1 - (0.2 - 0.1) * (abs_angle - 1) / (10 - 1)
    elif 10 < abs_angle <= 20 :
        hs = -0.2 - (0.5 - 0.2) * (abs_angle - 10) / (20 - 10)
    elif 20 < abs_angle <= 90 :
        hs = -0.5 - (1 - 0.5) * (abs_angle - 20) / (90 - 20)
    elif 90 < abs_angle :
        hs = -1
    else :
        hs = 0

    if angle < 0:
        hs = -hs
    return hs


def generate_vs(hs, distance, angle, rundirect):
    abs_hs = abs(hs)
    if 0 <= abs_hs <= 0.1 :
        vs = 1
    elif 0.1 < abs_hs <= 0.3 :
        vs = 1
    elif 0.3 < abs_hs <= 0.5 :
        vs = 1 - (1 - 0.7) * (abs_hs - 0.3) / (0.5 - 0.3)
    elif 0.5 < abs_hs <= 1 :
        vs = 0.7 - (0.7 - 0.5) * (abs_hs - 0.5) / (1 - 0.5)
    else :
        vs = 1

    #根据里目标的距离进行提前减速
    if distance is None:
        vs = vs
    elif 0 <= distance < 0.1:
        vs = 0
    elif 0.1 <= distance < 1:
        vs = 0.1
    elif 1 <= distance < 3:
        vs = 0.3
    elif 3 <= distance < 5:
        vs = 0.7
    elif 5 <= distance:
        vs = vs
    else:
        vs = vs

    if rundirect == 1:
        abs_angle = abs(angle)
    elif rundirect == -1:
        abs_angle = 180 - abs(angle)
        vs = -vs
    else:
        print(f"Error: 错误的 run direct")
    
    # 倒车调头
    if abs_angle > 150:
        vs = -vs
        hs = -hs
    
    return vs, hs
    
def get_vshs_run_to_pos(tank, posx, posy, keep_distance, tankname):
    global run_direct

    print(f"get_vshs_run_to_pos")
    angle = get_angle_to(tank, posx, posy)
    distance = get_distance_to(tank, posx, posy, keep_distance)
    print(f"run to pos: angle = {angle}, distance = {distance}")

    # #判断是是否切换正向或反向行驶
    # tank_speed = get_speed(tank)
    # abs_angle = abs(get_angle_to_pos(tank, opt.BALL))
    # if tank.cool_remain == 0 and tank_speed < 5 and abs_angle < 90 :
    #     # 有炮, 速度低, 球在前方
    #     run_direct[tankname] = 1
    # elif tank.cool_remain > 10000 and tank_speed < 5 and abs_angle >= 90 :
    #     # 无炮(20"-10")，速度低，球在后方
    #     run_direct[tankname] = -1

    hs = generate_hs(angle, run_direct[tankname])
    vs, hs = generate_vs(hs, None, angle, run_direct[tankname])
    
    return vs, hs

def get_vshs_run_to_pos_exact(tank, posx, posy, keep_distance, tankname):
    global run_direct
    print(f"get_vshs_run_to_pos_exact")
    angle = get_angle_to(tank, posx, posy)
    distance = get_distance_to(tank, posx, posy, keep_distance)
    print(f"run to pos exact: angle = {angle}, distance = {distance}")

    hs = generate_hs(angle, run_direct[tankname])
    vs, hs = generate_vs(hs, distance, angle, run_direct[tankname])
    
    return vs, hs

"""
推球入门，推球
"""

def get_angle_in(x1, y1, x2, y2, x3, y3):
    """
    返回角213的度数, 3在2的左侧为正, 反之为负
    """
    angle_12 = opt.relative_angle(x1, y1, 0, x2, y2)
    angle_13 = opt.relative_angle(x1, y1, 0, x3, y3)
    angle_213 = angle_13 - angle_12
    # print(f"(1) angle_213 = {angle_213}")
    if abs(angle_213) > 180:
        angle_213 = math.copysign((360-abs(angle_213)), -angle_213)
    
    # print(f"(2) angle_213 = {angle_213}")
    
    return angle_213

def get_position_face_target_keep_distance(src_sprite, target_pos, keep_distance):
    distance_to_target = get_distance_to_pos(src_sprite, target_pos, 0.0000001)
    posx = src_sprite.x - keep_distance * (target_pos.x - src_sprite.x) / distance_to_target
    posy = src_sprite.y - keep_distance * (target_pos.y - src_sprite.y) / distance_to_target
    print(f"target_pos = ({target_pos.x} , {target_pos.y})")
    print(f"src_sprite = ({src_sprite.x} , {src_sprite.y})")
    return opt.Pos(posx, posy)

def get_position_beside(me, ball, target_pos, keep_distance):
    # 要跑过头
    if target_pos.x > 0:
        posx = ball.x - 15
    else:
        posx = ball.x + 15

    if ball.y > me.y :
        posy = ball.y - keep_distance 
    else:
        posy = ball.y + keep_distance
    return opt.Pos(posx, posy)


def get_position(me, ball, target_pos, type, keep_distance):
    if type == "BESIDE":
        pos = get_position_beside(me, ball, target_pos, keep_distance)
    elif type == "FACE_TARGET":     
        pos = get_position_face_target_keep_distance(ball, target_pos, keep_distance)
    else:
        pos = ball

    print(f"raw_pos = ({pos.x} , {pos.y})")

    pos = opt.Pos(max(min(pos.x, 50),-50), max(min(pos.y, 25),-25)) # 不能超出范围
    return pos


def get_line_direct_to_pos_onside(k, b, direct):
    # print(f"k = {k}, b = {b}, direct = {direct}")
    if k == 0:
        print(f"Error : K == 0")
    else:
        posup = opt.Pos((25 - b) / k, 25)
        posdown = opt.Pos((-25 - b) / k, -25)
        posleft = opt.Pos(-50, k * -50 + b)
        posright = opt.Pos(50, k * 50 + b)
        if direct == 1:
            if -25 <= posright.y <= 25: return posright
            elif posright.y > 0: return posup 
            else: return posdown
        elif direct == -1:
            if -25 <= posleft.y <= 25: return posleft
            elif posleft.y > 0: return posup 
            else: return posdown
    return None


def get_s2s_to_pos_onside(sp1, sp2, rebound):
    """
    链接 sprite 1 到 sprite 2 与边的交点的坐标
    rebound == 0, 1 : 获取再次反弹后与边的交点坐标
    """
    # 获得计算公式 y = kx + b ; x = (y - b) / k
    if (sp2.y - sp1.y) != 0 and (sp2.x - sp1.x) != 0:
        k = (sp2.y - sp1.y) / (sp2.x - sp1.x)
        b = sp1.y - k * sp1.x
        pos = None
        if (sp2.x - sp1.x) > 0:
            direct = 1
        elif (sp2.x - sp1.x) < 0:
            direct = -1
        pos = get_line_direct_to_pos_onside(k, b, direct)
        if rebound == 1:
            k = -k
            b = pos.y - k * pos.x
            if abs(pos.x) == 50:
                direct = -direct
            pos = get_line_direct_to_pos_onside(k, b, direct)

    elif (sp2.y - sp1.y) == 0:
        # 水平线，不可使用上面公式
        if (sp2.x - sp1.x) > 0:
            pos = opt.Pos(50, sp2.y)
        elif (sp2.x - sp1.x) < 0:
            pos = opt.Pos(-50, sp2.y)
        if rebound == 1:
            pos = sp1 # 反弹自己身上
   
    elif (sp2.x - sp1.x) == 0: 
        # 垂直线，不可使用上面公式
        if (sp2.y - sp1.y) > 0:
            pos = opt.Pos(sp2.x, 25)
        elif (sp2.y - sp1.y) < 0:
            pos = opt.Pos(sp2.x, -25)
        if rebound == 1:
            pos = sp1

    if pos.x == sp1.x and pos.y == sp1.y:
        print(f"get_s2s_to_pos_onside: rebound to sp1: ({pos.x}, {pos.y})")
    else :
        print(f"get_s2s_to_pos_onside: rebound = {rebound} : ({pos.x}, {pos.y})")
    return pos


def get_vshs_adjust_to_target(me, pos, target, vs, hs, tankname):
    dist_pos = get_distance_to_pos(me, pos, 0)
    angle_pos = get_angle_to_pos(me, pos)
    pos_onside = get_s2s_to_pos_onside(me, pos, 0)

    print(f"{tankname}-微调-dist_pos = {dist_pos}")
    print(f"{tankname}-微调-angle_pos = {angle_pos}")
    print(f"{tankname}-微调-pos_onside = ({pos_onside.x},{pos_onside.y})")

    if (dist_pos <= (opt.BALL.radius + opt.TANK.length * 0.7)) \
        and (abs(angle_pos) < 5) \
        and 49 <= abs(pos_onside.x) <= 51:

        adj_hs = 0.5
        if (opt.ENEMY_DOOR_LEFT.x > 0):
            None
        else: 
            # 考虑敌人的门在左   
            adj_hs = -adj_hs
        
        # 调整方向与正开反开无关
        if (opt.ENEMY_DOOR_LEFT.x-1 <= pos_onside.x <= opt.ENEMY_DOOR_LEFT.x+1) \
            and ( 8 < pos_onside.y < 18 ) \
            :
            hs = hs + adj_hs
            print(f"{tankname}-微调-开始")
        elif (opt.ENEMY_DOOR_LEFT.x-1 <= pos_onside.x <= opt.ENEMY_DOOR_LEFT.x+1) \
            and (-18 < pos_onside.y < -8 ) \
            :
            hs = hs - adj_hs
            print(f"{tankname}-微调-开始")
        if (opt.MY_DOOR_LEFT.x-1 <= pos_onside.x <= opt.MY_DOOR_LEFT.x+1) \
            and ( 0 <= pos_onside.y < 8 ) \
            :
            hs = hs + adj_hs
            print(f"{tankname}-微调-开始")
        elif (opt.MY_DOOR_LEFT.x-1 <= pos_onside.x <= opt.MY_DOOR_LEFT.x+1) \
            and ( -8 < pos_onside.y < 0 ) \
            :
            hs = hs - adj_hs
            print(f"{tankname}-微调-开始")

        hs = max(min(hs, -1), 1)

    return vs, hs

def get_vshs_shot(me, ball, target, exact_pos, tankname):
    """
    停到球的后面，推向对方球门
    """
    print(f"----get_vshs_shot----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    print(f"target = ({target.x}, {target.y}), ball = ({ball.x}, {ball.y}), distance_to_ball = {distance_to_ball}")
    
    angle_target_ball_me = get_angle_in(ball.x, ball.y, target.x, target.y, me.x, me.y)
    angle_optarget_ball_me = 180 - abs(angle_target_ball_me)
    print(f"angle_target_ball_me = {angle_target_ball_me}, angle_optarget_ball_me = {angle_optarget_ball_me}")
    
    keep_distance = 25 * opt.BALL_RADIUS 

    if  (me.x - ball.x) * target.x > 0 : # 我在球和目标之间
        print(f"Run to ball side to behind")
        keep_distance = 7 * opt.BALL_RADIUS # 8以上会导致守门员回不到位
        to_pos = get_position(me, ball, target, "BESIDE", keep_distance)
    elif 0 <= angle_optarget_ball_me < 90 :
        print(f"Run to ball opp pos to target")
        keep_distance = keep_distance * ((0.5*(math.sin(opt.a2r(2 * angle_optarget_ball_me - 90))+1))**0.5)
        to_pos = get_position(me, ball, target, "FACE_TARGET", keep_distance)        
    else :
        print(f"Run to ball opp pos from > 90")
        keep_distance = keep_distance
        to_pos = get_position(me, ball, target, "FACE_TARGET", keep_distance)
    
    print(f"shot: keep_distance = {keep_distance}")
 
    posx, posy = to_pos.x, to_pos.y
    print(f"shot: to_pos = ({to_pos.x} , {to_pos.y})")

    # 跑向目标点
    if exact_pos == True:   
        vs, hs = get_vshs_run_to_pos_exact(me, posx, posy, 0, tankname) # 修改减速可以停到位子
    else :
        vs, hs = get_vshs_run_to_pos(me, posx, posy, 0, tankname)
    
    return vs, hs

def get_vshs_run(me, ball, target, exact_pos, in_sec, tankname):
    print(f"----get_vshs_run----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    angle_target_ball_me = get_angle_in(ball.x, ball.y, target.x, target.y, me.x, me.y)
    print(f"distance_to_ball = {distance_to_ball}")
    print(f"angle_target_ball_me = {angle_target_ball_me}")
    angle_optarget_ball_me = 180 - abs(angle_target_ball_me)
    print(f"angle_optarget_ball_me = {angle_optarget_ball_me}")
    
    keep_distance = 1 * opt.BALL_RADIUS 
    
    if  (me.x - ball.x) * target.x > 0 : # 我在球和目标之间
        print(f"Run to ball side to behind")
        keep_distance = 0 * opt.BALL_RADIUS
        to_pos = get_position(me, ball, target, "BESIDE", keep_distance)
    elif 0 <= angle_optarget_ball_me < 90 :
        print(f"Run to ball opp pos to target")
        keep_distance = keep_distance
        if in_sec > 0:
            to_pos = get_position_in_second(ball, in_sec)
        else:
            to_pos = get_position(me, ball, target, "FACE_TARGET", keep_distance)        
    else :
        print(f"Run to ball opp pos from > 90")
        keep_distance = keep_distance
        to_pos = get_position(me, ball, target, "FACE_TARGET", keep_distance)
 
    print(f"keep_distance = {keep_distance}")
 
    posx, posy = to_pos.x, to_pos.y
    print(f"to_pos = ({to_pos.x} , {to_pos.y})")

    # 跑向目标点
    if exact_pos == True:   
        vs, hs = get_vshs_run_to_pos_exact(me, posx, posy, 0, tankname) # 修改减速可以停到位子
    else :
        vs, hs = get_vshs_run_to_pos(me, posx, posy, 0, tankname)

    # 控球情况下，往门里带球
    # pos = opt.Pos(posx, posy)
    # vs, hs = get_vshs_adjust_to_target(me, pos, target, vs, hs, tankname)

    return vs, hs

def get_vshs_response_to_stuck(vs, hs, me, tankname):
    global run_direct
    global stuck_count
    speed = 1
    if is_stuck(me, speed, tankname) : # is_stuck 的倒计时机制（30帧，一秒80帧），可以保证倒退一定时间
        if run_direct[tankname] == 1:
            vs, hs = -1, 0
        elif run_direct[tankname] == -1:
            vs, hs = 1, 0
        if -10 < stuck_count[tankname] < 0 and get_speed(me) < speed:
            vs = -vs
    return vs, hs

"""
策略战术
"""

def tank_fire(tank):
    print(f"冷却时间 = {tank.cool_remain}")
    if tank.cool_remain == 0:
        tank.do_fire()
        print(f"开火")
        return True
    else: 
        print(f"缺弹药")
    return False


def check_for_fire(vs, hs, me, ball):
    print(f" Check for fire ")

    # 球在紧贴边上
    left, right = -50 + 1.5 * opt.BALL_RADIUS, 50 - 1.5 * opt.BALL_RADIUS
    top, bottom = 25 - 1.5 * opt.BALL_RADIUS, -25 + 1.5 * opt.BALL_RADIUS

    left2, right2 = -50, 52
    top2, bottom2 = 9, -9

    acc_rate = 1

    if (
        is_sprite_in_area(ball, left, right, top, bottom) 
        or is_sprite_in_area(ball, left2, right2, top2, bottom2) 
    ):
        ball_dis_to_door = get_distance_to(ball, opt.ENEMY_DOOR_LEFT.x, 0, 0)
        me_dis_to_ball = get_distance_to_pos(me, ball, 0)
        if ball_dis_to_door <= 8 and me_dis_to_ball <= 4:
            acc_rate = 5

        pos = get_s2s_to_pos_onside(me, ball, 0)
        if (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= acc_rate) \
            and (opt.ENEMY_DOOR_LEFT.x-1 <= pos.x <= opt.ENEMY_DOOR_LEFT.x+1) \
            and (-8 <= pos.y <= 8) \
            :
            if tank_fire(me):
                vs, hs = 0, 0
        
        if (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= acc_rate) \
            and (opt.MY_DOOR_LEFT.x-1 <= pos.x <= opt.MY_DOOR_LEFT.x+1) \
            and (abs(pos.y) <= 25) \
            :
            # 面对自己门不能开折射跑
            None
        elif (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= acc_rate) \
            and (abs(pos.x) >= 45 ) \
            :
            # 面对太靠底线不能开折射跑
            None
        else:
            pos = get_s2s_to_pos_onside(me, ball, 1)
            if (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 0.5) \
                and (opt.ENEMY_DOOR_LEFT.x-1 <= pos.x <= opt.ENEMY_DOOR_LEFT.x+1) \
                and (-4 <= pos.y <= 4) \
                and abs(opt.r2a(me.vr)) < 100 \
                :
                if tank_fire(me):
                    vs, hs = 0, 0

    return vs, hs


def is_in_selectside(sprite, side):
    if side == "ENEMY":
        if (sprite.x * opt.ENEMY_DOOR_LEFT.x) >= 0:
            return True
    elif side == "MY":
        if (sprite.x * opt.MY_DOOR_LEFT.x) > 0:
            return True
    else:
        return False
    

def is_run_toward_selectside(sprite, side, speed):
    if side == "ENEMY":
        # 有一定的速度跑向
        if abs(sprite.vx) > speed and (sprite.vx * opt.ENEMY_DOOR_LEFT.x) >= 0:
            return True
    elif side == "MY":
        # 有一定的速度跑向
        if abs(sprite.vx) > speed and (sprite.vx * opt.MY_DOOR_LEFT.x) > 0:
            return True
    else:
        return False


"""
守门员
"""

def is_ball_run_to_my_door(ball, keep_distance):
    if ball.vx * opt.MY_DOOR_LEFT.x > 0:
        ball_point_gate_disx = abs(opt.MY_DOOR_LEFT.x - ball.x)
        ball_point_gate_posx = math.copysign(abs(opt.MY_DOOR_LEFT.x) - keep_distance , opt.MY_DOOR_LEFT.x)
        ball_point_gate_posy = ball.y +  ball_point_gate_disx * ball.vy / abs(ball.vx + 0.0000001)
        if abs(ball_point_gate_posy) <= abs(opt.MY_DOOR_LEFT.y) :
            return True, opt.Pos(ball_point_gate_posx, ball_point_gate_posy)
    return False, None


def get_gate_keeper_position(me, ball, keep_distance):
    global switch_keeper_pos
    gate_center_pos = opt.Pos(
        math.copysign(abs(opt.MY_DOOR_LEFT.x) - 0  , opt.MY_DOOR_LEFT.x),
        0
    )
    # 球向着球门运动，检测目标是否在球门范围内
    is_ball_to_my_door, pos = is_ball_run_to_my_door(ball, keep_distance)

    if is_ball_to_my_door: 
        print(f"Goto Door Specific : ({pos.x}, {pos.y})")
        return pos

    # 来回跑
    if switch_keeper_pos == "CENTER" and get_distance_to(me, gate_center_pos.x, gate_center_pos.y, 0) < 2:
        switch_keeper_pos = "LEFT"
    if switch_keeper_pos == "LEFT" and get_distance_to(me, opt.MY_DOOR_LEFT.x, opt.MY_DOOR_LEFT.y, 0) < 6:
        switch_keeper_pos = "RIGHT"
    
    if switch_keeper_pos == "RIGHT" and get_distance_to(me, opt.MY_DOOR_RIGHT.x, opt.MY_DOOR_RIGHT.y, 0) < 6:
        switch_keeper_pos = "LEFT"
    
    if switch_keeper_pos == "LEFT" : 
        print(f"Goto Door Left")
        return opt.MY_DOOR_LEFT
    elif switch_keeper_pos == "RIGHT" :
        print(f"Goto Door Right")
        return opt.MY_DOOR_RIGHT
    elif switch_keeper_pos == "CENTER" :
        print(f"Goto Door Center")
        return gate_center_pos
    return gate_center_pos


def generate_keeper_hs(angle):
    abs_angle = abs(angle)
    if 0 <= abs_angle <= 1 :
        hs = 0
    elif 1 < abs_angle <= 10 :
        hs = 0.1
    elif 10 < abs_angle <= 20 :
        hs = 0.3
    elif 20 < abs_angle <= 30 :
        hs = 0.5
    elif 30 < abs_angle <= 90 :
        hs = 1
    elif 90 < abs_angle <= 150 :
        hs = 1
    elif 150 < abs_angle <= 160 :
        hs = 0.5
    elif 160 < abs_angle <= 170 :
        hs = 0.3
    elif 170 < abs_angle <= 179 :
        hs = 0.1
    elif 179 < abs_angle <= 180 :
        hs = 0
    else :
        hs = 0
    if angle > 0:
        hs = -hs
    return hs

def generate_keeper_vs(hs, distance, angle):
    abs_hs = abs(hs)
    if 0 <= abs_hs <= 0.1 :
        vs = 1
    elif 0.1 < abs_hs <= 0.3 :
        vs = 1
    elif 0.3 < abs_hs <= 0.5 :
        vs = 0.7
    elif 0.5 < abs_hs <= 1 :
        vs = 0.4
    else :
        vs = 1
    
    if abs(angle) > 90:
        vs = -vs
    return vs

def keeper_to_pos(tank, posx, posy, keep_distance) :
    angle = get_angle_to(tank, posx, posy)
    print(f"angle = {angle}")
    distance = get_distance_to(tank, posx, posy, keep_distance)
    print(f"distance = {distance}")
    hs = generate_keeper_hs(angle)
    vs = generate_keeper_vs(hs, distance, angle)
    return vs, hs

def get_vshs_door_keeper(me, ball, tankname):
    print(f"----get_vshs_door_keeper----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    print(f"distance_to_ball = {distance_to_ball}")

    to_pos = get_gate_keeper_position(me, ball, 0)
    posx, posy = to_pos.x, to_pos.y
    print(f"to_pos = ({to_pos.x} , {to_pos.y})")
    
    vs, hs = keeper_to_pos(me, posx, posy, 0)
    
    # 防止卡住
    vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)

    return vs, hs

def door_keeper(me, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = get_vshs_door_keeper(me, ball, tankname)

    # 守门员开局开炮
    if abs(me.y) < 0.25:
        vs, hs = check_for_fire(vs, hs, me, ball)

    return vs, hs

"""
占位队员
"""

def get_position_in_horizontal_line(x, ly, minx, maxx):
    x = max(min(x, maxx), minx)
    y = ly
    return opt.Pos(x, y)

def get_position_in_second(ball, second):
    x = ball.x + ball.vx * second
    y = ball.y + ball.vy * second
    return opt.Pos(x, y)

def get_position_in_front_center_line(me, ball, ly = 0):
    print(f"get_position_in_front_center_line")
    exact_pos = True
    x = ball.x
    y = ball.y

    distance_to_enemydoor = 1.8
    distance_to_position = 10

    dist_x = abs(opt.ENEMY_DOOR_LEFT.x - x)
    dist_y = abs(y)

    enemydoor_front_x = opt.ENEMY_DOOR_LEFT.x

    if dist_x >= distance_to_position:
        # 跑到门前准备位
        enemydoor_front_x = opt.ENEMY_DOOR_LEFT.x - math.copysign( 
            distance_to_position * opt.BALL_RADIUS, 
            opt.ENEMY_DOOR_LEFT.x
        )
        exact_pos = True
    elif dist_x < distance_to_position:
        # 门前冲球
        rate = max( dist_x / distance_to_position, dist_y / (opt.GROUND_HEIGHT/2) )
        dist_diff = math.copysign( 
            (distance_to_position - distance_to_enemydoor) * rate + distance_to_enemydoor,
            opt.ENEMY_DOOR_LEFT.x
        )
        enemydoor_front_x = opt.ENEMY_DOOR_LEFT.x - dist_diff
        
        ball_in_sec = get_distance_to_pos(ball, opt.Pos(enemydoor_front_x, ly), 0) / get_speed(ball)
        me_in_sec = get_distance_to_pos(me, opt.Pos(enemydoor_front_x, ly), 0) / get_speed(me)
        print(f"ball in sec: {ball_in_sec}, me in sec: {me_in_sec}")

        if abs(opt.ENEMY_DOOR_LEFT.x - ball.x) < 1.5 and ball_in_sec < me_in_sec :
            print(f"加速冲球")
            exact_pos = False
        else :
            exact_pos = True
        
    lminx = min(0, enemydoor_front_x)
    lmaxx = max(0, enemydoor_front_x)

    # 与球保持水平
    # 需要提前或者落后，在此处调整
    pos = get_position_in_horizontal_line(x, ly, lminx, lmaxx)

    # 球往回滚, 球往中线滚
    if ball.vx * opt.ENEMY_DOOR_LEFT.x < 0 \
        and ball.vy * ball.y < 0 \
        : 
        pos_temp = get_position_in_second(ball, abs((ball.y-ly)/(ball.vy + 0.000001)))
        pos = opt.Pos(
                pos_temp.x - math.copysign(1.5 * opt.BALL_RADIUS, opt.ENEMY_DOOR_LEFT.x),
                pos_temp.y
            )
        exact_pos = True # 即使反弹，球还会在前方，False 会导致冲太快

    return pos, exact_pos

def is_sprite_in_area(tank, left, right, top, bottom):
    if left <= tank.x <= right and bottom <= tank.y <= top:
        return True
    else:
        return False

def get_enemy_tanks_at_mydoor(me):
    closest_tank = None
    closest_distance = 255
    for tank in opt.enemy_tanks():
        left = min(
                math.copysign(abs(opt.MY_DOOR_LEFT.x) - opt.TANK_WIDTH * 1.5, opt.MY_DOOR_LEFT.x), 
                math.copysign(abs(opt.MY_DOOR_LEFT.x) - 40, opt.MY_DOOR_LEFT.x)
            )
        right = max(
                math.copysign(abs(opt.MY_DOOR_LEFT.x) - opt.TANK_WIDTH * 1.5, opt.MY_DOOR_LEFT.x), 
                math.copysign(abs(opt.MY_DOOR_LEFT.x) - 40, opt.MY_DOOR_LEFT.x)
            )
        top = 23
        bottom = -23 
        if tank.is_enemy() and is_sprite_in_area(tank, left, right, top, bottom):
            distance = get_distance_to(tank, opt.MY_DOOR_LEFT.x, 0, 0)
            if distance < closest_distance :
                closest_tank = tank
                closest_distance = distance
    
    return closest_tank

def get_position_in_back_side_line(me, ball, ly = 12):
    print(f"get_position_in_back_side_line")
    exact_pos = True
    distance_to_mydoor = 40
    if ball.y < 0:
        ly = -ly
    
    ball_pos = get_position_in_second(ball, 1)
    x = ball_pos.x
    # 考虑惯性可以多加几个 防守来挡人
    mydoor_side_x = opt.MY_DOOR_LEFT.x - math.copysign( 
        distance_to_mydoor * opt.BALL_RADIUS, opt.MY_DOOR_LEFT.x)
    lminx = min(0, mydoor_side_x)
    lmaxx = max(0, mydoor_side_x)

    # 与球保持水平
    # 需要提前或者落后，在此处调整
    pos = get_position_in_horizontal_line(x, ly, lminx, lmaxx)

    in_sec = 0.5 * get_distance_to_pos(me, ball, 0) / get_speed(ball)
    ball_next_pos = get_position_in_second(ball, in_sec)
    print(f"back_side_line: ball_next_pos : ({ball_next_pos.x}, {ball_next_pos.y})")
    if ( # 如果球到底线，我在底线，
        abs(ball_next_pos.x - opt.MY_DOOR_LEFT.x) <= (distance_to_mydoor * opt.BALL_RADIUS) 
        and abs(me.x - opt.MY_DOOR_LEFT.x) <= ((distance_to_mydoor + 4) * opt.BALL_RADIUS) 
    ) :
        print(f"back_side_line: ball at bottom line")
        # 如果有敌方在门口，改成撞击敌方坦克
        enemy_tank = get_enemy_tanks_at_mydoor(me)
        if enemy_tank != None:
            print(f"back_side_line: hit tank at the door : ({enemy_tank.x}, {enemy_tank.y})")
            pos = get_position_in_second(enemy_tank, 0.2)
            exact_pos = False
        elif ( # 我在球与门柱之间
            me.y * ball_next_pos.y >= 0 and abs(opt.MY_DOOR_LEFT.y) < abs(me.y) < abs(ball_next_pos.y)
        ) :
            print(f"back_side_line: hit ball close to door : ({ball_next_pos.x}, {ball_next_pos.y})")
            pos = ball_next_pos
            exact_pos = False #冲击

    return pos, exact_pos

def get_vshs_line_keeper(me, ball, att_ly, def_ly, tankname):
    print(f"----get_vshs_keeper----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    print(f"distance_to_ball = {distance_to_ball}, att_ly = {att_ly}, def_ly = {def_ly}")
    
    # 默认跑向中心
    to_pos = opt.Pos( 0, 0 ) 
    center_position = opt.Pos(0, 0)
    exact_pos = True

    # 移动

    # 前场中心线进攻线
    # 后场防御线
    if is_run_toward_selectside(ball, "ENEMY", 20):
        to_pos, exact_pos = get_position_in_front_center_line(me, ball, att_ly)
    elif is_run_toward_selectside(ball, "MY", 20):
        to_pos, exact_pos = get_position_in_back_side_line(me, ball, def_ly)
    elif is_in_selectside(ball, "ENEMY"):
        to_pos, exact_pos = get_position_in_front_center_line(me, ball, att_ly)
    elif is_in_selectside(ball, "MY"):
        to_pos, exact_pos = get_position_in_back_side_line(me, ball, def_ly)

    print(f"keeper: to_pos = ({to_pos.x} , {to_pos.y})")

    if exact_pos:   
        vs, hs = get_vshs_run_to_pos_exact(me, to_pos.x, to_pos.y, 0, tankname) # 修改减速可以停到位子
    else :
        vs, hs = get_vshs_run_to_pos(me, to_pos.x, to_pos.y, 0, tankname)

    vs, hs = get_vshs_not_push_to_my_door(vs, hs, me, ball, tankname)

    if (
            get_distance_to_pos(me, to_pos, 0) > (4 * opt.BALL_RADIUS) 
            and get_distance_to_pos(me, center_position, 0) > (10 * opt.BALL_RADIUS)
    ):
        # 目标位置，中场位置以外
        vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)
    
    return vs, hs

def is_push_to_mydoor(me, ball, tankname):
    global no_push_to_mydoor_count
    no_push_to_mydoor_duration = -30
    print(f"no_push_to_mydoor_count[{tankname}] = {no_push_to_mydoor_count[tankname]}")
    if no_push_to_mydoor_count[tankname] < 0 : # 卡住中，倒计时
        no_push_to_mydoor_count[tankname] = no_push_to_mydoor_count[tankname] + 1
        return True
    else:
        if (
            get_distance_to_pos(me, ball, 0) <= 6 * opt.BALL_RADIUS # 我在球的一定范围内, 
            and abs(me.y) < 11 and abs(me.x) <= 50 # 坦克在门前
            and abs(ball.x - opt.MY_DOOR_LEFT.x) <= 1.2 * opt.BALL_RADIUS # 球在我方底线，
            and (ball.vy * ball.y < 0 or abs(ball.y) < 9) # 朝着门在运动，或在门口
        ) : 
            no_push_to_mydoor_count[tankname] = no_push_to_mydoor_count[tankname] + 1 
        else:
            no_push_to_mydoor_count[tankname] = 0
    if no_push_to_mydoor_count[tankname] >= 5: # 卡住了
        no_push_to_mydoor_count[tankname] = no_push_to_mydoor_duration
        return True
    return False


def get_vshs_not_push_to_my_door(vs, hs, me, ball, tankname):
    if is_push_to_mydoor(me, ball, tankname):
        print(f"后退防止球被撞入自家球门")
        
        # 直接往门里倒车
        if run_direct[tankname] == 1:
            vs, hs = -1, math.copysign(0.7, get_angle_to(me, opt.MY_DOOR_LEFT.x, 0))
        elif run_direct[tankname] == -1:
            vs, hs = 1, math.copysign(0.7, get_angle_to(me, opt.MY_DOOR_LEFT.x, 0))

    return vs, hs

def line_keeper(me, target, att_ly, def_ly,  tankname):
    print(f"{tankname} is line keeper")
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = get_vshs_line_keeper(me, ball, att_ly, def_ly, tankname)

    vs, hs = check_for_fire(vs, hs, me, ball)

    return vs, hs

"""
攻击队员
"""

def get_closest_enemy_tank(sprite):
    closest_tank = None
    closest_distance = 255
    for tank in opt.enemy_tanks():
        if tank.is_enemy():
            distance = get_distance_to_pos(sprite, tank, 0)
            if distance < closest_distance :
                closest_tank = tank
                closest_distance = distance
    return closest_tank, closest_distance


def attack_move(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    center_position = opt.Pos(0, 0)
    # run and push the ball to the enemy gate

    # 获取车球的指向
    pos = get_s2s_to_pos_onside(me, ball, 0)
    # vs, hs = get_vshs_run(me, ball, target, tankname)
    dist_pos = get_distance_to_pos(me, ball, 0)
    # angle_pos = get_angle_to_pos(me, ball)

    safe_distance = 10 * opt.TANK_LENGTH
    enemy_tank, etanktome = get_closest_enemy_tank(me)
    enemy_tank, etanktoball = get_closest_enemy_tank(ball)
    if  etanktome >= safe_distance and etanktoball >= safe_distance :
        # 一定范围内，没有敌人
        # 采用get_vshs_shot
        vs, hs = get_vshs_shot(me, ball, target, False, tankname)

    elif (
            (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 20) # 面前 
            and (opt.MY_DOOR_LEFT.x-1 <= pos.x <= opt.MY_DOOR_LEFT.x+1) and (abs(pos.y) <= 8) # 推球在家门范围
            and (dist_pos <= (opt.BALL.radius + opt.TANK.length * 3.5)) # 3.5车身距离
            and is_in_selectside(me, "MY") # 自己半场
    ) :
        # 如果把球对推向自己的门, 采用get_vshs_shot
        vs, hs = get_vshs_shot(me, ball, target, False, tankname)
    elif (
            (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 20) # 面前
            and (opt.ENEMY_DOOR_LEFT.x-1 <= pos.x <= opt.ENEMY_DOOR_LEFT.x+1) and (8 < abs(pos.y) <= 18) # 推球在门范围外
            and (dist_pos <= (opt.BALL.radius + opt.TANK.length * 3.5)) # 3.5车身距离
            and is_in_selectside(me, "ENEMY") # 对方半场
    ):
        # 如果把球对推向自己的门, 采用get_vshs_shot
        vs, hs = get_vshs_shot(me, ball, target, False, tankname)
    else:
        vs, hs = get_vshs_run(me, ball, target, False, 0, tankname) 

    vs, hs = get_vshs_not_push_to_my_door(vs, hs, me, ball, tankname)

    # 防止卡住
    if get_distance_to_pos(me, center_position, 0) > (10 * opt.BALL_RADIUS): 
        #中场位置以外
        vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)

    return vs, hs

def attack(me, target, tankname):
    print(f"{tankname} is attack")
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = attack_move(me, target, tankname)

    vs, hs = check_for_fire(vs, hs, me, ball)
    
    return vs, hs

"""
门前，后场防守型队员
"""

def defence_move(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    my_position = opt.Pos(math.copysign(abs(opt.MY_DOOR_RIGHT.x) - 1.2 * opt.TANK_LENGTH, opt.MY_DOOR_RIGHT.x), 0)
    center_position = opt.Pos(0, 0)
    # run and push the ball to the enemy gate

    # 获取车球的指向
    # pos = get_s2s_to_pos_onside(me, ball, 0)
    # vs, hs = get_vshs_run(me, ball, target, tankname)
    # dist_pos = get_distance_to_pos(me, ball, 0)
    # angle_pos = get_angle_to_pos(me, ball)

    if is_run_toward_selectside(ball, "MY", 15) \
        or (is_in_selectside(ball, "MY") and not is_run_toward_selectside(ball, "ENEMY", 20))\
        : # 球快速朝向我方，球在我方场地，没有朝向对方场地
        in_sec = 0.5 * get_distance_to_pos(me, ball, 1) / get_speed(ball)
        vs, hs = get_vshs_run(me, ball, target, False, in_sec, tankname) 
    else:
        # 跑到门口守门员位子
        vs, hs = get_vshs_shot(me, my_position, target, True, tankname)

    vs, hs = get_vshs_not_push_to_my_door(vs, hs, me, ball, tankname)

    enemytank, enemytank_dist = get_closest_enemy_tank(me)
    ball_dist = get_distance_to_pos(me, ball, 0)
    if get_distance_to_pos(me, my_position, 0) <= ((opt.DOOR_WIDTH - opt.TANK_LENGTH) / 2): # 守门位子
        None
    else :
        if (( abs(me.x) < (50-opt.TANK_LENGTH) and abs(me.x - opt.MY_DOOR_LEFT.x) < 50 and abs(me.y - 0) < 22 ) # 禁区
           or (get_distance_to_pos(me, center_position, 0) < (10 * opt.BALL_RADIUS)) # 中场位子
        ) : 
            if (enemytank_dist > 40) or (ball_dist > 40) : # 没有敌人，或没有球。
                vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)
        else :
            vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)

    return vs, hs

def defence(me, target, tankname):
    print(f"{tankname} is defence")
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = defence_move(me, target, tankname)

    vs, hs = check_for_fire(vs, hs, me, ball)
    
    return vs, hs

## ===================================================================================================

# 控制你的 1 号机器人
def tank1_update():
    tankname = "tank1"

    print_start(tankname)

    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    
    print_status(me, ball, tankname)

    #======== begin ==============================
    
    vs, hs = attack(me, target, tankname)
   
    #======== end ================================

    print_end(me, vs, hs, tankname)

    return vs, hs


# 控制你的 2 号机器人
def tank2_update():
    tankname = "tank2"
    print_start(tankname)

    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    
    print_status(me, ball, tankname)
    
    vs, hs = line_keeper(me, ball, 0, 12, tankname)
    
    print_end(me, vs, hs, tankname)

    return vs, hs


# 控制你球门的3号机器人
def tank3_update():
    tankname = "tank3"
    print_start(tankname)
    
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    
    print_status(me, ball, tankname)

    vs, hs = defence(me, target, tankname)    

    print_end(me, vs, hs, tankname)
    
    return vs, hs
