import pytest

import numpy as np

from mastermind.data_readers import read_image_pil
from mastermind.models import TensorFlowDetector


def test_expected_class_output(data_path):
    model = TensorFlowDetector(
        model=str(data_path / "example_coco_detector.pb"),
        labels=str(data_path / "coco_labels.txt"))
    image = read_image_pil(
        str(data_path / "coco_hotdog.jpg"),
        height=300,
        width=300)
    boxes, classes = model(image)
    print(classes)
    assert "hotdog" in classes
