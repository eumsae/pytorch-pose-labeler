import os

from src.files import get_files


def split_img_files(target_dir, split_idx:int):
    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)

    imgs = list(get_files(target_dir, "*.jpg", recursive=False))
    imgs.sort()

    imgs_split_1 = imgs[:split_idx]
    imgs_split_2 = imgs[split_idx:]

    dir_split_1 = target_dir + "_split_1"
    dir_split_2 = target_dir + "_split_2"

    os.makedirs(dir_split_1)
    os.makedirs(dir_split_2)

    def rename(imgs, split_dir):
        for img in imgs:
            new_img = os.path.basename(img)
            new_img = os.path.join(split_dir, new_img)
            os.rename(img, new_img)
    rename(imgs_split_1, dir_split_1)
    rename(imgs_split_2, dir_split_2)

    os.system(f"rm -rf {target_dir}")


if __name__ == "__main__":
    dataset_dir = "/workspace/data/aihub-human-action-50/action-5-frmext"
    target = "9-6_633"
    split_idx = 6

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
            split_img_files(target_dir, split_idx)