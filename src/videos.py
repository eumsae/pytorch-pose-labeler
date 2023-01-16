import os

import cv2


def get_frame_imgs(video:str, start_idx:int=0, end_idx:int=-1, step:int=1):
    if not os.path.exists(video):
        raise FileNotFoundError(video)

    cap = cv2.VideoCapture(video)

    last_idx = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    end_idx = last_idx if end_idx == -1 else end_idx

    if start_idx < 0 or start_idx > last_idx:
        msg = f"The start_idx must be '>= 0' and '<= idx of last frame'"
        msg += f"(start_idx:{start_idx}, idx of last frame:{last_idx})."
        raise IndexError(msg)
    if end_idx < 0 or last_idx < end_idx:
        msg = f"The end_idx must be '>= 0' and '<= idx of last frame'"
        msg += f"(end_idx:{end_idx}, idx of last frame:{last_idx})"
        raise IndexError(msg)
    if end_idx < start_idx:
        msg = f"The end_idx must be >= start_idx"
        msg += f"(start_idx:{start_idx}, end_idx:{end_idx})."
        raise IndexError(msg)

    indices = range(start_idx, end_idx+1, step)
    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame_img = cap.read()
        if i == indices[-1]:
            cap.release()
        yield i, frame_img
