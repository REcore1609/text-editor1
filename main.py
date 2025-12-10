#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import *
from PyQt5.QtWidgets import ( QApplication, QWidget, QPushButton, QHBoxLayout, 
QVBoxLayout, QLabel, QListWidget, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QPixmap
import os
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

app = QApplication([])

files_list = QListWidget()
image = QLabel('Картинка')

Button_Folder = QPushButton('Папка')
Button_Save = QPushButton('Сохранить')
Button_Reset = QPushButton('Сбросить')
Button_Left = QPushButton('Лево')
Button_Right = QPushButton('Право')
Button_Mirror = QPushButton('Зеркало')
Button_Contrast = QPushButton('Резкость')
Button_BlacknWhite = QPushButton('Ч/Б')

layout_main = QHBoxLayout()
layoutV1 = QVBoxLayout()
layoutV2 = QVBoxLayout()
layoutHDown = QHBoxLayout()

layoutV1.addWidget(Button_Save)
layoutV1.addWidget(Button_Reset)
layoutV1.addWidget(Button_Folder)
layoutHDown.addWidget(Button_Left)
layoutHDown.addWidget(Button_Right)
layoutHDown.addWidget(Button_Mirror)
layoutHDown.addWidget(Button_Contrast)
layoutHDown.addWidget(Button_BlacknWhite)
layoutV1.addWidget(files_list)
layoutV2.addWidget(image, 95)
layoutV2.addLayout(layoutHDown)
layout_main.addLayout(layoutV1, stretch = 1)
layout_main.addLayout(layoutV2, stretch = 5)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return(result)

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', 'bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    files_list.clear()
    for filename in filenames:
        files_list.addItem(filename)

Button_Folder.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
        self.original_image = None
    
    def loadimage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)
        self.original_image = self.image.copy()
    
    def showimage(self, path):
        image.hide()
        pixmapimage = QPixmap(path)
        label_width, label_height = image.width(), image.height()
        pixmapimage = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        image.setPixmap(pixmapimage)
        image.show()
    
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    
    def resetImage(self):
        if self.original_image is None:
            return
        self.image = self.original_image.copy()
        self.showimage(os.path.join(workdir, self.filename))

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)
    
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)
    
    def do_rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)
    
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

def showChosenImage():
    if files_list.currentRow() >= 0:
        filename = files_list.currentItem().text()
        workimage.loadimage(filename)
        workimage.showimage(os.path.join(workdir, workimage.filename))

workimage = ImageProcessor()

files_list.currentRowChanged.connect(showChosenImage)

Button_BlacknWhite.clicked.connect(workimage.do_bw)
Button_Mirror.clicked.connect(workimage.do_flip)
Button_Contrast.clicked.connect(workimage.do_sharpen)
Button_Left.clicked.connect(workimage.do_rotate_left)
Button_Right.clicked.connect(workimage.do_rotate_right)
Button_Reset.clicked.connect(workimage.resetImage)
Button_Save.clicked.connect(workimage.saveImage)

files_list.currentRowChanged.connect(showChosenImage)

main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.setLayout(layout_main)
main_win.resize(900, 700)
main_win.show()

app.exec()