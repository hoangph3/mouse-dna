import numpy as np
import math

from keeper.environments import SystemEnv
from . import stats


def stats_action_feature(x, y, t, n_from, n_to, action_type):
    _dt = 0.01
    n = len(x)
    if n < SystemEnv.MIN_ACTION_LENGTH:
        return {}

    # ensure data type
    x = list(map(int, x))
    y = list(map(int, y))
    t = list(map(float, t))

    for i in range(1, n):
        if x[i] > SystemEnv.X_LIMIT or y[i] > SystemEnv.Y_LIMIT:
            x[i] = x[i - 1]
            y[i] = y[i - 1]

    # trajectory from the beginning point of the action
    trajectory = 0

    # angles
    angles = []
    path = []

    # velocities
    vx = []
    vy = []
    v = []
    for i in range(1, n):
        dx = x[i] - x[i - 1]
        dy = y[i] - y[i - 1]
        dt = (t[i] - t[i - 1]) or _dt
        vx_val = dx/dt
        vy_val = dy/dt
        vx.append(vx_val)
        vy.append(vy_val)
        v.append(math.sqrt(vx_val**2 + vy_val**2))
        angle = math.atan2(dy, dx)
        angles.append(angle)
        distance = math.sqrt(dx**2 + dy**2)
        trajectory = trajectory + distance
        path.append(trajectory)

    # sum of angles
    sum_of_angles = sum(angles)

    mean_vx = stats.__mean(vx)
    sd_vx = stats.__std(vx)
    max_vx = stats.__max(vx)
    min_vx = stats.__min(vx)

    mean_vy = stats.__mean(vy)
    sd_vy = stats.__std(vy)
    max_vy = stats.__max(vy)
    min_vy = stats.__min(vy)

    mean_v = stats.__mean(v)
    sd_v = stats.__std(v)
    max_v = stats.__max(v)
    min_v = stats.__min(v)

    # angular velocity
    omega = []
    for i in range(1, len(angles)):
        dtheta = angles[i] - angles[i - 1]
        dt = (t[i] - t[i - 1]) or _dt
        omega.append(dtheta/dt)

    mean_omega = stats.__mean(omega)
    sd_omega = stats.__std(omega)
    max_omega = stats.__max(omega)
    min_omega = stats.__min(omega)

    # acceleration
    a = []
    acc_time = 0
    cont = True
    for i in range(1, len(v)):
        dv = v[i] - v[i - 1]
        dt = (t[i] - t[i - 1]) or _dt
        if cont and dv > 0:
            acc_time += dt
        else:
            cont = False
        a.append(dv/dt)

    mean_a = stats.__mean(a)
    sd_a = stats.__std(a)
    max_a = stats.__max(a)
    min_a = stats.__min(a)

    # jerk
    j = []
    for i in range(1, len(a)):
        da = a[i] - a[i - 1]
        dt = (t[i] - t[i - 1]) or _dt
        j.append(da/dt)

    mean_jerk = stats.__mean(j)
    sd_jerk = stats.__std(j)
    max_jerk = stats.__max(j)
    min_jerk = stats.__min(j)

    # curvature
    c = []
    # number of critical points
    num_critical_points = 0
    for i in range(1, len(path)):
        dp = path[i] - path[i - 1]
        if dp == 0:
            continue
        dtheta = angles[i] - angles[i - 1]
        curve = dtheta/dp
        c.append(curve)
        if abs(curve) < SystemEnv.CURVE_THRESHOLD:
            num_critical_points = num_critical_points + 1
    mean_curve = stats.__mean(c)
    sd_curve = stats.__std(c)
    max_curve = stats.__max(c)
    min_curve = stats.__min(c)

    # time
    elapsed_time = t[n - 1] - t[0]

    # direction: -pi..pi
    theta = math.atan2(y[n - 1] - y[0], x[n - 1] - x[0])
    direction = __get_direction(theta)

    # distance end-to-end line
    dist_end_to_end_line = math.sqrt((x[0] - x[n-1])**2 + (y[0] - y[n-1])**2)

    # straightness
    if trajectory == 0:
        straightness = 0
    else:
        straightness = dist_end_to_end_line / trajectory
    if straightness > 1:
        straightness = 1

    # largest deviation
    largest_deviation = __get_largest_deviation(x, y)

    feature = {
        "mean_vx": mean_vx, "sd_vx": sd_vx, "max_vx": max_vx, "min_vx": min_vx,
        "mean_vy": mean_vy, "sd_vy": sd_vy, "max_vy": max_vy, "min_vy": min_vy,
        "mean_v": mean_v, "sd_v": sd_v, "max_v": max_v, "min_v": min_v,
        "mean_a": mean_a, "sd_a": sd_a, "max_a": max_a, "min_a": min_a,
        "mean_jerk": mean_jerk, "sd_jerk": sd_jerk, "max_jerk": max_jerk, "min_jerk": min_jerk,
        "mean_omega": mean_omega, "sd_omega": sd_omega, "max_omega": max_omega, "min_omega": min_omega,
        "mean_curve": mean_curve, "sd_curve": sd_curve, "max_curve": max_curve, "min_curve": min_curve,
        "action_type": action_type,
        "elapsed_time": elapsed_time,
        "trajectory_length": trajectory,
        "dist_end_to_end_line": dist_end_to_end_line,
        "direction": direction,
        "straightness": straightness,
        "num_points": n,
        "sum_of_angles": sum_of_angles,
        "largest_deviation": largest_deviation,
        "num_sharp_angles": num_critical_points,
        "a_beg_time": acc_time,
        "n_from": n_from,
        "n_to": n_to
    }
    return feature


def __get_direction(theta):
    direction = 0
    directions = {
        "0": [0, math.pi/4],
        "1": [math.pi * 1/4, math.pi * 1/2],
        "2": [math.pi * 1/2, math.pi * 3/4],
        "3": [math.pi * 3/4, math.pi],
        "4": [-math.pi, -math.pi * 3/4],
        "5": [-math.pi * 3/4, -math.pi/2],
        "6": [-math.pi/2, -math.pi/4],
        "7": [-math.pi/4, 0]
    }
    for direction, (min_theta, max_theta) in directions.items():
        if min_theta < theta < max_theta:
            return int(direction)
    return direction


def __get_largest_deviation(x, y):
    n = len(x)
    a = x[n - 1] - x[0]
    b = y[0] - y[n - 1]
    c = x[0]*y[n - 1] - x[n - 1]*y[0]
    d_max = 0
    den = math.sqrt(a**2 + b**2)
    for i in range(1, n-1): # not contain start_point (0), end_point (n)
        d = math.fabs(a*x[i] + b*y[i] + c)
        if d > d_max:
            d_max = d
    if den > 0:
        d_max /= den
    return d_max
