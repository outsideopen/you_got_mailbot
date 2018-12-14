try:                                                                    #import necessary modules
    print("importing modules...")
    from gdrive.drivePublisher import Gpublisher
    from slack.slackPublisher import Spublisher
    from camera.cam import Camera
    import datetime
    import os
    import cv2
    import numpy as np
    import time
    print("done")
except Exception as e:                                                  #handle import errors
    print("error importing modules")
    print(e)
    exit()

try:                                                                    #initialize component classes
    print("initializing modules...")
    camera = Camera()
    slack = Spublisher()
    drive = Gpublisher()
    print("done")
except Exception as e:                                                  #handle initialization errors
    print("error initializing modules")
    print(e)
    exit()

def closeAll():                                                         #soft exit method
    print("stopping MailBot")
    exit()

def Upload(frame, face):                                                #upload method
    imagePath = "camera/image/image.jpg"                                #location for temporary image storage   
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")           #time stamp for image

    camera.saveFrame(frame, imagePath)                                  #save frame to disk
    
    fileID = drive.upload(imagePath, date)                              #upload frame to gdrive
    
    URL = "https://drive.google.com/uc?id=" + str(fileID)               #convert gdrive fileID into embeddable URL
    if face:                                                            #post image to slack using URL
        slack.post(URL, message="Mail-Person Spotted! Face Found!", name=date)
    else:
        slack.post(URL, message="Mail-Person Spotted!", name=date)
    
    os.remove(imagePath)                                                #remove frame from disk

    print("uploaded image")
    
print("starting main loop")
                                                                        #timer variables
timer = 0                                                               #timer counter AKA the tick
timerConstant = 1                                                       #timer delay time AKA the tock

isOpen = False                                                          #state detection variables
doorState1 = False                                                      #current door state - true = open, false = closed
doorState2 = False                                                      #previous doorState1 value
openFrames=[]                                                           #frame buffer for all frames captured while door is open
startDetection = False                                                  
faceDetected = False
faceArray = []

while True:                                                             #main loop
    try:
        frame = camera.getFrame()                                       #get frame from camera
        gray = camera.convertGray(frame)                                #convert to grayscale
        
        if timer <= 0:                                                  #continue of there is no delay
            average = camera.averageGraySpace(gray)                     #calculate average light-level of the frame

            if average > 100:                                           #detect is door is open
                doorState1 = True
                openFrames.append(frame)

            else:
                doorState1 = False

            if doorState2 == doorState1 and doorState2 == True:         #see if door is open
                isOpen = True
                
            elif doorState2 == doorState1 and doorState2 == False:      #see if door has just been closed
                if isOpen == True:
                    startDetection = True
                    
                isOpen = False

            if startDetection == True:                                  #begin face detection
                for f in openFrames:                                    #use frames stored in buffer
                    print("searching for faces...")
                    faces = camera.getFaces(f)                          #detect faces in gray frame
                    
                    for i in range(0, faces.shape[2]):
                        confidence = faces[0, 0, i, 2]
                        
                        if confidence > camera.minimumConfidence:
                            print("face found", confidence)
                            (h, w) = f.shape[:2]
                            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")

                            text = "{:.2f}%".format(confidence * 100)
                            y = startY - 10 if startY - 10 > 10 else startY + 10

                            cv2.rectangle(f, (startX, startY), (endX, endY), (0, 0, 255), 2)
                            cv2.putText(f, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                            
                            faceDetected = True
                            faceArray.append([f,confidence])
                            break

                if faceDetected == False:                               #if no faces are found upload anyways
                    print("no face found")
                    median = int(len(openFrames)/2)                     #find middle frame
                    print("uploading image")
                    Upload(openFrames[median], False)                   #upload image to the internet
                    timer = 30                                          #wait 30 seconds before attempting to capture again
                    print("delay", timer, " seconds")
                else:
                    highestConfidence = 0
                    bestFrame = None
                    for i in range(len(faceArray)):
                        if faceArray[i][1] > highestConfidence:
                            highestConfidence = faceArray[i][1]
                            bestFrame = faceArray[i][0]

                    print("uploading image")
                    Upload(bestFrame, True)
                    timer = 30
                    print("delay", timer, " seconds")

                faces=None
                faceArray=[]
                openFrames=[]                                           #clear frame buffer
                faceDetected = False                                    #reset detection variables
                startDetection = False

            doorState2 = doorState1                                     #update previous door status before beginning next loop

        else:                                                           #if timer is set delay a given amount of time
            time.sleep(timerConstant)                                   #total delay time = timmerConstant * timer
            timer-=1

    except KeyboardInterrupt:                                           #handle keyboard interrupts
        print("keyboard interrupt")
        break                                                           #stop loop

    except Exception as e:                                              #handle misc errors
        print("error")
        print(e)
        break                                                           #stop loop

closeAll()                                                              #exit safely
