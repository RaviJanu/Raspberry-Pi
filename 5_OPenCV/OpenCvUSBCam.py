#!!AUM!!

from picamera import PiCamera
from picamera.array import PiRGBArray
import pytesseract
# Import OpenCV2 for image processing
# Import os for file path
import cv2
import os
# Import numpy for matrix calculation
import numpy as np
# Import Python Image Library (PIL)
from PIL import Image
import pytesseract
import time
import RPi.GPIO as GPIO
from subprocess import call



class OpenCvClass:
    def init(self,resol_x,resol_y,fr):
        print ('initialize the camera and grab a reference to the raw camera capture')
        self.camera = PiCamera()
        self.camera.resolution = (resol_x, resol_y)
        self.camera.framerate = fr
        self.rawCapture = PiRGBArray(self.camera, size=(resol_x, resol_y))
        print('allow the camera to warmup')
        time.sleep(1)
        return self.camera,self.rawCapture
        
    def captureframe(self,UserNum):
        print('capture frames from the camera')
        captureImagenum = 1
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
#               print('grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text')
                image = frame.array
#               print('show the frame')
                cv2.imshow("Frame", image)
                key = cv2.waitKey(1) & 0xFF
#               print('clear the stream in preparation for the next frame')
                self.rawCapture.truncate(0)
#               print('if the q key was pressed, break from the loop')
                if GPIO.input(3) == False:
                    print ("Image Captured - User"+str(UserNum)+"."+str(captureImagenum)+'.jpg')
                    self.camera.capture('dataset/User'+str(UserNum)+'.'+str(captureImagenum)+'.jpg')
                    captureImagenum += 1
                    time.sleep(1)
                
                if GPIO.input(4) == False:
                    self.stop_cam()
                    return 


    def getImagesAndLabels(self,path):
#       print ('Create method to get the images and label data')
#       print('Get all file path')
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
#       print('Initialize empty face sample')
        faceSamples=[]
#       print('Initialize empty id')
        ids = []
#       print('Loop all the file path')
        for imagePath in imagePaths:
#           print('Get the image and convert it to grayscale')
            PIL_img = Image.open(imagePath).convert('L')
#           print('PIL image to numpy array')
            img_numpy = np.array(PIL_img,'uint8')
#           print('Get the image id')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            print(id)
#           print('Get the face from the training images')
            faces = self.detector.detectMultiScale(img_numpy)
#           print('Loop for each face, append to their respective ID')
            for (x,y,w,h) in faces:
#               print('Add the image to face samples')
                faceSamples.append(img_numpy[y:y+h,x:x+w])
#               print('Add the ID to IDs')
                ids.append(id)
        print('Pass the face array and IDs array')
        return faceSamples,ids

                    
    def training(self):
        print('Create Local Binary Patterns Histograms for face recognization')
        recognizer = cv2.face.createLBPHFaceRecognizer()
        print('Using prebuilt frontal face training model, for face detection')
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        print('Get the faces and IDs')
        faces,ids = self.getImagesAndLabels('dataset')
        print('Train the model using the faces and IDs')
        recognizer.train(faces, np.array(ids))
        print('Save the model into trainer.yml')
        recognizer.save('trainer/trainer.yml')
                

    def face_recognization(self,person_name):
#        self.camera.start_preview()
        print('Create Local Binary Patterns Histograms for face recognization')
        recognizer = cv2.face.createLBPHFaceRecognizer()
        print('Load the trained mode')
        recognizer.load('trainer/trainer.yml')
        print('Load prebuilt model for Frontal Face')
        cascadePath = "haarcascade_frontalface_default.xml"
        print('Create classifier from prebuilt model')
        faceCascade = cv2.CascadeClassifier(cascadePath);
        print('Set the font style')
        font = cv2.FONT_HERSHEY_SIMPLEX
        print('Initialize and start the video frame capture')
        cam = cv2.VideoCapture(0)
        
        print('Loop')
        while True:
            # Read the video frame
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Get all face from the video frame
            faces = faceCascade.detectMultiScale(gray, 1.2,5)
            # For each face in faces
            for(x,y,w,h) in faces:
                # Create rectangle around the face
                cv2.rectangle(img, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
                # Recognize the face belongs to which ID
                Id = recognizer.predict(gray[y:y+h,x:x+w])
                # Check the ID if exist 
                if(Id == 1):
                    Id = person_name[0]
                    call(["espeak Hello_"+person_name[0]], shell=True)
                #If not exist, then it is Unknown
                elif(Id == 2):
                    Id = person_name[1]
                    call(["espeak Hello_"+person_name[1]], shell=True)
                else:
                    print(Id)
                    Id = "Unknow"
                # Put text describe who is in the picture
                cv2.rectangle(img, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.putText(img, str(Id), (x,y-40), font, 2, (255,255,255), 3)

            # Display the video frame with the bounded rectangle
            cv2.imshow('image',img) 
            # If 'q' is pressed, close program
            if cv2.waitKey(10) & 0xFF == ord('q'):
                print('Stop the camera')
                cam.release()
                print('Close all windows')
                cv2.destroyAllWindows()
                return
            if GPIO.input(4) == False:
                print('Stop the camera')
                cam.release()
                print('Close all windows')
                cv2.destroyAllWindows()
                time.sleep(2)
                return

    def Continous_imgToText(self):
        print('Initialize and start the video frame capture')
        cam = cv2.VideoCapture(1)
        
        while True:
            ret, img = cam.read()
#            print('show the frame')
            cv2.imshow("Frame", img)
            key = cv2.waitKey(1) & 0xFF
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#            print('Apply dilation and erosion to remove some noise')
            kernel = np.ones((1, 1), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
#            print('Write image after removed noise')
            cv2.imwrite("removed_noise.png", img)
            text = pytesseract.image_to_string(Image.open('removed_noise.png'), lang = 'eng')
            
            if text:
                text = text.replace(' ', '_')
                print (text)
                call(["espeak "+text], shell=True)
            else:
                print('*')
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                print('Stop the camera')
                cam.release()
                print('Close all windows')
                cv2.destroy

            if GPIO.input(4) == False:
                self.stop_cam()
                time.sleep(2)
                return 

    def single_img_ocr(self):
            img = cv2.imread("sample.jpg")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1, 1), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
            print('remove noice')
            cv2.imwrite("removed_noise.png", img)
            text = pytesseract.image_to_string(Image.open('removed_noise.png'), lang = 'eng')
            print('print text '+text)
                       
                
    def stop_cam(self):
        # Stop the camera
        #self.camera.release()
        # Close all windows
        cv2.destroyAllWindows()
        

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setwarnings(False)
        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        print ('Start Sample code')
        myCV = OpenCvClass()
#        myCV.init(640,480,32)
#        myCV.captureframe(1)
#        myCV.training()
        myCV.face_recognization(['Ravi','JTS'])
#        myCV.single_img_ocr()
#        myCV.Continous_imgToText()
        
    except KeyboardInterrupt:
        print ('Exit Project')
        myCV.stop_cam()






























