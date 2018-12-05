import cv2
import time
from openni import openni2
import numpy as np


class StructureSensorPart(object):

    def __init__(self):
        # self.cap = cv2.VideoCapture(camera_idex)
        # self.frame = None
        self.combined_array = None
        self.running = True

        openni2.initialize()  # can also accept the path of the OpenNI redistribution

        self.dev = openni2.Device.open_any()
        print(dev.get_device_info())

        self.ir_stream = dev.create_stream(openni2.SENSOR_IR)
        print(ir_stream.__dict__)
        self.depth_stream = dev.create_stream(openni2.SENSOR_DEPTH)
        print(depth_stream.__dict__)

        ir_stream.start()
        depth_stream.start()

    def poll(self):
        # ret, self.frame = self.cap.read()
        # get frames
        ir_frame = self.ir_stream.read_frame()
        ir_frame_data = self.ir_frame.get_buffer_as_uint16()

        depth_frame = self.depth_stream.read_frame()
        depth_frame_data = depth_frame.get_buffer_as_uint16()

        print(ir_frame.__dict__)
        print(depth_frame.__dict__)

        # convert and pack into numpy array
        ir_array = np.reshape(np.asarray(ir_frame_data, dtype=np.int16), (ir_frame.width, ir_frame.height))
        depth_array = np.reshape(np.asarray(depth_frame_data, dtype=np.int16),
                                 (depth_frame.width, depth_frame.height))

        # stack both images along z-axis
        self.combined_array = np.dstack((ir_array, depth_array))

    def update(self):
        while self.running:
            self.poll()

    def run_threaded(self):
        # return self.frame
        return self.combined_array

    def run(self):
        self.poll()
        # return self.frame
        return self.combined_array

    def shutdown(self):
        self.running = False
        time.sleep(0.2)
        # self.cap.release()
        ir_stream.stop()
        depth_stream.stop()
        openni2.unload()


class CvImageDisplay(object):
    def run(self, image):
        cv2.imshow('frame', image)
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllWindows()
