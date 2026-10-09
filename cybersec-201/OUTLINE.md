# Cybersec-201: Uvod v kibernetske operacije za radovedne

## Kratek povzetek

Delavnica je namenjena radovednim udeležencem brez poklicnega znanja informatike, tehnično spretnejšim uporabnikom in operativnim ekipam. Prvi sklop bo predstavil zbiranje javno dostopnih informacij in raziskovanje digitalnih sledi. Drugi sklop bo povezal osnove omrežij, segmentacijo in pregled izpostavljenih storitev. V tretjem sklopu bodo udeleženci v pripravljenem učnem okolju spoznali Kali Linux, dekodiranje podatkov in pregled spletnih zahtev ter ugotovitve povezali z obrambo. Delavnica traja 150 minut, od tega 55 minut predstavitve in 95 minut praktičnega dela.

## Načrt izvedbe

| Sklop | Predstavitev | Praktično delo | Skupaj |
| --- | --- | --- | --- |
| 1. Javno dostopne informacije in digitalne sledi | 20 minut | 30 minut | 50 minut |
| 2. Segmentacija omrežij in pregled ranljivosti | 20 minut | 30 minut | 50 minut |
| 3. Kali Linux in razmišljanje napadalca | 15 minut | 35 minut | 50 minut |
| **Skupaj** | **55 minut** | **95 minut** | **150 minut** |

Uvod je vključen v predstavitev prvega sklopa, zaključek pa v predstavitev tretjega. Čas praktičnega dela se razdeli med tri vaje posameznega sklopa. Spodnji opisi določajo namen prosojnic; končno besedilo, prikazi orodij, primeri in rešitve se pripravijo pozneje. Datoteka `slides.md` vsebuje enake naslove v enakem vrstnem redu, brez vsebine.

## Prosojnice po vrsti

### 1. sklop: Javno dostopne informacije in digitalne sledi

| Št. | Naslov prosojnice | Kaj bo prosojnica vsebovala |
| --- | --- | --- |
| 1 | Cybersec-201: Uvod v kibernetske operacije za radovedne | Naslov delavnice ter prostor za ime izvajalca in datum. |
| 2 | Cilji delavnice in priprava okolja | Predstavitev ciljne skupine in priprave prenosnika z VirtualBox ali VMware oziroma dostopom do vaj v brskalniku ter pogona USB. |
| 3 | Potek delavnice in dogovor o učnem okolju | Pregled treh sklopov, časovnega razporeda, dovoljenih učnih tarč in dela v izoliranem okolju. |
| 4 | Javno dostopne informacije in digitalne sledi | Uvod v prvi sklop in pregled vrst sledi, ki jih bodo udeleženci raziskovali. |
| 5 | Kaj je zbiranje javno dostopnih informacij | Predvidena razlaga pojma OSINT ter primerov uporabe v preiskovanju, novinarstvu in informacijski varnosti. |
| 6 | Kje puščamo digitalne sledi | Načrt prikaza povezav med fotografijami, uporabniškimi imeni, javnimi objavami in repozitoriji programske kode. |
| 7 | Metapodatki v fotografijah | Opis prikaza podatkov EXIF, med drugim lokacije, modela fotoaparata in časa nastanka, ter njihove morebitne odsotnosti. |
| 8 | Družbena omrežja in javni repozitoriji | Predvideni primeri povezovanja javnih profilov, odnosov med računi in informacij v objavljeni programski kodi. |
| 9 | Napredno iskanje z iskalniki | Načrt predstavitve iskalnih operatorjev za domeno, vrsto datoteke in del spletnega naslova na pripravljenih učnih primerih. |
| 10 | Preverjanje in povezovanje ugotovitev | Opis razprave o zanesljivosti virov, zastarelih podatkih in nevarnosti napačnega povezovanja enakih uporabniških imen. |
| 11 | Vaja 1.1: Preglej metapodatke fotografije | Navodila za pregled pripravljene fotografije z ExifTool ali spletnim pregledovalnikom ter zapis opaženih podatkov. |
| 12 | Vaja 1.2: Poišči javne učne dokumente | Navodila za uporabo naprednih iskalnih poizvedb za dokumente in odprte imenike na določenih učnih domenah. |
| 13 | Vaja 1.3: Razišči uporabniško ime | Navodila za preverjanje pripravljenega javnega psevdonima z WhatsMyName.app ter presojo, ali najdeni profili pripadajo isti osebi. |
| 14 | Pogovor o ugotovitvah prvega sklopa | Vprašanja za primerjavo rezultatov vaj in povezavo ugotovljenih digitalnih sledi z ukrepi za zasebnost. |

### 2. sklop: Segmentacija omrežij in pregled ranljivosti

| Št. | Naslov prosojnice | Kaj bo prosojnica vsebovala |
| --- | --- | --- |
| 15 | Od omrežja do izpostavljenih storitev | Uvod v drugi sklop in pregled povezave med napravami, storitvami in ranljivostmi. |
| 16 | Naslovi IP in podomrežja | Načrt preproste sheme omrežja za razlago naslovov IP, podomrežij in dosegljivosti naprav. |
| 17 | Vrata in omrežni protokoli | Predviden prikaz povezave med omrežnimi vrati in storitvami HTTP, SSH ter SMB. |
| 18 | Zakaj razdelimo omrežje | Opis sheme, ki primerja skupno omrežje z ločenimi skupinami osebnih, službenih in pametnih naprav. |
| 19 | Omrežje za goste in navidezna lokalna omrežja | Predvidena primerjava omrežja za goste in segmentacije z VLAN ter pomena pravil za promet med segmenti. |
| 20 | Odkrivanje naprav z Nmap in Zenmap | Načrt prikaza osnovnega odkrivanja naprav in storitev v pripravljenem omrežju prek grafičnega vmesnika. |
| 21 | Pregled storitev in ranljivosti | Opis razlike med odkrivanjem odprtih vrat z Nmap in širšim pregledom ranljivosti z OpenVAS na že pripravljenih rezultatih. |
| 22 | Kako razlagamo zadetke in oznake CVE | Predviden prikaz branja različic, iskanja v NVD ali CVE Details ter preverjanja, ali ugotovitev velja za konkretno napravo. |
| 23 | Vaja 2.1: Odkrij naprave v učnem omrežju | Navodila za pregled izoliranega omrežja z Zenmap oziroma Fing na telefonu ter izdelavo preprostega zemljevida aktivnih naprav. |
| 24 | Vaja 2.2: Prepoznaj omrežne storitve | Navodila za pregled vrat na določeni učni napravi in povezovanje rezultatov s spletnimi storitvami, oddaljenim dostopom in deljenjem datotek. |
| 25 | Vaja 2.3: Preveri možne ranljivosti | Navodila za primerjavo ugotovljenih različic z zapisi CVE, preverjanje pogojev za ranljivost in zapis predlaganega obrambnega ukrepa. |
| 26 | Pogovor o ugotovitvah drugega sklopa | Vprašanja za primerjavo zemljevidov omrežja in izbiro prednostnih ukrepov za izpostavljene storitve. |

### 3. sklop: Kali Linux in razmišljanje napadalca

| Št. | Naslov prosojnice | Kaj bo prosojnica vsebovala |
| --- | --- | --- |
| 27 | Kali Linux v učnem okolju | Uvod v tretji sklop in pregled pripravljenega navideznega računalnika oziroma zagonskega pogona USB. |
| 28 | Faze napadalčevega pristopa | Načrt sheme od zbiranja informacij prek pregledovanja in izrabe ranljivosti do dejavnosti po pridobitvi dostopa. |
| 29 | Kaj vsebuje Kali Linux | Predviden prikaz namizja, vnaprej nameščenih varnostnih orodij in njihove razvrstitve po namenu. |
| 30 | Kako ugotovitve uporabimo za obrambo | Opis povezovanja posameznih faz napada z možnostmi preprečevanja, zaznavanja in omejevanja posledic. |
| 31 | Kodiranje podatkov in CyberChef | Načrt kratkega prikaza razlike med kodiranjem in šifriranjem ter sestavljanja postopka za dekodiranje podatkov. |
| 32 | Spletne zahteve, obrazci in piškotki | Predviden prikaz poti zahteve HTTP, poslanih podatkov obrazca in varnostnih zastavic piškotkov v učni aplikaciji. |
| 33 | Razvijalska orodja in prestrezni posrednik | Opis prikaza pregleda prometa z razvijalskimi orodji Firefox ter po potrebi z OWASP ZAP ali Burp Suite Community. |
| 34 | Vaja 3.1: Razišči Kali Linux | Navodila za zagon pripravljenega navideznega računalnika ali zagonskega pogona USB ter raziskovanje namizja in menijev varnostnih orodij. |
| 35 | Vaja 3.2: Dekodiraj pripravljene podatke | Navodila za uporabo CyberChef pri dekodiranju nizov Base64, parametrov spletnih naslovov in pripravljenih kodiranih podatkov. |
| 36 | Vaja 3.3: Preglej promet učne spletne aplikacije | Navodila za pregled zahtev, prestrezanje podatkov obrazca in pregled zastavic piškotkov v lokalni aplikaciji OWASP Juice Shop. |
| 37 | Pogovor o ugotovitvah tretjega sklopa | Vprašanja za primerjavo rezultatov vaj ter razlikovanje med opazovanjem podatkov, spreminjanjem zahtev in izrabo ranljivosti. |
| 38 | Od ugotovitve do obrambnega ukrepa | Prostor za zaključni zapis opažene izpostavljenosti, dokazov, omejitev ugotovitve in predlagane izboljšave zaščite. |
| 39 | Vprašanja in zaključek | Prostor za vprašanja, povratne informacije in povezavo nazaj na pregled delavnic. |

## Priprava izvajalca

- Izolirano brezžično učno omrežje ali namenski usmerjevalnik s tremi do petimi pripravljenimi napravami.
- Vnaprej prenesena in preizkušena slika Kali Linux, pogoni USB ter možnost izvedbe vaj v brskalniku.
- Vnaprej nameščen Zenmap; rezultate OpenVAS pripraviti vnaprej, da namestitev in konfiguracija ne porabita časa delavnice.
- Lokalna učna spletna aplikacija, na primer OWASP Juice Shop v vsebniku Docker, ter preverjen dostop iz učnega okolja.
- Pripravljena fotografija z metapodatki, učne domene, javni učni psevdonim in kodirani vzorci za CyberChef.
