## 1. sklop · Digitalne sledi

**Kaj lahko o podjetju izvemo iz javnih virov?**

![Spletna stran, dokument in repozitorij kot viri sledi](./images/traces.svg)

ACME: ljudje, domenska imena, dokumenti in objavljene storitve.

Note:
Za prvi sklop skupaj sedem minut. Začnemo neposredno z vsebino, brez naslovnice ali organizacijskega uvoda. ACME je izmišljeno podjetje v pripravljenem laboratoriju. OSINT pomeni zbiranje in povezovanje javno dostopnih informacij. Varnostni pregled začnemo z vprašanjem, kaj podjetje že razkriva o sebi. Predhodno uredimo prijave; dostop in obseg preverjanja sta opisana na strani z vajami.

---

## Kaj razkrijejo stran in dokumenti?

<div class="example">
<div class="example-label">PRIPRAVLJENI UČNI METAPODATKI · ACME PDF</div>

```plaintext
Title:    Interni cenik 2026
Author:   Maja Kovac
Creator:  LibreOffice 7.0
Created:  2026-09-14
```

</div>

Na strani »O nas« najdemo Majo Kovač, odgovorno za finance.

**Podatka se ujemata. Avtorstvo še ni dokazano.**

Note:
Pripravljeni dokument je na www.acme.lab/dokumenti/cenik-2026.pdf in v deljeni mapi javno. Metapodatke preberemo z ExifTool. Ime lahko izvira iz predloge ali drugega računalnika. Pojasni razliko med podatkom v dokumentu in našim sklepom o osebi. Fotografije lahko vsebujejo tudi podatke GPS. Ukrep: pred objavo preverimo vidno vsebino in metapodatke. Brez dolgega naštevanja polj.

---

## Iskanje omejimo na uporabne sledi

<div class="example">
<div class="example-label">PRIMER SINTAKSE · IZMIŠLJENA DOMENA</div>

```plaintext
site:podjetje.example filetype:pdf
site:podjetje.example inurl:backup
```

</div>

[Wayback Machine](https://web.archive.org/) pokaže stare objave.

[crt.sh](https://crt.sh/) razkrije imena iz javnih certifikatov.

**Čas objave in izvor podatka sta del ugotovitve.**

Note:
Operatorja omejita domeno ter vrsto datoteke oziroma del naslova. Učna domena acme.lab ni javno indeksirana; za javne vire uporabimo domeno, izbrano pred dogodkom, in pripravljen posnetek kot rezervo. Certifikat lahko vsebuje staro ali nadomestno ime; ne potrjuje delujoče storitve. Izvorna koda in robots.txt na ACME lahko pokažeta pozabljene poti. Tehnične posledice objave kopije obravnavamo v tretjem sklopu. Druga orodja so povezave v gradivu, ne katalog dodatnih prosojnic.

---

## Shodan: kaj je bilo zaznano in kdaj?

<div class="example">
<div class="example-label">PONAZORITEV ZADETKA · NI REZULTAT ŽIVEGA PREGLEDA</div>

```plaintext
Naslov         [izbrani javni IP]
Organizacija   [podatek ponudnika]
80/tcp         [opažena storitev in odziv]
Opaženo        [datum pri storitvi]
```

</div>

Preberemo storitev, odziv in čas zadnjega opažanja.

**Oznaka CVE je namig za preverjanje.**

Note:
Približno minuto namenimo prikazu že izbranega resničnega zadetka v Shodanu. Ne iščemo simuliranih naslovov 198.51.100.x. Lokacija je ocena ponudnika, ne dokaz fizične lokacije naprave. Trenutne dosegljivosti iz zgodovinskega zapisa ne moremo potrditi. Censys je lahko omenjen kot alternativa. Pri ponudniku ne naročamo novega pregleda javne tarče. Pripravi datiran posnetek za primer omejitev dostopa.

---

## Povežimo podatke, preverimo sklep

| Sled | Kaj izvemo? | Kaj še manjka? |
| --- | --- | --- |
| Ime v dokumentu | Navedeni avtor | Potrditev avtorstva |
| Ime v certifikatu | Objavljeno domensko ime | Trenutno stanje storitve |
| Zapis v Shodanu | Preteklo opažanje | Nova meritev |

**Vir + čas + neodvisna potrditev → utemeljen sklep.**

Note:
Zaključi digitalne sledi z razliko med opaženim in sklepom. Enako uporabniško ime samo ne povezuje dveh oseb. Udeleženci lahko izberejo osnovni profil Shodan, spletne namige ali DNS; dodatna izziva sta dokument in certifikati. DNS AXFR ostane v praktični vaji 1.3 po poznejšem dogovoru, tehnično razlago pa umestimo med omrežne storitve. Nadaljuj neposredno na Omrežja; vse vaje so po vseh treh sklopih.

---

## 2. sklop · Omrežja

**Katere storitve lahko dosežemo?**

![DMZ, LAN in IoT podjetja ACME](./images/acme.svg)

IP določi naslov · vrata označijo storitev · TCP in UDP ločimo.

Note:
Za Omrežja skupaj štirinajst minut. Na shemi razloži eno pot: Kali do spletnega strežnika ter do notranje naprave. IP je naslov omrežnega vmesnika, vrata pa številka v transportnem protokolu, prek katere je storitev dosegljiva. Isti strežnik lahko ponuja več storitev. 53/tcp in 53/udp nista ista meritev. DMZ vsebuje javne strežnike, LAN delovne naprave in datoteke, IoT kamero, tiskalnik ter krmilnik. Omrežje 198.51.100.0/24 v labu simulira javni internet.

---

## Nmap: od vrat do storitve

<div class="example">
<div class="example-label">UKAZ ZA UČNO TARČO · IZPIS JE PONAZORITEV</div>

```plaintext
nmap -Pn -sT -sV -p 80 198.51.100.11

PORT    STATE  SERVICE  VERSION
80/tcp  open   http     Apache httpd 2.4.49
```

</div>

`-p` izbere vrata · `-sV` preveri vrsto in različico storitve.

**Odprta vrata potrdijo dostop. Ranljivost preverimo posebej.**

Note:
Kratek prikaz na dejanski tarči; pripravi izpis kot rezervo. -Pn preskoči odkrivanje prisotnosti, -sT preveri povezavo TCP. Ime storitve brez -sV lahko temelji samo na številki vrat. Odprta storitev ni samodejno napaka; pomembno je, kdo jo potrebuje. Ukrep pri nepotrebni izpostavljenosti: storitev odstranimo ali omejimo dovoljene izvore. V tem laboratoriju odprto/neodprto zanesljiveje pokaže dostop kot razlika med closed in filtered.

---

## DNS: kdo lahko prenese celotno območje?

<div class="example">
<div class="example-label">UČNA TARČA ACME · IZSEK PRIČAKOVANIH ZAPISOV</div>

```plaintext
dig @198.51.100.14 acme.lab AXFR

files.acme.lab.     A  172.20.20.10
intranet.acme.lab.  A  172.20.20.11
cam01.acme.lab.     A  172.20.30.10
```

</div>

**Napaka:** prenos območja je dovoljen vsakomur.

**Ukrep:** omejimo AXFR in ločimo notranje podatke DNS.

Note:
AXFR prenese podatke območja in je namenjen med drugim izmenjavi med ustreznimi strežniki DNS. V ACME allow-transfer any razkrije tudi notranja imena. To je neposredna poizvedba učnemu strežniku. Dokaz je vrnjeno območje, ne zgolj odprta vrata 53. Ime in naslov ne dokazujeta dosegljive storitve. Ne trdimo, da so vsa notranja imena sama po sebi skrivnost; presodimo, ali je tako razkritje namerno.

---

## SMB: kdo lahko bere deljene datoteke?

<div class="example">
<div class="example-label">DVA KORAKA · UČNI DATOTEČNI STREŽNIK</div>

```plaintext
smbclient -N -L //172.20.20.10
smbclient -N //172.20.20.10/javno -c 'ls'
```

</div>

Seznam map → dostop do vsebine → pregled dovoljenj.

**Napaka:** gost lahko bere podatke o notranjih napravah.

**Ukrep:** uredimo dostop gostov in vsebino deljenih map.

Note:
-N preskoči poziv za geslo. Ime mape uprava je lahko vidno, čeprav vsebine ne moremo brati. Pokaži razliko med javno in uprava, ne razkrivaj gesel. Datoteka seznam-naprav.csv v javno razkriva naslove in lokacije. Javno branje ni vedno napaka; težava je neskladje z namenom podatkov. Enum4linux-ng lahko zbere širši pregled SMB, osnovno razliko pa jasneje pokažeta dva ukaza smbclient. Vaja ne zahteva spremembe segmentacije.

---

## Kako segmentacija spremeni dostop?

![V visitor so IoT storitve omejene, v flat pa dosegljive iz istega Kali](./images/segmentation-compare.svg)

**Isti Kali, ista tarča in isti pregled; spremenijo se pravila.**

Note:
Približno dve minuti za skupni prikaz segmentacije, pred samostojnimi vajami. Enak omejen pregled vrat 80,445,502,554,9100 izvedi nad files in IoT najprej v visitor, nato v flat. Primerjaj odprta vrata; za rezervo pripravi oba izpisa. Krmilnik hvac v flat pokaže 80 in 502, kamera 80 in 554. Ločen VLAN brez pravil ne zagotovi omejitve dostopa. Povezave, odprte pred preklopom, lahko ostanejo, zato uporabljamo nove preglede. Po naslednjem prikazu SNMP nastavi visitor za ves praktični blok. Napaka DMZ → IoT je ločeno vprašanje, ki zahteva meritev iz DMZ; s tem prikazom je ne dokazujemo.

---

## IoT: dostop do naprav in njihovih podatkov

| Naprava | Storitev | Kaj preverimo? |
| --- | --- | --- |
| Kamera | HTTP, RTSP 554/tcp | Izpostavljenost vmesnika |
| Tiskalnik | SNMP 161/udp | Podatke s skupnostjo `public` |
| Klima | Modbus 502/tcp | Dosegljivost krmilnika |

<div class="example">


```plaintext
snmpwalk -v2c -c public 172.20.30.11 1.3.6.1.2.1.1
```

</div>

**Ukrep:** dostop omejimo na potrebne upravljavske poti.

Note:
Kratek prikaz samo v flat med predstavitvijo: SNMP vrne ime, lokacijo in kontakt. Ukaz uporablja številčni OID, da ne potrebuje dodatnih imen MIB. Uporabi le branje. Nato vrni visitor in preveri stanje; samostojne vaje nimajo preklopov. Kamera je statični prijavni obrazec s simuliranim odgovorom RTSP, ne prava kamera; ne obljubljaj ogleda videa ali uspešne prijave. Na Modbus ne pošiljamo ukazov za spremembo nastavitev. Ukrep pri SNMP: omejitev izvorov in ustrezno zaščiten SNMPv3. Wireshark lahko pokaže lasten oziroma pripravljen promet; v preklopljenem omrežju ne vidi samodejno vsega tujega prometa.

---

## Zastarela storitev: kaj pove različica?

![Zaznana različica, pogoji in potrditev vedenja so ločeni koraki](./images/verification.svg)

**Nmap prepozna storitev. Naslednji preizkus preveri konkreten pogoj.**

Note:
Uporabi Metasploitable 2 na 172.20.20.30 kot primer starega notranjega strežnika. Nmap -sV pokaže programe; izbrana skripta NSE, denimo ftp-anon ali smb-protocols, preveri konkretno nastavitev. Ne zaganjamo vseh skript. Zastarel program je razlog za ukrep, vendar lahko različica v odzivu zavaja ali ima paket prenesene popravke. V aplikacijskem sklopu pokažemo še Apache, kjer privzeta omejitev poti vpliva na možnost izrabe. Odprava: nadgradnja oziroma zamenjava nepotrebne storitve in ponovna meritev.

---

## Greenbone: preverimo eno ugotovitev

| V poročilu | Vprašanje za preizkuševalca |
| --- | --- |
| Tarča in dokaz | Kaj je bilo izmerjeno? |
| Resnost | Kakšne so lahko posledice? |
| Quality of Detection | Kako zanesljiva je metoda zaznave? |
| Predlog odprave | Kaj spremenimo in kako preverimo popravek? |

**Opozorilo pregledovalnika povežemo z odzivom storitve.**

Note:
Dve minuti za eno ugotovitev iz končanega dejanskega poročila. Pred dogodkom osveži vire, izberi ugotovitev in pripravi izvoz. Ne čakaj na nov pregled. Pokaži dokaz; če temelji na različici, to povej. CVSS oziroma prikazana resnost ni verjetnost napada. Quality of Detection opisuje metodo zaznave, ne potrjuje vseh pogojev izrabe. Greenbone v tem labu teče ločeno na https://10.20.0.11/; paket gvm je na voljo tudi v Kali. Udeleženci dobijo izsek za samostojno presojo v dodatni vaji 2.5.

---

## 3. sklop · Aplikacije

**Kaj se zgodi z našim vnosom?**

<div class="example">
<div class="example-label">UČNI PRIMER JUICE SHOP · ZAHTEVA IN OBLIKA ODGOVORA</div>

```plaintext
GET /rest/products/search?q=jabolko HTTP/1.1
Host: shop.acme.lab

HTTP/1.1 200 OK
Content-Type: application/json

{"status":"success","data":[...]}
```

</div>

Metoda in pot → podatki → obdelava → odgovor.

Note:
Za Aplikacije skupaj štirinajst minut. Razloži HTTP na eni zahtevi, brez ločenega predavanja o vseh statusih. Iskalni niz je v URL, pri prijavi so podatki v telesu JSON. Data z ... je ponazoritev oblike, ne veljaven zajeti JSON. Status 200 beremo skupaj z vsebino. 401 navadno pomeni manjkajočo ali neveljavno prijavo, 403 zavrnjen dostop. Spletna aplikacija lahko vsebuje napako tudi, ko sta prenos in strežnik pravilno nastavljena.

---

## ZAP: zahtevo spremenimo in ponovimo

![Brskalnik pošlje zahtevo prek lokalnega ZAP do aplikacije](./images/zap.svg)

**Ohranimo izhodišče, spremenimo en podatek in primerjamo odgovor.**

Note:
Približno dve minuti za orodje, skupaj z naslednjim prikazom IDOR največ pet minut. V ZAP zaženi njegov brskalnik, da ni potrebna ročna sprememba Firefoxovega proxyja Squid. Pokaži zgodovino zahtev in odpiranje zahteve za urejanje ter ponovno pošiljanje. Pri lokalnih tarčah ZAP ne sme uporabljati zunanjega proxyja. Začnemo z ogledom ene zahteve; ne zaganjamo samodejnega aktivnega pregleda. Firefox F12 je najlažja alternativa za opazovanje, Burp Suite Community pa alternativa za prestrezanje in ponavljanje. Žetonov ne projiciraj v celoti.

---

## Razkrite datoteke: kopija na javni strani

<div class="example">
<div class="example-label">UČNA TARČA ACME</div>

```plaintext
curl http://www.acme.lab/backup/config.php.bak

# Razkrito: notranje ime in prijavni podatki.
```

</div>

**Dokaz:** vsebina datoteke je dosegljiva brez prijave.

**Ukrep:** odstranimo kopijo in zamenjamo razkrite skrivnosti.

Note:
To je posledica sledi, ki smo jo omenili v prvem sklopu. Robots.txt ali odsotnost povezave datoteke ne zaščitita. Prikaži samo vrste podatkov, vrednosti gesla prekrij. curl preveri konkretno pot; ffuf pomaga odkrivati poti z omejenim seznamom imen. Ne izvajaj množičnih pregledov skupnih tarč. Razkrito geslo je lahko ponovno uporabljeno na SSH; vaja 3.3 samostojno preverja to povezavo z minimalnim dokazom dostopa. Prikaz ni zagotovilo skrbniških pravic.

---

## Prijava: geslo in zaščita prenosa

| Primer ACME | Težava | Ukrep |
| --- | --- | --- |
| NAS | Predvidena privzeta prijava | Zamenjava privzetih podatkov |
| Intranet | HTTP Basic brez TLS | HTTPS in omejen dostop |

<div class="example">
<div class="example-label">IZMIŠLJENA UČNA PODATKA</div>

```plaintext
Authorization: Basic dWNlbmVjOnVjbm8=
                       ↓ From Base64
                    ucenec:ucno
```

</div>

**Base64 je kodiranje. HTTPS zaščiti prenos.**

Note:
Privzeto prijavo NAS potrdi pred dogodkom; kamera nima delujočega prijavnega zaledja. Vrednost zgoraj je rezervni učni niz, ne zajem intraneta. Na intranetu se Basic dekodira v pripravljena podatka zaposleni:acme123. Lokalni CyberChef izvede From Base64. Lastni brskalnik vidi podatke tudi pri HTTPS, kar ni dokaz prisluškovanja tretje osebe. Razlikuj preverjanje identitete od pravic do podatkov; to pripravlja naslednji primer IDOR. Ne spreminjamo skupnega gesla NAS med delavnico.

---

## SQL injection: vnos spremeni poizvedbo

<div class="example">
<div class="example-label">POENOSTAVLJENA POIZVEDBA · UČNI PRIMER</div>

```plaintext
SELECT ... WHERE email = '[vnos]'
             AND password = ...

Vnos: admin@juice-sh.op'--

SELECT ... WHERE email = 'admin@juice-sh.op'-- ...
```

</div>

**Napaka:** aplikacija podatke združi z navodili SQL.

**Ukrep:** parametrizirane poizvedbe ločijo podatke od kode.

Note:
Pokaži osnovni mehanizem, celoten postopek je v dodatni vaji 3.4. V Juice Shop v20.3.0 login.ts sestavi poizvedbo iz req.body.email; narekovaj zaključi niz, -- pa izloči nadaljnji pogoj. V vaji uporabljamo presledek za -- in JSON v ponovljeni zahtevi, da nismo odvisni od omejitev obrazca. Dokaz obhoda je vrnjen prijavni objekt z računom, ne samo 200. Ne razlagaj, da zadošča splošno čiščenje vnosa. Sqlmap je orodje za avtomatizirano preverjanje SQL injection, ne univerzalen iskalnik aplikacijskih napak.

---

## XSS: vnos postane skripta v brskalniku

<div class="example">
<div class="example-label">POENOSTAVLJEN PRIMER KODE V BRSKALNIKU</div>

```javascript
// Nevarno, če vnos vsebuje nezaupanja vreden HTML:
rezultat.innerHTML = vnos;

// Za prikaz navadnega besedila:
rezultat.textContent = vnos;
```

</div>

**Napaka:** brskalnik vnos obravnava kot izvajalno vsebino.

**Ukrep:** varen DOM in kontekstu primerna obdelava izhoda.

Note:
XSS pomeni cross-site scripting. V Juice Shop uporabimo lokalni DOM XSS za prikaz učnega sporočila, ki ne spreminja skupnih podatkov. Posledice XSS so odvisne od konteksta aplikacije in razpoložljivih pravic. DOM primer se lahko izvede v brskalniku; samo pregled odziva HTTP ga ne potrdi. ZAP pomaga pregledati zahteve, ročni ogled DOM in vedenja pa ostane pomemben. textContent je ustrezna izbira za navadno besedilo; za dovoljen HTML potrebujemo ustrezno sanitizacijo. CSP je dodatna plast zaščite. Ne obljubljaj, da bo pasivni pregled ZAP samodejno odkril vse XSS.

---

## Prijava še ne pomeni pravice do vseh podatkov

<div class="example">
<div class="example-label">PONAZORITEV ID-JEV · PRIJAVNI ŽETON OSTAJA OD A</div>

```plaintext
Račun A → GET /rest/basket/7   → košarica A
Račun A → GET /rest/basket/12  → košarica B
```

</div>

**IDOR / BOLA:** strežnik ne preveri pravice do zahtevanega objekta.

**Ukrep:** pri vsaki zahtevi preverimo lastništvo in dovoljene pravice.

Note:
Osrednji aplikacijski prikaz: Juice Shop View Basket. Pred dogodkom pripravi učna računa A in B z različnima izdelkoma in zapiši dejanska ID košaric. Številki 7 in 12 sta ponazoritev. Kot navaden uporabnik A odpri košarico, v ZAP ponovi zahtevo in spremeni samo ID na košarico B; žeton ohrani. Dokaz je izdelek iz B v odgovoru, ne skupni score board. Koda retrieveBasket v20.3.0 poišče objekt po ID brez preverjanja lastnika. IDOR pomeni insecure direct object reference, BOLA broken object level authorization. Skrivanje gumba ali težje ugibanje ID ne nadomestita preverjanja pravic. V košarici ničesar ne spreminjamo.

---

## Zastarele komponente: preverimo pogoje

<div class="example">
<div class="example-label">APACHE 2.4.49 · CVE-2021-41773</div>

```plaintext
Prizadeta različica       namig za preverjanje
Dovoljenja do datotek     pogoj za razkritje
Omogočeni CGI             dodaten pogoj za izvajanje kode
```

</div>

**V pripravi ACME je dostop zunaj spletnega imenika zavrnjen.**

<small>[Apache: varnostna obvestila](https://httpd.apache.org/security/vulnerabilities_24.html)</small>

Note:
Poveži prepoznavo storitve iz drugega sklopa s konfiguracijo aplikacijskega strežnika. Ne načrtuj uspešnega vdora prek www, ker privzeta konfiguracija preprečuje obravnavano pot izrabe. Nmap ali Nikto lahko opozorita na različico oziroma znake napačne nastavitve; nato preverimo pogoje. Negativen poskus ene poti ne pomeni, da je namestitev v celoti varna. Ukrep: podprta različica in pregled nastavitev. Za učenje uspešnega aplikacijskega preverjanja uporabimo preverjen primer Juice Shop.

---

## Katero orodje uporabimo?

| Vprašanje | Orodje v Kali |
| --- | --- |
| Kaj pošiljam in kaj lahko spremenim? | Firefox, ZAP ali Burp |
| Katere poti so objavljene? | curl, ffuf |
| Kaj razkriva nastavitev spletnega strežnika? | Nikto |
| Ali vnos vpliva na poizvedbo SQL? | ZAP, dodatno sqlmap |
| Ali lahko A bere podatke B? | Ročni preizkus z dvema učnima računoma |

**Orodje izberemo glede na vprašanje in preverimo njegov rezultat.**

Note:
Zaokroži aplikacijski sklop. ZAP je glavno orodje in je izrecno v pripravi Kali. Drugih orodij ne nameščamo med delavnico; preverimo jih pred dogodkom. Ne prikazujemo dveh prestreznih posrednikov zapored. Zaženi samo dogovorjene prikaze; podrobni ukazi in pomoč so pri posamezni vaji. Vaje so samostojne in v celoti potekajo v visitor.

---

## Od ugotovitve do ukrepa

**Kaj smo opazili? → Kaj to omogoča? → Kaj spremenimo?**

| Dokaz | Ukrep | Ponovno preverjanje |
| --- | --- | --- |
| Gost prebere interno datoteko | Uredimo dovoljenja | Gostujoče branje je zavrnjeno |
| Račun A vidi košarico B | Preverimo lastništvo | Zahteva A za B je zavrnjena |

[Praktične vaje](./vaje/) · naloga → namig → postopek

Note:
S tem zaključimo 35 minut predstavitev. Sledi 25 minut za digitalne sledi, 40 za omrežja, 40 za aplikacije in 10 za skupni pogovor; skupaj 150 minut. V vsakem krogu izberemo eno od treh osnovnih vaj glede na izkušnje, hitrejši imajo še dva dodatna izziva. Dostop in pravila so na strani z vajami. Za skupni pogovor po vajah zberemo tri najkoristnejše ukrepe za ACME ter pri vsaki ugotovitvi ločimo dokaz in omejitev.
