import numpy as np

from cerebro.data_readers import read_image_tensorflow, read_image_pil


def test_default_expected_shape_tensorflow(data_path):
    image = read_image_tensorflow(str(data_path / "hot-dog.jpeg"))
    assert list(image.shape) == [1, 299, 299, 3]

def test_default_expected_shape_pil(data_path):
    image = read_image_pil(str(data_path / "hot-dog.jpeg"))
    assert list(image.shape) == [1, 299, 299, 3]

def test_default_normalization_tensorflow(data_path):
    image = read_image_tensorflow(str(data_path / "hot-dog.jpeg"))
    assert np.all(image <= 1.)
    assert np.all(image >= 0.)
    
def test_default_normalization_pil(data_path):
    image = read_image_pil(str(data_path / "hot-dog.jpeg"))
    assert np.all(image <= 1.)
    assert np.all(image >= 0.)