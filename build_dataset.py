import os
import json
import math
from pathlib import Path
import numpy as np
from multiprocessing import Pool

from keeper.environments import SystemEnv
from processing.features import stats_session_feature


def main(data_dir, training=True):
    # load data of 1 user
    X = []
    for file in Path(data_dir).glob("**/*"):
        file = str(file)
        with open(file) as f:
            data = [json.loads(line) for line in f]
        data = [d for d in data if d]
        session_data = []
        for d in data:
            session_data.append(d)
            if len(session_data) >= SystemEnv.MAX_SESSION_LENGTH:
                session_feat = stats_session_feature(session_data)
                X.append(session_feat)
                session_data = session_data[-int(len(session_data)*0.3):]
        if len(session_data) >= SystemEnv.MAX_SESSION_LENGTH:
            session_feat = stats_session_feature(session_data)
            X.append(session_feat)

    # save to npy
    X = np.array(X)
    print("Process feature:", data_dir)
    print("Feature shape:", X.shape)

    filename = "X_train.npy"
    if not training:
        filename = "X_test.npy"
    output_file = os.path.join(os.path.dirname(data_dir), filename)
    np.save(output_file, X)
    return


if __name__ == "__main__":
    for i in range(1, 20):
        main("/media/hoang/Data/boun-mouse-dynamics-features/users/user{}/training".format(i), training=True)