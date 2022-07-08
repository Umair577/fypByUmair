from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import numpy as np
import cv2
from keras.models import load_model
import os
from keras.preprocessing import image
from PyQt5.QtWidgets import ( QMessageBox)
import PySimpleGUI as sg



class Ui_MainWindow(object):
    imagePath = " "
    batch_holder = None
    model = load_model('plant.h5')

    def backtoMain(self):
        self.stackedWidget.setCurrentIndex(0)
    def Preprocessing(self):
        self.stackedWidget.setCurrentIndex(1)
    def Classifier(self):
        self.stackedWidget.setCurrentIndex(2)


    def uploadimage(self):
            fname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image File", '.', "(*.jpg *.png)")
            self.imagePath = fname
            img = cv2.imread(self.imagePath)
            cv2.imwrite('Original_Pic.jpg', img)
            self.ImageView.setPixmap(QPixmap('Original_Pic.jpg'))

    def removeimage(self):

        self.ImageView.setText(" ")
        self.Image_PPout.setText(" ")
        self.ImageView2.setText(" ")
        if os.path.isfile('Original_Pic.jpg'):
            os.remove('Original_Pic.jpg')
        else:
            self.imagePath = " "

    def resizeimg(self):
            if self.imagePath == " ":
                    self.Image_PPout.setText(" ")
            else:
                    img = cv2.imread('Original_Pic.jpg')
                    res = cv2.resize(img, (250, 250))
                    cv2.imwrite(self.imagePath, res)
                    self.Image_PPout.setPixmap(QPixmap('Original_Pic.jpg'))


    def contrast(self):
            if self.imagePath == " ":
                    (self.image_PP.setPixmap(QPixmap("Pic/qq.png")))
            else:
                    img = cv2.imread('Original_Pic.jpg', cv2.IMREAD_COLOR)
                    norm_img1 = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                    norm_img2 = (255 * norm_img1).astype(np.uint8)
                    cv2.imwrite('Original_Pic.jpg', norm_img2)
                    self.Image_PPout.setPixmap(QPixmap('Original_Pic.jpg'))


    def median(self):
            if self.imagePath == " ":
                    (self.image_PP.setPixmap(QPixmap("Pic/qq.png")))
            else:
                    img = cv2.imread('Original_Pic.jpg')
                    median = cv2.medianBlur(img, 3)
                    cv2.imwrite('Original_Pic.jpg', median)
                    self.Image_PPout.setPixmap(QPixmap('Original_Pic.jpg'))
                    self.ImageView2.setPixmap(QPixmap('Original_Pic.jpg'))
    def clear1(self):
            self.Image_PPout.setText(" ")
            self.ImageView2.setText(" ")
    def nexttoclass(self):
        self.stackedWidget.setCurrentIndex(2)
        self.cinput.setPixmap(QPixmap('Original_Pic.jpg'))

    def closeEvent(self, event):
            reply = QMessageBox.question(
                    self, "Message",
                    "Are you sure you want to quit?",
                     QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                    event.accept()
            else:
                    event.ignore()
    def read_imagesnew(self,imgpath):
        self.batch_holder = np.zeros((1, 100, 100, 3))
        img = image.load_img(os.path.join(imgpath), target_size=(100, 100))

        self.batch_holder[0, :] = img
        return self.batch_holder
    def predict(self):
            labels = ['Grape Black_rot',
                      'Grape Esca',
                      'Grape Leaf_blight',
                      'Grape healthy',
                      'Peach Bacterial_spot',
                      'Peach healthy'
                      ]

            self.read_imagesnew(self.imagePath)
            for i, img in enumerate(self.batch_holder):
                    result = self.model.predict(self.batch_holder)
                    #print(result)
                    result_classes = result.argmax(axis=-1)
                    #print(result_classes[0])
                    check = labels[result_classes[0]]
                    if result_classes == [0]:
                           self.prediction.setText("Class Grape \nDisease Black Rot")
                           self.pests.setText("Recommended Pesticides:Mancozeb, and Ziram. \nThese are highly effective against Grape Black Rot.")

                    elif result_classes == [1]:
                           self.prediction.setText("Class Grape \nDisease Esca")
                           self.pests.setText(
                                   "A mixture of antimicrobial molecules\ninhibit mycelial growth and spore germination.")

                    elif result_classes == [2]:
                           self.prediction.setText("Class Grape \nDisease Leaf Blight")
                           self.pests.setText("Spraying fungicides like Bordeaux mixture @ 0.8% \nor Copper Oxychloride @ 0.25%")
                    elif result_classes == [3]:
                           self.prediction.setText("Class Grape \nHealthy Leaf ")
                           self.pests.setText("Healthy Leaf No Pesticides Required")
                    elif result_classes == [4]:
                           self.prediction.setText("Class peach \nDisease Bacterial Spot")
                           self.pests.setText("Use copper in dormant and early season \nor Use chemicals that contain zinc and ziram sulfate")
                    elif result_classes == [5]:
                           self.prediction.setText("Class Peach \nHealthy Leaf")
                           self.pests.setText("Healthy Leaf No Pesticides Required")
    def clear2(self):
            self.ImageView2.setText(" ")
            self.prediction.setText(" ")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 599)
        MainWindow.setMinimumSize(QtCore.QSize(873, 599))
        MainWindow.setMaximumSize(QtCore.QSize(873, 599))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/Icocn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 871, 601))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet("background-color: rgb(234, 234, 234); ")
        self.stackedWidget.setObjectName("stackedWidget")
        self.Mian = QtWidgets.QWidget()
        self.Mian.setObjectName("Mian")

        self.BtnPP = QtWidgets.QPushButton(self.Mian)
        self.BtnPP.setGeometry(QtCore.QRect(395, 510, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.BtnPP.setFont(font)
        self.BtnPP.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnPP.setObjectName("BtnPP")
        self.BtnPP.clicked.connect(self.Preprocessing)
        self.BtnClass = QtWidgets.QPushButton(self.Mian)
        self.BtnClass.setGeometry(QtCore.QRect(565, 510, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.BtnClass.setFont(font)
        self.BtnClass.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnClass.setObjectName("BtnClass")
        self.BtnClass.clicked.connect(self.Classifier)

        self.label_7 = QtWidgets.QLabel(self.Mian)
        self.label_7.setGeometry(QtCore.QRect(0, 100, 871, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_7.setLineWidth(3)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.Header1 = QtWidgets.QLabel(self.Mian)
        self.Header1.setGeometry(QtCore.QRect(0, 0, 871, 101))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(60)
        self.Header1.setFont(font)
        self.Header1.setStyleSheet("color: rgb(251, 248, 255);\n"
"background-color: rgb(0, 103, 120)")
        self.Header1.setFrameShape(QtWidgets.QFrame.Panel)
        self.Header1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Header1.setLineWidth(6)
        self.Header1.setAlignment(QtCore.Qt.AlignCenter)
        self.Header1.setObjectName("Header1")

        self.ImageView = QtWidgets.QLabel(self.Mian)
        self.ImageView.setGeometry(QtCore.QRect(400, 200, 300,300))
        self.ImageView.setFrameShape(QtWidgets.QFrame.Panel)
        self.ImageView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ImageView.setLineWidth(2)
        self.ImageView.setScaledContents(True)
        self.ImageView.setText("")
        self.ImageView.setObjectName("ImageView")

        self.Btn_Upload = QtWidgets.QPushButton(self.Mian)
        self.Btn_Upload.setGeometry(QtCore.QRect(30, 290, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.Btn_Upload.setFont(font)
        self.Btn_Upload.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));;border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.Btn_Upload.setObjectName("Btn_Upload")
        self.Btn_Upload.clicked.connect(self.uploadimage)
        self.Btn_remove = QtWidgets.QPushButton(self.Mian)
        self.Btn_remove.setGeometry(QtCore.QRect(30, 370, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.Btn_remove.setFont(font)
        self.Btn_remove.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.Btn_remove.setObjectName("Btn_remove")
        self.Btn_remove.clicked.connect(self.removeimage)
        self.Image = QtWidgets.QLabel(self.Mian)
        self.Image.setGeometry(QtCore.QRect(400, 160, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.Image.setFont(font)
        self.Image.setStyleSheet("color: rgb(251, 248, 255);\n"
"background-color: rgb(0, 103, 120)")
        self.Image.setFrameShape(QtWidgets.QFrame.Panel)
        self.Image.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Image.setLineWidth(2)
        self.Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Image.setObjectName("Image")
        self.stackedWidget.addWidget(self.Mian)
        self.pre = QtWidgets.QWidget()
        self.pre.setObjectName("pre")
        self.Header2 = QtWidgets.QLabel(self.pre)
        self.Header2.setGeometry(QtCore.QRect(0, 0, 871, 101))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(50)
        font.setItalic(True)
        self.Header2.setFont(font)
        self.Header2.setStyleSheet("color: rgb(251, 248, 255);\n"
"background-color: rgb(0, 103, 120)")
        self.Header2.setFrameShape(QtWidgets.QFrame.Panel)
        self.Header2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Header2.setLineWidth(10)
        self.Header2.setAlignment(QtCore.Qt.AlignCenter)
        self.Header2.setObjectName("Header2")

        self.BtnResize = QtWidgets.QPushButton(self.pre)
        self.BtnResize.setGeometry(QtCore.QRect(30, 200, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.BtnResize.setFont(font)
        self.BtnResize.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnResize.setObjectName("BtnResize")
        self.BtnResize.clicked.connect(self.resizeimg)
        self.BtnContrast = QtWidgets.QPushButton(self.pre)
        self.BtnContrast.setGeometry(QtCore.QRect(30, 270, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.BtnContrast.setFont(font)
        self.BtnContrast.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnContrast.setObjectName("BtnContrast")
        self.BtnContrast.clicked.connect(self.contrast)
        self.BtnNoiseR = QtWidgets.QPushButton(self.pre)
        self.BtnNoiseR.setGeometry(QtCore.QRect(30, 340, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.BtnNoiseR.setFont(font)
        self.BtnNoiseR.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnNoiseR.setObjectName("BtnNoiseR")
        self.BtnNoiseR.clicked.connect(self.median)
        self.BtnBack1 = QtWidgets.QPushButton(self.pre)
        self.BtnBack1.setGeometry(QtCore.QRect(30, 530, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.BtnBack1.setFont(font)
        self.BtnBack1.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnBack1.setObjectName("BtnBack1")
        self.BtnBack1.clicked.connect(self.backtoMain)
        self.BtnClr1 = QtWidgets.QPushButton(self.pre)
        self.BtnClr1.setGeometry(QtCore.QRect(30, 410, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.BtnClr1.setFont(font)
        self.BtnClr1.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnClr1.setObjectName("BtnClr1")
        self.BtnClr1.clicked.connect(self.clear1)

        self.Image_PPout = QtWidgets.QLabel(self.pre)
        self.Image_PPout.setGeometry(QtCore.QRect(400, 220, 250, 250))
        self.Image_PPout.setFrameShape(QtWidgets.QFrame.Panel)
        self.Image_PPout.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Image_PPout.setLineWidth(2)
        self.Image_PPout.setText("")
        self.Image_PPout.setObjectName("Image_PPout")


        self.oImage = QtWidgets.QLabel(self.pre)
        self.oImage.setGeometry(QtCore.QRect(400, 179, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.oImage.setFont(font)
        self.oImage.setStyleSheet("color: rgb(251, 248, 255);\n"
"background-color:rgb(0, 103, 120);")
        self.oImage.setFrameShape(QtWidgets.QFrame.Panel)
        self.oImage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.oImage.setLineWidth(2)
        self.oImage.setAlignment(QtCore.Qt.AlignCenter)
        self.oImage.setObjectName("oImage")
        self.PP_Header = QtWidgets.QLabel(self.pre)
        self.PP_Header.setGeometry(QtCore.QRect(0, 100, 871, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        font.setItalic(True)
        self.PP_Header.setFont(font)
        self.PP_Header.setFrameShape(QtWidgets.QFrame.Box)
        self.PP_Header.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PP_Header.setLineWidth(3)
        self.PP_Header.setAlignment(QtCore.Qt.AlignCenter)
        self.PP_Header.setObjectName("PP_Header")

        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)

        self.btnpnxt = QtWidgets.QPushButton(self.pre)
        self.btnpnxt.setGeometry(QtCore.QRect(400, 500, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.btnpnxt.setFont(font)
        self.btnpnxt.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.btnpnxt.setObjectName("btnpnxt")
        self.btnpnxt.clicked.connect(self.Classifier)
        self.stackedWidget.addWidget(self.pre)
        self.classi = QtWidgets.QWidget()
        self.classi.setObjectName("classi")


        self.BtnPred = QtWidgets.QPushButton(self.classi)
        self.BtnPred.setGeometry(QtCore.QRect(330, 480, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.BtnPred.setFont(font)
        self.BtnPred.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnPred.setChecked(False)
        self.BtnPred.clicked.connect(self.predict)
        self.BtnPred.setObjectName("BtnPred")
        self.BtnBack2 = QtWidgets.QPushButton(self.classi)
        self.BtnBack2.setGeometry(QtCore.QRect(30, 540, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.BtnBack2.setFont(font)
        self.BtnBack2.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnBack2.setObjectName("BtnBack2")
        self.BtnBack2.clicked.connect(self.Preprocessing)
        self.BtnClr2 = QtWidgets.QPushButton(self.classi)
        self.BtnClr2.setGeometry(QtCore.QRect(30, 300, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.BtnClr2.setFont(font)
        self.BtnClr2.setStyleSheet("QPushButton {color: rgb(232, 249, 253);\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(130, 219, 216), stop:1 rgb(59, 172, 182));border-radius:10px;}\n"
"QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnClr2.setObjectName("BtnClr2")
        self.BtnClr2.clicked.connect(self.clear2)

        self.BtnExt = QtWidgets.QPushButton(self.classi)
        self.BtnExt.setGeometry(QtCore.QRect(30, 370, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.BtnExt.setFont(font)
        self.BtnExt.setStyleSheet("QPushButton {color: rgb(255,255,255);\n"
                                   "background-color:rgb(255,0,0);border-radius:10px;}\n"
                                   "QPushButton:pressed { background-color: rgb(189, 213, 234); border-radius:10px; ;}")
        self.BtnExt.setObjectName("BtnClr2")
        self.BtnExt.clicked.connect(self.closeEvent)

        self.ImageView2 = QtWidgets.QLabel(self.classi)
        self.ImageView2.setGeometry(QtCore.QRect(310, 220, 250, 250))
        self.ImageView2.setFrameShape(QtWidgets.QFrame.Box)
        self.ImageView2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ImageView2.setLineWidth(3)
        self.ImageView2.setText("")
        self.ImageView2.setObjectName("ImageView2")
        self.Image2 = QtWidgets.QLabel(self.classi)
        self.Image2.setGeometry(QtCore.QRect(310, 179, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Image2.setFont(font)
        self.Image2.setStyleSheet("color: rgb(251, 248, 255);;\n"
"background-color: rgb(0, 103, 120)")
        self.Image2.setLineWidth(0)
        self.Image2.setAlignment(QtCore.Qt.AlignCenter)
        self.Image2.setObjectName("Image2")
        self.Classifier_header = QtWidgets.QLabel(self.classi)
        self.Classifier_header.setGeometry(QtCore.QRect(0, 100, 871, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        font.setItalic(True)
        self.Classifier_header.setFont(font)
        self.Classifier_header.setFrameShape(QtWidgets.QFrame.Box)
        self.Classifier_header.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Classifier_header.setLineWidth(3)
        self.Classifier_header.setAlignment(QtCore.Qt.AlignCenter)
        self.Classifier_header.setObjectName("Classifier_header")
        self.Result_box = QtWidgets.QGroupBox(self.classi)
        self.Result_box.setGeometry(QtCore.QRect(580, 180, 261, 201))
        font = QtGui.QFont()
        font.setFamily("Microsoft Himalaya")
        font.setPointSize(16)
        self.Result_box.setFont(font)
        self.Result_box.setObjectName("Result_box")
        self.prediction = QtWidgets.QLabel(self.Result_box)
        self.prediction.setGeometry(QtCore.QRect(10, 80, 241, 71))
        self.prediction.setFrameShape(QtWidgets.QFrame.Box)
        self.prediction.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.prediction.setLineWidth(2)
        self.prediction.setText("")
        self.prediction.setObjectName("prediction")
        self.label_35 = QtWidgets.QLabel(self.Result_box)
        self.label_35.setGeometry(QtCore.QRect(10, 30, 241, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")

        self.recommendation = QtWidgets.QGroupBox(self.classi)
        self.recommendation.setGeometry(QtCore.QRect(580, 400, 301, 201))
        font = QtGui.QFont()
        font.setFamily("Microsoft Himalaya")
        font.setPointSize(16)
        self.recommendation.setFont(font)
        self.recommendation.setObjectName("Recommendation_Box")
        self.pests = QtWidgets.QLabel(self.recommendation)
        self.pests.setGeometry(QtCore.QRect(10, 80, 281, 71))
        self.pests.setFrameShape(QtWidgets.QFrame.Box)
        self.pests.setFrameShadow(QtWidgets.QFrame.Sunken)
        font = QtGui.QFont()
        font.setFamily("Microsoft Himalaya")
        font.setPointSize(14)
        self.pests.setFont(font)
        self.pests.setLineWidth(2)
        self.pests.setText("")
        self.pests.setObjectName("Pests")
        self.pesticides = QtWidgets.QLabel(self.recommendation)
        self.pesticides.setGeometry(QtCore.QRect(10, 30, 241, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pesticides.setFont(font)
        self.pesticides.setAlignment(QtCore.Qt.AlignCenter)
        self.pesticides.setObjectName("pesticides")


        self.Header3 = QtWidgets.QLabel(self.classi)
        self.Header3.setGeometry(QtCore.QRect(0, 0, 871, 101))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(60)
        font.setItalic(True)
        self.Header3.setFont(font)
        self.Header3.setStyleSheet("color: rgb(251, 248, 255);\n"
"background-color: rgb(0, 103, 120)")
        self.Header3.setFrameShape(QtWidgets.QFrame.Panel)
        self.Header3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Header3.setLineWidth(6)
        self.Header3.setAlignment(QtCore.Qt.AlignCenter)
        self.Header3.setObjectName("Header3")
        self.stackedWidget.addWidget(self.classi)




        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Integrated Deep Learning Framework Of Fruit Plant Diseases"))
        self.BtnPP.setText(_translate("MainWindow", "Pre-Processing"))
        self.BtnClass.setText(_translate("MainWindow", "Classifier"))

        self.label_7.setText(_translate("MainWindow", "Main Window"))
        self.Header1.setText(_translate("MainWindow", "Integrated Deep Learning Framework Of Fruit Plant Diseases"))
        self.Btn_Upload.setText(_translate("MainWindow", "Upload Image"))
        self.Btn_remove.setText(_translate("MainWindow", "Delete Image"))
        self.Image.setText(_translate("MainWindow", "Input Image"))
        self.Header2.setText(_translate("MainWindow", "Integrated Deep Learning Framework Of Fruit Plant Diseases"))
        self.BtnResize.setText(_translate("MainWindow", "Image Resizing"))
        self.BtnContrast.setText(_translate("MainWindow", "Image Enhancement"))
        self.BtnNoiseR.setText(_translate("MainWindow", "Noise Removal"))
        self.BtnBack1.setText(_translate("MainWindow", "Back"))
        self.BtnClr1.setText(_translate("MainWindow", "Clear All"))

        self.oImage.setText(_translate("MainWindow", "Output Image"))
        self.PP_Header.setText(_translate("MainWindow", "Pre-Processing"))

        self.btnpnxt.setText(_translate("MainWindow", "Next"))
        self.BtnPred.setText(_translate("MainWindow", "Prediction"))
        self.BtnBack2.setText(_translate("MainWindow", "Back"))
        self.BtnClr2.setText(_translate("MainWindow", "Clear All"))
        self.BtnExt.setText(_translate("MainWindow", "Exit"))
        self.Image2.setText(_translate("MainWindow", "Input Image"))
        self.Classifier_header.setText(_translate("MainWindow", "Classifier"))
        self.Result_box.setTitle(_translate("MainWindow", "Results"))
        self.label_35.setText(_translate("MainWindow", "Prediction"))
        self.recommendation.setTitle(_translate("MainWindow", "Recommendations"))
        self.pesticides.setText(_translate("MainWindow", "Pesticides"))
        self.Header3.setText(_translate("MainWindow", "Integrated Deep Learning Framework Of Fruit Plant Diseases"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IMAGE_FILE = "assets/2.png"
    time = 3000

    sg.Window('Window Title', [[sg.Image(IMAGE_FILE)]], transparent_color=sg.theme_background_color(), no_titlebar=True,
              keep_on_top=True).read(timeout=time, close=True)



    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

