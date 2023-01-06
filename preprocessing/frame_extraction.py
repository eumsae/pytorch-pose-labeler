import os
import fnmatch
import multiprocessing as mp

import cv2
from tqdm import tqdm


def get_files(root_dir:str, posix_regex:str, recursive:bool):
    if not os.path.exists(root_dir):
        msg = f"{root_dir} is not exists or not a directory."
        raise ValueError(msg)
    for par_dir, _, files in os.walk(root_dir):
        if files:
            for file in fnmatch.filter(files, posix_regex):
                yield os.path.join(par_dir, file)
        if not recursive:
            break


def get_frame_images(video:str, start_idx:int=0, end_idx:int=-1, step:int=1):
    if not os.path.exists(video):
        raise FileNotFoundError(video)

    cap = cv2.VideoCapture(video)

    last_idx = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    if end_idx == -1:
        end_idx = last_idx

    if start_idx < 0 or last_idx < start_idx:
        raise ValueError
    if end_idx < 0 or last_idx < end_idx:
        raise ValueError
    if end_idx < start_idx:
        raise ValueError

    indices = range(start_idx, end_idx+1, step)
    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame_img = cap.read()
        if i == indices[-1]:
            cap.release()
        yield i, frame_img


def extract_frames(video:str):
    if not os.path.exists(video):
        raise FileNotFoundError(video)

    video_name = os.path.splitext(video)[0]  # .../.../1-1_004-C10
    video_name = os.path.basename(video_name)  # 1-1_004-C10

    current_dir = os.path.abspath('./out')
    out_dir = video_name.split('_')[0]  # 1-1
    out_dir = os.path.join(out_dir.split('-')[0], out_dir)  # 1/1-1
    out_dir = os.path.join(current_dir, out_dir)  # $(current_dir)/1/1-1
    out_dir = os.path.join(out_dir, video_name)  # $(current_dir)/1/1-1/1-1_004-c10
    os.makedirs(out_dir)

    for frame_num, frame_img in get_frame_images(video, step=3):
        frame_img = cv2.resize(frame_img, (1280, 768))
        img = f"{video_name}_{str(frame_num).zfill(4)}.jpg"
        img = os.path.join(out_dir, img)
        cv2.imwrite(img, frame_img)


class QueueMP():
    def __init__(self, job_fn, job_items):
        self.num_units = mp.cpu_count()
        self.job_fn = self._wrap(job_fn)
        self.job_items = job_items
        self.queue = mp.Queue(maxsize=self.num_units)
        self.queue_lock = mp.Lock()

    def run(self):
        pool = mp.Pool(self.num_units, self.job_fn)
        for queue_item in tqdm(self.job_items, total=len(self.job_items)):
            self.queue.put(queue_item)
        for _ in range(self.num_units):
            self.queue.put(None)
        pool.close()
        pool.join()
    
    def _wrap(self, job_fn):
        def wrapped():
            while True:
                with self.queue_lock:
                    item = self.queue.get()
                if item is None:
                    break
                job_fn(item)
        return wrapped


if __name__ == "__main__":
    dataset_dir = "/workspace/datasets/1"
    videos = list(get_files(dataset_dir, "*.mp4", recursive=True))
    qmp = QueueMP(extract_frames, videos)
    qmp.run()
