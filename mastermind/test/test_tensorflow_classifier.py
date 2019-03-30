import pytest

import numpy as np

from mastermind.data_readers import read_image_pil
from mastermind.models import TensorFlowClassifier


def test_key_error_if_input_node_not_in_graph(data_path):
    with pytest.raises(KeyError):
        TensorFlowClassifier(
            model=str(data_path / "example_imagenet_classifier.pb"),
            labels=str(data_path / "imagenet_labels.txt"),
            input_node="NOT_IN_GRAPH",
            output_nodes=["MobilenetV2/Predictions/Reshape_1"])


def test_key_error_if_output_nodes_not_in_graph(data_path):
    with pytest.raises(KeyError):
        TensorFlowClassifier(
            model=str(data_path / "example_imagenet_classifier.pb"),
            labels=str(data_path / "imagenet_labels.txt"))


def test_labels_are_correctly_loaded(data_path):
    model = TensorFlowClassifier(
        model=str(data_path / "example_imagenet_classifier.pb"),
        labels=str(data_path / "imagenet_labels.txt"),
        output_nodes=["MobilenetV2/Predictions/Reshape_1"])
    # implicitly checks if labels is a numpy array instance
    assert model.labels.shape[0] == 1001


def test_expected_class_output(data_path):
    model = TensorFlowClassifier(
        model=str(data_path / "example_imagenet_classifier.pb"),
        labels=str(data_path / "imagenet_labels.txt"),
        output_nodes=["MobilenetV2/Predictions/Reshape_1"])
    image = read_image_pil(
        str(data_path / "hot-dog.jpeg"),
        height=128,
        width=128)
    predicted_classes = model(image)
    assert "hotdog" in predicted_classes
