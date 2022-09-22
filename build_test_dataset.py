import os
import json
import math
from pathlib import Path
import numpy as np
from multiprocessing import Pool

from keeper.environments import SystemEnv
from processing.features import stats_session_feature


def main(data_dir):
    # prepare labels
    with open("/media/hoang/Data/boun-mouse-dynamics-features/labels.csv") as f:
        labels = {}
        for line in f:
            idx, filename, is_illegal = line.strip().replace('.csv', '').split(',')
            session_id = filename[8:]
            labels[session_id] = int(is_illegal)

    # load data of 1 user
    X_negative = []
    Y_negative = []
    session_negative = []

    X_positive = []
    Y_positive = []
    session_positive = []

    for file in Path(data_dir).glob("**/*.csv"):
        file = str(file)
        session_id = os.path.basename(file).replace('.csv', '')[8:]
        y = labels.get(session_id, 0)
        with open(file) as f:
            for line in f:
                line = json.loads(line)
                if not line:
                    continue
                if not y:
                    session_negative.append(line)
                else:
                    session_positive.append(line)

        if len(session_negative) >= SystemEnv.MAX_SESSION_LENGTH:
            X_negative.append(stats_session_feature(session_negative))
            Y_negative.append(y)
            session_negative = []

        if len(session_positive) >= SystemEnv.MAX_SESSION_LENGTH:
            X_positive.append(stats_session_feature(session_positive))
            Y_positive.append(y)
            session_positive = []

    # save to npy
    X_negative = np.array(X_negative)
    Y_negative = np.array(Y_negative)

    X_positive = np.array(X_positive)
    Y_positive = np.array(Y_positive)

    X = np.concatenate([X_negative, X_positive])
    Y = np.concatenate([Y_negative, Y_positive])

    print("Process feature:", data_dir)
    print("Feature shape:", X.shape)
    print("Label shape:", Y.shape)

    output_file = os.path.join(os.path.dirname(data_dir), "X_test.npy")
    np.save(output_file, X)

    output_file = os.path.join(os.path.dirname(data_dir), "Y_test.npy")
    np.save(output_file, Y)
    return


if __name__ == "__main__":
    for i in range(1, 20):
        main("/media/hoang/Data/boun-mouse-dynamics-features/users/user{}/internal_tests".format(i))
