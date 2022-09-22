import json

from keeper.environments import SystemEnv
from .features import stats_action_feature


def process_click_actions(data, action_file, n_from, n_to):
    # can be a compound action: {MM}*PC
    new_data = []
    prev_time = 0
    start = n_from
    counter = 0

    for item in data:
        counter += 1
        if item['state'] == 'Pressed':
            if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
                new_data.append(item)
                feature = stats_action_feature(new_data, start, n_to, SystemEnv.PC_CODE)
                if SystemEnv.DEBUG:
                    print("PC", new_data)
                action_file.write("{}\n".format(json.dumps(feature)))
            return
        else:
            if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
                stop = n_from + counter - 2
                if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
                    feature = stats_action_feature(new_data, start, stop, SystemEnv.MM_CODE)
                    if SystemEnv.DEBUG:
                        print("MM", new_data)
                    action_file.write("{}\n".format(json.dumps(feature)))
                new_data = []
                start = stop + 1
            else:
                new_data.append(item)

        prev_time = item['t']
    return


def process_move_actions(data, action_file, n_from, n_to):
    # can be a compound action: {MM}*
    new_data = []
    start = n_from
    counter = 0
    prev_time = 0

    for item in data:
        counter += 1
        new_data.append(item)

        if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
            stop = n_from + counter - 2
            if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
                feature = stats_action_feature(new_data, start, stop, SystemEnv.MM_CODE)
                if SystemEnv.DEBUG:
                    print("MM", new_data)
                action_file.write("{}\n".format(json.dumps(feature)))
                new_data = []
                start = stop + 1
        prev_time = item['t']

    if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
        feature = stats_action_feature(new_data, start, n_to, SystemEnv.MM_CODE)
        if SystemEnv.DEBUG:
            print("MM", new_data)
        action_file.write("{}\n".format(json.dumps(feature)))
    return


def process_drag_actions(data, action_file, n_from, n_to):
    # data can be a compound action: {MM}*DD
    new_data = []
    start = n_from
    stop = start
    counter = 0
    prev_time = 0

    for item in data:
        counter += 1
        if item['button'] == 'None' and item['state'] == 'Move':
            if item['t'] - prev_time > SystemEnv.EXPIRATION_ACTION_TIME:
                stop = n_from + counter - 2
                if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
                    feature = stats_action_feature(new_data, start, stop, SystemEnv.MM_CODE)
                    if SystemEnv.DEBUG:
                        print("MM", new_data)
                    action_file.write("{}\n".format(json.dumps(feature)))
                new_data = []
                start = stop + 1
            new_data.append(item)

        if item['button'] == 'Left' and item['state'] == 'Pressed':
            # ends the MM action
            if len(new_data) > SystemEnv.MIN_ACTION_LENGTH:
                stop = n_from + counter - 2
                feature = stats_action_feature(new_data, start, stop, SystemEnv.MM_CODE)
                if SystemEnv.DEBUG:
                    print("MM", new_data)
                action_file.write("{}\n".format(json.dumps(feature)))
            # starts the DD action
            new_data = []
            start = stop + 1
            new_data.append(item)

        if item['button'] == 'Left' and item['state'] == 'Released':
            # ends the DD action
            new_data.append(item)
            feature = stats_action_feature(new_data, start, n_to, SystemEnv.DD_CODE)
            if SystemEnv.DEBUG:
                print("DD", new_data)
            action_file.write("{}\n".format(json.dumps(feature)))

        # handle Drag event
        if item['state'] == 'Drag':
            new_data.append(item)

        prev_time = item['t']
    return
