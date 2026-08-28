# NetSecOps Laboratory

Bu proje, staj kapsamında ağ varlık envanteri, port/risk denetimi ve yapılandırma değişikliği takibini göstermek amacıyla hazırlanmış simüle edilmiş bir laboratuvar uygulamasıdır.

## Kapsam

- Simüle edilmiş IP, MAC ve cihaz envanteri
- Tanımlı kritik portların risk değerlendirmesi
- Zaman damgalı örnek yapılandırma yedekleri
- Satır bazlı yapılandırma fark analizi ve kritik değişiklik uyarısı
- JSON tabanlı envanter ve rapor çıktıları

## Güvenlik sınırı

Uygulama yalnızca `config/simulated_network.json` içindeki örnek laboratuvar verileriyle çalışır. Gerçek kurum ağına bağlantı, gerçek IP taraması veya gerçek cihazlara SSH erişimi içermez.

## Çalıştırma

```powershell
python main.py
```

Menüden sırasıyla varlık keşfi, port/risk denetimi veya config yedekleme ve diff işlemi seçilebilir.

## Dosya açıklamaları

- `config/`: Uygulama ayarları ve simüle edilmiş cihaz verileri
- `modules/`: Uygulamanın işlevsel modülleri
- `data/inventory/`: Oluşturulan envanter kayıtları
- `data/backups/`: Örnek yapılandırma yedekleri
- `data/reports/`: Port ve fark analizi raporları
- `logs/`: İleride eklenecek uygulama günlükleri

## Staj raporu için not

Çalışma, kurumsal güvenlik politikalarına uygun biçimde simüle edilmiş laboratuvar verileri üzerinde tasarlanmıştır. Hedef, ağ güvenliği süreçlerinde envanter yönetimi, risk görünürlüğü ve değişiklik takibinin otomasyonla nasıl desteklenebileceğini göstermektir.
