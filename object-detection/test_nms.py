import torch
from nms import nms


def test_remove_on_iou():
    t1_boxes = [
        [1, 1, 0.5, 0.45, 0.4, 0.5],
        [1, 0.8, 0.5, 0.5, 0.2, 0.4],
        [1, 0.7, 0.25, 0.35, 0.3, 0.1],
        [1, 0.05, 0.1, 0.1, 0.1, 0.1],
    ]

    c1_boxes = [[1, 1, 0.5, 0.45, 0.4, 0.5], [1, 0.7, 0.25, 0.35, 0.3, 0.1]]

    bboxes = nms(
        t1_boxes,
        threshold=0.2,
        iou_threshold=7 / 20,
        box_format="midpoint",
    )
    assert sorted(bboxes) == sorted(c1_boxes)


def test_keep_on_class():
    t2_boxes = [
        [1, 1, 0.5, 0.45, 0.4, 0.5],
        [2, 0.9, 0.5, 0.5, 0.2, 0.4],
        [1, 0.8, 0.25, 0.35, 0.3, 0.1],
        [1, 0.05, 0.1, 0.1, 0.1, 0.1],
    ]

    c2_boxes = [
        [1, 1, 0.5, 0.45, 0.4, 0.5],
        [2, 0.9, 0.5, 0.5, 0.2, 0.4],
        [1, 0.8, 0.25, 0.35, 0.3, 0.1],
    ]

    bboxes = nms(
        t2_boxes,
        threshold=0.2,
        iou_threshold=7 / 20,
        box_format="midpoint",
    )
    assert sorted(bboxes) == sorted(c2_boxes)


def test_remove_on_iou_and_class():
    t3_boxes = [
        [1, 0.9, 0.5, 0.45, 0.4, 0.5],
        [1, 1, 0.5, 0.5, 0.2, 0.4],
        [2, 0.8, 0.25, 0.35, 0.3, 0.1],
        [1, 0.05, 0.1, 0.1, 0.1, 0.1],
    ]

    c3_boxes = [[1, 1, 0.5, 0.5, 0.2, 0.4], [2, 0.8, 0.25, 0.35, 0.3, 0.1]]

    bboxes = nms(
        t3_boxes,
        threshold=0.2,
        iou_threshold=7 / 20,
        box_format="midpoint",
    )
    assert sorted(bboxes) == sorted(c3_boxes)


def test_keep_on_iou():
    t4_boxes = [
        [1, 0.9, 0.5, 0.45, 0.4, 0.5],
        [1, 1, 0.5, 0.5, 0.2, 0.4],
        [1, 0.8, 0.25, 0.35, 0.3, 0.1],
        [1, 0.05, 0.1, 0.1, 0.1, 0.1],
    ]

    c4_boxes = [
        [1, 0.9, 0.5, 0.45, 0.4, 0.5],
        [1, 1, 0.5, 0.5, 0.2, 0.4],
        [1, 0.8, 0.25, 0.35, 0.3, 0.1],
    ]

    bboxes = nms(
        t4_boxes,
        threshold=0.2,
        iou_threshold=9 / 20,
        box_format="midpoint",
    )
    assert sorted(bboxes) == sorted(c4_boxes)
