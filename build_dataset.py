import os
import math
from pathlib import Path
from multiprocessing import Pool


def main(data_dir):
    data_fields = ["action_type", "traveled_distance", "elapsed_time", "direction"]
    for file in Path(data_dir).glob("**/*.CSV"):
        file = str(file)
        


if __name__ == "__main__":
    # 1 file
    # main(args=["data/balabit/training_files/user12/session_2144641057"])
    # all
    # files = []
    # for file in Path("data/dfl").glob("**/*.CSV"):
    #     files.append(str(file))
    # N = 20
    # files = list(chunks(files, math.ceil(len(files)/N)))
    # pool = Pool(N)
    # pool.map(main, files)
    pass