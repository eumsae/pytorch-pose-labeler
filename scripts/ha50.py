import os
import json
import traceback

import numpy as np

from skeleton import HA50Skeleton
from submodules.pyutils.files import get_files
from submodules.pyutils.mulproc import QueuedMultiProcessingUnit


def del_mac_files(root_dir):
    name_pattern = "._*"
    for mac_file in get_files(name_pattern, root_dir):
        print(mac_file)
        os.remove(mac_file)


def load_ha50(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def parse_video_name(data):
    # e.g. .../.../1-1_004-C10_009.jpg
    name = data["images"][0]["img_path"]
    name = name.split('/')[-1]
    name = '_'.join(name.split('_')[:-1])
    name += ".mp4"
    return name


def parse_resolution(data):
    w = data["images"][0]["width"]
    h = data["images"][0]["height"]
    return w, h


def parse_keypoints(kpts):
    kpts = np.array(kpts)
    kpts = kpts.reshape(-1, 3)[:, :2]
    kpts = HA50Skeleton.reindex(kpts)
    kpts = kpts.reshape(-1).astype(int)
    kpts = kpts.tolist()
    return kpts


def parse_video_info(data):
    video_name = parse_video_name(data)
    width, height = parse_resolution(data)
    action_category = int(video_name.split('-')[0])

    info = {
        "video_name": video_name,
        "fps": 30,
        "width": width,
        "height": height,
        "action_category": action_category}
    return info


def parse_video_frames(data):
    image_map = {}
    for img in data["images"]:
        img_id = img["img_no"]
        frm_no = os.path.splitext(img["img_path"])[0]
        frm_no = int(frm_no.split('_')[-1])
        image_map[img_id] = frm_no

    frames = {}
    for annot in data["annotations"]:
        frm_no = image_map[annot["img_no"]]
        per_no = annot["person_no"]
        pose = {"bbox": np.array(annot["bbox"], dtype=int).tolist(),
                "keypoints": parse_keypoints(annot["keypoints"])}

        if frm_no not in frames.keys():
            frames[frm_no] = {"persons": {}}
        if per_no not in frames[frm_no]["persons"].keys():
            frames[frm_no]["persons"][per_no] = pose
    return frames


def restruct_ha50(data):
    try:
        video_info = parse_video_info(data)
        video_frames = parse_video_frames(data)
    except:
        traceback.print_exc()  # dataset error (ignore)
        return

    data = {"info": video_info, "frames": video_frames}
    return data


def dump_ha50(data):
    # e.g. 1-1_004-C10_009.mp4
    json_path = data["info"]["video_name"]
    json_path = os.path.splitext(json_path)[0] + ".json"
    parent_dir = os.path.join(
        "./out",
        json_path.split('-')[0],
        json_path.split('_')[0])

    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
        except:
            # avoid collision between subprocesses
            pass

    json_path = os.path.join(parent_dir, json_path)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)


def main(json_path):
    data = load_ha50(json_path)
    data = restruct_ha50(data)
    dump_ha50(data)


if __name__ == '__main__':
    dataset_dir = "/workspace/datasets/ha50/origin"
    del_mac_files(dataset_dir)

    files = list(get_files('*.json', dataset_dir))
    mpu = QueuedMultiProcessingUnit(main, files)
    mpu.run()