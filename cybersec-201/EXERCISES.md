# Cybersec-201: priprava in opombe za izvajalca

Udeleženska navodila, namigi in postopki so v `vaje/VAJE.md`. Ta dokument ostane namenjen izvajalcu. Opis temelji na kodi priprave in izvorni kodi Juice Shop v20.3.0; dejanske odzive laboratorija preveri pred dogodkom.

## Pred dogodkom

- Preveri osebne prijave v pripravljeni Kali prek Guacamole oziroma povezave WireGuard. Prijave uredimo pred začetkom predstavitve. Lokalna VM ni obvezna.
- Preveri Nmap, dig, curl, smbclient, ExifTool, lokalni CyberChef, ZAP in izbrani skripti NSE. Predloga Kali jih namesti v `infra/kali/build-template.sh`; pri že zgrajeni predlogi sprememba seznama paketov sama ne posodobi obstoječih VM. Dodatna orodja za predstavitev so Wireshark, snmpwalk, ffuf, Nikto in sqlmap.
- Za Shodan izberi resničen javni IP z uporabnim zadetkom ter pripravi datiran posnetek. Za crt.sh izberi resnično domeno z več imeni in pripravi datiran izvoz. Javne vire udeleženci odpirajo v svojem običajnem brskalniku; računi in nakupi niso pogoj.
- V ZAP preveri zagon njegovega brskalnika, zgodovino in urejanje ter ponovno pošiljanje zahteve. Ta brskalnik uporablja lokalni ZAP. Lokalnih tarč ACME ne pošiljaj prek zunanjega posrednika Squid. Preveri dodatke pred dogodkom, ne med prikazom.
- Preveri iskanje v Juice Shop: `GET /rest/products/search?q=…`. Za dodatno vajo SQL injection preveri `POST /rest/user/login`, privzeto domeno računa `admin@juice-sh.op` in odgovor `authentication.umail`. Ta vaja ne spreminja podatkov in ne potrebuje administratorskih operacij po prijavi.
- Za prikaz XSS izberi lokalni DOM XSS z učnim sporočilom, ne shranjenega XSS, ki bi vplival na druge. Privzeto prijavo NAS potrdi pred dogodkom. Kamera ima statični obrazec in simulirani odgovor RTSP 401, zato tam ne načrtuj uspešne prijave ali videa.
- Preveri SSH iz trenutnega Kali do `peter.horvat@vpn.acme.lab` in pripravi prstni odtis ključa. Morebitno izjemo za star algoritem omeji na to tarčo in posamezen ukaz. Ne spreminjaj globalnih nastavitev odjemalcev.
- Lokalni CyberChef preveri z nizom `dWNlbmVjOnVjbm8=` → `ucenec:ucno`. Udeležencem pokaži način zagona. Vaja 3.2 ima tudi terminalski postopek.

## Dokument za vajo 1.4

PDF je pripravljen v repozitoriju na dveh mestih:

- `infra/acme/files/www/htdocs/dokumenti/cenik-2026.pdf` za HTTP;
- `infra/acme/files/files/javno/cenik-2026.pdf` za SMB in obstoječi korak priprave metapodatkov.

Za ponovno izdelavo uporabi `python3 infra/acme/generate-document.py`. Generator uporablja samo standardno knjižnico, zapiše enak učni dokument na obe mesti in ne uporablja resničnih podatkov. Metapodatki »Maja Kovac«, »LibreOffice 7.0« in datum so namerno pripravljeni učni podatki, ne dokaz o orodju, s katerim je bil PDF ustvarjen.

Pred dogodkom preveri prenos prek `http://www.acme.lab/dokumenti/cenik-2026.pdf` in izpis ExifTool. Obstoječi že pripravljeni gostitelji novih datotek ne dobijo samodejno: pri naslednji načrtovani osvežitvi sinhroniziraj vsebino in pripravi `www` ter `files` skladno z `infra/README.md`. Med vajami ne izvajaj ponovne priprave.

## Poročilo za vajo 2.5

Greenbone teče ločeno na `https://10.20.0.11/`. Pred dogodkom posodobi vire in pripravi končan pregled izbranih tarč ACME. Udeležencem daj izvoz ali dostop do poročila, ne izvajalskega administratorskega računa.

Izberi eno ali dve ugotovitvi, ki ju lahko preverijo z omejeno zahtevo: na primer zaznava različice Apache ali dovoljen AXFR, če ga dejanski pregled zazna. Izsek naj vsebuje naslov in vrata, dokaz zaznave, opis pogojev, vpliv, predlagan ukrep ter prikazano resnost in Quality of Detection. Ne načrtuj hkratnih novih pregledov vseh udeležencev.

Če dejansko poročilo ni na voljo, je v postopku vaje jasno označena besedilna ponazoritev za presojo različice Apache. Ta omogoča izvedbo naloge, ni pa predstavljena kot rezultat Greenbone. Predstavitev Greenbone naj uporablja dejansko poročilo oziroma prej izvoženo rezervo.

## Učna računa za IDOR, vaja 3.5

Pred dogodkom v običajnem vmesniku Juice Shop pripravi dva navadna učna računa, denimo `ucni-a@acme.lab` in `ucni-b@acme.lab`. Uporabi ločeni seji brskalnika, da se prijavi in žetona ne pomešata. Gesli in dejanska ID košaric posreduj udeležencem za to vajo; ne zapisuj prijavnih žetonov na prosojnice.

1. Prijavi se kot A in mu dodaj en izdelek v košarico. V Network zapiši ID iz `GET /rest/basket/:id`.
2. Kot B dodaj drug izdelek in zapiši njegov ID košarice. ID košarice ni nujno ID uporabnika.
3. Kot A v ZAP ponovi zahtevo za njegovo košarico. Spremeni samo ID v poti na košarico B, žeton pa ohrani od A.
4. Preveri, da odgovor vsebuje pripravljeni izdelek B. To je dokaz; status 200 in skupni score board sama ne zadostujeta.
5. V vaji udeleženci uporabljajo ti dve košarici samo za branje. Zaradi samostojnega tempa ne spreminjaj njune vsebine med praktičnim blokom. Po ponastavitvi Juice Shop ponovno pripravi računa in preveri ID.

Izvorna koda: [registracija poti](https://github.com/juice-shop/juice-shop/blob/v20.3.0/server.ts), [branje košarice brez preverjanja lastništva](https://github.com/juice-shop/juice-shop/blob/v20.3.0/routes/basket.ts) in [sestavljanje prijavne poizvedbe](https://github.com/juice-shop/juice-shop/blob/v20.3.0/routes/login.ts).

## Scenariji in časovnica

Prikaz segmentacije je osrednji prikaz predstavitve (približno tri minute). Priporočen je skupni preklop med predstavitvijo: `./infra/lab.sh scenario visitor`, nato `flat`, nato nazaj `visitor`; z istega Kali ponovi `nmap -Pn -sT -p 80,502 172.20.30.12`. Rezerva je izpis na prosojnici. Preklopi veljajo za vse. SNMP lahko pojasniš s pripravljenim izsekom; za živi prikaz tiskalnika potrebuješ flat. Za primerjavo uporabljaj nove povezave; že odprte povezave lahko preživijo preklop. Daljše prikaze zamenja splošna razlaga resničnih primerov, da ostane časovni okvir predstavitve 45 minut.

**Pred praktičnim blokom nastavi in preveri visitor. Med vajami scenarija ne spreminjamo.** Meritev javnih naslovov v vaji 2.1 zato opišemo kot pregled javnih naslovov z notranjega izhodišča. IoT ni samostojna vaja in ostane omejen.

| Čas od začetka praktičnega bloka | Scenarij | Dejavnost |
| --- | --- | --- |
| 0–25 min | visitor | Digitalne sledi |
| 25–65 min | visitor | Omrežja |
| 65–105 min | visitor | Aplikacije |
| 105–115 min | visitor | Skupni pogovor |

Pred tem je 45 minut predstavitve; celotna delavnica traja 160 minut. V vsakem krogu je cilj ena od treh osnovnih vaj glede na izkušnje, nato poljubna druga vaja ali dodatni izziv. Nihče ne potrebuje uspeha pri prejšnji vaji. Ne ponastavljaj skupnih tarč med delom udeležencev.

## Pričakovani izidi

| Vaja | Dokaz uspeha in omejitve |
| --- | --- |
| 1.1 | Vir, datum, organizacija in opažene storitve. Brez sklepa o trenutni dosegljivosti ali točni fizični lokaciji. |
| 1.2 | Komentar in robots.txt vodita do `/backup/config.php.bak`. Kopija razkrije prijavne podatke in notranje ime. |
| 1.3 | AXFR vrne tudi notranje gostitelje LAN in IoT. DNS ni dokaz dosegljive storitve. |
| 1.4 | Učni PDF vsebuje navedbo Maja Kovac, program in datum. Ujemanje z ekipo ne dokazuje avtorstva. |
| 1.5 | Imena iz certifikatov, odstranjene podvojitve in časovni kontekst; brez aktivnega preverjanja javnih tarč. |
| 2.1 | Dejanska odprta vrata vsaj treh javnih naslovov; brez predpostavke, da so vsa vrata iz pravil NAT tudi odprta. |
| 2.2 | Gost prebere `javno/seznam-naprav.csv`; `uprava` zavrne dostop. Seznam map in branje vsebine sta različna dokaza. |
| 2.3 | Apache 2.4.49 je namig. Privzeta omejitev poti preprečuje pričakovano izrabo; en negativen poskus ne pomeni popolne varnosti. |
| 2.4 | Odziv skript ftp-anon in smb-protocols; sprejmemo zapis dejanskega rezultata ali napake z razlago omejitve. |
| 2.5 | Povezava ugotovitve iz poročila z lastnim preverjanjem; ponazoritev je jasno ločena od dejanskega poročila. |
| 3.1 | Zahteva za lastno iskanje: metoda, pot, parameter, status in vsebina odgovora. |
| 3.2 | Authorization Basic se dekodira v zaposleni:acme123. Razlikovanje med lastnim ogledom zahteve in prisluškovanjem prenosu. |
| 3.3 | Prijava peter.horvat z razkritim geslom, whoami/hostname in odjava. Brez sklepa o višjih pravicah ali dostopu do IoT. |
| 3.4 | Običajna prijava je zavrnjena; spremenjena vrne authentication s pravim računom. Gesel in žetonov ne zbiramo v skupnih zapisih. |
| 3.5 | Žeton A in ID košarice B vrneta vsebino B. Identiteta A mora ostati enaka, ne sme biti administratorski račun iz vaje 3.4. |

## Sklepni pogovor

Vsak izbere eno ugotovitev: kaj je neposredno dokazal, kakšen vpliv predvideva in kako bi preveril popravek. Skupaj izberemo tri najkoristnejše ukrepe za ACME. Pri ocenjevanju šteje tudi kakovostno omejen sklep ob neuspelem preverjanju. Namig in postopek sta pomoč pri učenju, ne razlog za slabšo oceno.
