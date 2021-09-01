import RPi.GPIO as io
import time
#import cv2
from picamera import PiCamera
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import psutil


def triggered(_imLoc, _imCount):
    
    iCount = _imCount + 1
    
    for n in range(4,0,-1):
        camera.annotate_text = str(n)
        time.sleep(1)
    io.output(3,io.HIGH)    
    camera.annotate_text = "Spaghettiiiiii"
    time.sleep(0.5)
    camera.annotate_text = ""
    sC=str(iCount)
    
    #save image
    imName = _imLoc + times + "-" +sC.zfill(4) +".jpg"
    camera.hflip = False
    camera.capture(imName)
    camera.hflip= True
    camera.stop_preview()
    
    #show img
    io.output(3,io.LOW)
    img = Image.open(imName)
    imgt= ImageDraw.Draw(img)
    myFont = ImageFont.truetype('FreeMono.ttf', 30)
    imgt.text((10,10),sC.zfill(4),font=myFont, fill=(255,0,0))
    img.show()
    
    time.sleep(5)
    
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()
        
    camera.start_preview()
    
    
    return iCount


###############
#Main Program
#
##############

print("Hy")

imLoc = '/home/pi/Pictures/Event'

io.setwarnings(False)
io.setmode(io.BCM)
io.setup(4, io.IN, pull_up_down=io.PUD_DOWN) # Trigger pin
io.setup(3, io.OUT) # Flash pin
io.output(3,io.LOW)

times = time.localtime()
camera = PiCamera()
camera.resolution=(1280,1024)
camera.rotation = 0
camera.hflip = True
#camera.mirror =1
camera.start_preview()
camera.annotate_text_size= 100
excount = 0
imcount = 0

# picture loop
while excount <= 3:
    traw = time.gmtime()
    times = time.strftime("%H-%M-%S ", traw)
    camera.annotate_text = "FOTOBOX"
    
    while io.input(4) == 1:
        b = 0 #idle
    
    #exit condition
    excount = 0    
    while io.input(4) == 0:
        excount +=1
        time.sleep(1)
        
    #exit
    if excount >= 3:
        print("EXIT")
        camera.close()
        time.sleep(1)
        exit()
    # take image
    else:
        print("trigger")
        time.sleep(0.5)
        imcount = triggered(imLoc, imcount)    
    #countdown timer
    
camera.stop_preview()
exit()




