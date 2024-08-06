from PyQt5 import uic

with open("giris_.py","w",encoding="utf-8") as fout:
    uic.compileUi("giris.ui", fout)


with open("ana_sayfa.py","w",encoding="utf-8") as fout:
    uic.compileUi("anasayfa.ui", fout)



with open("misafir_giris.py","w",encoding="utf-8") as fout:
    uic.compileUi("misafirgiris.ui", fout)



with open("ogrenci_giris.py","w",encoding="utf-8") as fout:
    uic.compileUi("ogrencigiris.ui", fout)



with open("akademisyen_giris.py","w",encoding="utf-8") as fout:
    uic.compileUi("akademisyen.ui", fout)


with open("akademisyen_cikis.py","w",encoding="utf-8") as fout:
    uic.compileUi("akademisyencikis.ui", fout)


with open("ogrenci_cikis.py","w",encoding="utf-8") as fout:
    uic.compileUi("ogrencicikis.ui", fout)


with open("misafir_cikis.py","w",encoding="utf-8") as fout:
    uic.compileUi("misafircikisi.ui", fout)


