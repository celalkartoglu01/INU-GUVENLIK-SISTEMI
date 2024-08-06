from PyQt5.QtWidgets import *
from ana_sayfa import Ui_MainWindow
from akademisyen import Akademisyen
from ogrenci import Ogrenci
from misafir import Misafir
from ogrencicikis import OgrenciCikis
from akademisyencikis import AkademisyenCikis
from misafircikis import MisafirCikis

class AnaSayfa(QMainWindow):
    def __init__(self)->None:
        super().__init__()
        self.anasayfa = Ui_MainWindow()
        self.anasayfa.setupUi(self)
        self.anasayfa.akademisyengiris.clicked.connect(self.AkademisyenGiris)
        self.anasayfa.ogrencigiris.clicked.connect(self.OgrenciGiris)
        self.anasayfa.misafirgiris.clicked.connect(self.MisafirGiris)
        self.anasayfa.ogrencicikis.clicked.connect(self.OgrenciCikis)
        self.anasayfa.akademisyencikis.clicked.connect(self.AkademisyenCikis)
        self.anasayfa.misafircikis.clicked.connect(self.MisafirCikis)
        self.akademisyen = Akademisyen()
        self.misafircikis = MisafirCikis()
        self.ogrenci = Ogrenci()
        self.misafir = Misafir()
        self.ogrencicikis = OgrenciCikis()
        self.akademisyencikis = AkademisyenCikis()
    
    def MisafirCikis(self):
        self.misafircikis.show()
    

    def AkademisyenGiris(self):
        self.akademisyen.show()
    
    def AkademisyenCikis(self):
        self.akademisyencikis.show()

    def OgrenciGiris(self):
        self.ogrenci.show()
    

    def MisafirGiris(self):
        self.misafir.show()
    

    def OgrenciCikis(self):
        self.ogrencicikis.show()