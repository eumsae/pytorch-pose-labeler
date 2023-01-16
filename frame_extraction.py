import os

import cv2

from src.files import get_files
from src.videos import get_frame_imgs
from src.mulproc import MulprocWithQueue


def job_func(video:str):
    if not os.path.exists(video):
        raise FileNotFoundError(video)

    # e.g. video) .../1-1_004-C10.mp4    
    video_name = os.path.splitext(video)[0]  # .../1-1_004-C10
    video_name = os.path.basename(video_name)  # 1-1_004-C10

    dst_dir_root = os.path.abspath("./out")  # .../out
    dst_dir = video_name.split("_")[0]  # 1-1
    dst_dir = os.path.join(dst_dir.split("-")[0], dst_dir)  # 1/1-1
    dst_dir = os.path.join(dst_dir_root, dst_dir)  # .../out/1/1-1
    dst_dir = os.path.join(dst_dir, video_name)  # .../out/1/1-1/1-1_004-C10
    os.makedirs(dst_dir)

    # e.g.) fps 30, step=3 -> fps 10
    for frame_idx, frame_img in get_frame_imgs(video, step=3):
        frame_img = cv2.resize(frame_img, dsize=(1280, 768))
        img_path = f"{video_name}_{str(frame_idx).zfill(4)}.jpg"
        img_path = os.path.join(dst_dir, img_path)
        cv2.imwrite(img_path, frame_img)


if __name__ == "__main__":
    #dataset_dir = "/workspace/data/aihub-human-actions-50/actions-5-origin"
    dataset_dir = "/workspace/pytorch-pose-labeler/sample"
    posix_regex = "*.mp4"

    job_items = list(get_files(dataset_dir, posix_regex))
    mpq = MulprocWithQueue(job_func, job_items)
    mpq.run()
