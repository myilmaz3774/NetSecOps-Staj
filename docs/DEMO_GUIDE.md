# Demo Kılavuzu

## Hazırlık

```powershell
cd C:\Projects\NetSecOps-Staj
python --version
```

Python 3.10 veya daha yeni bir sürüm yeterlidir; harici paket gerekmez.

## Kısa demo

```powershell
python main.py --run all
```

Sunum sırasında şu çıktılar gösterilebilir:

1. Konsolda 3 simüle cihaz ve 6 açık port.
2. Telnet ve FTP için yüksek risk uyarısı.
3. Loopback TCP servisinde bir açık ve bir kapalı port.
4. VLAN 10 -> VLAN 20 değişikliği.
5. ACL deny satırının kaldırılması ve geniş permit satırının eklenmesi.
6. Başarılı SHA-256 bütünlük kontrolü.
7. `data/reports` altındaki JSON/metin raporları ve `logs/app.log`.

## Menü seçenekleri

- `1`: Simüle varlık keşfi
- `2`: Simüle port ve risk denetimi
- `3`: Config yedekleme ve diff
- `4`: Tam denetim
- `5`: Loopback TCP Socket laboratuvarı
- `0`: Çıkış

## Test

```powershell
python -m unittest discover -s tests -v
```

## Sunum önerisi

`NetSecOps_Teknik_Sunum.pptx` dosyasında problem, mimari, modüller, örnek bulgular, kalite kanıtı ve güvenlik sınırları sıralı biçimde anlatılır.
