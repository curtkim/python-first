import torch
from iou import intersection_over_union


# Accept if the difference in iou is small
EPSILON = 0.001


def test_both_inside_cell_shares_area():
    # midpoint (x,y,w,h)
    # test cases we want to run
    t1_box1 = torch.tensor([0.8, 0.1, 0.2, 0.2])
    t1_box2 = torch.tensor([0.9, 0.2, 0.2, 0.2])
    t1_correct_iou = 1 / 7

    iou = intersection_over_union(t1_box1, t1_box2, box_format="midpoint")
    assert torch.abs(iou - t1_correct_iou) < EPSILON


def test_partially_outside_cell_shares_area():
    t2_box1 = torch.tensor([0.95, 0.6, 0.5, 0.2])
    t2_box2 = torch.tensor([0.95, 0.7, 0.3, 0.2])
    t2_correct_iou = 3 / 13

    iou = intersection_over_union(t2_box1, t2_box2, box_format="midpoint")
    assert torch.abs(iou - t2_correct_iou) < EPSILON


def test_both_inside_cell_shares_no_area():
    t3_box1 = torch.tensor([0.25, 0.15, 0.3, 0.1])
    t3_box2 = torch.tensor([0.25, 0.35, 0.3, 0.1])
    t3_correct_iou = 0

    iou = intersection_over_union(t3_box1, t3_box2, box_format="midpoint")
    assert torch.abs(iou - t3_correct_iou) < EPSILON


def test_midpoint_outside_cell_shares_area():
    t4_box1 = torch.tensor([0.7, 0.95, 0.6, 0.1])
    t4_box2 = torch.tensor([0.5, 1.15, 0.4, 0.7])
    t4_correct_iou = 3 / 31

    iou = intersection_over_union(t4_box1, t4_box2, box_format="midpoint")
    assert torch.abs(iou - t4_correct_iou) < EPSILON


def test_both_inside_cell_shares_entire_area():
    t5_box1 = torch.tensor([0.5, 0.5, 0.2, 0.2])
    t5_box2 = torch.tensor([0.5, 0.5, 0.2, 0.2])
    t5_correct_iou = 1

    iou = intersection_over_union(t5_box1, t5_box2, box_format="midpoint")
    assert torch.abs(iou - t5_correct_iou) < EPSILON


def test_box_format_x1_y1_x2_y2():
    # (x1,y1,x2,y2) format
    t6_box1 = torch.tensor([2, 2, 6, 6])
    t6_box2 = torch.tensor([4, 4, 7, 8])
    t6_correct_iou = 4 / 24

    iou = intersection_over_union(t6_box1, t6_box2, box_format="corners")
    assert torch.abs(iou - t6_correct_iou) < EPSILON


def test_additional_and_batch():
    t12_bboxes1 = torch.tensor(
        [
            [0, 0, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 3, 2],
        ]
    )
    t12_bboxes2 = torch.tensor(
        [
            [3, 0, 5, 2],
            [3, 0, 5, 2],
            [0, 3, 2, 5],
            [2, 0, 5, 2],
            [1, 1, 3, 3],
            [1, 1, 3, 3],
        ]
    )
    t12_correct_ious = torch.tensor([0, 0, 0, 0, 1 / 7, 0.25])

    ious = intersection_over_union(
        t12_bboxes1, t12_bboxes2, box_format="corners"
    )
    all_true = torch.all(
        torch.abs(t12_correct_ious - ious.squeeze(1)) < EPSILON
    )
    assert all_true