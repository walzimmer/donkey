import os
import time
import numpy as np
from PIL import Image
import glob
from donkeycar.utils import rgb2gray

class BaseCamera:

    def run_threaded(self):
        return self.frame

class PiCamera1(BaseCamera):
#    def __init__(self, image_w=160, image_h=120, image_d=3, framerate=20):
    def __init__(self, image_w=320, image_h=240, image_d=2, framerate=10):
        #from picamera.array import PiRGBArray
        #from picamera import PiCamera
        
        self.resolution = (image_w, image_h)
        # initialize the camera and stream
        #self.camera = PiCamera() #PiCamera gets resolution (height, width)
        self.framerate = framerate
        #self.rawCapture = PiRGBArray(self.camera, size=resolution)
        #self.stream = self.camera.capture_continuous(self.rawCapture,
        #    format="rgb", use_video_port=True)

        openni2.initialize()  # can also accept the path of the OpenNI redistribution
        self.dev = openni2.Device.open_any()

        self.ir_stream = self.dev.create_stream(openni2.SENSOR_IR)
        self.depth_stream = self.dev.create_stream(openni2.SENSOR_DEPTH)
        self.depth_stream.configure_mode(width=320,height=240,fps=30,pixel_format=openni2.PIXEL_FORMAT_DEPTH_1_MM)

        self.ir_stream.start()
        self.depth_stream.start()

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True
        self.image_d = image_d

        print('Pi_StructureCamera loaded.. .warming camera')
        time.sleep(2)


    def run(self):
        # get frames
        depth_frame = self.depth_stream.read_frame()
        depth_frame_data = depth_frame.get_buffer_as_uint16()

        ir_frame = self.ir_stream.read_frame()
        ir_frame_data = ir_frame.get_buffer_as_uint16()
        
        # convert and pack into numpy array
        ir_array = np.reshape(np.asarray(ir_frame_data, dtype=np.int16), (ir_frame.height, ir_frame.width))
        depth_array = np.reshape(np.asarray(depth_frame_data, dtype=np.int16),
                                 (depth_frame.height, depth_frame.width))

        #f = next(self.stream)
        #frame = f.array
        ir_array = 6*ir_array+90
        frame = np.array(ir_array, depth_array)
        #self.rawCapture.truncate(0)
        if self.image_d == 1:
            frame = rgb2gray(frame)
        return frame


    def poll(self):
        # get frames
        depth_frame = self.depth_stream.read_frame()
        depth_frame_data = depth_frame.get_buffer_as_uint16()

        ir_frame = self.ir_stream.read_frame()
        ir_frame_data = ir_frame.get_buffer_as_uint16()
        
        # convert and pack into numpy array
        ir_array = np.reshape(np.asarray(ir_frame_data, dtype=np.int16), (ir_frame.height, ir_frame.width))
        depth_array = np.reshape(np.asarray(depth_frame_data, dtype=np.int16),
                                 (depth_frame.height, depth_frame.width))

        ir_array = 5*ir_array+90
        self.frame = np.array(ir_array, depth_array)

        
    def update(self):
        # keep looping infinitely until the thread is stopped
        '''for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.image_d == 1:
                self.frame = rgb2gray(self.frame)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break
         '''
        while self.running:
             self.poll()
             if not self.on:
               break 
               
    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        #self.stream.close()
        #self.rawCapture.close()
        #self.camera.close()
        self.ir_stream.stop()
        self.depth_stream.stop()
        openni2.unload()
        
