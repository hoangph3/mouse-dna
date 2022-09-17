import json

from keeper.environments import SystemEnv
from .features import stats_action_feature


def process_click_actions(data, action_file, n_from, n_to):
    # can be a compound action: {MM}*PC
    x = []
    y = []
    t = []
    prev_time = 0
    start = n_from
    counter = 0

    for item in data:
        counter += 1
        if item['state'] == 'Pressed':
            if len(t) > SystemEnv.MIN_ACTION_LENGTH:
                x.append(item['x'])
                y.append(item['y'])
                t.append(item['t'])
                feature = stats_action_feature(x, y, t, start, n_to, SystemEnv.PC_CODE)
                action_file.write("{}\n".format(json.dumps(feature)))
            return
        else:
            if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
                stop = n_from + counter - 2
                if len(t) > SystemEnv.MIN_ACTION_LENGTH:
                    feature = stats_action_feature(x, y, t, start, stop, SystemEnv.MM_CODE)
                    action_file.write("{}\n".format(json.dumps(feature)))
                x = []
                y = []
                t = []
                start = stop + 1
            else:
                x.append(item['x'])
                y.append(item['y'])
                t.append(item['t'])

        prev_time = item['t']
    return


def process_move_actions(data, action_file, n_from, n_to):
    # can be a compound action: {MM}*
    x = []
    y = []
    t = []
    start = n_from
    counter = 0
    prev_time = 0
    for item in data:
        counter += 1
        x.append(item['x'])
        y.append(item['y'])
        t.append(item['t'])

        if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
            stop = n_from + counter - 2
            if len(t) > SystemEnv.MIN_ACTION_LENGTH:
                feature = stats_action_feature(x, y, t, start, stop, SystemEnv.MM_CODE)
                action_file.write("{}\n".format(json.dumps(feature)))
                x = []
                y = []
                t = []
                start = stop + 1
        prev_time = item['t']

    if len(t) > SystemEnv.MIN_ACTION_LENGTH:
        feature = stats_action_feature(x, y, t, start, n_to, SystemEnv.MM_CODE)
        action_file.write("{}\n".format(json.dumps(feature)))
    return


def process_drag_actions(data, action_file, n_from, n_to):
    # data can be a compound action: {MM}*DD
    x = []
    y = []
    t = []
    start = n_from
    stop = start
    counter = 0
    prev_time = 0

    for item in data:
        counter += 1
        if item['button'] == 'NoButton' and item['state'] == 'Move':
            if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
                stop = n_from + counter - 2
                if len(t) > SystemEnv.MIN_ACTION_LENGTH:
                    feature = stats_action_feature(x, y, t, start, stop, SystemEnv.MM_CODE)
                    action_file.write("{}\n".format(json.dumps(feature)))
                x = []
                y = []
                t = []
                start = stop + 1
            x.append(item['x'])
            y.append(item['y'])
            t.append(item['t'])

        if item['button'] == 'Left' and item['state'] == 'Pressed':
            # ends the MM action
            if len(t) > SystemEnv.MIN_ACTION_LENGTH:
                stop = n_from + counter - 2
                feature = stats_action_feature(x, y, t, start, stop, SystemEnv.MM_CODE)
                action_file.write("{}\n".format(json.dumps(feature)))
            # starts the DD action
            x = []
            y = []
            t = []
            start = stop + 1
            x.append(item['x'])
            y.append(item['y'])
            t.append(item['t'])

        if item['button'] == 'Left' and item['state'] == 'Released':
            # ends the DD action
            x.append(item['x'])
            y.append(item['y'])
            t.append(item['t'])
            feature = stats_action_feature(x, y, t, start, n_to, SystemEnv.DD_CODE)
            action_file.write("{}\n".format(json.dumps(feature)))

        if item['button'] == 'NoButton' and item['state'] == 'Drag':
            x.append(item['x'])
            y.append(item['y'])
            t.append(item['t'])

        prev_time = item['t']
    return
