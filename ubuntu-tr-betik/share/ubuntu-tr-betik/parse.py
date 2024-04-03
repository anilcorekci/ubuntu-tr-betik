#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
class parse(): 
    def __init__(self):
        pass
        
    def dosya(self,yaz=None):
        """ yazmak için ise yaz parametresi bir string , okumak için ise , 
        bir parametre yok , dosyayı satırlara böl ve geri dön """
        if type(yaz)  is str  :    
            with open(  "../../bin/ubuntu-tr-betik","wb") as file_:
                file_.write(bytes(yaz.encode()))
            file_.close() 
        else:
            return open( "../../bin/ubuntu-tr-betik").read().splitlines()     
               
    def fonksiyon_icerigi(self,fonksiyon_ismi  ):
        """  
        start_line   değişkeni parse sınıfının ortak değişkenidir . 
        Başlangıç   satırı bir fonksiyon silinirken veya değiştirilirken daha sonra , kullanılacaktır.
        
        bir satırda fonksiyon ismine denk geliniyorsa , ayirma_basladi değeri True ,
        buf fonksiyon içinde bulunan satırların içine eklendiği tanımsız liste,
        karakter_var , fonksiyon ismi ayıklanırken {} karakterlerini es geçmemek için.. 
        """
 
        self.start_line  = ""
        ayirma_basladi = None 
        buf = [] 
        karakter_var = 0  
 
           
        for line in self.dosya():
            """Eğer satır içinde fonksiyon ismine denk gelirsen başa dön 
            ve ayırmayı başlat"""
            if fonksiyon_ismi  in line and  "{"  in  line :
                #    print ( " Fonksiyon bulundu , %s " )  %  (fonksiyon_ismi ) 
                    ayirma_basladi = True
                    self.start_line = line
                    continue
            """ Ayırma başlamışsa { ve } karakterleni kontrol et
            bir satırın içinde yalnızca { denk gelirsen karakter_var'ı bir arttır
            bir satırın içinde yalnızca }  karakter_var"ı bir eksilt 
            eğer karakter_var 0  ise işlemi   bitir.. """                   
            if ayirma_basladi is True: 
                if  "{" in line and "}" in line:
                    pass
                elif "{" in line:   
                    karakter_var +=1                                         
                elif "}" in line:
                    if karakter_var == 0:
                        ayirma_basladi = None 
                        break
                    else:
                        karakter_var -=1                        
                buf.append(line)
                
             
                    
        return "\n".join(buf)
 
                
    def ekle(self,fonksiyon):
        """ Fonksiyon için uygun bir satır belirlenmeli.. 
        "#Paket bilgilerinin uygulayacağı fonksiyonlar@@@"
        O satır ise yukarıda tırnak içinde bulunan kısım , dosya açılır ,
        Yeni fonksiyon ilgili satırdan sonra eklenir.
        """
        buf = [] 
        ilgili_satir = "#Paket bilgilerinin uygulayacağı fonksiyonlar@@@"

        for line in self.dosya():
            if line == ilgili_satir:
                buf.append("%s\n%s(){\n\t echo 'Yeni fonksiyon eklendi'\n} " %(ilgili_satir , fonksiyon) )
            else:
                buf.append(line)

        self.dosya( "\n".join(buf)   )
        
        return ( "%s fonksiyonu başarı ile eklendi. " ) %(fonksiyon)
        

        
    def duzenle( self , fonksiyon , veri ) :
        """ Fonksiyon ismini bul , ayirma fonksiyonunu kullanarak  ilgili içeriği atlat , 
        Yeni veriyi ekle . Diğer satırları da ekleyip , 
        dosyaya yaz """ 
        ayrilmis = self.fonksiyon_icerigi(fonksiyon) 
        if ayrilmis == "" :
            return  ( " Belirtilen fonksiyona ait hiçbir bilgi bulunamadı." ) 
            
        buf = []      
        silinecek = ayrilmis+"\n" 
        silinecek = silinecek.splitlines()
        fonksiyon_bulundu = None
        satir_sayisi = len(silinecek)  
 
        for line in self.dosya():
            if line == self.start_line :
                fonksiyon_bulundu = True 
                continue
                
            if fonksiyon_bulundu is True:
                if satir_sayisi != -1:
                    satir_sayisi -= 1 
                    continue          
                else :
                    buf.append( self.start_line + "\n" + veri+"\n"+"}")
                    fonksiyon_bulundu = False 
                    
            buf.append(line)         

        new_content = "\n".join(buf)
    #    print(new_content)                           
        self.dosya(new_content)
        
        return ("%s fonksiyonu düzenlendi.. ") %(fonksiyon)                                                              
    def sil(self,fonksiyon):

        
        """ fonksiyon içeriği  , ilgili fonksiyon yardımıyla alınır ve
        başlangıç ve bitiş satırlarıyla beraber , silinecekler ortaya çıkar , 
        dosya satır   satır okunur ve buf adlı listeye , silinmeyecek olan satırlar eklenir .
        Ancak  fonksiyon ismi haricindeki satırlar ortak olabilir .. Bu yüzden başlangıç satırı 
        bulunduktan sonra , kalan satır sayısı kadar , döngü başa döndürülerek listeye ekleme işlemi atlatılır.. 
        fonksiyon_bulundu ve satir_sayisi adlı değişkenler bunun içindir.
        Son olarak  buf adlı liste ilgili dosyaya yazdırılır. 
        """
        
        ayrilmis = self.fonksiyon_icerigi(fonksiyon) 
        if ayrilmis == "" :
            return  ( " Belirtilen fonksiyona ait hiçbir bilgi bulunamadı." ) 
            
        buf = []      
        silinecek = ayrilmis+"\n" 
        silinecek = silinecek.splitlines()
        fonksiyon_bulundu = None
        satir_sayisi = len(silinecek)  
        
        for line in self.dosya():
            if line == self.start_line :
                fonksiyon_bulundu = True 
                continue
                
            if fonksiyon_bulundu is True:
                if satir_sayisi != -1:
                    satir_sayisi -= 1 
                    continue                                                      
            
            buf.append(line)
                
        self.dosya("\n".join(buf) )
        
        return ("%s fonksiyonu silindi. ") %(fonksiyon)
