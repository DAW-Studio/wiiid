
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLTexture
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt
from OpenGL.GL import *
from PIL import Image


class OpenGLImage(QOpenGLWidget):
    def __init__(self, parent, image_path):
        super().__init__(parent=parent)
        # self.image_path = image_path
        self.texture = None

        images = [Image.open(path) for path in image_path]

        base_image = images[0].copy()

        for image in images[1:]:
            base_image.paste(image, (0,0), image)

        base_image.save("temp.png")
        self.image_path = "temp.png"

        # Load image and calculate aspect ratio
        with Image.open(self.image_path) as img:
            self.aspect_ratio_width = img.width
            self.aspect_ratio_height = img.height
        self.aspect_ratio = self.aspect_ratio_width / self.aspect_ratio_height

        # self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # Make widget background transparent
        # self.setAutoFillBackground(False)  # Disable Qt's background painting


    def initializeGL(self):
        glClearColor(1,1,1,1)
        glEnable(GL_TEXTURE_2D)

        image = QImage(self.image_path).convertToFormat(QImage.Format_RGBA8888)
        self.texture = QOpenGLTexture(image)
        self.texture.setMinificationFilter(QOpenGLTexture.Nearest)
        self.texture.setMagnificationFilter(QOpenGLTexture.Nearest)
        self.texture.setWrapMode(QOpenGLTexture.ClampToEdge)

    def resizeGL(self, w, h):
        # Set the OpenGL viewport to match the new size
        # new_height = int(w / self.aspect_ratio)
        # Set the widget's height to match the aspect ratio, while keeping the width fixed
        # self.setFixedWidth(new_height)
        self.setFixedWidth(self.image_width)
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        if self.texture:
            self.texture.bind()

            # Get widget's width and height
            width = self.width()
            height = self.height()
            
            # Calculate the aspect ratio of the widget
            aspect_ratio = width / height

            # Adjust coordinates based on the aspect ratio
            # if aspect_ratio > self.aspect_ratio:
            #     # If widget is wider than the image, adjust height
            #     new_height = height
            #     new_width = int(new_height * self.aspect_ratio)
            #     x_offset = (width - new_width) / 2.0
            #     y_offset = 0
            # else:
            #     # If widget is taller than the image, adjust width
            #     new_width = width
            #     new_height = int(new_width / self.aspect_ratio)
            #     x_offset = 0
            #     y_offset = (height - new_height) / 2.0

            new_height = height
            new_width = int(new_height * self.aspect_ratio)
            x_offset = (width - new_width) / 2.0
            y_offset = 0

            self.image_width = new_width

            # Scale the image into the normalized OpenGL coordinates
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(x_offset / width * 2 - 1, y_offset / height * 2 - 1)
            glTexCoord2f(1, 1); glVertex2f((x_offset + new_width) / width * 2 - 1, y_offset / height * 2 - 1)
            glTexCoord2f(1, 0); glVertex2f((x_offset + new_width) / width * 2 - 1, (y_offset + new_height) / height * 2 - 1)
            glTexCoord2f(0, 0); glVertex2f(x_offset / width * 2 - 1, (y_offset + new_height) / height * 2 - 1)
            glEnd()

            self.texture.release()


