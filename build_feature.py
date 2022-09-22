import os
import math
from pathlib import Path
from multiprocessing import Pool

from processing.raw2actions import process_session


def main(args):
    for filepath in args:
        print("Process session: {}".format(filepath))
        action_file = filepath.replace("dataset", "features")
        os.makedirs(os.path.dirname(action_file), exist_ok=True)
        with open(action_file, "w") as f:
            process_session(filepath, action_file=f)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    # 1 file
    # main(args=["/media/hoang/Data/balabit_dfl_sapi_data/balabit/training_files/user12/session_2144641057"])
    # all
    files = []
    for file in Path("/media/hoang/Data/boun-mouse-dynamics-dataset/users/").glob("**/*"):
        file = str(file)
        if '.ipynb_checkpoints' in file or os.path.isdir(file):
            continue
        files.append(file)
    # print(files)
    N = 20
    files = list(chunks(files, math.ceil(len(files)/N)))
    pool = Pool(N)
    pool.map(main, files)