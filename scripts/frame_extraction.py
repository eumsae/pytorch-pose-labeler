import os
import json

import cv2

from submodules.pyutils.files import get_files
from submodules.pyutils.videos import get_frames


if __name__ == "__main__":
    datasets = "."
    
    videos = get_files(datasets, "*.mp4", True)
    for video in videos:
        out = os.path.splitext(video)[0]
        if os.path.exists(out):
            os.system(f"rm -rf {out}")
        os.mkdir(out)

        for i, frame in get_frames(video):
            img = f"{os.path.basename(out)}_{str(i).zfill(4)}.png"
            img = os.path.join(out, img)
            cv2.imwrite(img, frame)
    
    print("Done.")