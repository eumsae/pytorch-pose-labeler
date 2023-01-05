import os
import json

import cv2
import numpy as np
from tqdm import tqdm

from submodules.estim.pose import PoseEstimator
from submodules.pyutils.files import get_files
from submodules.pyutils.videos import get_frames
from submodules.pyutils.mulproc import QueuedMultiProcessingUnit


def get_size(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height


def get_frame_count(cap):
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return n_frames


def get_fps(cap):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return fps


def get_frames(cap, stt=0, end=-1, step=1):
    cap.set(cv2.CAP_PROP_POS_FRAMES, stt)

    n_frames = get_frame_count(cap)
    end = n_frames-1 if end == -1 else end

    if stt < 0 or n_frames <= stt:
        raise ValueError
    if end < 0 or n_frames <= end:
        raise ValueError
    if end < stt:
        raise ValueError
    
    indices = range(stt, end+1, step)
    for i in indices:
        _, frame = cap.read()
        if i == indices[-1]:
            cap.release()
        yield i, frame


if __name__ == "__main__":
    root = "/workspace/datasets/ha5"
    videos = list(get_files(root, "*.mp4", True))
    estimator = PoseEstimator()

    for video in tqdm(videos, total=len(videos)):
        cap = cv2.VideoCapture(video)

        name = os.path.basename(video)
        par_dir = os.path.dirname(video)
        action_cat = int(name.split('-')[0])
        frame_size = get_size(cap)
        frames = get_frame_count(cap)
        fps = get_fps(cap)
        
        info = {
            "video_name": name,
            "video_path": par_dir,
            "action_category": action_cat,
            "resolution": frame_size,
            "frames": frames,
            "fps": fps}

        dir_ = os.path.join(par_dir, os.path.splitext(name)[0])
        if os.path.exists(dir_):
            os.system(f"rm -rf {dir_}")
        os.mkdir(dir_)

        frames = {}
        for i, frame in get_frames(cap):
            frame_name = f"{os.path.splitext(name)[0]}"
            frame_name += f"_{str(i).zfill(4)}.png"

            outputs = estimator.estimate_with_visualization(frame, 4, 4)

            frame_path = os.path.join(dir_, frame_name)
            cv2.imwrite(frame_path, frame)

            for person_i, output in enumerate(outputs):
                top_left, bottom_right = output["bbox"]
                top_left = list(top_left)
                bottom_right = list(bottom_right)
                kpts = np.array(output["kpts"]).reshape(-1, 3)[:, :-1].tolist()
                pose = {"bbox": [top_left, bottom_right], "kpts": kpts}
                if frame_name not in frames.keys():
                    frames[frame_name] = {"persons": {}}
                if person_i not in frames[frame_name]["persons"].keys():
                    frames[frame_name]["persons"][person_i] = pose
        
        data = {"info": info, "frames": frames}
        
        json_path = os.path.join(dir_, f"{os.path.splitext(name)[0]}.json")
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    print("Done.")