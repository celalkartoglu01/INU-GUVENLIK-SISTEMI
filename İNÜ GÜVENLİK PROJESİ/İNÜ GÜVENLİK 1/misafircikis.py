from PyQt5.QtWidgets import *
from misafir_cikis import Ui_Form
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import os
import mysql.connector
from ultralytics import YOLO
import pytesseract
import numpy as np
from PIL import Image
import re

con = mysql.connector.connect(user='root', password='', host='localhost', database='inuguvenlik')
cursor = con.cursor()


model = YOLO("plakatanima.pt")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class MisafirCikis(QWidget):
    def __init__(self)->None:
        super().__init__()
        self.misafir = Ui_Form()
        self.misafir.setupUi(self)
        self.misafir.aracsec.clicked.connect(self.AracSec)
        self.scene = QGraphicsScene(self)
        self.timer = QTimer(self)
        self.known_face_encodings = []
        self.known_face_names = []
        self.folder_path = "misafirler"
        self.file_path = None
        self.current_frame = None
        self.scene1 = QGraphicsScene(self)
        self.misafir.aracgoruntu.setScene(self.scene1)
        self.detected_plate = ""
        self.plate_counter = 1
        self.kayit = ""
        self.misafir.cikisiniyap.clicked.connect(self.CikisiniYap)
        self.photo_name = ""
        self.photo_path = ""
        self.is_capturing = False
    
    def clean_plate_text(self, text):
        text = text.upper()
        
        text = re.sub(r'[^A-Z0-9\s]', '', text)
        
        text = ' '.join(text.split())
        
        if text and text[0].isalpha():
            text = text[1:].lstrip()  
        
        return text
    
    def AracSec(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "*.png *.jpg *.jpeg")

        if self.file_path:
            pixmap = QPixmap(self.file_path)
            view_rect = self.misafir.aracgoruntu.rect()
            scaled_pixmap = pixmap.scaled(view_rect.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.scene1.clear()
            self.scene1.addPixmap(scaled_pixmap)
            self.misafir.aracgoruntu.setScene(self.scene1)
            self.misafir.aracgoruntu.horizontalScrollBar().setVisible(False)
            self.misafir.aracgoruntu.verticalScrollBar().setVisible(False)

            im1 = Image.open(self.file_path)

            results = model.predict(source=im1)

            result = results[0]

            boxes = result.boxes

            image_np = np.array(im1)

            for box in boxes.data:
                x1, y1, x2, y2, conf, cls = box
            
                if cls == 0: 
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                
                    plate_image = image_np[y1:y2, x1:x2]
                
                    plate_filename = f'plakalar/plate{self.plate_counter}.jpg'

                    self.plate_counter += 1
                    os.makedirs(os.path.dirname(plate_filename), exist_ok=True)
                    cv2.imwrite(plate_filename, plate_image)

                    plate_image = Image.open(plate_filename)

                    text = pytesseract.image_to_string(plate_image, config='--psm 8')

                    self.detected_plate = text.strip()
                    self.detected_plate = self.clean_plate_text(text)
                    self.misafir.plaka.setText(self.detected_plate)
                    query = "select * from misafirler where plaka = %s"
                    cursor.execute(query,(self.detected_plate,))
                    result = cursor.fetchone()
                    if result:
                        self.misafir.isim.setText(result[1])
                        self.misafir.soyisim.setText(result[2])
                        self.misafir.ziyaretsebebi.setText(result[3])
                    break
    
    def CikisiniYap(self):
        plaka = self.detected_plate
        isim = self.misafir.isim.text()
        soyisim = self.misafir.soyisim.text()
        isimsoyisim = isim + " " + soyisim
        query2 = "select * from girenaraclar where plaka = %s"
        cursor.execute(query2,(plaka,))
        result = cursor.fetchone()
        if result:
            giriszamani = result[3]
        query = "INSERT INTO cikanaraclar (aracsahibi,plaka,giriszamani) VALUES (%s, %s,%s)"
        cursor.execute(query,(isimsoyisim,plaka,giriszamani))
        con.commit()
        query1 = "DELETE FROM girenaraclar where plaka = %s"
        cursor.execute(query1,(plaka,))
        con.commit()
        query2 = "DELETE FROM misafirler where plaka = %s"
        cursor.execute(query2,(plaka,))
        con.commit()
        QMessageBox.information(self,"Uyarı","Çıkış Başarılı, Güle Güle !")
        self.misafir.isim.clear()
        self.misafir.soyisim.clear()
        self.misafir.ziyaretsebebi.clear()
        self.misafir.plaka.clear()
        self.scene.clear()
        self.scene1.clear()
    

   


    
 



    

    