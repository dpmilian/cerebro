from threading import Thread
from time import sleep

from picamera import PiCamera

from picamera.array import PiRGBArray


class PiCameraStream(object):
    """
      Capture frames from PiCamera using separated thread
    """

    def __init__(self, resolution=(300, 300), preview=False, force_sleep=None):
        """
        :param resolution:
        :param preview:
        """
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.vflip = True
        self.camera.hflip = True
        
        self.force_sleep = force_sleep

        self.rgb_array = PiRGBArray(
            self.camera,
            size=self.camera.resolution)

        self.stream = self.camera.capture_continuous(
            self.rgb_array,
            format="bgr",
            use_video_port=True)

        self.frame = None
        self.stopped = False

        self.preview = preview

        if self.preview:
            self.camera.start_preview()

    def start(self):
        Thread(target=self.continuous_capture).start()

    def stop(self):
        self.stopped = True

    def continuous_capture(self):
        for f in self.stream:
            self.frame = f.array
            self.rgb_array.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rgb_array.close()
                self.camera.close()
                return

    def read(self):
        if self.force_sleep is not None:
            sleep(int(self.force_sleep))
        return self.frame
