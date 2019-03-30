import argparse
import time

from pathlib import Path

import numpy as np

from PIL import Image

from capture import PiCameraStream
from models import TensorFlowDetector


def process_stream(detector=None, labels=None, output=None, force_sleep=None, preview=False):

    stream = PiCameraStream(force_sleep=force_sleep, preview=preview)
    if output is not None:
        print(output)
        Path(output).mkdir(parents=True, exist_ok=True)
    model = None
    if detector and labels:
        model = TensorFlowDetector(
            model=detector,
            labels=labels)

    try:
        stream.start()

        while not stream.stopped:
            if stream.frame is not None:
                image = stream.read()
                image = np.expand_dims(image, 0)
                if model:
                    predictions = model(image)
                    print(predictions[1])
                if output:
                    print("Saving image")
                    Image.fromarray(image[0]).save("{}/{}.jpg".format(output, time.time()))

    except KeyboardInterrupt:
        stream.stop()


def get_parser():
    parser = argparse.ArgumentParser(
        description="Command line program to capture and process images from PiCamera")
    parser.add_argument(
        "-d", "--detector",
        help="Path to a frozen TensorFlow model in protobuf format (.pb)")
    parser.add_argument(
        "-l", "--labels",
        help="Path to a .txt file with one class name per line")
    parser.add_argument(
        "-o", "--output",
        help="Output path where captured images will be stored")
    parser.add_argument(
        "-s", "--force_sleep",
        help="Force the stream to wait between N seconds between image captures")    
    parser.add_argument(
        "-p", "--preview",
        help="Visualize the capture")
    return parser

if __name__ == "__main__":

    parser = get_parser()
    args = vars(parser.parse_args())
    process_stream(**args)
