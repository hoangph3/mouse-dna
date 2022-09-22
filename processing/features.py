from collections import defaultdict
import numpy as np
import math

from keeper.environments import SystemEnv
from . import stats


def stats_action_feature(action_data, n_from, n_to, action_type):

    x = []
    y = []
    t = []
    for item in action_data:
        x.append(item['x'])
        y.append(item['y'])
        t.append(item['t'])

    _dt = 0.01
    n = len(x)
    if n < SystemEnv.MIN_ACTION_LENGTH:
        return {}

    # ensure data type
    x = list(map(int, x))
    y = list(map(int, y))
    t = list(map(float, t))

    for i in range(1, n):
        if x[i] > SystemEnv.X_MAX or y[i] > SystemEnv.Y_MAX:
            x[i] = x[i - 1]
            y[i] = y[i - 1]
        if x[i] < SystemEnv.X_MIN or y[i] < SystemEnv.Y_MIN:
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
        "traveled_distance": trajectory,
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
    data_fields = ["action_type", "traveled_distance", "elapsed_time", "direction"]
    feature = {k: v for k, v in feature.items() if k in data_fields}

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
    for key, (min_theta, max_theta) in directions.items():
        if min_theta < theta < max_theta:
            return int(key)
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


def min_max_scaler(x):
    x = np.array(x)
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x.tolist()


def max_scaler(x):
    x = np.array(x)
    if np.max(x):
        x = x / np.max(x)
        return x.tolist()
    return x.tolist()


def stats_session_feature(session_data):
    """
    [
        {"action_type": 1, "traveled_distance": 100, "elapsed_time": 10, "direction": 5},
        {"action_type": 3, "traveled_distance": 200, "elapsed_time": 15, "direction": 3},
        ...
    ]
    """
    # Periodic sampling traveled_distance
    min_x = min(session_data, key=lambda x: x["traveled_distance"])["traveled_distance"]
    max_x = max(session_data, key=lambda x: x["traveled_distance"])["traveled_distance"]
    num_points = 12
    delta_x = (max_x - min_x) / (num_points - 1)
    TD = [min_x]
    for i in range(1, num_points):
        TD.append(delta_x + TD[i - 1])

    # Average movement speed compared with traveled distance (MSD): 1-100, 101-200, 201-300, ..., 901-1000
    MSD = defaultdict(lambda: defaultdict(list))
    for action_data in session_data:
        if action_data["traveled_distance"] < 1 or action_data["traveled_distance"] > 1000:
            continue
        idx = math.ceil(action_data["traveled_distance"] / 1000 * 10)
        MSD[str(idx)]["traveled_distance"].append(action_data["traveled_distance"])
        MSD[str(idx)]["elapsed_time"].append(action_data["elapsed_time"])
    for k in MSD:
        MSD[k]["average_speed"] = sum(MSD[k]["traveled_distance"]) / sum(MSD[k]["elapsed_time"]) if len(MSD[k]["elapsed_time"]) else 0
    MSD = [MSD[str(idx)]["average_speed"] if MSD[str(idx)]["average_speed"] else 0 for idx in range(1, 11)]

    # Average movement speed per movement direction (MDA): 1, 2, 3, 4, 5, 6, 7, 8
    MDA = defaultdict(lambda: defaultdict(list))
    for action_data in session_data:
        idx = action_data["direction"]
        MDA[str(idx)]["traveled_distance"].append(action_data["traveled_distance"])
        MDA[str(idx)]["elapsed_time"].append(action_data["elapsed_time"])
    for k in MDA:
        MDA[k]["average_speed"] = sum(MDA[k]["traveled_distance"]) / sum(MDA[k]["elapsed_time"]) if len(MDA[k]["elapsed_time"]) else 0
    MDA = [MDA[str(idx)]["average_speed"] if MDA[str(idx)]["average_speed"] else 0 for idx in range(1, 9)]

    # Movement Direction Histogram (MDH): 1, 2, 3, 4, 5, 6, 7, 8
    MDH = defaultdict(int)
    for action_data in session_data:
        idx = action_data["direction"]
        MDH[str(idx)] += 1
    MDH = [MDH[str(idx)] / len(session_data) if MDH[str(idx)] else 0 for idx in range(1, 9)]

    # Average movement speed per type of action (ATA): MM, PC, DD
    ATA = defaultdict(lambda: defaultdict(list))
    for action_data in session_data:
        idx = action_data["action_type"]
        ATA[str(idx)]["traveled_distance"].append(action_data["traveled_distance"])
        ATA[str(idx)]["elapsed_time"].append(action_data["elapsed_time"])
    for k in ATA:
        ATA[k]["average_speed"] = sum(ATA[k]["traveled_distance"]) / sum(ATA[k]["elapsed_time"]) if len(ATA[k]["elapsed_time"]) else 0
    ATA = [ATA[str(idx)]["average_speed"] if ATA[str(idx)]["average_speed"] else 0 for idx in [SystemEnv.MM_CODE, SystemEnv.PC_CODE, SystemEnv.DD_CODE]]

    # Action Type Histogram (ATH): MM, PC, DD
    ATH = defaultdict(int)
    for action_data in session_data:
        idx = action_data["action_type"]
        ATH[str(idx)] += 1
    ATH = [ATH[str(idx)] / len(session_data) if ATH[str(idx)] else 0 for idx in [SystemEnv.MM_CODE, SystemEnv.PC_CODE, SystemEnv.DD_CODE]]

    # Traveled Distance Histogram (TDH): 1-100, 101-200, 201-300, ..., 901-1000
    TDH = defaultdict(int)
    for action_data in session_data:
        if action_data["traveled_distance"] < 1 or action_data["traveled_distance"] > 1000:
            continue
        idx = math.ceil(action_data["traveled_distance"] / 1000 * 10)
        TDH[str(idx)] += 1
    TDH = [TDH[str(idx)] / len(session_data) if TDH[str(idx)] else 0 for idx in range(1, 11)]

    # Movement Elapsed Time Histogram (MTH): 0-0.5, 0.5-1.0, 1.0-1.5, ..., 4.5-5.0
    MTH = defaultdict(int)
    for action_data in session_data:
        idx = math.ceil(action_data["elapsed_time"] / 5 * 10)
        MTH[str(idx)] += 1
    MTH = [MTH[str(idx)] / len(session_data) if MTH[str(idx)] else 0 for idx in range(1, 11)]

    # Max normalize
    TD = max_scaler(TD)
    MSD = max_scaler(MSD)
    MDA = max_scaler(MDA)
    ATA = max_scaler(ATA)

    if SystemEnv.DEBUG:
        print("TD:", TD)
        print("MSD:", MSD)
        print("MDA:", MDA)
        print("MDH:", MDH)
        print("ATA:", ATA)
        print("ATH:", ATH)
        print("TDH:", TDH)
        print("MTH:", MTH)

    feature = np.concatenate([TD, MSD, MDA, MDH, ATA, ATH, TDH, MTH])
    return feature
