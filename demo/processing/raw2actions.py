from io import StringIO
import csv
import os

from keeper.environments import SystemEnv
from . import actions


def process_session_in_duration(filename, action_file):
    start_time = None
    prev_row = None

    with open(filename, encoding='utf-8') as csv_file:
        reader = csv_file.read()
        reader = reader.replace('\x00', '')
        reader = csv.DictReader(StringIO(reader))
        data = []
        for row in reader:
            # validate
            valid = True
            for key in ['client_timestamp', 'button', 'state', 'x', 'y']:
                if not row.get(key, ''):
                    valid = False
                    break
            if not valid:
                continue

            # Skip duplicate
            if prev_row and prev_row == row:
                continue

            item = {
                "x": int(row['x']),
                "y": int(row['y']),
                "t": float(row['client_timestamp']),
                "button": row['button'],
                "state": row['state']
            }

            # start session time
            if start_time is None:
                start_time = item['t']

            # duration
            if item['t'] - start_time <= SystemEnv.EXPIRATION_ACTION_TIME:
                data.append(item)
            else:
                actions.stats_action_feature(action_data=data,
                                             n_from=None, n_to=None,
                                             action_type=None,
                                             action_file=action_file)
                data = data[-int(len(data) * 0.2):]
                start_time = item['t']

            prev_row


def process_session_to_action(filename, action_file):
    counter = 1
    prev_row = None
    n_from = 2
    n_to = 2
    with open(filename, encoding='utf-8') as csv_file:
        reader = csv_file.read()
        reader = reader.replace('\x00', '')
        reader = csv.DictReader(StringIO(reader))
        data = []
        for row in reader:
            # validate
            valid = True
            for key in ['client_timestamp', 'button', 'state', 'x', 'y']:
                if not row.get(key, ''):
                    valid = False
                    break
            if not valid:
                continue

            counter = counter + 1
            # Skip duplicate
            if prev_row and prev_row == row:
                continue

            item = {
                "x": int(row['x']),
                "y": int(row['y']),
                "t": float(row['client_timestamp']),
                "button": row['button'],
                "state": row['state']
            }
            # Skip scroll
            if row["button"] == 'Scroll':
                if prev_row:
                    item['x'] = prev_row['x']
                    item['y'] = prev_row['y']

            if row['button'] == 'Left' and row['state'] == 'Released':
                data.append(item)
                # Skip short sequence
                if len(data) <= 2:
                    data = []
                    n_from = counter
                    continue

                # A Drag Drop Action (4) ends here.
                # It can be a compound action: {MM}*DD - several MM actions followed by a DD action
                if prev_row and prev_row['state'] != 'Pressed':
                    n_to = counter
                    # print("DD", data)
                    actions.process_drag_actions(data, action_file, n_from, n_to)

                # A Point Click Action (3) ends here.
                # It can be a compound action: {MM}*PC - several MM actions followed by a DD action
                if prev_row and prev_row['state'] == 'Pressed':
                    n_to = counter
                    # print("PC", data)
                    actions.process_click_actions(data, action_file, n_from, n_to)

                # It starts a new action
                data = []
                n_from = n_to + 1
            else:
                if SystemEnv.X_MIN <= int(item['x']) <= SystemEnv.X_MAX or SystemEnv.Y_MIN <= int(item['y']) <= SystemEnv.Y_MAX:
                    data.append(item)
            prev_row = row
        n_to = counter
        # print("MM", data)
        actions.process_move_actions(data, action_file, n_from, n_to)
        return
