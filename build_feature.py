import os
import math
from pathlib import Path
from multiprocessing import Pool

from processing.raw2actions import process_session


def main(args):
    # if os.path.exists("features"):
        # shutil.rmtree("features")
    for filepath in args:
        print("Process session: {}".format(filepath))
        action_file = filepath.replace("data", "features")
        if not os.path.exists(os.path.dirname(action_file)):
            os.makedirs(os.path.dirname(action_file))
        with open(action_file, "w") as f:
            process_session(filepath, action_file=f)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    files = []
    for file in Path("data/dfl/User3").glob("**/*.CSV"):
        files.append(str(file))
    N = 10
    files = list(chunks(files, math.ceil(len(files)/N)))
    pool = Pool(N)
    pool.map(main, files)
