import numpy as np
import cv2
from django.conf import settings
import urllib
from uploadS3 import UploadToS3
from random import randrange, uniform
import os



class MakeVideoFX:
    imagePaths = []
    images = []
    MEDIA_PATH = settings.MEDIA_URL
    #MEDIA_PATH = "/home/ubuntu/django/app/minimal-django-file-upload-example/src/for_django_1-8/myproject/media/"

    def __init__(self, imagePaths0):
        self.imagePaths = imagePaths0

 
    def makeVideo (self):
        print "start video production"
        
        for imagePath in self.imagePaths:
            imageFullPath = self.MEDIA_PATH + imagePath
            req = urllib.urlopen(imageFullPath)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr,-1) # 'load it as it is'
            #img = cv2.imread(imageFullPath)
            print "image"
            print imageFullPath
            img = cv2.resize(img, (480, 320))
            self.images.append(img)
        
        for image in self.images:
            self.height , self.width , self.layers =  image.shape
            break;
            
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 1
        
        video = cv2.VideoWriter('video.avi',fourcc,fps,(self.width,self.height))

        for image in self.images:
            video.write(image)

        cv2.destroyAllWindows()
        video.release()
        # uploadToS3 = UploadToS3()
        # uploadToS3.uploadFile('video.avi')
        

class ImageEffects:
    EXTRA_PATH = 'output/'
    LOCAL_PATH = '/home/ubuntu/django/app/minimal-django-file-upload-example/src/for_django_1-8/myproject/media/'

    MEDIA_PATH = settings.MEDIA_URL
    dstFileName = ""

    def __init__(self, imgPath, imgFXPath, owner):
        self.imgPath = imgPath
        self.imgFXPath = imgFXPath
        self.owner = owner
    
    def applyFX (self):
        print 'Read images 1 and 2'
        req1 = urllib.urlopen(self.imgPath)
        arr1 = np.asarray(bytearray(req1.read()), dtype=np.uint8)
        img1 = cv2.imdecode(arr1,-1)
        
        req2 = urllib.urlopen(self.imgFXPath)
        arr2 = np.asarray(bytearray(req2.read()), dtype=np.uint8)
        img2 = cv2.imdecode(arr2,-1)

        if not img1.data:
            print '############################## ERROR WITH img1'
        else:
            print '########### img1 is loaded'
        if not img2.data:
            print '############################## ERROR WITH img2'
        else:
            print '########### img2 is loaded'
            
        height , width , layers =  img1.shape
        img2 = cv2.resize(img2, (width, height))

        dst = cv2.addWeighted(img1,0.7,img2,0.3,0)
        randomNumber = str(randrange(0, 1000000))
        self.dstFileName = self.owner +'_output_' + randomNumber + '.jpg'
        
        #Write the file in the local storage
        cv2.imwrite(self.dstFileName ,dst)
        
        #Upload to S3 cloud
        uploadToS3 = UploadToS3()
        uploadToS3.uploadFile(self.dstFileName, 'media/'+ self.owner + '//')
        
        #Remove the file from the local storage after sending it to the S3 cloud
        os.remove(self.dstFileName)

    def getDstPath (self):
        fullPath = self.owner + '//' + self.dstFileName
        return fullPath 


class FaceDetection:
    imagePath = ''
    
    def __init__(self, imgpath):
        self.imagePath = imgpath

        
    cascPath = '/home/ubuntu/django/app/minimal-django-file-upload-example/src/for_django_1-8/myproject/myproject/myapp/static/haarcascade_frontalface_default.xml'
    #imagePath = imgpath

    def detect(self):
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(self.cascPath)

        # Read the image
        image = cv2.imread(self.imagePath)
        #print image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #gray = np.array(gray, dtype='uint8')

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        print "Found {0} faces!".format(len(faces))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #cv2.imshow('messigray.png',img)
        cv2.imwrite("/home/ubuntu/django/app/minimal-django-file-upload-example/src/for_django_1-8/myproject/media/output.jpg" ,image)
        #cv2.waitKey(0)