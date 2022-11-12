import opt
import math

# 变量定义
glb_env_var = {'totaltime': 180}
stuck_count = {"tank1": 0, "tank2": 0, "tank3": 0, "tank4": 0, "tank5": 0}
run_direct = {"tank1": 1, "tank2": 1, "tank3": 1, "tank4": 1, "tank5": 1}


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

# last_pos = opt.Pos(255, 255)
def get_speed(sprite):
    """ 
    利用物体的vx，vy，计算v的量
    两直角边计算斜边
    """
    return math.sqrt(sprite.vx ** 2 + sprite.vy ** 2)


def is_stuck(me, speed, tankname):
    global stuck_count
    stuck_duration = -30
    if me.is_stuck(speed): # 卡住了 系统函数
        stuck_count[tankname] = stuck_duration
        return True
    if stuck_count[tankname] < 0 : # 卡住中，倒计时
        stuck_count[tankname] = stuck_count[tankname] + 1
        return True
    else:
        if get_speed(me) < speed: # 卡了 ， 连续卡 20帧，就是卡住了
            stuck_count[tankname] = stuck_count[tankname] + 1 
        elif get_speed(me) >= 2 : # 有点动了
            stuck_count[tankname] = 0
    if stuck_count[tankname] >= 20: # 卡住了
        stuck_count[tankname] = stuck_duration
        return True
    return False


def get_line_direct_to_pos_onside(k, b, direct):
    print(f"k = {k}, b = {b}, direct = {direct}")
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
            pos = opt.Pos(sp2.x, 25)
        elif (sp2.x - sp1.x) < 0:
            pos = opt.Pos(sp2.x, -25)
        if rebound == 1:
            pos = None
   
    elif (sp2.x - sp1.x) == 0: 
        # 垂直线，不可使用上面公式
        if (sp2.y - sp1.y) > 0:
            pos = opt.Pos(sp2.x, 25)
        elif (sp2.y - sp1.y) < 0:
            pos = opt.Pos(sp2.x, -25)
        if rebound == 1:
            pos = None

    if pos is None:
        print(f"get_s2s_to_pos_onside: pos = None")
    else :
        print(f"get_s2s_to_pos_onside: x={pos.x}, y={pos.y}")
    return pos

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

def get_distance_to_pos(sprite, pos, keep_distance):
    return get_distance_to(sprite, pos.x, pos.y, keep_distance)

def get_distance_to(sprite, posx, posy, keep_distance):
    distance = sprite.distance_to(posx, posy) - keep_distance   
    return distance

def is_ball_run_to_my_door(ball, keep_distance):
    if ball.vx * opt.MY_DOOR_LEFT.x > 0:
        ball_point_gate_disx = abs(opt.MY_DOOR_LEFT.x - ball.x)
        ball_point_gate_posx = math.copysign(abs(opt.MY_DOOR_LEFT.x) - keep_distance , opt.MY_DOOR_LEFT.x)
        ball_point_gate_posy = ball.y +  ball_point_gate_disx * ball.vy / abs(ball.vx)
        if abs(ball_point_gate_posy) <= abs(opt.MY_DOOR_LEFT.y) :
            return True, opt.Pos(ball_point_gate_posx, ball_point_gate_posy)
    return False, None

switch_keeper_pos = "CENTER"
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

    # if ball.vx * opt.MY_DOOR_LEFT.x > 0:
    #     ball_point_gate_disx = abs(opt.MY_DOOR_LEFT.x - ball.x)
    #     ball_point_gate_posx = math.copysign(abs(opt.MY_DOOR_LEFT.x) - keep_distance , opt.MY_DOOR_LEFT.x)
    #     ball_point_gate_posy = ball.y +  ball_point_gate_disx * ball.vy / abs(ball.vx)
    #     if abs(ball_point_gate_posy) <= abs(opt.MY_DOOR_LEFT.y) :
    #         print(f"Goto Door Specific : ({ball_point_gate_posx}, {ball_point_gate_posy})")
    #         return opt.Pos(ball_point_gate_posx, ball_point_gate_posy)

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

def get_position_face_target_keep_distance(src_sprite, target_pos, keep_distance):
    distance_to_target = src_sprite.distance_to(target_pos.x, target_pos.y)
    posx = src_sprite.x - keep_distance * (target_pos.x - src_sprite.x) / distance_to_target
    posy = src_sprite.y - keep_distance * (target_pos.y - src_sprite.y) / distance_to_target
    return opt.Pos(posx, posy)

def get_position_beside(me, target_pos, keep_distance):
    # 要跑过头
    if opt.ENEMY_DOOR_RIGHT.x > 0:
        posx = target_pos.x - 5
    else:
        posx = target_pos.x + 5
    #
    if target_pos.y > me.y :
        posy = target_pos.y - keep_distance 
    else:
        posy = target_pos.y + keep_distance
    return opt.Pos(posx, posy)

def get_position(me, src_sprite, target_pos, keep_distance):
    if target_pos == None:
        pos = get_position_beside(me, src_sprite, keep_distance)
    elif target_pos != None:     
        pos = get_position_face_target_keep_distance(src_sprite, target_pos, keep_distance)
    else:
        pos = src_sprite

    pos = opt.Pos(max(min(pos.x, 50),-50), max(min(pos.y, 25),-25)) # 不能超出范围
    return pos

def generate_hs(angle, rundirect):
    if rundirect == 1:
        abs_angle = abs(angle)
    elif rundirect == -1:
        abs_angle = 180 - abs(angle)
    else:
        print(f"Error: 错误的 run direct")

    if 0 <= abs_angle <= 1 :
        hs = 0
    elif 1 < abs_angle <= 10 :
        hs = -0.1
    elif 10 < abs_angle <= 20 :
        hs = -0.3
    elif 20 < abs_angle <= 30 :
        hs = -0.5
    elif 30 < abs_angle :
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
        vs = 0.7
    elif 0.5 < abs_hs <= 1 :
        vs = 0.5
    else :
        vs = 1

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


def get_vshs_run_to_pos(tank, posx, posy, keep_distance, tankname):
    global run_direct

    angle = get_angle_to(tank, posx, posy)
    print(f" = {angle}")
    distance = get_distance_to(tank, posx, posy, keep_distance)
    print(f"distance = {distance}")

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

    angle = get_angle_to(tank, posx, posy)
    print(f" = {angle}")
    distance = get_distance_to(tank, posx, posy, keep_distance)
    print(f"distance = {distance}")

    hs = generate_hs(angle, run_direct[tankname])
    vs, hs = generate_vs(hs, distance, angle, run_direct[tankname])
    
    return vs, hs

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
    if angle < 0:
        hs = -hs
    return hs

def generate_keeper_vs(hs, distance, angle):
    abs_hs = abs(hs)
    if 0 <= abs_hs <= 0.1 :
        vs = 1
    elif 0.1 < abs_hs <= 0.3 :
        vs = 1
    elif 0.3 < abs_hs <= 0.5 :
        vs = 1
    elif 0.5 < abs_hs <= 1 :
        vs = 1
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

def tank_fire(tank):
    print(f"冷却时间 = {tank.cool_remain}")
    if tank.cool_remain == 0:
        tank.do_fire()
        print(f"开火")
        return True
    else: 
        print(f"缺弹药")
    return False

def get_vshs_response_to_stuck(vs, hs, me, tankname):
    global run_direct
    if is_stuck(me, 1, tankname) : # is_stuck 的倒计时机制（30帧，一秒80帧），可以保证倒退一定时间
        if run_direct[tankname] == 1:
            vs, hs = -1, 0
        elif run_direct[tankname] == -1:
            vs, hs = 1, 0
    return vs, hs

def get_vshs_shot(me, ball, target, tankname):
    """

    """
    print(f"----get_vshs_shot----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    print(f"target = ({target.x}, {target.y})")
    angle_target_ball_me = get_angle_in(ball.x, ball.y, target.x, target.y, me.x, me.y)
    print(f"distance_to_ball = {distance_to_ball}")
    print(f"angle_target_ball_me = {angle_target_ball_me}")
    angle_optarget_ball_me = 180 - abs(angle_target_ball_me)
    print(f"angle_optarget_ball_me = {angle_optarget_ball_me}")
    keep_distance = 15 * opt.BALL_RADIUS 
    if 0 <= angle_optarget_ball_me < 90 :
        print(f"Run to ball opp pos to target")
        keep_distance = keep_distance * math.sin(opt.a2r(angle_optarget_ball_me))
        to_pos = get_position(me, ball, target, keep_distance)
    elif 90 <= angle_optarget_ball_me <= 180 :
        print(f"Run to ball side to behind")
        keep_distance = 4 * opt.BALL_RADIUS
        to_pos = get_position(me, ball, None, keep_distance)
    else :
        print(f"Error Case")
        keep_distance = keep_distance
        to_pos = get_position(me, ball, target, keep_distance)
    
    print(f"keep_distance = {keep_distance}")
 
    posx, posy = to_pos.x, to_pos.y
    print(f"to_pos = ({to_pos.x} , {to_pos.y})")

    # 跑向目标点
    vs, hs = get_vshs_run_to_pos(me, posx, posy, 0, tankname)
    
    vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)
    
    return vs, hs

def get_vshs_run(me, ball, target, tankname):
    print(f"----get_vshs_run----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    angle_target_ball_me = get_angle_in(ball.x, ball.y, target.x, target.y, me.x, me.y)
    print(f"distance_to_ball = {distance_to_ball}")
    print(f"angle_target_ball_me = {angle_target_ball_me}")
    angle_optarget_ball_me = 180 - abs(angle_target_ball_me)
    print(f"angle_optarget_ball_me = {angle_optarget_ball_me}")
    
    keep_distance = 1 * opt.BALL_RADIUS 
    
    if 0 <= angle_optarget_ball_me < 90 :
        print(f"Run to ball opp pos to target")
        keep_distance = keep_distance
        to_pos = get_position(me, ball, target, keep_distance)
    elif 90 <= angle_optarget_ball_me <= 180 :
        print(f"Run to ball side to behind")
        keep_distance = 0 * opt.BALL_RADIUS
        to_pos = get_position(me, ball, None, keep_distance)
    else :
        print(f"Error Case")
        keep_distance = keep_distance
        to_pos = get_position(me, ball, target, keep_distance)
    
    print(f"keep_distance = {keep_distance}")
 
    posx, posy = to_pos.x, to_pos.y
    print(f"to_pos = ({to_pos.x} , {to_pos.y})")

    # 跑向目标点
    vs, hs = get_vshs_run_to_pos(me, posx, posy, 0, tankname)

    # 控球情况下，往门里带球
    pos = opt.Pos(posx, posy)
    vs, hs = get_vshs_adjust_to_target(me, pos, target, vs, hs, tankname)
    
    vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)

    return vs, hs

def get_vshs_keeper1(me, ball, tankname):
    print(f"----get_vshs_keeper----")
    distance_to_ball = get_distance_to(me, ball.x, ball.y, 0)
    print(f"distance_to_ball = {distance_to_ball}")
    
    # 默认跑向中心
    pos = opt.Pos( 0, 0 ) 

    # 移动

    # 前场中心线进攻线
    if is_run_toward_selectside(ball, "ENEMY", 20):
        pos = get_position_in_front_center_line(ball)
    elif is_run_toward_selectside(ball, "MY", 20):
        pos = get_position_in_back_side_line(ball)
    elif is_in_selectside(ball, "ENEMY"):
        pos = get_position_in_front_center_line(ball)
    elif is_in_selectside(ball, "MY"):
        pos = get_position_in_back_side_line(ball)

    # 后场防御线

    vs, hs = get_vshs_run_to_pos_exact(me, pos.x, pos.y, 0, tankname) # 修改减速可以停到位子
   
    if get_distance_to_pos(me, pos, 0) < (5 * opt.BALL_RADIUS):
        vs, hs = get_vshs_response_to_stuck(vs, hs, me, tankname)
    
    return vs, hs


def get_position_in_horizontal_line(x, ly, minx, maxx):
    x = max(min(x, maxx), minx)
    y = ly
    return opt.Pos(x, y)


def get_position_in_front_center_line(ball):
    ly = 0
    x = ball.x

    distance_to_enemydoor = 2

    # 考虑惯性可以多加几个, 进攻来挡球
    enemydoor_front_x = opt.ENEMY_DOOR_LEFT.x - math.copysign( distance_to_enemydoor * opt.BALL_RADIUS, opt.ENEMY_DOOR_LEFT.x)
    lminx = min(0, enemydoor_front_x)
    lmaxx = max(0, enemydoor_front_x)

    # 与球保持水平
    # 需要提前或者落后，在此处调整
    pos = get_position_in_horizontal_line(x, ly, lminx, lmaxx)

    return pos

def get_position_in_back_side_line(ball):
    ly = 12
    distance_to_mydoor = 3
    if ball.y < 0:
        ly = -ly
    
    x = ball.x
    # 考虑惯性可以多加几个 防守来挡人
    mydoor_side_x = opt.MY_DOOR_LEFT.x - math.copysign( distance_to_mydoor * opt.BALL_RADIUS, opt.MY_DOOR_LEFT.x)
    lminx = min(0, mydoor_side_x)
    lmaxx = max(0, mydoor_side_x)

    # 与球保持水平
    # 需要提前或者落后，在此处调整
    pos = get_position_in_horizontal_line(x, ly, lminx, lmaxx)

    return pos

def keeper1(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = get_vshs_keeper1(me, ball, tankname)

    # 守门员开局开炮
    if abs(me.y) < 0.25:
        vs, hs = check_for_fire(vs, hs, me, ball)

    return vs, hs

def keeper2(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
  
    vs, hs = attack_move(me, target, tankname)

    #守门员开局开炮
    if abs(me.y) < 0.25:
        vs, hs = check_for_fire(vs, hs, me, ball)

    return vs, hs


def attack_move(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
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
        vs, hs = get_vshs_shot(me, ball, target, tankname)

    elif (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 1) \
        and (opt.MY_DOOR_LEFT.x-1 <= pos.x <= opt.MY_DOOR_LEFT.x+1) \
        and (abs(pos.y) <= 8) \
        and (dist_pos <= (opt.BALL.radius + opt.TANK.length * 3.5)) \
        and is_in_selectside(me, "MY") \
        :
        # 对准 # 朝家门 # 在家门范围  # 1.5车身距离 # 自己半场
        # 如果把球对推向自己的门, 采用get_vshs_shot
        vs, hs = get_vshs_shot(me, ball, target, tankname)
    elif (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 1) \
        and (opt.ENEMY_DOOR_LEFT.x-1 <= pos.x <= opt.ENEMY_DOOR_LEFT.x+1) \
        and (18 >= abs(pos.y) > 8) \
        and (dist_pos <= (opt.BALL.radius + opt.TANK.length * 3.5)) \
        and is_in_selectside(me, "ENEMY") \
        :
        # 对准 # 朝敌门 # 在门范围外  # 1车身距离 # 对方半场
        # 如果把球对推向自己的门, 采用get_vshs_shot
        vs, hs = get_vshs_shot(me, ball, target, tankname)
    else:
        vs, hs = get_vshs_run(me, ball, target, tankname) 

    return vs, hs


# tank_status = "RUN"
def attack(me, target, tankname):
    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)

    vs, hs = attack_move(me, target, tankname)

    vs, hs = check_for_fire(vs, hs, me, ball)
    
    return vs, hs

def check_for_fire(vs, hs, me, ball):
    pos = get_s2s_to_pos_onside(me, ball, 0)
    if (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 1) \
        and (opt.ENEMY_DOOR_LEFT.x-1 <= pos.x <= opt.ENEMY_DOOR_LEFT.x+1) \
        and (-8 <= pos.y <= 8) \
        :
        if tank_fire(me):
            vs, hs = 0, 0
    
    if (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 1) \
        and (opt.MY_DOOR_LEFT.x-1 <= pos.x <= opt.MY_DOOR_LEFT.x+1) \
        and (abs(pos.y) <= 25) \
        :
        # 面对自己门不能开折射跑
        None
    elif (0 <= abs(get_angle_to(me, ball.x, ball.y)) <= 1) \
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

def print_start(tankname):
    global glb_env_var
    print(f"----{tankname}---- 秒 = {glb_env_var['totaltime'] - opt.time_step()/80} -----------")


def print_status(me, ball, tankname):
    print(f"{tankname} 的位置 x={me.x}, y={me.y}, 速度 x={me.vx}, y={me.vy} r={opt.r2a(me.vr)}")
    print(f"{tankname} 的卡住情况 = {is_stuck(me, 0.3, tankname)} {me.is_stuck(0.3)}")
    print(f"Ball 的位置 x={ball.x}, y={ball.y}; 球的角度 = {ball.angle}; 球的速度 x={ball.vx}, y={ball.vy}")
    

def print_end(me, vs, hs, tankname):
    global run_direct
    # if get_speed(me) < 0.3: print(f"{tankname}速度慢了")
    print(f"<<<<<< {tankname}输出了 vs={vs}, hs={hs}, 行驶方向={run_direct[tankname]}=======")


# 控制你的 1 号机器人
def tank1_update():
    tankname = "tank1"

    print_start(tankname)

    me = opt.TANK
    ball = opt.BALL
    target = opt.Pos(opt.ENEMY_DOOR_RIGHT.x, opt.ENEMY_DOOR_RIGHT.y * 0)
    
    print_status(me, ball, tankname)
    
    vs, hs = attack(me, target, tankname)
   
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
    
    vs, hs = attack(me, target, tankname)
    
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
    
    vs, hs = keeper1(me, ball, tankname)
    # vs, hs = keeper2(me, target, tankname)
    
    print_end(me, vs, hs, tankname)
    
    return vs, hs

