from donkeycar import Vehicle
from donkeycar.parts.my_camera import CvImageDisplay, MyCamera

V = Vehicle()
cam = MyCamera(0)

V.add(cam, outputs=['camera/image'], threaded=True)
disp = CvImageDisplay()  # part
V.add(disp, inputs=["camera/image"])
V.start()
