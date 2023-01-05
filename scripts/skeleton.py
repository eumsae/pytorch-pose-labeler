import cv2


COLOR = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "MAGENTA": (255, 0, 255),
    "ORANGE": (255, 128, 0),
    "AZURE": (0, 128, 255),
    "CYAN": (0, 255, 255),
    "GRAY": (170, 170, 170),
}


def visualize_kpts(img, kpts, kpts_map, bone_map, radius, thickness):
    # Check error: out of range
    w, h = img.shape[:2][::-1]
    for kpt in kpts:
        x, y = kpt
        isvalid_x = 0 <= x and x < w
        isvalid_y = 0 <= y and y < h
        if not (isvalid_x and isvalid_y):
            msg = "some keypoint is out of the image size."
            raise ValueError(msg)

    # Draw bones
    for i in range(len(kpts)):
        bones = bone_map[i]
        for j in bones.keys():
            color = bones[j]
            cv2.line(img, kpts[i], kpts[j], color, thickness)

    # Draw keypoints
    for i in range(len(kpts)):
        color = kpts_map[i]["color"]
        cv2.circle(img, kpts[i], radius, color, thickness)


class CustomSkeleton():

    kpts_map = {
        0: {"part": "HEAD", "color": COLOR["GREEN"]},
        1: {"part": "L_SHOULDER", "color": COLOR["RED"]},
        2: {"part": "L_ELBOW", "color": COLOR["RED"]},
        3: {"part": "L_WRIST", "color": COLOR["RED"]},
        4: {"part": "R_SHOULDER", "color": COLOR["BLUE"]},
        5: {"part": "R_ELBOW", "color": COLOR["BLUE"]},
        6: {"part": "R_WRIST", "color": COLOR["BLUE"]},
        7: {"part": "L_HIP", "color": COLOR["RED"]},
        8: {"part": "L_KNEE", "color": COLOR["RED"]},
        9: {"part": "L_ANKLE", "color": COLOR["RED"]},
        10: {"part": "R_HIP", "color": COLOR["BLUE"]},
        11: {"part": "R_KNEE", "color": COLOR["BLUE"]},
        12: {"part": "R_ANKLE", "color": COLOR["BLUE"]}}

    bone_map = {
        0: {},
        1: {2: COLOR["GRAY"],
            4: COLOR["GRAY"],
            7: COLOR["GRAY"]},
        2: {3: COLOR["GRAY"]},
        3: {},
        4: {5: COLOR["GRAY"],
            10: COLOR["GRAY"]},
        5: {6: COLOR["GRAY"]},
        6: {},
        7: {8: COLOR["GRAY"],
            10: COLOR["GRAY"]},
        8: {9: COLOR["GRAY"]},
        9: {},
        10: {11: COLOR["GRAY"]},
        11: {12: COLOR["GRAY"]},
        12: {}}

    """
    bone_map = {
        0: {},
        1: {2: COLOR["RED"],
            4: COLOR["MAGENTA"],
            7: COLOR["MAGENTA"]},
        2: {3: COLOR["RED"]},
        3: {},
        4: {5: COLOR["ORANGE"],
            10: COLOR["MAGENTA"]},
        5: {6: COLOR["ORANGE"]},
        6: {},
        7: {8: COLOR["BLUE"],
            10: COLOR["MAGENTA"]},
        8: {9: COLOR["BLUE"]},
        9: {},
        10: {11: COLOR["AZURE"]},
        11: {12: COLOR["AZURE"]},
        12: {}}
    """


class HA50Skeleton():

    @classmethod
    def reindex(cls, kpts):
        """ Reindex keypoints to fit the CustomSkeleton.
        Args:
            kpts(numpy.ndarray): shape=(16, -1)
        Returns:
            kpts(numpy.ndarray): shape=(13, -1)
        """
        return kpts[[9, 13, 14, 15, 12, 11, 10, 3, 4, 5, 2, 1, 0]]

    kpts_map = {
        0: {"part": "R_ANKLE", "color": COLOR["AZURE"]},
        1: {"part": "R_KNEE", "color": COLOR["AZURE"]},
        2: {"part": "R_HIP", "color": COLOR["MAGENTA"]},
        3: {"part": "L_HIP", "color": COLOR["MAGENTA"]},
        4: {"part": "L_KNEE", "color": COLOR["BLUE"]},
        5: {"part": "L_ANKLE", "color": COLOR["BLUE"]},
        6: {"part": "PELVIS", "color": COLOR["MAGENTA"]},
        7: {"part": "THORAX", "color": COLOR["MAGENTA"]},
        8: {"part": "NECK", "color": COLOR["GREEN"]},
        9: {"part": "HEAD", "color": COLOR["GREEN"]},
        10: {"part": "R_WRIST", "color": COLOR["ORANGE"]},
        11: {"part": "R_ELBOW", "color": COLOR["ORANGE"]},
        12: {"part": "R_SHOULDER", "color": COLOR["MAGENTA"]},
        13: {"part": "L_SHOULDER", "color": COLOR["MAGENTA"]},
        14: {"part": "L_ELBOW", "color": COLOR["RED"]},
        15: {"part": "L_WRIST", "color": COLOR["RED"]}}

    bone_map = {
        0: {1: COLOR["AZURE"]},
        1: {2: COLOR["AZURE"]},
        2: {3: COLOR["MAGENTA"],
            6: COLOR["MAGENTA"]},
        3: {4: COLOR["BLUE"],
            6: COLOR["MAGENTA"]},
        4: {5: COLOR["BLUE"]},
        5: {},
        6: {7: COLOR["MAGENTA"]},
        7: {8: COLOR["MAGENTA"],
            12: COLOR["MAGENTA"],
            13: COLOR["MAGENTA"]},
        8: {},
        9: {},
        10: {11: COLOR["ORANGE"]},
        11: {12: COLOR["ORANGE"]},
        12: {},
        13: {14: COLOR["RED"]},
        14: {15: COLOR["RED"]}}