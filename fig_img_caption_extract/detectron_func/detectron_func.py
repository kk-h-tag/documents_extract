from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image

from .default.predictor import VisualizationDemo

import easydict
import multiprocessing as mp
import glob
import os

class detectron2_configuration:

    def __init__(self):
        self.args = easydict.EasyDict({

            "config_file": "detectron_func/model/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml",

            "input": '',

            "output": '',

            "confidence_threshold": 0.5,

            "opts": ["MODEL.WEIGHTS", "detectron_func/model/model_final_trimmed.pth", "MODEL.DEVICE", "cpu"]

        })

    def main(self):
        mp.set_start_method("spawn", force=True)

        result_box = ''
        result_class = ''

        cfg = self._setup_cfg()
        demo = VisualizationDemo(cfg)

        if self.args.input:
            if len(self.args.input) == 1:
                self.args.input = glob.glob(os.path.expanduser(self.args.input[0]))
                assert self.args.input, "The input path(s) was not found"
            self.args.input = [self.args.input]
            for path in self.args.input:
                # use PIL, to be consistent with evaluation
                img = read_image(path, format="BGR")
                predictions, visualized_output, masks = demo.run_on_image(img)

                result_box = predictions['instances']._fields['pred_boxes']
                result_class = predictions['instances']._fields['pred_classes']

                if self.args.output:
                    if os.path.isdir(self.args.output):
                        assert os.path.isdir(self.args.output), self.args.output
                        out_filename = os.path.join(self.args.output, os.path.basename(path))
                    else:
                        assert len(self.args.input) == 1, "Please specify a directory with args.output"
                        out_filename = self.args.output
                    visualized_output.save(out_filename)

        return result_box, result_class

    def _setup_cfg(self):
        # load config from file and command-line arguments
        cfg = get_cfg()
        cfg.merge_from_file(self.args.config_file)
        cfg.merge_from_list(self.args.opts)
        # Set score_threshold for builtin models
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = self.args.confidence_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.args.confidence_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = self.args.confidence_threshold
        cfg.freeze()
        return cfg
