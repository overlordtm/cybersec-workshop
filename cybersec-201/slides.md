# Cybersec-201: Uvod v kibernetske operacije za radovedne

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

Izmišljeno podjetje ACME · pripravljeno učno okolje

Andraž Vrhovec, Koofr d.o.o.

oktober 2026

Note:
ACME nas prosi za pregled izpostavljenosti. Sledili bomo podatkom od javne objave do storitve in preverili, kaj ugotovitve pomenijo za obrambo. Uvod in orientacija skupaj trajata pet minut.

---

## Eno podjetje, trije pogledi

- **Digitalne sledi:** kaj o ACME izvemo od zunaj?
- **Omrežje:** katere storitve lahko dosežemo?
- **Preverjanje:** kaj nam povedo zahteve in odzivi?

**Najprej vsi trije sklopi, nato praktično delo.**

Note:
Predstavitev s prikazi traja 36 minut. Sledijo 104 minute praktičnega dela in deset minut skupnega pogovora. Podrobna navodila so na ločeni strani; ne prekinjamo vsakega sklopa z nalogami.

---

## Naše učno okolje

- Kali Linux odpreš v brskalniku prek pripravljenega namizja.
- Firefox, terminal in varnostna orodja so že pripravljeni.
- Aktivno preverjamo samo določene učne tarče ACME.
- Javni iskalniki kažejo podatke, ki so jih zbrali njihovi ponudniki.

**Za začetek zadostujeta brskalnik in prijava.**

Note:
Pokaži prijavo na https://lab.digilab-g.rtfm.si/, Firefox in terminal. Lastni Kali z WireGuard je dodatna možnost, ne pogoj. Javne iskalnike odpremo v brskalniku na lastnem računalniku. Lab ima omejen dostop v internet; njegovi simulirani javni naslovi niso resnična javna infrastruktura.

---

## 1. sklop: Javno dostopne informacije

- OSINT povezuje informacije iz javno dostopnih virov.
- Spletna stran razkrije ljudi, kontakte in povezane storitve.
- Dokument lahko vsebuje avtorja, čas in uporabljeno programsko opremo.
- Fotografija lahko vsebuje lokacijo; metapodatki lahko tudi manjkajo.

**Objavljena sled še ni preverjeno dejstvo.**

Note:
Osem minut za celoten prvi sklop. Poveži spletne strani, družbena omrežja in repozitorije. Isti psevdonim ni dokaz iste osebe. Metapodatki so lahko odstranjeni ali spremenjeni; ne sklepamo na podlagi ene sledi.

---

## Iskalniki za infrastrukturo

- [Shodan](https://www.shodan.io/) išče internetno izpostavljene naprave in njihove storitve.
- [Censys](https://censys.com/) povezuje podatke o gostiteljih, spletnih storitvah in certifikatih.
- [SecurityTrails](https://securitytrails.com/) pomaga raziskovati zapise DNS, poddomene in zgodovino infrastrukture.
- [crt.sh](https://crt.sh/) omogoča iskanje domenskih imen v javnih dnevnikih certifikatov.

Note:
Samo kratka orientacija: po en stavek o vsakem orodju, brez štirih demonstracij. Shodanov zapis ima čas opažanja; geolokacija ne dokazuje fizične lokacije strežnika. Obseg funkcij je odvisen od dostopa in naročnine.

---

## Iskalniki za razkritja in zgodovino

- [DeHashed](https://dehashed.com/) omogoča raziskovanje razkritih identitetnih in poverilnih podatkov.
- [IntelX](https://intelx.io/) išče po indeksiranih dokumentih, arhivih in razkritjih.
- [Have I Been Pwned](https://haveibeenpwned.com/) pomaga preveriti pojav e-poštnega naslova v znanih razkritjih.
- [VirusTotal](https://www.virustotal.com/) povezuje opažanja o datotekah, naslovih in domenah.
- [Wayback Machine](https://web.archive.org/) prikazuje arhivirane različice spletnih strani.

Note:
Orodja le omenimo. Zadetki lahko vsebujejo stare ali napačno povezane podatke. Ne prikazuj resničnih razkritih gesel udeležencev. Nekatere funkcije zahtevajo račun ali plačilo. Za iskanje po spletu omenimo še operatorje site:, filetype: in inurl:.

---

## Od sledi do ugotovitve

**Vir → opažanje → preverjanje → omejitev**

- Kje in kdaj smo podatek našli?
- Ali ga podpira še drug vir?
- Kaj je dejstvo in kaj naša domneva?
- Razkrit naslov naprave ne pomeni, da jo lahko dosežemo.

<aside class="humor">Iskalnik ima spomin. Tudi za stran, ki smo jo »že zdavnaj odstranili«.</aside>

Note:
Kratek primer: ime zaposlenega na spletni strani in avtor dokumenta sta dve sledi, ne samodejen dokaz lastništva računa. robots.txt je navodilo robotom, ne nadzor dostopa. DNS poizvedbe in prenosi območja so neposredne zahteve strežniku, zato jih izvajamo samo v dogovorjenem okolju.

---

## 2. sklop: Od naslova do storitve

| Pojem | Primer v ACME |
| --- | --- |
| Naslov IP: kam pošljemo promet | `198.51.100.11` |
| Vrata: katero storitev iščemo | `80` |
| Protokol: kako se sporazumevamo | HTTP |
| Podomrežje: skupina naslovov | `172.20.20.0/24` |

**Naprava lahko ponuja več storitev.**

Note:
Dvanajst minut za drugi sklop, od tega štiri za Greenbone. /24 na kratko razloži kot skupino naslovov z istimi prvimi tremi deli, brez računanja mask. SSH je običajno na 22, DNS na 53, HTTPS na 443, SMB na 445; številka sama še ne potrdi vrste storitve.

---

## Ista vtičnica, drugačna dosegljivost

| Položaj udeleženca | Dosegljivo |
| --- | --- |
| Internet | objavljene javne storitve |
| Obiskovalec v pisarni | LAN in dovoljene storitve DMZ |
| Omrežje brez segmentacije | tudi kamere, tiskalnik in krmilnik klime |

**Segmentacija omeji, kam lahko nadaljujemo.**

Note:
Pokaži preprosto pot: udeleženec → požarni zid → DMZ / LAN / IoT. VLAN loči omrežja, pravila določijo prehode. V ACME je tudi namerna napaka DMZ → IoT, ki jo lahko pokažemo kot posledico morebitnega dostopa v DMZ. Ne obljubljaj izvedljivega prehoda prek spletnega strežnika brez predhodno potrjenega dostopa.

---

## Nmap: kaj odgovarja?

- Odkrivanje naprav pomaga sestaviti začetni zemljevid.
- Pregled vrat pokaže dosegljive storitve.
- Prepoznavanje storitev doda namige o programski opremi.
- Rezultat velja za določeno izhodišče in trenutek.

**Odprta vrata so opažanje, ne dokaz ranljivosti.**

Note:
Kratek pripravljen izpis Nmap za www in SSH. V tem labu primerjamo odprte storitve; razlika closed/filtered ni zanesljiva razlaga delovanja požarnega zidu. Tudi odgovor pri odkrivanju gostiteljev še ne pomeni dosegljive storitve. Zenmap je lahko dodatni grafični prikaz, če je nameščen.

---

## Greenbone: od pregleda do poročila

**Prikaz pripravljenega pregleda ACME**

1. Tarča in obseg pregleda.
2. Ena ugotovitev: storitev, dokaz, resnost in zanesljivost zaznave.
3. Povezana ranljivost in pogoji zanjo.
4. Predlagan ukrep ter ponovni pregled.

**Poročilo usmeri preverjanje; vsako ugotovitev presodimo.**

Note:
Štiriminutni prikaz vmesnika. Odpri že končan pregled; po želji zaženi nov pregled ene učne tarče, vendar ne čakaj na zaključek. Razloži razliko med resnostjo in Quality of Detection. Pripravi izvoženo poročilo ali posnetke za primer nedosegljivosti. Greenbone mora biti nameščen in podatkovni viri posodobljeni pred dogodkom.

---

## Različica → CVE → preverjanje

- Oznaka CVE poimenuje znano ranljivost.
- Ujemanje različice je začetni namig.
- Pomembni so konfiguracija, popravki in dosegljiva funkcija.
- Zapišemo potrjeno vedenje in meje preverjanja.

**»Stara različica« in »potrjena izraba« sta različni ugotovitvi.**

Note:
ACME uporablja Apache 2.4.49. V priloženi konfiguraciji je dostop zunaj DocumentRoot zavrnjen, zato ne pričakujemo uspešne izrabe CVE-2021-41773 samo zaradi pasice. Poveži s pregledom Greenbone: zaznava na podlagi različice ni enaka preverjeni izrabi. Vir za konkretno ranljivost: https://httpd.apache.org/security/vulnerabilities_24.html .

---

## 3. sklop: Kako razmišlja preizkuševalec

**Zberi → preglej → preveri → razloži posledice**

- Kali združuje orodja; ugotovitve še vedno presoja človek.
- Izpostavljena datoteka lahko razkrije poverilnico.
- Ponovljeno geslo lahko odpre drugo storitev.
- Obramba prekine povezavo med koraki.

<aside class="humor">Kali ima veliko orodij. Gumba »razumi rezultat« še nima.</aside>

Note:
Enajst minut za tretji sklop. Brez dolgega sprehoda po menijih Kali. Poudari minimalen dokaz in razumevanje vpliva. Ne spreminjamo skupnih gesel ali stanja naprav. SSH dostop sam po sebi ne dokazuje skrbniških pravic ali dostopa do drugih segmentov.

---

## Kaj potuje v spletni zahtevi?

| Del | Kaj lahko vsebuje |
| --- | --- |
| Naslov in metoda | cilj ter vrsta dejanja |
| Glave | vrsta vsebine, piškotki, prijavni podatki |
| Telo | podatki obrazca ali JSON |
| Odgovor | status, vsebina, nove nastavitve piškotkov |

**HTTPS šifrira prenos; brskalnik še vedno vidi svoje podatke.**

Note:
Kratek prikaz zavihka Omrežje v Firefoxu na Juice Shop. Izberi eno zahtevo, pokaži metodo, status in telo. Za lastno zahtevo ne potrebujemo prestreznega posrednika. ZAP ali Burp sta dodatni orodji, ne dodaten obvezen postopek namestitve.

---

## Kodiranje ni šifriranje

- Base64 spremeni zapis podatkov in ne potrebuje skrivnega ključa.
- Kodiranje URL omogoča zapis posebnih znakov.
- CyberChef sestavlja postopke za pretvarjanje podatkov.
- HTTP Basic uporablja Base64; zaščito prenosa zagotavlja HTTPS.

**Berljivost podatkov ni merilo njihove zaščite.**

Note:
Pokaži izmišljeni niz dWNlbmVjOnVjbm8= in rezultat ucenec:ucno. Pripravi lokalni CyberChef v Kali in preveri zagon pred delavnico. Razloži, da dekodiranje lastne zahteve v orodjih brskalnika ne dokazuje možnosti prisluškovanja tretje osebe; pri HTTP podatki po omrežju nimajo zaščite TLS.

---

## Piškotek predstavlja sejo

- `Secure`: brskalnik piškotek pošilja prek HTTPS.
- `HttpOnly`: omeji dostop JavaScript do piškotka.
- `SameSite`: omeji pošiljanje pri zahtevah med spletnimi mesti.
- Namen piškotka določa, katere zaščite potrebuje.

**Vrednost seje obravnavamo kot skrivnost.**

Note:
Pokaži le piškotke, ki v pripravljeni različici aplikacije dejansko obstajajo. Odsotnost zastavice na nenevarnem nastavitvenem piškotku ni samodejno ranljivost. Če prijava uporablja žeton v drugem delu brskalnika, to jasno povej in ne izmišljaj sejnega piškotka.

---

## Od ugotovitve do zaščite

**Kaj smo opazili → dokaz → vpliv → ukrep**

- Javna varnostna kopija → odstranitev in menjava razkritih poverilnic.
- Dosegljiv IoT → omejitev prometa med segmenti.
- Prijava prek HTTP → HTTPS in preverjanje konfiguracije.
- Sumljiva različica → preverjanje pogojev in posodobitev.

**Dober rezultat je razumljiva in preverljiva izboljšava.**

Note:
Zaključi predstavitveni del. Skupni pogovor sledi šele po celotnem praktičnem bloku: udeleženci primerjajo dokaze in izberejo tri prednostne ukrepe. Vse konkretne naloge in izbira težavnosti so na ločeni strani vaje/; prosojnice ne vsebujejo navodil za vaje.
