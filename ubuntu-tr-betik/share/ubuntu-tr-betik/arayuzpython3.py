#! /bin/python3

import asamalar
import re, gi
import subprocess
gi.require_version('Gtk', '3.0') 
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
import os
class sec(gtk.Assistant):
    def __init__(self):
        gtk.Assistant.__init__(self) 
        self.connect('close', exit)
        self.connect('apply',self.kapat)
        self.connect('cancel', exit)
        self.set_title("Ubuntu Tr Betik")
    #    self.set_icon_from_file("./logo.png")

        
        self.eklenenler = []
        self.dict = asamalar.liste_ol("/tmp/kurulacaklar")
        self.lisans = open("./GPL/lisans","r").read()
 
        # Her sözlük için yeni bir pencere içerisine scrollView ekleniyor
        for i  in  range(len(self.dict) ) :
            sozluk = self.dict[i][1]
            x =  "%s " % (self.dict[i][0] ) 
            sw = self.olus_sw(  sozluk )
            self.add_page(x,sw)    
   

        # Sayfa 3
        vbox = gtk.VBox()
        vbox.set_border_width(12)
        image = gtk.Image() 
        image.set_from_file("./logo1.png")
        vbox.pack_start(image,False,False,3)
        
        label = gtk.Label() 
        label.set_markup(self.lisans)
    	
        sw = gtk.ScrolledWindow()
        sw.set_policy(True,True) 
        sw.add(label) 
    	
        vbox.pack_start(sw,True,True,3)
        
        button = gtk.CheckButton(label="Sözleşmeyi kabul et")
        button.connect("clicked",self.comple)  
        vbox.pack_start(button,False,False,3) 
        vbox.show_all()

        self.append_page(vbox)        
        self.set_page_title(vbox,"İşlemi Bitir!" )

        if   os.path.isfile("./GPL/.onay"): button.set_active(True)
        
        self.set_page_type(vbox, gtk.AssistantPageType.CONFIRM)       
        self.resize(780,420)
    def ev_style(self,widget):
        ev = gtk.EventBox()
        ev.add(widget)
        ev.get_style_context().add_class(gtk.STYLE_CLASS_PRIMARY_TOOLBAR)  
        return ev        
    def comple(self,data): 
        if data.get_active() is True:
            self.set_page_complete(data.get_parent(),True)	  
        else:
            self.set_page_complete(data.get_parent(),False)	                
    def add_page(self,asama,sw) :
        table = gtk.Table(n_rows=2,n_columns=2)  
        table.attach(sw,0,1,0,1)
        table.show_all()
        self.append_page(table)        
        self.set_page_title(table, asama)
        self.set_page_type(table, gtk.AssistantPageType.CONTENT)        
        self.set_page_complete(table,True)	    
        
    def kapat(self, assistant):
        text = " ".join(self.eklenenler)  
        #Kurulmak için seçilenleri kurulacaklarda artık gösterme..
        if not os.path.isfile("./GPL/.onay"):
            os.system("> ./GPL/.onay")
        if not len(text) > 1:            
            return False
        komut = subprocess.Popen("""dpkg --get-selections|sed -e "s/[install]*$//g" -e  "s/..*[de]$//g"|grep gnome-terminal -c
""",shell=True, stdout=subprocess.PIPE).communicate()[0]
        print("#############Kurulacaklar:\n",text)
        
        if int(komut) >= 1:
            os.system("../../bin/ubuntu-tr-betik "+text)
        else:
            os.system("""xterm \
-e "ubuntu-tr-betik" "{0}"  & """.format(text) )      
        
    def main(self): self.show()
 
    def olus_sw(self,liste):
        sw = gtk.ScrolledWindow() 
        self.view = gtk.TreeView()        
        self.view.set_headers_visible(False) 
        
        self.tree_store = gtk.TreeStore(str, str, bool ) 
        self.tree_store.set_sort_column_id(0, gtk.SortType.ASCENDING) 
        self.view.set_model(self.tree_store )
 
        self.renderer = gtk.CellRendererText()
        self.renderer1 = gtk.CellRendererText()
        self.renderer1 = gtk.CellRendererToggle()
        self.renderer1.set_property('activatable', True)
        self.renderer1.connect( 'toggled', self.col1_toggled_cb, self.tree_store,liste )
		
 
        self.column1 = gtk.TreeViewColumn(" Uygulamalar", self.renderer, text=0) 
        self.column2 = gtk.TreeViewColumn(" Açıklama", self.renderer, text=1) 
        
        self.column0 = gtk.TreeViewColumn("Seçim", self.renderer1 )
        self.column0.add_attribute( self.renderer1, "active", 2)
        self.view.append_column( self.column0 )
        self.view.append_column( self.column1 ) 
        self.view.append_column( self.column2 ) 
        
        sw.set_policy(True,True)
        sw.add(self.view) 
 
        vbox = gtk.VBox()
        image , label = None,None
        #simge ve açıklama bilgisi varsa image ve label'e ekle
        for x in liste:
            if x == "resim":
                image = gtk.Image()
                pix = gdkpixbuf.Pixbuf.new_from_file_at_size(liste[x],128,70)
                image.set_from_pixbuf(pix)
            elif x == "aciklama":
                label = gtk.Label()
                label.set_line_wrap(True)
                label.set_markup("<b>%s</b>" %(liste[x]) )                
            else:
                """Ubuntu-tr-betik kurulacak paketleri oluştururken , apt-cache search'ten 
                edinebildiği açıklamaları , paket hakkındaki açıklamadan sonra '|' karakteri ile
                ekliyor , bu satırda ise ; eklenmiş bir bilgi var ise , ağaç görünümünde gösterilmek 
                üzere ayıklanıyor."""
                if "|" in x:
                    x = x.split("|")
                    self.tree_store.append( None, (x[0],x[1], None) )
                else:
                    self.tree_store.append( None, (x,"", None) )
        # image ve label varsa  hbox'a hbox'ıda  vbox'a ekle                        
        if image and label:
            hbox = gtk.HBox()
            hbox.pack_start(image,False,False,2)
            hbox.pack_start(label,False,False,4)
            vbox.pack_start(hbox ,False,False,14)
            
        vbox.pack_start(sw,True,True,0)
        return vbox
    def col1_toggled_cb( self, cell, path, model ,liste ): 
        model[path][2] = not model[path][2] 
        sec = (model[path][0],model[path][1]) 
        
        if not "" in sec:  sec = ".".join(sec)
        else:  sec = "".join(sec)                   
           
        if  model[path][2]:     self.eklenenler.append( liste[sec] )
        else:    self.eklenenler.remove( liste[sec] )
        
        return
 

sec().main()
gtk.main()
