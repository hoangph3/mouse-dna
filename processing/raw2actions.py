import csv
import os

from keeper.environments import SystemEnv
from . import actions


def process_session(filename, action_file):
    counter = 1
    prev_row = None
    n_from = 2
    n_to = 2
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            counter = counter + 1
            # Skip duplicate
            if prev_row and prev_row == row:
                continue

            item = {
                "x": int(row['x']),
                "y": int(row['y']),
                "t": float(row['client timestamp']),
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
                if prev_row and prev_row['state'] == 'Drag':
                    n_to = counter
                    actions.process_drag_actions(data, action_file, n_from, n_to)

                # A Point Click Action (3) ends here.
                # It can be a compound action: {MM}*PC - several MM actions followed by a DD action
                if prev_row and prev_row['state'] == 'Pressed':
                    n_to = counter
                    actions.process_click_actions(data, action_file, n_from, n_to)

                # It starts a new action
                data = []
                n_from = n_to + 1
            else:
                if int(item['x']) < SystemEnv.X_LIMIT or int(item['y']) < SystemEnv.Y_LIMIT:
                    data.append(item)
            prev_row = row
        n_to = counter
        actions.process_move_actions(data, action_file, n_from, n_to)
        return