import torch

from mean_avg_precision import mean_average_precision

t3_preds = [
    # train_idx, class_prediction, prob_score, x, y, width, height
    [0, 1, 0.9, 0.55, 0.2, 0.3, 0.2],
    [0, 1, 0.8, 0.35, 0.6, 0.3, 0.2],
    [0, 1, 0.7, 0.8, 0.7, 0.2, 0.2],
]
t3_targets = [
    [0, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
    [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
    [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
]
t3_correct_mAP = 0

EPSILON = 1e-4


def test_all_correct_one_class():
    t1_preds = [
        # train_idx, class_prediction, prob_score, x, y, width, height
        [0, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]
    t1_targets = [
        [0, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]
    t1_correct_mAP = 1

    mean_avg_prec = mean_average_precision(
        t1_preds,
        t1_targets,
        iou_threshold=0.5,
        box_format="midpoint",
        num_classes=1,
    )
    assert abs(t1_correct_mAP - mean_avg_prec) < EPSILON


def test_all_correct_batch():
    t2_preds = [
        # train_idx, class_prediction, prob_score, x, y, width, height
        [1, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]
    t2_targets = [
        [1, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]
    t2_correct_mAP = 1

    mean_avg_prec = mean_average_precision(
        t2_preds,
        t2_targets,
        iou_threshold=0.5,
        box_format="midpoint",
        num_classes=1,
    )
    assert abs(t2_correct_mAP - mean_avg_prec) < EPSILON


def test_all_wrong_class():

    mean_avg_prec = mean_average_precision(
        t3_preds,
        t3_targets,
        iou_threshold=0.5,
        box_format="midpoint",
        num_classes=2,
    )
    assert abs(t3_correct_mAP - mean_avg_prec) < EPSILON


def test_one_inaccurate_box():
    t4_preds = [
        # train_idx, class_prediction, prob_score, x, y, width, height
        [0, 0, 0.9, 0.15, 0.25, 0.1, 0.1],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]

    t4_targets = [
        [0, 0, 0.9, 0.55, 0.2, 0.3, 0.2],
        [0, 0, 0.8, 0.35, 0.6, 0.3, 0.2],
        [0, 0, 0.7, 0.8, 0.7, 0.2, 0.2],
    ]
    t4_correct_mAP = 5 / 18

    mean_avg_prec = mean_average_precision(
        t4_preds,
        t4_targets,
        iou_threshold=0.5,
        box_format="midpoint",
        num_classes=1,
    )
    assert abs(t4_correct_mAP - mean_avg_prec) < EPSILON

    y = torch.tensor([0.0000, 0.5000, 0.6667])
    x = torch.tensor([0.0000, 0.3333, 0.6667])
    # trapz(Trapezoidal rule)
    assert abs(torch.trapz(y, x) - mean_avg_prec) < EPSILON


def test_all_wrong_class():
    mean_avg_prec = mean_average_precision(
        t3_preds,
        t3_targets,
        iou_threshold=0.5,
        box_format="midpoint",
        num_classes=2,
    )
    assert abs(t3_correct_mAP - mean_avg_prec) < EPSILON
