import os

from src.files import get_files


def del_img_files(target_dir, start_idx:int=None, end_idx:int=None):
    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)

    imgs = list(get_files(target_dir, "*.jpg", recursive=False))
    imgs.sort()

    for img in imgs[start_idx:end_idx]:
        os.remove(img)


if __name__ == "__main__":
    dataset_dir = "./samples"
    target = "1-1_004"
    start_idx = 1
    end_idx = None

    target_dir_base = target.split("_")[0]
    target_dir_base = os.path.join(
        target_dir_base.split("-")[0], target_dir_base)
    target_dir_base = os.path.join(target_dir_base, target)
    target_dir_base = os.path.join(dataset_dir, target_dir_base)

    cams = list(range(1, 13))
    cams = ["-C"+str(cam).zfill(2) for cam in cams]

    for cam in cams:
        target_dir = target_dir_base + cam
        if os.path.exists(target_dir):
            del_img_files(target_dir, start_idx, end_idx)