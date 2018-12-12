try:                                                                    #import necessary modules
    print("importing modules...")
    from gdrive.drivePublisher import Gpublisher
    from slack.slackPublisher import Spublisher
    from camera.cam import Camera
    import datetime
    import os
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
faceFrames=[]

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
                    g = camera.convertGray(f)                           #convert to grayscale
                    faces = camera.getFaces(g)                          #detect faces in gray frame
                
                    if len(faces) == 0 or len(faces) > 1:               #only continue with good data
                        pass

                    else:                                          
                        print("face found")
                        f = camera.highlightFace(f, faces)              #draw rectangle around detected face
                        faceFrames.append(f)                                 #record detected face frame
                        faceDetected = True

                if faceDetected == False:                               #if no faces are found upload anyways
                    print("no face found")
                    median = int(len(openFrames)/2)                     #find middle frame
                    print("uploading image")
                    Upload(openFrames[median], False)                   #upload image to the internet
                    timer = 30                                          #wait 30 seconds before attempting to capture again
                    print("delay", timer, " seconds")
                else:
                    median = int(len(faceFrames)/2)
                    print("uploading image")
                    Upload(faceFrames[median], True)                         #upload image to the internet
                    timer = 30                                          #wait 30 seconds before attempting to capture again
                    print("delay", timer, " seconds")

                faces=[]
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
