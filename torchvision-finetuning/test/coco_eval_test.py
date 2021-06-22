import os
import io
import tempfile
import json
import contextlib
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


# from detectron2.evaluation.fast_eval_api import COCOeval_opt
def load_json(filename: str):
    with open(filename) as json_file:
        return json.load(json_file)


def test_eval():
    detections = load_json("detections.json")
    gt_annotations = load_json("gt_annotations.json")

    with tempfile.TemporaryDirectory() as tmpdir:
        json_file_name = os.path.join(tmpdir, "gt_full.json")
        with open(json_file_name, "w") as f:
            json.dump(gt_annotations, f)
        with contextlib.redirect_stdout(io.StringIO()):
            coco_api = COCO(json_file_name)

    with contextlib.redirect_stdout(io.StringIO()):
        coco_dt = coco_api.loadRes(detections)
        coco_eval = COCOeval(coco_api, coco_dt, "bbox")
        coco_eval.evaluate()
        coco_eval.accumulate()

    coco_eval.summarize()


