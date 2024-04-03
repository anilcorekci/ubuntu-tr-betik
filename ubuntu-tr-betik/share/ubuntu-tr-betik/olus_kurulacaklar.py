#! /bin/python3
import gi
gi.require_version('Gtk', '3.0') 
gi.require_version('GtkSource', '4') 
from gi.repository import Gtk as gtk
from gi.repository import GtkSource as edit
import asamalar
from  parse import parse as pr
class olus_kurulacaklar():
# sınıf içinde kullanılıcak widget ve değişkenleri oluştur
    parse = pr() # import edilen parse sınıfı
    name = "" ; txt ="" # treeview öğesindeik seçilen öğe # seçilen  öğenin sözlük içerisindeki str değeri
    su_anki_kategori = 0   # şu an seçili olan kategori öğesinin , oluşturulan liste içerisindeki konum sırası
    
    builder = gtk.Builder() 
    builder.add_from_file("./glade/olus_kurulacaklar.glade")
    dialog = builder.get_object("dialog1") 
    fonk = builder.get_object("entry3")
    combo = builder.get_object("comboboxtext1")
    entry = builder.get_object("entry1")
    kategori = builder.get_object("entry2")
    mesaj = builder.get_object("messagedialog1")
    miptal  = builder.get_object("button6")
    
    kurulum_bilgisi = builder.get_object("entry8")
    kategori_aciklamasi = builder.get_object("entry6")
    kategori_simgesi = builder.get_object("entry7")
    
    yeni_kategori_aciklamasi = builder.get_object("entry4")
    yeni_kategori_simgesi =  builder.get_object("entry5")
    
    def __init__(self): 
        self.builder.connect_signals({"on_clicked":self.kayit,
                                                "up_down_list":self.up_down,
                                                "yeni": self.yeni,
                                                "sil":self.sil,
                                                "girdi_tıklaması":self.girdi_tiklamasi,
                                                "kategori_duzenle": self.kategori_duzenle, 
                                                "quit": gtk.main_quit } )
                                                
        #TEXT ALANI ################################## 

        self.edit = edit.View()
        self.tbuffer =  edit.Buffer() 
        self.edit.set_buffer(self.tbuffer)
        self.edit.set_wrap_mode(gtk.WrapMode.CHAR)	
        self.edit.set_show_line_numbers(True)
        
        self.lm = edit.LanguageManager.new()
        language = self.lm.guess_language(None,"application/x-shellscript")  
        self.tbuffer.set_language(language) 
                                                        
        ### LİSTE ALANI ####################################
        self.view = gtk.TreeView()
        self.view.connect("cursor-changed",self.active)        
        self.view.set_headers_visible(False)
        
        self.tree_store = gtk.TreeStore(str )          
        self.view.set_model(self.tree_store ) 
        
        self.renderer = gtk.CellRendererText()
        self.renderer.set_property( 'editable', True )
        self.renderer.connect( 'edited', self.col0_edited_cb, self.tree_store )        
 
        self.column1 = gtk.TreeViewColumn(" Depolar", self.renderer, text=0)    
        
        self.column1.set_cell_data_func(self.renderer, self.file_name)
        self.view.append_column(self.column1) 
        
        sw = self.builder.get_object("scrolledwindow1")
        sw.add(self.view)
        

        
        self.builder.get_object("scrolledwindow2").add(self.edit)        
        
        self.builder.get_object("window1").show_all()
        self.re_list()
        
    def yeni_mesaj(self,txt,soru=None):
        """ Mesaj dialoğunu rahatça kullanabilmek için , oluşturulan fonksiyon,
        Eğer soru var ise evet/ hayır gerektiren bir soru diyaloğu gibi çalışıyor. 
        miptal :iptal butonu 
        eğer , geri dönüş için olumsuz bir değer beklenmiyorsa 
        sadece txt değişkeninden gelen veriyi göstermesi yeterli .. """
        
        if soru:  self.miptal.show()
        else:      self.miptal.hide()            
        
        self.mesaj.set_markup(txt)
        self.mesaj.show()
        response_id = self.mesaj.run()
        self.mesaj.hide()
        if  response_id == 1:
            return True
        return None            
        
    def re_list(self):
        """yeni sozluğü al ve parçları yeniden listeye ekle;
        asamaların olusturduğu listenin içindeki liste sayısı kadar kategori olduğundan 
        kategorilerin sayısı kadar döngü oluşturup , bu sıraya göre bilgiler , listeye eklenir..   """
    #    reload(asamalar)
        self.sozluk =  asamalar.liste_ol()
        self.tree_store.clear()
        for i  in  range(len(self.sozluk) ):
            baslik =   self.sozluk[i][0]
            kategori = self.tree_store.append(None, [ baslik]  )
 
            for kategori_uyeleri in self.sozluk[i][1]:
                if not kategori_uyeleri in [ "aciklama","resim"] :
                    self.tree_store.append(kategori, [ kategori_uyeleri ]  )       
 
         
            self.view.expand_all() 
    def file_name(self,column, cell, model, iter,xx):
        """Kategori başlıklarını kalın yazılı göster """
        text =  model.get_value(iter, 0) 
        cell.set_property('text', text)
        if text in [x[0] for x in self.sozluk]: 
            cell.set_property('weight', 700) 
        else:cell.set_property('weight', 400) 
        
    def col0_edited_cb( self, cell, path, new_text, model ):    
        """Yeni girdiyi koşullara göre listeden yenile"""
        ex_text =   model[path][0]  
        model[path][0] = new_text        
        if ex_text != new_text :
            for i  in  range(len(self.sozluk) ): 
                if ex_text == self.sozluk[i][0]: 
                    self.sozluk[i][0] = new_text
                    return 
                for x in self.sozluk[i][1]: 
                    if ex_text == x: 
                        self.sozluk[i][1][new_text] =   self.sozluk[i][1][x]
                        del  self.sozluk[i][1][x]
                        return
        return        
    def up_down(self,widget=None):
        """kategori öğesinin sıralamasını değiştir..
    Burası biraz karışık gibi , bu fonksiyon , seçili kategori öğesini yukarı taşımak içinde ,
    aşağı taşımak içinde ortak olarak kullanılıyor .Yani , her iki gtkButton öğeside bu fonksiyonu 
    kullanıyor   tıklandığında .Peki hangisinin aşağı , hangisinin yukarı taşınacağı nereden anlaşılıyor ?
    Glade aracından . clicked sinyali fonksiyonlarda kullanılırken , birinci argüman olarak fonksiyona ,
    widget bilgisini verir. Burada glade üzerinden bir oynama ile , aşağı butonunu tıklandığından , 
    standart olan button widgeti yerine , label widgetini argüman olarak veriyor .
    Bu da işlemleri ayırmak için yeterli bir  farklılık .. """
        if not self.name in [x[0] for x in self.sozluk]:
            self.yeni_mesaj("Bu sadece kategorileri düzenlemek için\nPaket isimleri kendiliğinden ada göre sıralanır..")
            return False
        try:
            for i  in  range(len(self.sozluk) ):  
                if self.name == self.sozluk[i][0] :            
                        
                    once = self.sozluk[i]            
                    if  "Label" in str(widget): sonra = self.sozluk[i+1]  
                    else: sonra = self.sozluk[i-1]

                    self.sozluk[i]  = sonra
                    if  "Label" in str(widget): self.sozluk[i+1]  = once 
                    else: self.sozluk[i-1] = once 

                    self.degistir()   ; self.re_list()           
                    break  
        except:
            return False                           
 
    def active(self,data):
        self.tbuffer.set_text("")
        treeselection = data.get_selection() 
        try:
            (model, rows) = treeselection.get_selected_rows() 
            iter = model.get_iter(rows[0 ])
            self.name = model[iter][0]
        except:
            self.name = None
            return  
 
        # Seçilen İşlemi bul ve bilgileri textview'e ekle
        for i  in  range(len(self.sozluk) ):
            for x in self.sozluk[i][1]:
                if self.name == x:
                    txt = self.sozluk[i][1][x] 
                    self.kategori_simgesi.set_text ( self.sozluk[i][1]["resim"] )
                    self.kategori_aciklamasi.set_text(  self.sozluk[i][1]["aciklama"] )
                    
                    self.txt =txt
                    self.su_anki_kategori = i 
                    
                    if "_" in txt:
                    # _ karakteri txt "in içinde bulunuyorsa bu bir fonksiyona işaret eder.
                        self.tbuffer.set_text( self.parse.fonksiyon_icerigi(txt) )
                        self.fonk.set_text(txt)
                    else:
                        self.fonk.set_text("")
                        self.tbuffer.set_text( txt) 
                    break

    def degistir(self,neolsun=None):
    ## Kurulacakları listeye göre yeniden güncelle
    ## ne olsun değişkeni ise 
        with open("kurulacaklar","w") as dosya:
            for i  in  range(len(self.sozluk) ):  
                kategori_title = "\n#%s#%s#%s\n\n" % (self.sozluk[i][0],self.sozluk[i][1]["resim"],self.sozluk[i][1]["aciklama"]  )
                dosya.write(kategori_title )
               # print(kategori_title)
                for x in self.sozluk[i][1]:           
                    if x == self.name and neolsun: 
                        index_info = "{0}:{1}\n".format( x , neolsun)
                        dosya.write(index_info)       
                        print(index_info)                 
                    else:
                        try:
                            if x != "resim" and x != "aciklama":
                                index_info = "{0}:{1}\n".format( x , self.sozluk[i][1][x] )
                                #print(index_info)                 
                                dosya.write(index_info )
                        except IndexError: pass
            dosya.close()                                    
    def kayit(self,data=None): 
    ## Değişikleri kaydet ve listeyi yenile
        start, end = self.tbuffer.get_bounds()
        konu= self.tbuffer.get_slice(start, end,True)  
        if "_" in self.txt: 
            print ( self.parse.duzenle(self.txt,konu) ) 
            self.degistir(self.txt) 
        else:   
            self.degistir(konu)    
        self.re_list()
    def yeni(self,data=None):
    # yeni eklemeler dialogunu çalıştır ve
    # güncel bilgileri widgetlere ekle    
        self.combo.remove_all()
        for x in self.sozluk:
            self.combo.append_text(x[0] )
        self.combo.set_active(0)
        self.entry.set_text("")            
        self.kategori.set_text("")
        self.yeni_kategori_simgesi.set_text("./simgeler/")
        self.yeni_kategori_aciklamasi.set_text("")
        self.kurulum_bilgisi.set_text("")
        
        response_id = self.dialog.run() 
        self.dialog.hide()
        if response_id == 0:
            text = self.combo.get_active_text()
            yeni_paket = self.entry.get_text()
            yeni_kategori = self.kategori.get_text()
            if len(yeni_paket) > 0: # bir alt başlıkta paket bilgisi bulunmuyor, yeni_paket olarak değer ver 
                for i  in  range(len(self.sozluk) ): 
                    if text == self.sozluk[i][0]: 
                        self.sozluk[i][1][yeni_paket] = self.kurulum_bilgisi.get_text()
            if len(yeni_kategori ) > 0:  

                # yeni kategori eklenirken , yeni kategori açıklamasını ve kategori simgesini sözlüğe ekle..
                self.sozluk.append( [yeni_kategori, {"resim":self.yeni_kategori_simgesi.get_text()\
                , "aciklama":self.yeni_kategori_aciklamasi.get_text()  }   ]  )                 
            self.degistir() ; self.re_list()                    
            
    def sil(self,data=None):
        # Seçilen ağaç görünümü öğesini önce listeden 
        # sonrada ağaç görünümünden çıkar,değişikleri kaydet ve 
        # listeyi yenile
        treeselection =  self.view.get_selection()
        (model, rows) = treeselection.get_selected_rows()
        try:
            iter = model.get_iter(rows[0])
            name = model[iter][0] 
        except:
            return 
                    
        bitir = None
        for i  in  range(len(self.sozluk) ):
            if bitir is True : break 
            if  name == self.sozluk[i][0]: 
                    if self.yeni_mesaj("Bu seçenek kategoriye ait tüm bilgileri siler \nAncak fonksiyon içerikleri bash scriptinden silinmez \n Devam etmek istiyor musunuz ?",True):
                        del self.sozluk[i]
                    break 
            for paket_ismi in self.sozluk[i][1]:  
                if  name == paket_ismi:  
                    print (paket_ismi)
                    paket_yonergesi = self.sozluk[i][1][paket_ismi ]
                    print (paket_yonergesi)
                    if "_" in paket_yonergesi  :
                        print ( self.parse.sil(paket_yonergesi ) ) 
                        
                    del self.sozluk[i][1][paket_ismi]
                    
                    bitir = True ; break 
        model.remove(iter)  
        self.degistir() ; self.re_list()
    def girdi_tiklamasi(self,entry,icon_pos,void):
        # Baştaki ve sondaki küçük resimli girdi düğmelerine göre
        # fonksiyon ekle veya sil
        text = entry.get_text()
        if icon_pos == gtk.EntryIconPosition.PRIMARY:
            if  not "_" in text or len(text) < 1:
                self.yeni_mesaj("Hiç bir şey yazılmadı ya da\nYeni fonksiyon eklemek için _ karakteri kullanılmalı..")
                return False
            if filter(lambda i:text in i,self.parse.dosya()  ):
                self.yeni_mesaj("Bu fonsiyon zaten eklenmiş , başka bir fonksiyon ismi yazmayı deneyin!")
                return False                
            self.parse.ekle(text)    
            self.degistir(text)
        if icon_pos ==  gtk.EntryIconPosition.SECONDARY:    
            if not "_"  in text :
                self.yeni_mesaj(" Bu bir fonksiyona işaret etmiyor .\nBu işlem sadece fonksiyonlar için uygulanabilir." )
                return False
            self.yeni_mesaj( self.parse.sil(text)      ) 
            self.degistir("yenipaket")       
        self.re_list() 


    def kategori_duzenle( self, entry_widget , iconpos = None , void = None ) :
        if entry_widget == self.kategori_aciklamasi :
            self.sozluk[self.su_anki_kategori] [1] ["aciklama"] = self.kategori_aciklamasi.get_text()
        if entry_widget == self.kategori_simgesi :
            self.sozluk[self.su_anki_kategori] [1] ["resim"] = self.kategori_simgesi.get_text()      
            
        self.degistir() ; self.re_list() 
                                     
olus_kurulacaklar()
gtk.main()        
