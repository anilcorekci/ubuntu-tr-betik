#-*-coding:utf-8-*-
#vim:ts=4:sw=4
import os

"""
    "kurulacaklar" isimli dosyada da belirli formatta paketler ve başlıklar bildirilir. Bu betiğin amacı ise
    bu belirli formata uygun yazılmış olan dosyayı iç içe Python yapıları haline getirmektir. İç içe Python yapıları
    haline getirilen bu bilgiler diğer betiklere import ile geçirilerek diğer betikler tarafından kullanılmaktadır.

    "kurulacaklar" dosya yapısı:
    * @@@ ile başlayan satırlar yorum satırı olarak algılanırlar ve herhangi bir işleme tabii tutulmazlar. Eğer geliştiricilere
      belirtmek istediğiniz bir not varsa notlarınızı @@@ karakterleri ile başlayan satırlarda belirtiniz. Aksi halde bu betik
      istenildiği şekilde çalışmayacakıtır ve bu durum tüm uygulamaya bozukluk olarak yansıyacaktır.

    * # karakteri ile başlayan satırlar kendinden sonra belirtilecek olan paket/ppa/depo vs gibi birimlerin hangi alanda olduklarını 
      belirten başlıkları bildirmektedir. Bu nedenle rastgele paket ismi yerleştirmeyiniz. Örneğin Firefox tarayıcısı "Anlık İleti Araçları"  
      altında belirtilirse bu durum aynı şekilde son kullanıcıya yansıyacaktır ve anlık ileti araçları içerisinde Firefox'u görecektir. Bu nedenle
      ekleyeceğiniz yeni paketleri/ppaları vs ilgili başlığa ekleyiniz. 

      Aynı zamanda # karakteri ile başlaran satırlar kullanıcıya başlık olarak yansıyacaktır. Bu nedenle oluşturacağınız yeni bölümler olursa başlıkları
      son kullanıcının göreceğini düşünerek belirtiniz ve kısaltmalar kullanmayınız; Örneğin An. Mes. Araçları yerine Anlık İleti Araçları gibi
      anlaşılır isimler kullanınız.

    * Başlık ve yorum dışındaki satırlar genel olarak 3 bölümden oluşmaktadır;

      Görünür İsim:paket_ismi/ppa=ppa_ismi

      - Görünür isim: Opsiyon olarak kullanıcıya sunulan ve kullanıcının uygulamayı ayırt edeceği isimdir.
      - Paket ismi: Görünür ismin depolardaki tanımına denk gelir.
      - PPA ismi: Kurulacak olan paket varsayılan depolar yerine harici bir PPA gerektiriyorsa ayrıca bu PPA'yı belirtmek için kullanılır.
        Aksi halde yani uygulama varsayılan olarak depolarda bulunuyorsa PPA belirtilmez.

      Örneğin depolarda bulunan AMSN uygulamasının
      Amsn:amsn    Şeklinde belirtmek yeterlidir. Kullanıcı burada sadece Amsn'i görür ve uygulamayı bu isimden ayırt eder. amsn ise 
                   kurulum komutunda verilecek olan paketin ismidir.

      Harici PPA gerektiren AMSN Günlük Geliştirme sürümü için ise PPA belirtmek gerekir. Bu durumda tanım şu şekilde yapılmalıdır;
      Amsn Geliştirme Deposu:amsn-daily/ppa=amsn   Burada kullanıcının ilgilendiği ve muhattap olduğu salt olarak görünür isim yani;
      "Amsn Geliştirme Deposu'dur". Burada kurulacak olan paket amsn ppasından amsn-daily paket ismi ile kurulacaktır.              
    

    Aktarılan Python yapısı:

    Genel olarak tüm yapı bir liste olarak tutulur; steps[]
    Bu listenin her bir elemanı yeni alt bir listedir. steps[[]]
    Her bir elemanı oluşturan yapı olan alt liste ise bir string ve bir sözlükten oluşur. Burada string olan eleman kurulacaklar
    dosyasından # ile başlayan satırlar çekilir ve kullanıcıya gösterilmek üzere başlık olarak saklanır.
    Bu string'in başlık olarak kullanıldığı sözlükte ise (yani alt listenin ikinci elemanı) kurulacak olan uygulamalar/ppalar ve 
    diğer birimler saklanır.
     # ile başlayan satırlar çekilirek oluşturulan  ve kullanıcıya gösterilmek üzere oluşturulan string yapısında  :
    0. # Karakteri >  Bu sözlüğün başlığıdır  . Aynı satır içindeki diğer iki # karakteri ise bu başlığın özel bilgileridir ,
    Sırasıyla:
    1. # Karakteri > Bu kategori başlığına ait simgeyi belirtir. 
    2. # Karakteri > Bu kategori başlığına ait açıklamaları barındırır.
    
    Açıklama ve simgeler aynı başlığa ait olan sözlükte , "resim" ve "açiklama" olarak iki ayrı öğede saklanır    .  
    Örnek veri yapısı:

    [["Anlık ileti araçları", {"Amsn":"amsn", "Pidgin":"pidgin", "resim": "simge/yolu", "aciklama":"kategori bilgisi"}], ....... ] , 

"""
 
def liste_ol(file_="./kurulacaklar"):
    if not os.path.isfile(file_):
        print ( "Kurulacaklar ayar dosyası bulunamadı." )
        exit(1)
        
    dosya = open(file_,"r").read()
    i = -1
    steps = []
    for x in dosya.splitlines():
        if x[: 3] == '@@@':
            continue
        elif "#" in x:
            baslik = x.split("#")[1]
            steps.append( [baslik , {}  ] )
            i+=1
            try:
                simge = x.split("#")[2]
                steps[i][1]["resim"] = simge 
                genel_bilgi = x.split("#")[3]                        
                steps[i][1]["aciklama"] = genel_bilgi  
            except IndexError:
                pass
        elif ":" in x:
            aciklama = x.split(":")[0]
            bilgi = x.split(":")[1]      
            steps[i][1][aciklama] = bilgi 
 
 
    return steps        
 
 

