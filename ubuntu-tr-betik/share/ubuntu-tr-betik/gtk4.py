#!/bin/python3

import asamalar
import re, gi
import subprocess
gi.require_version('Gtk', '4.0')
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
import os



class sec(gtk.Assistant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('close', exit)
        self.connect('apply',self.kapat)
        self.connect('cancel', exit)
        self.set_title("Ubuntu Tr Betik")
        self.set_icon_name("./logo.png")
        self.set_size_request(600,400)

        
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
        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL)
#        vbox.set_border_width(12)
        image = gtk.Image() 
        image.set_from_file("./logo1.png")
        
        vbox.append(image)
        
        label = gtk.Label() 
        label.set_markup(self.lisans)
    	
        sw = gtk.ScrolledWindow()
        sw.set_policy(True,True) 
        sw.set_child(label) 
    	
        vbox.append(sw)
        
        button = gtk.CheckButton(label="Sözleşmeyi kabul et")
        button.connect("toggled", self.comple)  
        vbox.set_hexpand(True)            
        vbox.set_vexpand(True)
        vbox.set_homogeneous(True)           
        vbox.append(button)
      #  vbox.show_all()

        self.append_page(vbox)        
        self.set_page_title(vbox,"İşlemi Bitir!" )

        if   os.path.isfile("./GPL/.onay"): button.set_active(True)
                         
        self.set_page_type(vbox, gtk.AssistantPageType.CONFIRM)       
   #     self.resize(780,420)
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
        table = gtk.Box()
        table.append(sw)
   #     table.show_all()
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
        self.destroy()    
        komut = subprocess.Popen("""dpkg --get-selections|sed -e "s/[install]*$//g" -e  "s/..*[de]$//g"|grep gnome-terminal -c
""",shell=True, stdout=subprocess.PIPE).communicate()[0]
        print("#############Kurulacaklar:\n",text)
        
        if int(komut) >= 1:
            os.system("../../bin/ubuntu-tr-betik "+text)
        else:
            os.system("""xterm \
-e "ubuntu-tr-betik" "{0}"  & """.format(text) )      
        exit()
    def main(self): self.present()
 
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
        
        
        print(dir(sw))
        sw.set_policy(True,True)
        sw.set_child(self.view) 
 
        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        image , label = None,None
        #simge ve açıklama bilgisi varsa image ve label'e ekle
        for x in liste:
            if x == "resim":
                image = gtk.Image()
                pix = gdkpixbuf.Pixbuf.new_from_file_at_size(liste[x],128,70)
                image.set_from_pixbuf(pix)
                image.set_size_request(78,70)
            elif x == "aciklama":
                label = gtk.Label()
              #  label.set_line_wrap(True)
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
            hbox = gtk.Box(orientation=gtk.Orientation.HORIZONTAL)
            hbox.append(image)
            hbox.append(label)
            hbox.set_hexpand(False)            
            hbox.set_vexpand(False)
            hbox.set_spacing(12)
            hbox.set_margin_start(50)
            hbox.set_margin_end(50)            

            hbox.set_homogeneous(False)   
            
            vbox.append(hbox )
        vbox.set_hexpand(True)            
        vbox.set_vexpand(True)
        vbox.set_homogeneous(True)   
        vbox.set_spacing(3)
        vbox.set_margin_start(50)
        vbox.set_margin_end(50)  
        vbox.set_margin_bottom(50)                
        sw.set_size_request(200,200)        
        vbox.append(sw)
        return vbox
    def col1_toggled_cb( self, cell, path, model ,liste ): 
        model[path][2] = not model[path][2] 
        sec = (model[path][0],model[path][1]) 
        
        if not "" in sec:  sec = "|".join(sec)
        else:  sec = "".join(sec)                   
           
        if  model[path][2]:     self.eklenenler.append( liste[sec] )
        else:    self.eklenenler.remove( liste[sec] )
        
        return

import sys
gi.require_version('Adw', '1')
from gi.repository import  Adw

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = sec(application=app)
        self.win.present()


app = MyApp(application_id="com.example.My_Ubuntu")
app.run(sys.argv)
