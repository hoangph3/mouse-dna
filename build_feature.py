import os
import shutil
from pathlib import Path

from keeper.environments import SystemEnv
from processing.raw2actions import process_session


def main():
    if os.path.exists("features"):
        shutil.rmtree("features")
    for filepath in Path("data/balabit/training_files/user12").glob("**/*"):
        filepath = str(filepath)
        action_file = filepath.replace("data", "features")
        if not os.path.exists(os.path.dirname(action_file)):
            os.makedirs(os.path.dirname(action_file))
        f = open(action_file, "w")
        process_session(filepath, action_file=f)
        f.close()
        break


if __name__ == "__main__":
    main()
