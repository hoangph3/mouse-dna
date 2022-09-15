import pandas as pd
import csv
import os


__X_LIMIT = 4000
__Y_LIMIT = 4000


def event_to_action(filename):
    # Grouping events to action: {MM}*DD, {MM}*PC
    counter = 1
    prevrow = None
    n_from = 2 # line 2, header is line 1
    n_to = 2
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            
        #     counter = counter + 1

        #     # Skip duplicates
        #     if prevrow != None and prevrow == row:
        #         continue
        #     item = {
        #         "x": float(row['x']),
        #         "y": float(row['y']),
        #         "t": float(row['client timestamp']),
        #         "button": row['button'],
        #         "state": row['state']
        #     }

        #     # Skip Scroll
        #     if row["button"] == 'Scroll':
        #         if prevrow != None:
        #             item['x'] = prevrow['x']
        #             item['y'] = prevrow['y']

        #     if row['button'] == 'Left' and row['state'] == 'Released':
        #         data.append(item)
        #         # Skip short sequence
        #         if len(data) <= 2:
        #             data = []
        #             n_from = counter
        #             continue

        #         # Drag Drop
        #         if prevrow != None and prevrow['state'] != 'Pressed':
        #             n_to = counter
        #             # TODO:
        #             print("DD", data, n_from, n_to)

        #         # Point Click
        #         if prevrow != None and prevrow['state'] == 'Pressed':
        #             n_to = counter
        #             # TODO:
        #             print("PC", data, n_from, n_to)

        #         # New action
        #         data = []
        #         n_from = n_to + 1
        #     else:
        #         if float(item['x']) < __X_LIMIT or float(item['y']) < __Y_LIMIT:
        #             data.append(item)
        #     prevrow = row
        # n_to = counter
        # # TODO:
        # print('MM', data, n_from, n_to)


if __name__ == "__main__":
    event_to_action(filename="raw_data/balabit/training_files/user12/session_9838420452")