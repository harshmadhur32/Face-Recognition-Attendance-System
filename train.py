import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from urllib.request import urlopen
from ssl import SSLContext, PROTOCOL_TLSv1

window = tk.Tk()
window.title("Attendance System Develop By Sandeep & Aman")
dialog_title = 'QUIT'
window.geometry('1366x768')
window.configure()  # background='grey')
window.configure(background='white')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
path2 = "img0.JFIF"
# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img2 = ImageTk.PhotoImage(Image.open(path2))
# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel2 = tk.Label(window, image=img2)
panel2.pack(side="top", fill="x", expand="no")
panel2.place(x=100, y=200)
message = tk.Label(window, text="TEERTHANKER MAHAVEER UNIVERSITY MBD", bg="white",
                   fg="black", width=40, height=3, font=('Times New Roman', 40, 'italic bold underline'))

message.place(x=60, y=20)

lbl = tk.Label(window, text="Student id", width=20, height=2,
               fg="white", bg="green", font=('times', 15, ' bold '))
lbl.place(x=400, y=200)

txt = tk.Entry(window, width=20, bg="green",
               fg="white", font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Student Name", width=20, fg="white",
                bg="green", height=2, font=('times', 15, ' bold '))
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window, width=20, bg="green",
                fg="white", font=('times', 15, ' bold '))
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Notification : ", width=20, fg="white",
                bg="green", height=2, font=('times', 15, ' bold '))
lbl3.place(x=400, y=400)

message = tk.Label(window, text="", bg="green", fg="white", width=30,
                   height=2, activebackground="yellow", font=('times', 15, ' bold '))
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Attendance : ", width=20, fg="white",
                bg="green", height=2, font=('times', 15, ' bold  underline'))
lbl3.place(x=400, y=570)

message2 = tk.Label(window, text="", fg="white", bg="green",
                    activeforeground="green", width=30, height=2, font=('times', 15, ' bold '))
message2.place(x=700, y=570)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        #url= 'http://192.168.43.73:8080/shot.jpg'
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            # gcontext = SSLContext(PROTOCOL_TLSv1)  # Only for gangstars
            #info = urlopen(url, context=gcontext).read()

            # imgNp=np.array(bytearray(info),dtype=np.uint8)
            # image_frame=cv2.imdecode(imgNp,-1)

            # Convert frame to grayscale
            #gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

            # Detect frames of different sizes, list of faces rectangles
            #faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum+1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('EmployeeDetails\EmployeeDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text=res)


def TrainImages():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Corrected function from opencv-contrib
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, Id = getImagesAndLabels("TrainingImage")
        if len(faces) == 0 or len(Id) == 0:
            message.configure(text="No images found to train.")
            return
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        res = "Image Trained Successfully!"
        message.configure(text=res)
    except Exception as e:
        message.configure(text=f"Error: {str(e)}")
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    #recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer=cv2.createLBPHFaceRecognizer()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("EmployeeDetails\EmployeeDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) +
                            ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        # if (cv2.waitKey(10000)):
        #  break
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    # cv2.waitKey
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)


clearButton = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow",
                        width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="red", bg="yellow",
                         width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)
takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="red", bg="yellow",
                    width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
takeImg.place(x=100, y=470)
trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="red",
                     bg="yellow", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
trainImg.place(x=400, y=470)
trackImg = tk.Button(window, text="Track Images", command=TrackImages, fg="red",
                     bg="yellow", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
trackImg.place(x=700, y=470)
quitWindow = tk.Button(window, text="Quit", command=quit, fg="red", bg="yellow",
                       width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=980, y=470)

window.mainloop()
