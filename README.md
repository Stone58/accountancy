## Kodlama ile ilgili
- Kodlama için ingilizce kullandım . dolaysıyla takstaki tablolar şuna çevirdim: Firmalar -> company ; işlemler -> operation;
- o tablolar dışında başka tablolar mevcut: işlemler türü -> operationType; kullanıcı -> user

## Projeyi nasıl test edilir: 
- varsayılan olarak username = 'admin' ve password='1234' olan bir admin superuser mevcuttur
- roller (id ve açılımları bunlar ): 1 ->Admin; 2 -> Accountant; 3 -> Worker
- onu kullanıp token almak gerekiyor
- işlemler oluşturmak için önce kullanıcılar, işlem türü, firma oluşturmak lazım

## Automatik test için: 
```bash
python manage.py test
```

## Proje çalıştırmaları
- Proje windows bir ortamda gelistirdim ve onun icin bir bat dosyayi hazirladim oradan ortam ve 'python' path değişkenine göre düzeleyip çalıştırılabilir (ya da tek tek)

## Proje Geliştirmeleri ve Sorular

### Kalan sorular:
- Şu an muhasebeciler veya yöneticiler işlem oluşturabilir mi?
- İşlemleri düzenlemek mümkün mü, yoksa silme ve tekrar oluşturma tek seçenek mi?
- Tarih manuel olarak girilebilir mi, yoksa yalnızca sistem zamanına dayalı mıdır?

### Yetki Yönetimini Geliştirmek:
- Mevcut task spesifikasyonlara göre, ve zaman kisilti olmasindan dolayi grup özelliklerini kullanarak yetkilendirmeyi uygulandi. Daha optimize bir yaklaşım, her yöntem için özel izinler oluşturup bunları gruplarla ilişkilendirmek olabilir mi? Bu, daha esnek bir yapı sağlayabilir.

### Detaylı Testler:
- CRUD işlemleri şu an için yönetici rolü kullanılarak doğru bir şekilde çalışıyor gibi görünse de, farklı kullanıcı rollerini kapsayacak daha detaylı test vakaları geliştirilebilir.

### tablolardaki Değişiklik hakkinda:
- Bir veriyi en son kimin değiştirdiğini izleyen ek bir alan eklemeyi düşünülebilir. Bu, denetim ve hesap verebilirlik için faydalı olabilir.

