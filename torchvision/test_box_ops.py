import torch
from torchvision.ops import box_convert, box_area, box_iou, remove_small_boxes, nms


def test_box_convert():
    """
    box_convert는 dtype(int, float)에 상관없는 것 같다.
    """
    boxes = torch.tensor([
        [100, 100, 150, 150],
        [100, 100, 200, 200],
    ], dtype=torch.float32)

    assert torch.allclose(box_convert(boxes, 'xyxy', 'xywh'), torch.tensor([
        [100, 100, 50, 50],
        [100, 100, 100, 100]
    ], dtype=torch.float32))


def test_box_area():
    boxes = torch.tensor([
        [100, 100, 150, 150],
        [100, 100, 200, 200],
    ], dtype=torch.float32)
    assert torch.allclose(box_area(boxes), torch.tensor([50 * 50, 100 * 100], dtype=torch.float32))


def test_box_iou():
    boxes1 = torch.tensor([
        [100, 100, 150, 150],
    ], dtype=torch.float32)
    boxes2 = torch.tensor([
        [100, 100, 200, 200],
    ], dtype=torch.float32)

    assert torch.allclose(box_iou(boxes1, boxes2), torch.tensor([0.25], dtype=torch.float32))


def test_remove_small_boxes():
    boxes = torch.tensor([
        [100, 100, 150, 150],
        [100, 100, 150, 200],
        [100, 100, 200, 200],
    ], dtype=torch.float32)

    assert torch.allclose(remove_small_boxes(boxes, 70.0), torch.tensor([2]))

    # 조건을 만족하는 row만 filter한다.
    assert torch.allclose(boxes[remove_small_boxes(boxes, 70.0)], torch.tensor([
        [100, 100, 200, 200],
    ], dtype=torch.float32))


def test_nms():
    boxes = torch.tensor([[285.3538, 185.5758, 1193.5110, 851.4551],
                          [285.1472, 188.7374, 1192.4984, 851.0669],
                          [279.2440, 197.9812, 1189.4746, 849.2019]])
    scores = torch.tensor([0.6370, 0.7569, 0.3966])
    iou_thres = 0.2
    keep = nms(boxes, scores, iou_thres)

    # 두번째 box만 남긴다.
    assert torch.allclose(keep, torch.tensor([1]))
