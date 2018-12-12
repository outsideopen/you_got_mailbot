import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread

class Camera():                                                                                                 #Camera object - handles everything image related
        def __init__(self):                                                                                     
                print("initializing Pi Camera...")

                self.cap = PiCamera()                                                                           #create Raspberry Pi camera module
                self.cap.resolution = (640, 480)                                                                #define capture resolution
                self.cap.rotation = 90                                                                          #compensate for camera orientation
                self.cap.framerate = 30                                                                         #define capture rate
                self.cap.led = False                                                                            #diasable camera status indicator LED
                self.rawCapture = PiRGBArray(self.cap, size=(640, 480))                                         #image numpy array object

                self.frame = None
                self.captureThread = Thread(target=self.__captureFrame)                                         #frame retrieval thread - reduce I/O latency
                self.captureThread.daemon = True                        
                self.captureThread.do_run = True
                self.captureThread.start()

                self.faceCascade = cv2.CascadeClassifier('camera/haarcascade_frontalface_default.xml')          #haar cascade classifier for facial detection

                print("done")
    
        def __captureFrame(self):                                                                               #frame retrieval thread
            for capture in self.cap.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):     #capture frames in infinte iterator
                self.frame = capture.array
                self.rawCapture.truncate(0)

                if (self.captureThread.do_run == False):
                    break

        def averageGraySpace(self, grayFrame):                                                                  #calculate average light level from frame in gray space
                average = np.mean(grayFrame.flatten())
                return average

        def getFrame(self):                                                                                     #retrieve frame from camera as an array
                return self.frame

        def convertGray(self, frame):                                                                           #convert RGB frame to gray space
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                return gray

        def getFaces(self, frame):                                                                              #find faces in frame array with haarcascade classifier
                faces = self.faceCascade.detectMultiScale(frame, 1.3, 5)
                return faces

        def highlightFace(self, frame, faces):                                                                  #draw rectangle around the faces returned by getFaces()
                img = frame
                for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                return img

        def saveFrame(self, frame, name="image"):                                                               #save frame array to disk
                cv2.imwrite(name, frame)
                
        def __del__(self):                                                                                      #close safely
                print("stopping Pi Camera...")
                self.captureThread.do_run = False
                self.captureThread.join()
                self.cap.close()
                print("done")
