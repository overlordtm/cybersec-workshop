# OSINT, omrežna in aplikacijska varnost

<!-- .slide: class="title-slide" -->

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

![Prenosnik, telefon in odprt zvezek na mizi](../cybersec-101/images/devices-desk.jpg)

Andraž Vrhovec, Koofr d.o.o.

oktober 2026

Note:
*[pozdrav · čas je vključen v prvi sklop]*

Dober dan in dobrodošli na delavnici Cybersec-201. Danes bomo v treh sklopih pogledali digitalne sledi, omrežja in spletne aplikacije, nato pa boste vse skupaj preizkusili še sami.

Geslo današnjega dne je na prosojnici: poišči sled, preveri dokaz, predlagaj zaščito.

---

## Od sledi do ukrepa

**Pri vsaki ugotovitvi danes odgovorimo na isto zaporedje vprašanj.**

<div class="case-chain"><span>Kaj smo opazili?</span><b>→</b><span>Kakšen je dokaz in kdaj je nastal?</span><b>→</b><span>Česa še ne vemo?</span><b>→</b><span>Kaj to omogoča?</span><b>→</b><span>Kaj spremenimo?</span></div>

<div class="example">
<div class="example-label">PRIMER · IZMIŠLJENA DOMENA</div>

```plaintext
Opazili     ime test.podjetje.example v javnem certifikatu
Dokaz       zapis v crt.sh, certifikat izdan 2026-03-12
Ne vemo     ali strežnik še obstaja in kaj teče na njem
Omogoča     morda pozabljen testni sistem, dosegljiv od zunaj
Spremenimo  popis sistemov; umik ali zaprtje testnega okolja
```

</div>

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

Note:
*[≈1,5 min]*

Preden začnemo, en okvir, ki nas bo spremljal ves dan. Ko nekaj najdemo, se najprej vprašamo, kaj smo dejansko opazili. Nato, kakšen je dokaz in kdaj je nastal. Tretje vprašanje je najpomembnejše in ga najraje preskočimo: česa še ne vemo? Šele potem razmišljamo, kaj ugotovitev omogoča napadalcu, in na koncu, kaj bi spremenili.

Primer. V javnem dnevniku certifikatov opazimo ime test.podjetje.example. Dokaz je zapis v crt.sh z datumom izdaje. Ne vemo pa, ali strežnik še obstaja in kaj na njem teče, zato ne trdimo, da je odprt. Omogoča lahko marsikaj, če gre za pozabljen testni sistem, dosegljiv z interneta. Predlog je preprost: popis sistemov in umik ali zaprtje testnega okolja.

In že zdaj povem: pošteno omejen sklep, na primer »oglašena različica je med prizadetimi, izrabe nisem potrdil«, je povsem dober rezultat.

---

## 1. sklop · Digitalne sledi

**Kaj o nas in organizacijah povedo podatki, ki jih puščamo za sabo?**

![Spletna stran, dokument in repozitorij kot viri sledi](./images/traces.svg)

**OSINT** je zbiranje in povezovanje javno dostopnih informacij. Objave, dokumenti, fotografije in storitve puščajo povezljive sledi.

Note:
*[sklop skupaj ≈12 min, z naslovnico in okvirom]*

Začnimo s sledmi, ki jih puščamo za sabo. OSINT pomeni zbiranje in povezovanje javno dostopnih informacij: spletnih strani, dokumentov, objav in javnih evidenc. Sorodno področje je digitalna forenzika, ki preiskuje podatke na napravah, v datotekah in v zajemih prometa. Področji se dopolnjujeta, meja pa je jasna: ko pregledujemo tuj disk ali pomnilnik, to ni več OSINT.

Ogledali si bomo splošne vzorce in nekaj resničnih dogodkov.

---

## Kaj razkrijejo stran in dokumenti?

<div class="example">
<div class="example-label">PRIMER · METAPODATKI DOKUMENTA</div>

![Lastnosti dokumenta Word v sistemu Windows: avtor, zadnji urejevalec, program Microsoft Office Word ter datuma ustvarjanja in shranjevanja](./images/metadata.png)

</div>

Ime avtorja lahko povežemo z javnim seznamom zaposlenih.

**Ujemanje imena še ne dokaže avtorstva.**

Note:
*[PDF ACME je v vaji 1.4; tu ga ne odpiraj]*

Vsak dokument nosi tudi podatke o sebi, metapodatke: kdo naj bi ga napisal, s katerim programom in kdaj. Fotografije imajo pogosto še lokacijo GPS.

Na prosojnici so lastnosti dokumenta Word, kot jih pokaže Windows: avtor, kdo ga je zadnji shranil, program in datuma. Če na spletni strani podjetja najdemo osebo s tem imenom, se podatka ujemata. Ali je dokument res napisala ta oseba? Tega ne vemo. Ime lahko izvira iz predloge ali iz računalnika, ki ga je nekdo podedoval.

Napadalcu so takšni podatki vseeno koristni: razkrijejo imena zaposlenih, stare različice programov ali notranje poti do datotek.

---

## Philadelphia, 2020: majica poveže spletne sledi

<p class="case-tag">RESNIČEN PRIMER · POVEZOVANJE JAVNIH VIROV</p>

<div class="case-chain"><span>Majica na posnetku</span><b>→</b><span>Ocena nakupa na Etsyju</span><b>→</b><span>Povezani spletni profili</span></div>

FBI je spletne sledi dopolnil s primerjavo tetovaže in uradnimi evidencami.

**Nauk:** več drobnih objav skupaj lahko razkrije identiteto.

<small>Vir: [sodna izjava FBI, 2020, str. 9–11](https://storage.courtlistener.com/recap/gov.uscourts.paed.572055/gov.uscourts.paed.572055.1.1.pdf#page=9)</small>

Note:
*[≈1 min · ne navajaj zasebnih podatkov iz sodne vloge]*

Resničen primer: Philadelphia, maj 2020. Med preiskavo požiga policijskih vozil so preiskovalci na fotografijah opazili značilno majico. Po sodni izjavi FBI so našli enak model majice in oceno kupca na Etsyju. Isto uporabniško ime so nato povezali s profilom na Poshmarku in naprej z LinkedInom.

Pomembna je razlika med viri. Ocena in profili so javni, to je OSINT. FBI pa je sled dopolnil še s primerjavo tetovaže na javnem posnetku ter z uradnimi evidencami in podatki, pridobljenimi s sodnim pozivom, ki javnosti niso dostopni.

Sama majica ali uporabniško ime nista dokaz identitete. Sklep utemelji šele več neodvisnih virov skupaj.

*Če kdo vpraša za izid: opisan je v objavi ameriškega pravosodnega ministrstva iz julija 2022.*

---

## Iskanje omejimo na uporabne sledi

<div class="example">
<div class="example-label">PRIMER SINTAKSE</div>

```plaintext
site:podjetje.example filetype:pdf
site:podjetje.example inurl:backup
```

</div>

[Wayback Machine](https://web.archive.org/) pokaže stare objave.

[ctlogs.dev](https://ctlogs.dev/) in [crt.sh](https://crt.sh/) razkrijeta imena iz javnih certifikatov.

Tudi DNS je javni vir: zapisi razkrivajo imena, napačno nastavljen strežnik pa celotno območje.

Note:
*[poizvedb ne izvajaj v živo; acme.lab ni javno indeksiran]*

Kako takšne sledi iščemo? Iskalniki poznajo operatorje: `site` omeji iskanje na domeno, `filetype` na vrsto datoteke, `inurl` na del naslova. Tako hitro najdemo objavljene PDF-je ali pozabljene varnostne kopije.

Wayback Machine hrani stare različice strani, tudi tiste, ki jih je podjetje že umaknilo. ctlogs.dev in crt.sh iščeta po javnih dnevnikih certifikatov, kjer se pojavijo imena strežnikov, na primer test ali vpn.

Javni vir je tudi DNS. Običajni zapisi razkrivajo imena, napačno nastavljen strežnik pa celotno območje. Tehnično ozadje razložim v sklopu omrežij. Pri tem upoštevajte, da je poizvedba na strežnik že neposreden stik s tarčo, ne pasivno iskanje.

Še dve opozorili. Noben vir ni popoln ali nujno aktualen, zato vedno zapišemo, od kod je podatek in iz katerega dne. In robots.txt je samo prošnja iskalnikom, naj nečesa ne indeksirajo, ne pa zaklepanje.

---

## Shodan: kaj je bilo zaznano in kdaj?

![Shodan, iskanje country:SI: 259.423 zadetkov z razčlenitvijo po mestih, vratih, organizacijah in produktih ter zadetki s ponudnikom, lokacijo, odzivom storitve in časom opažanja](./images/shodan.png)

Preberemo storitev, odziv in čas zadnjega opažanja.

**Oznaka CVE je namig za preverjanje.**

Note:
*[posnetek: iskanje country:SI, 20. 10. 2026; poizvedb ne izvajaj v živo]*

Shodan in podobna storitev Censys neprestano pregledujeta internet in shranjujeta, kaj se odziva na posameznih naslovih. Ko gledamo zadetek, torej ne pregledujemo sami, ampak beremo njihov zapis.

Tukaj smo iskali vse, kar je Shodan zaznal v Sloveniji. Levo je povzetek: mesta, odprta vrata, organizacije in produkti. Desno so posamezni zadetki.

Preberimo enega. Organizacija in lokacija sta podatek ponudnika oziroma ocena iz baze naslovov, ne fizični naslov naprave. Pod tem je odziv storitve, na primer pozdrav poštnega strežnika Dovecot ali SSH z različico OpenSSH. Ključen je čas zgoraj desno: pove, kdaj je bilo zaznano, ne kakšno je stanje zdaj.

Če Shodan ob zadetku pokaže oznako CVE, je to namig za preverjanje, ne dokaz ranljivosti.

---

## Orodja za sledi, povezave in forenziko

| Kaj raziskujemo? | Primeri orodij |
| --- | --- |
| Spletne storitve in domene | [Shodan](https://www.shodan.io/), [Censys](https://censys.com/), [ctlogs.dev](https://ctlogs.dev/), [crt.sh](https://crt.sh/) |
| Javno objavljene naslove in imena | [theHarvester](https://github.com/laramies/theHarvester) |
| Povezave med podatki | [Maltego](https://www.maltego.com/), [SpiderFoot](https://github.com/smicallef/spiderfoot) |
| Rekurzivno odkrivanje domen in storitev | [BBOT](https://github.com/blacklanternsecurity/bbot) |
| Metapodatke in nosilce | [ExifTool](https://exiftool.org/), [Autopsy](https://www.autopsy.com/) |
| Zajeme delovnega pomnilnika | [Volatility](https://volatilityfoundation.org/) |

Note:
*[orientacija, orodij ne zaganjaj]*

Za vse to obstajajo orodja. Ta tabela je zemljevid, ne seznam za namestitev. Shodan, Censys, ctlogs.dev in crt.sh že poznamo. theHarvester zbira e-poštne naslove in imena iz javnih virov. Maltego in SpiderFoot povezujeta podatke iz več virov in jih prikažeta kot graf. BBOT rekurzivno odkriva domene in storitve; glede na izbrane module uporablja pasivne vire ali pa že aktivno poizveduje.

Spodnji vrstici sodita večinoma v forenziko. ExifTool bere metapodatke, Autopsy preiskuje diske, Volatility pa analizira zajeme pomnilnika. Pri ExifToolu odloča vir: metapodatki javno objavljenega dokumenta so OSINT, datoteke z zaseženega diska pa forenzika. Diski in pomnilnik niso javni viri, zato jih ne mešamo z OSINT.

Da ne bo pomote: ne trdim, da so bila ta orodja uporabljena v primerih, ki smo jih pravkar videli.

---

## 2. sklop · Omrežja

**Kaj sme doseči uporabnik, naprava ali zunanji izvajalec?**

| Del okolja | Primer storitve | Vprašanje o dostopu |
| --- | --- | --- |
| Javni strežniki | Spletna stran, pošta | Kaj mora biti dosegljivo od zunaj? |
| Notranji sistemi | Dokumenti, zbirke podatkov | Kdo jih potrebuje za delo? |
| Naprave in upravljanje | Kamera, klima, skrbniški vmesnik | Od kod je dostop upravičen? |


Note:
*[sklop skupaj ≈15 min, s prikazom segmentacije]*

Drugi sklop so omrežja. Osnovno vprašanje ni tehnično, ampak organizacijsko: kaj sme doseči uporabnik, naprava ali zunanji izvajalec?

Javna spletna stran in pošta morata biti dosegljivi od zunaj. Notranje dokumente in baze potrebujejo samo zaposleni, ki z njimi delajo. Kamere, klima in skrbniški vmesniki pa naj bodo dosegljivi le z mest, od koder jih res upravljamo.

Še trije pojmi. IP je naslov naprave, vrata so številka, na kateri posluša posamezna storitev, TCP in UDP pa sta različna protokola. 53/tcp in 53/udp sta torej dve različni meritvi.

Za predstavo: doma imate morda omrežje za goste, ločeno od službenega prenosnika in kamere. V podjetju je vprašanje enako, le resnejše, na primer pri izvajalcu, ki vzdržuje klimo, in pri plačilnem sistemu.

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

**Odprta vrata potrdijo dosegljivost. Ranljivost preverimo posebej.**

Note:
*[ukaz izvedejo v vajah 2.1 in 2.3; v živo ni obvezen]*

Najbolj znano orodje za pregled omrežja je Nmap. Na izpisu iščemo odgovore na tri vprašanja: ali naprava obstaja, katera vrata so dosegljiva in katera storitev na njih teče.

V ukazu `-Pn` preskoči preverjanje prisotnosti, `-sT` vzpostavi povezavo TCP, `-p` izbere vrata, `-sV` pa storitev vpraša, kaj je. Brez `-sV` Nmap ime storitve le ugiba po številki vrat.

Izpis pravi: na vratih 80 teče Apache 2.4.49. To potrdi, da je storitev dosegljiva. Ali je ranljiva, je drugo vprašanje. Odprta vrata sama po sebi tudi niso napaka.

---

## DNS: kdo lahko prenese celotno območje?

<div class="example">
<div class="example-label">PONAZORITEV · IZMIŠLJENA DOMENA IN DOKUMENTACIJSKI NASLOV</div>

```plaintext
dig @192.0.2.53 podjetje.example AXFR

files.podjetje.example.     A  10.10.20.10
intranet.podjetje.example.  A  10.10.20.11
cam01.podjetje.example.     A  10.10.30.10
```

</div>

**Napaka:** prenos območja je dovoljen vsakomur.

**Ukrep:** omejimo AXFR in ločimo notranje podatke DNS.

Note:
*[izpis je sintetičen, 192.0.2.53 ni tarča; preizkus je vaja 1.3]*

DNS je imenik interneta: imena prevaja v naslove. Strežniki si celotno območje izmenjujejo s prenosom AXFR, kar je med glavnim in rezervnim strežnikom povsem normalno.

Težava nastane, ko strežnik prenos dovoli komurkoli. Takrat napadalec z enim ukazom dobi seznam vseh imen, tudi notranjih: datotečni strežnik, intranet, kamero. To je zemljevid infrastrukture.

Ime v DNS pa še ne pomeni, da storitev lahko dosežemo; o tem odloča požarni zid. Popravek je dvojen: prenos omejimo na prave strežnike, notranja imena pa sploh ne sodijo v javni DNS.

---

## SMB: kdo lahko bere deljene datoteke?

| Opažanje | Kaj dokazuje? | Česa še ne vem? |
| --- | --- | --- |
| Vidim ime mape | Mapa obstaja | Ali jo lahko odprem |
| Brez prijave preberem datoteko | Gost lahko bere | Ali so podatki občutljivi |
| Prodaja bere mapo kadrovske | Pravice so širše od vloge | Kdo vse še ima dostop |

**Javna mapa sama ni napaka; težava je, kaj je v njej.**

**Ukrep:** pravice uskladimo z vlogo uporabnika in namenom podatkov.

Note:
*[ukazi so pri vaji 2.2; tu jih ne izvajaj]*

Deljene mape so v podjetjih eden najpogostejših virov preširokega dostopa. Na prosojnici so tri opažanja, ki dokazujejo različne stvari, in pri vsakem nekaj še manjka. Če vidim ime mape, vem le, da obstaja, ne pa, ali jo lahko odprem. Če datoteko preberem brez prijave, ima gost pravico branja, ne vem pa še, ali je vsebina občutljiva. Če račun iz prodaje bere mapo kadrovske službe, so pravice širše od vloge, odprto pa ostane, kdo vse ima še tak dostop.

Javna mapa ni nujno napaka, če so v njej res javni podatki. Težava nastane, ko vanjo nekdo odloži seznam naprav, izvoz baze ali kopijo pogodbe.

Dostop preverimo s smbclient, širši pregled pa naredi enum4linux-ng.

---

## Kako segmentacija spremeni dostop?

![Isti prenosnik iz vtičnice v sejni sobi: v segmentiranem omrežju kamera in klima nista dosegljivi, v omrežju brez omejitev pa postaneta dosegljivi](./images/segmentation-compare.svg)

**Segmentacija omeji dovoljene poti in s tem doseg napadenega sistema.**

Za razpravo: kam lahko pride nekdo, ki prevzame spletni strežnik v DMZ?

Note:
*[≈3 min · osrednji prikaz delavnice]*

Zdaj osrednji prikaz današnje delavnice. Segmentacija pomeni, da omrežje razdelimo po vlogah in s pravili določimo, kateri promet med deli je dovoljen. Ločen VLAN brez pravil še ni segmentacija.

Predstavljajte si, da ste obiskovalec v podjetju in prenosnik priključite v vtičnico v sejni sobi. Z istega mesta poženemo isti ukaz proti krmilniku klime. V segmentiranem omrežju so vrata filtrirana. Ko segmentacijo izklopimo, sta odprta spletni vmesnik in Modbus, protokol za krmiljenje naprav, ki ne pozna prijave.

Na krmilniku se ni spremenilo nič, spremenila so se le pravila poti. Segmentacija ne prepreči vdora, omeji pa, kam pride nekdo, ki je že notri.

In vprašanje za vas: kam lahko pride nekdo, ki prevzame spletni strežnik v DMZ? Odgovor pustimo za naslednjo prosojnico.

*Izvedba:* `./infra/lab.sh scenario flat`, z istega Kalija ponovi ukaz (nova povezava), nato takoj `./infra/lab.sh scenario visitor` in preveri status. Preklop velja za vse, zato ga izvedi samo med predstavitvijo, nikoli med vajami. Brez laboratorija uporabi izpis s prosojnice. `nmap -sn` lahko v visitor napravo IoT pokaže kot dosegljivo; šteje rezultat vrat.

---

## Target, 2013: od dobavitelja do občutljivih sistemov

<p class="case-tag">RESNIČEN PRIMER · ANALIZA AMERIŠKEGA SENATA IZ LETA 2014</p>

<div class="case-chain"><span>Zlorabljen dostop dobavitelja</span><b>→</b><span>Premik med notranjimi sistemi</span><b>→</b><span>Podatki plačilnih kartic</span></div>

Analiza opozarja na nezadostno ločitev občutljivih delov omrežja.

**Nauk:** dostop zunanjega izvajalca naj vodi le do storitev, ki jih potrebuje.

<small>Vir: [odbor ameriškega senata, 2014, povzetek](https://www.commerce.senate.gov/wp-content/uploads/media/doc/2014%200325%20Target%20Kill%20Chain%20Analysis.pdf#page=2)</small>

Note:
*[≈1 min]*

Target, ameriška trgovska veriga, leto 2013. Napadalci so najprej zlorabili dostop zunanjega dobavitelja, od tam prišli do notranjih sistemov in nazadnje do podatkov plačilnih kartic. Analiza odbora ameriškega senata iz leta 2014 opozarja, da občutljivi deli omrežja niso bili dovolj ločeni.

Pogosto slišimo poenostavitev, da so vdrli »prek klime«. V sam krmilnik klime niso vdrli; zlorabili so dostop izvajalca, ki je segal dlje, kot je bilo treba. Poročilo je tudi zgodnja analiza, ne končna forenzika. Segmentacija bi lahko omejila premikanje, sama pa vdora ne bi zagotovo preprečila. Potrebni so še omejeni računi, spremljanje in odziv na opozorila.

Zdaj pa odgovor na vprašanje od prej. Če pravila dovoljujejo pot iz DMZ v IoT, kdor prevzame spletni strežnik, doseže kamero, tiskalnik in klimo, čeprav jih obiskovalec v sejni sobi ne vidi. Ena preširoka pot zadošča.

---

## WannaCry, 2017: ko izpad IT prekine zdravstveno oskrbo

<p class="case-tag">RESNIČEN PRIMER · NHS V ANGLIJI</p>

<div class="case-chain"><span>Neposodobljeni sistemi Windows</span><b>→</b><span>Samodejno širjenje po omrežju</span><b>→</b><span>Odpovedane operacije in preusmerjeni pacienti</span></div>

NAO je pri okuženih organizacijah izpostavil neposodobljene ali nepodprte sisteme Windows.

**Nauk:** popravki zmanjšajo možnost okužbe; omejene omrežne poti omejijo širjenje in posledice.

<small>Vir: [National Audit Office, poročilo o WannaCry in NHS](https://www.nao.org.uk/reports/investigation-wannacry-cyber%20attack-and-the-nhs/)</small>

Note:
*[≈1 min]*

WannaCry, maj 2017. Izsiljevalski program se je samodejno širil med računalniki Windows, ki niso imeli nameščenega popravka. V angleškem zdravstvenem sistemu NHS so morali odpovedati preglede in operacije ter preusmerjati paciente.

Britanski državni revizor, National Audit Office, je pri prizadetih organizacijah izpostavil neposodobljene in nepodprte sisteme. Motnje pa niso bile omejene na okužene naprave: nekateri sistemi so bili od okuženih odvisni, druge so preventivno izklopili.

Nauk za nas: popravki zmanjšajo možnost okužbe, omejene omrežne poti pa omejijo širjenje. Segmentacijo dodajam kot splošni nauk; poročilo je ne navaja kot vzrok. Popravkov in načrta obnovitve ne nadomesti.

---

## IoT: dostop do naprav in njihovih podatkov

| Naprava | Storitev | Kaj preverimo? |
| --- | --- | --- |
| Kamera | HTTP, RTSP 554/tcp | Izpostavljenost vmesnika |
| Tiskalnik | SNMP 161/udp | Podatke s skupnostjo `public` |
| Klima | Modbus 502/tcp | Dosegljivost krmilnika |

<div class="example">
<div class="example-label">VZOREC UKAZA · SNMP</div>

```plaintext
snmpwalk -v2c -c public [IP-tiskalnika] 1.3.6.1.2.1.1
```

</div>

**Ukrep:** dostop omejimo na potrebne upravljavske poti.

Note:
*[uporabi izsek s prosojnice, povezav ne vzpostavljaj]*

Pri napravah IoT je težava pogosto v tem, da jih nihče ne šteje za računalnike. Kamera ima spletni vmesnik in video tok RTSP. Tiskalnik prek protokola SNMP s privzeto skupnostjo public izda lokacijo in kontakt. Krmilnik klime uporablja Modbus, ki ne preverja, kdo pošilja ukaze.

Na prosojnici je primer ukaza, ki iz tiskalnika prebere osnovne podatke. Dosegljiva vrata pa še ne pomenijo, da lahko spremenimo nastavitve.

Ukrep je enak kot pri segmentaciji: dostop do naprav omejimo na mesta, od koder jih upravljamo.

*Izvedba:* ukaz ima nadomestni naslov. SNMP v živo (tiskalnik 172.20.30.11) izvedi samo skupaj s prikazom segmentacije v flat, nato vrni visitor. Če kdo vpraša za Wireshark: vidi le promet, ki doseže naš vmesnik, ne vsega prometa v preklopljenem omrežju.

---

## Zastarela storitev: kaj pove različica?

![Zaznana različica, pogoji in potrditev vedenja so ločeni koraki](./images/verification.svg)

**Nmap prepozna storitev. Naslednji preizkus preveri konkreten pogoj.**

Note:
*[≈1 min]*

Recimo, da Nmap pokaže staro različico. Kaj to pomeni? Najprej le to, da jo je vredno preveriti in načrtovati nadgradnjo.

Na sliki so trije ločeni koraki. Različica pove, kaj storitev oglašuje, in oglas lahko zavaja: distribucije pogosto vgradijo varnostne popravke, ne da bi spremenile številko različice. Pogoje ranljivosti preberemo v obvestilu proizvajalca. Šele preizkus, na primer izbrana skripta Nmap, pokaže, kaj storitev res omogoča.

Metasploit pomaga pri nadzorovanem preverjanju znanih ranljivosti, a sam obstoj modula ni dokaz.

---

## Pregledovalniki ranljivosti: kako beremo ugotovitev

| V poročilu | Vprašanje za preizkuševalca |
| --- | --- |
| Tarča, storitev in dokaz | Kaj je pregledovalnik dejansko izmeril? |
| Resnost (CVSS) | Kakšne so lahko posledice? |
| Zanesljivost zaznave | Ali temelji le na različici ali na preizkusu? |
| Predlog odprave | Kaj spremenimo in kako preverimo popravek? |

**Ugotovitev pregledovalnika je hipoteza, dokler je ne potrdi odziv storitve.**

Note:
*[splošen pregled, orodij ne zaganjaj]*

Pregledovalniki ranljivosti, kot sta OpenVAS iz paketa Greenbone in Nessus, za veliko naprav hkrati naredijo to, kar smo pravkar opisali: prepoznajo storitve in jih primerjajo z bazo znanih ranljivosti. Poročila so dolga, zato se naučimo brati eno ugotovitev.

Pri vsaki pogledamo štiri stvari. Najprej tarčo, storitev in dokaz, torej izpis, iz katerega je orodje sklepalo. Nato resnost, običajno po lestvici CVSS, ki pove možne posledice, ne pa verjetnosti napada; za to nekatera orodja dodajo oceno, kot je EPSS. Tretja je zanesljivost zaznave: OpenVAS jo izrazi kot Quality of Detection, pri Nessusu pa iz opisa vtičnika razberemo, ali je preveril le različico ali dejansko vedenje. In na koncu predlog odprave, skupaj s tem, kako bomo popravek preverili.

Še dve omejitvi. Pregled brez prijave vidi le, kar storitev pokaže navzven; pregled s prijavo v sistem pozna nameščene pakete in je zato natančnejši. In pregledovalnik ne najde ničesar na napravi, ki je ni v obsegu pregleda. Zato je inventar temelj vsega.

---

## Omrežna orodja: pregled, preizkus in zaznava

| Namen | Primeri orodij |
| --- | --- |
| Odkrijemo storitve in izpostavljenost | [Nmap](https://nmap.org/), [Masscan](https://github.com/robertdavidgraham/masscan) |
| Preverimo deljene mape | [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html), [enum4linux-ng](https://github.com/cddmp/enum4linux-ng) |
| Razumemo omrežni promet | [Wireshark](https://www.wireshark.org/docs/), [tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html) |
| Poiščemo znane težave | [Greenbone](https://greenbone.github.io/docs/latest/), [Nessus](https://www.tenable.com/products/nessus) |
| Preverimo izbrano znano ranljivost | [Metasploit](https://www.rapid7.com/products/metasploit/) |
| Spremljamo dogajanje in opozorila | [Zeek](https://zeek.org/), [Suricata](https://suricata.io/), [Wazuh](https://wazuh.com/platform/overview/) |

**Enkraten pregled in stalno spremljanje odgovarjata na različni vprašanji.**

Note:
*[pregled področja, orodij ne zaganjaj]*

Še pogled na širše področje. Nmap in Masscan odkrivata storitve; Masscan je zelo hiter, a storitve prepozna manj natančno. Wireshark in tcpdump zajemata promet, ki ga vidimo. Greenbone in Nessus iščeta znane težave, Metasploit pa preverja izbrane znane ranljivosti.

Spodnja vrstica je druga stran, obramba. Zeek iz prometa izdela zapise o dogodkih, Suricata zaznava sumljiv promet in opozarja, Wazuh pa zbira dnevnike sistemov, spremlja spremembe datotek in povezuje dogodke.

Pregled, izraba in zaznava niso isto. Enkraten pregled pove, kakšno je stanje danes, stalno spremljanje pa, kdaj se nekaj spremeni. Niso vsa ta orodja del vaj.

---

## 3. sklop · Aplikacije

**Kaj se zgodi z našim vnosom?**

![Brskalnik pošlje zahtevo HTTP strežniku, ta jo obdela in vrne odgovor s statusom in vsebino](./images/http.svg)

Primer: `GET /api/izdelki?q=jabolko` → strežnik vrne `200 OK` z JSON. Metoda in pot → podatki → obdelava → odgovor.

Note:
*[sklop skupaj ≈14 min, s sklepno prosojnico]*

Tretji sklop so spletne aplikacije. Vse se vrti okoli enega vprašanja: kaj se zgodi z našim vnosom?

Ko v trgovini iščete jabolko, brskalnik pošlje zahtevo HTTP z metodo, potjo in parametri, tukaj q=jabolko. Strežnik podatke obdela in vrne odgovor s statusom in vsebino. Vnos je lahko v naslovu, v telesu zahteve ali v glavah.

Status beremo skupaj z vsebino; 200 OK še ne pomeni, da je vse v redu. HTTPS zaščiti prenos, ne pa logike aplikacije ali preverjanja pravic.

---

## ZAP: zahtevo spremenimo in ponovimo

![Brskalnik pošlje zahtevo prek lokalnega ZAP do aplikacije](./images/zap.svg)

**Ohranimo izhodišče, spremenimo en podatek in primerjamo odgovor.**

Note:
*[če prikazuješ: ena spremenjena zahteva, npr. ID košarice, največ 2 min; posrednik pripravi vnaprej]*

Da svoje zahteve vidimo in spremenimo, uporabimo prestrezni posrednik, kot sta ZAP ali Burp Suite. Brskalnik pošilja zahteve prek njega, mi pa jih lahko pregledamo, spremenimo in ponovno pošljemo. Za prvi pogled zadoščajo že razvijalska orodja v Firefoxu.

Pravilo je preprosto: ohranimo izhodišče, spremenimo en sam podatek in primerjamo odgovor. Če spremenimo več stvari hkrati, ne vemo, kaj je vplivalo na rezultat.

Ločimo tri dejavnosti: opazovanje prometa, ročno preverjanje in samodejni aktivni pregled, ki pošlje veliko zahtev.

---

## Razkrite datoteke: kopija na javni strani

<div class="example">
<div class="example-label">IZMIŠLJEN PRIMER OBJAVLJENE KOPIJE</div>

```plaintext
GET /backup/config.php.bak HTTP/1.1
Host: podjetje.example

# Razkrito: notranje ime in prijavni podatki.
```

</div>

**Dokaz:** vsebina datoteke je dosegljiva brez prijave.

**Ukrep:** odstranimo kopijo in zamenjamo razkrite skrivnosti.

Note:
*[ne prikazuj resničnih razkritih gesel; primer ACME je v vajah 1.2 in 3.3]*

Ena najpogostejših napak je zelo preprosta: na javnem strežniku ostane kopija, ki tja ne sodi. To so varnostne kopije, izvozi baz, dnevniki, datoteke z nastavitvami ali kar cel repozitorij .git.

Primer na prosojnici je izmišljen: datoteke config.php.bak strežnik ne izvede, ampak jo vrne kot besedilo, skupaj z notranjim imenom in geslom. Dokaz je, da vsebino dobimo brez prijave. Če datoteka ni povezana s strani ali je navedena v robots.txt, to še ne pomeni, da je zaščitena.

Ukrep ima dva dela: kopijo odstranimo, razkrito geslo pa zamenjamo, saj ga je morda kdo že prebral. Konkretno pot preverimo s curl; ffuf in Gobuster pa iščeta poti po seznamu.

---

## Prijava: geslo in zaščita prenosa

| Primer | Težava | Ukrep |
| --- | --- | --- |
| Upravljavski vmesnik | Privzeti ali ponovno uporabljeni podatki | Ločene, ustrezno zaščitene prijave |
| Notranji portal | HTTP Basic brez TLS | HTTPS in omejen dostop |

![Base64 pretvori ucenec:ucno v dWNlbmVjOnVjbm8= in nazaj brez skrivnega ključa](./images/encoding.svg)

**Base64 je kodiranje, ne šifriranje.** Glavo `Authorization: Basic …` dekodira vsak brez ključa; prenos zaščiti šele HTTPS.

Note:
*[primera ACME sta NAS in intranet (vaja 3.2); tu ju ne odpiraj]*

Pri prijavah ločimo tri težave. Prva je privzeto geslo, ki ga nihče ni zamenjal. Druga je isto geslo na več mestih. Tretja je prenos brez šifriranja.

Poglejmo tretjo. Pri HTTP Basic brskalnik pošlje uporabniško ime in geslo v glavi, zapisano v Base64. To ni šifriranje, ampak le drugačen zapis: v CyberChef ali v terminalu ga dekodiramo brez ključa. Brez HTTPS ga torej prebere vsak, ki vidi promet. Niz na prosojnici je izmišljen.

Še dve pojasnili. Vaš brskalnik podatke vidi tudi pri HTTPS, saj jih šifrira šele ob pošiljanju. MFA zmanjša tveganje prevzema računa, ne nadomesti pa preverjanja, do česa ima prijavljeni uporabnik pravico.

---

## Eno razkritje, več vrat

![Javna kopija razkrije geslo, ponovljeno geslo odpre drugo storitev; ukrepi prekinejo vsak člen](./images/chain.svg)

**Geslo iz ene napake odpre drugo storitev, če ga ponovno uporabimo.**

Note:
*[≈1 min · ne razkrivaj vrednosti gesla]*

Posamezne napake so redko usodne same po sebi. Nevarne postanejo, ko se povežejo. Zgornja vrsta je veriga: na javni strani je kopija z geslom, isto geslo uporablja še druga storitev, in napadalec dobi dostop s pravicami tega računa.

Spodnja vrsta pokaže, da lahko vsak člen prekinemo. Kopijo odstranimo in geslo zamenjamo. Za vsako storitev uporabljamo ločeno geslo ali ključ. Pravice računov omejimo in prijave beležimo.

Povezava med dvema ugotovitvama je pogosto pomembnejša od vsake posebej.

---

## SQL injection: vnos spremeni poizvedbo

<div class="example">
<div class="example-label">POENOSTAVLJENA POIZVEDBA · UČNI PRIMER</div>

```plaintext
SELECT ... WHERE uporabnik = '[vnos]'
             AND geslo = ...

Vnos: ana'--

SELECT ... WHERE uporabnik = 'ana'-- ...
```

</div>

**Napaka:** aplikacija podatke združi z navodili SQL.

**Ukrep:** parametrizirane poizvedbe ločijo podatke od kode.

Note:
*[postopek na Juice Shop je v vaji 3.4]*

SQL injection je klasična napaka. Aplikacija sestavi poizvedbo tako, da vnos uporabnika preprosto prilepi med navodila SQL.

Poglejmo poenostavljen primer. Če v polje za uporabnika vpišemo »ana«, narekovaj in dva vezaja, narekovaj zaključi vrednost, vezaja pa preostanek poizvedbe spremenita v komentar. Preverjanje gesla izgine in prijava uspe brez gesla.

Rešitev ni filtriranje posebnih znakov, ampak parametrizirane poizvedbe, ki podatke ločijo od kode. Za ročno preverjanje uporabimo ZAP ali Burp, sqlmap pa avtomatizira preverjanje nekaterih vrst te napake.

*Če kdo vpraša: v MySQL mora za dvema vezajema stati presledek; Juice Shop uporablja SQLite, kjer ni potreben.*

---

## XSS: vnos postane skripta v brskalniku

<div class="example">
<div class="example-label">POENOSTAVLJEN PRIMER KODE V BRSKALNIKU</div>

```javascript
// Nevarno, če vnos ni zaupanja vreden:
rezultat.innerHTML = vnos;

// Za prikaz navadnega besedila:
rezultat.textContent = vnos;
```

</div>

**Napaka:** brskalnik vnos obravnava kot kodo.

**Ukrep:** varen DOM in kontekstu primerna obdelava izhoda.

Note:
*[neobvezen prikaz samo na lokalnem učnem primeru, nikoli shranjenega XSS na skupni tarči]*

XSS, cross-site scripting, je sorodna napaka, le da se ne zgodi v bazi, ampak v brskalniku. Aplikacija vstavi v stran vnos, ki mu ne bi smela zaupati, brskalnik pa ga izvede kot kodo.

V primeru je razlika ena sama beseda. innerHTML vnos razume kot HTML, textContent pa kot navadno besedilo. Za prikaz besedila je textContent prava izbira; če moramo dovoliti HTML, ga je treba sanitizirati.

Posledice so odvisne od konteksta: skripta lahko izvaja dejanja v imenu uporabnika ali bere podatke, ki jih ta vidi. Glavni ukrep je kontekstno kodiranje izhoda; politika CSP je dodatna obramba, ki omeji škodo, napake pa ne odpravi. DOM XSS lahko nastane v celoti v brskalniku, brez sledi v strežniškem odgovoru.

---

## Prijava še ne pomeni pravice do vseh podatkov

<div class="example">
<div class="example-label">PONAZORITEV ID-JEV · VES ČAS ŽETON RAČUNA A</div>

```plaintext
Račun A → GET /api/kosarice/7   → košarica A
Račun A → GET /api/kosarice/12  → košarica B
```

</div>

**IDOR / BOLA:** strežnik ne preveri pravice do zahtevanega objekta.

**Ukrep:** pri vsaki zahtevi preverimo lastništvo in dovoljene pravice.

Note:
*[neobvezen kratek prikaz na Juice Shop: /rest/basket/:id, pripravljena računa, žeton A ostane; vaja 3.5]*

Zadnja napaka v tem sklopu je v sodobnih API-jih morda najpogostejša. Uporabnik A je pravilno prijavljen in odpre svojo košarico številka 7. Nato v zahtevi številko spremeni v 12 in dobi košarico uporabnika B.

Strežnik je preveril, kdo je uporabnik, ni pa preveril, ali sme videti ta objekt. Temu rečemo IDOR, insecure direct object reference, ali BOLA, broken object level authorization.

Isto se lahko zgodi pri računih, naročilih, zdravstvenih dokumentih ali datotekah. Težje uganljiv ID ni rešitev; strežnik mora pri vsaki zahtevi preveriti lastništvo.

---

## Equifax, 2017: znana ranljivost, veliko razkritje

<p class="case-tag">RESNIČEN PRIMER · OČITKI FTC OB PORAVNAVI</p>

<div class="case-chain"><span>Nenameščen popravek</span><b>→</b><span>Vstop in dostop do drugih sistemov</span><b>→</b><span>Podatki približno 147 milijonov ljudi</span></div>

FTC je očital tudi neustrezno segmentacijo in prijavne podatke v nezaščiteni datoteki.

**Nauk:** upravljanje komponent, skrivnosti in notranjih dostopov deluje skupaj.

<small>Vir: [FTC, objava poravnave iz leta 2019 o vdoru 2017](https://www.ftc.gov/news-events/news/press-releases/2019/07/equifax-pay-575-million-part-settlement-ftc-cfpb-states-related-2017-data-breach)</small>

Note:
*[≈1 min · navedbe so očitki FTC, ne sodna ugotovitev]*

Equifax, ena od treh velikih ameriških kreditnih agencij, leto 2017. Podjetje ni pravočasno namestilo popravka za znano ranljivost v spletnem ogrodju Apache Struts. Napadalci so vstopili prek nje, dostopali do drugih sistemov, razkriti pa so bili podatki približno 147 milijonov ljudi.

Ameriški regulator FTC je ob poravnavi leta 2019 podjetju očital še neustrezno ločitev baz in prijavne podatke v nezaščiteni datoteki. To so očitki regulatorja, ne naša forenzična analiza.

Ta vzorec smo danes videli že večkrat: aplikacijska vstopna točka, razkrite skrivnosti in preširoki notranji dostopi. Ključna sta inventar komponent in preverjanje, ali je bil popravek res nameščen.

---

## Zastarele komponente: preverimo pogoje

<div class="example">
<div class="example-label">APACHE 2.4.49 · CVE-2021-41773</div>

```plaintext
Prizadeta različica         namig za preverjanje
Dovoljen dostop do datotek  pogoj za razkritje
Omogočen CGI                dodaten pogoj za izvajanje kode
```

</div>

**Različica + nastavitev + dejanski odziv → utemeljen sklep.**

<small>[Apache: varnostna obvestila](https://httpd.apache.org/security/vulnerabilities_24.html)</small>

Note:
*[zakaj Apache ACME ni izrabljiv, razloži šele pri vaji 2.3]*

Pri Equifaxu je bila znana ranljivost dejanska vstopna točka. Oznaka CVE sama pa še ne pove, ali je konkreten strežnik izrabljiv.

Primer je Apache 2.4.49 z ranljivostjo CVE-2021-41773. Prizadeta različica je šele namig. Za branje datotek zunaj spletnega imenika mora to dovoljevati nastavitev dovoljenj, za izvajanje ukazov pa mora biti vklopljen še CGI. Sklep zato temelji na treh stvareh: različici, nastavitvi in dejanskem odzivu.

Negativen preizkus ene poti pa ne pomeni, da je strežnik varen. Ukrep ostaja enak: podprta različica in preverjena konfiguracija.

---

## Varnost preverjamo tudi med razvojem programske opreme

| Kaj pregledamo? | Primeri orodij | Kaj iščemo? |
| --- | --- | --- |
| Izvorno kodo | [Semgrep](https://semgrep.dev/docs/) | Nevarne vzorce v kodi |
| Knjižnice | [Dependency-Check](https://owasp.org/www-project-dependency-check/), [Trivy](https://trivy.dev/) | Znane ranljivosti komponent |
| Slike zabojnikov in nastavitve | [Trivy](https://trivy.dev/) | Ranljive pakete, skrivnosti, napačne nastavitve |
| Različice knjižnic | [Renovate](https://github.com/renovatebot/renovate) | Nove različice, s samodejnimi predlogi posodobitev |

**Pregled kode in komponent dopolni preizkus delujoče aplikacije.**

Note:
*[orodij ne nameščamo za vaje]*

Do zdaj smo aplikacije preizkušali od zunaj. Veliko napak pa lahko ujamemo že prej, med razvojem.

Semgrep v izvorni kodi išče nevarne vzorce, na primer sestavljanje poizvedbe SQL iz vnosa. OWASP Dependency-Check in Trivy preverjata, ali uporabljene knjižnice vsebujejo znane ranljivosti; Trivy pregleda tudi slike zabojnikov, skrivnosti in nastavitve. Najdena skrivnost ne pomeni nujno, da ključ še velja.

Renovate poskrbi za drugo polovico, redno vzdrževanje: samodejno predlaga posodobitve knjižnic, mi pa jih preverimo s testi in pregledom sprememb.

Vsa ta orodja so koristna le, če nekdo njihove ugotovitve tudi obravnava.

---

## Katero orodje uporabimo?

| Vprašanje | Primeri orodij |
| --- | --- |
| Kaj pošiljam in kaj lahko spremenim? | [Firefox](https://firefox-source-docs.mozilla.org/devtools-user/), [ZAP](https://www.zaproxy.org/docs/) ali [Burp](https://portswigger.net/burp/documentation) |
| Katere poti so objavljene? | [curl](https://curl.se/docs/), [ffuf](https://github.com/ffuf/ffuf) |
| Kaj razkriva nastavitev spletnega strežnika? | [Nikto](https://github.com/sullo/nikto) |
| Ali se odziv ujema z znanim vzorcem napake? | [Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/overview) in izbrane predloge |
| Ali vnos vpliva na poizvedbo SQL? | [ZAP](https://www.zaproxy.org/docs/), dodatno [sqlmap](https://sqlmap.org/) |
| Ali lahko A bere podatke B? | Ročni preizkus z dvema učnima računoma |

**Orodje izberemo glede na vprašanje in preverimo njegov rezultat.**

Note:
*[pregled, ne navodilo za zagon]*

Kako izbrati orodje? Začnemo pri vprašanju, ne pri orodju. Če želim videti, kaj pošiljam, odprem razvijalska orodja ali ZAP. Če iščem objavljene poti, uporabim curl ali ffuf. Nikto preveri nastavitve spletnega strežnika, Nuclei pa preizkuša znane vzorce napak po predlogah.

SQL injection najprej preverimo ročno v ZAP, po potrebi še s sqlmap. Pri vprašanju, ali lahko A bere podatke B, pa orodja skoraj ne pomagajo. Potrebujemo dva učna računa in ročni preizkus, ker mora nekdo razumeti, čigav je kateri podatek.

Rezultat vsakega orodja preverimo, preden ga zapišemo kot ugotovitev.

---

## ACME: izmišljeno podjetje za vaje

![Udeleženec prek požarnega zidu do treh segmentov ACME: DMZ, LAN in IoT](./images/acme.svg)

<small>Javni naslovi 198.51.100.11–15 · DMZ 172.20.10.0/24 · LAN 172.20.20.0/24 · IoT 172.20.30.0/24</small>

**Vaš položaj:** prenosnik v vtičnici sejne sobe. Dosežete javne naslove, LAN in storitve DMZ, IoT pa ne.

Note:
*[≈2 min]*

Zdaj pa k vajam. ACME je izmišljeno podjetje, ki obstaja samo v našem laboratoriju. Javni naslovi 198.51.100 so dokumentacijski in delujejo samo tam, imena pod acme.lab pa razreši laboratorijski DNS.

Omrežje ima tri dele. V DMZ so javne storitve: spletna stran, trgovina, pošta, DNS in strežnik za oddaljeni dostop. V pisarniškem omrežju LAN so datotečni strežnik, intranet, NAS, delovna postaja in Metasploitable 2, star, nevzdrževan strežnik. V IoT so kamera, tiskalnik in klima.

Ves čas ste v vlogi obiskovalca, ki je prenosnik priključil v sejni sobi. Dosežete javne naslove, pisarniško omrežje in storitve v DMZ, naprav IoT pa ne. Zakaj, smo videli pri segmentaciji.

Notranjih naslovov ACME ne iščite na javnem internetu.

---

## Pravila in potek vaj

<div class="cards">
<div class="card">

### Dostop

S svojo kodo odpri [prevzem dostopa](./vaje/dostop/). Kali v brskalniku ali svoj Kali prek WireGuarda.

</div>
<div class="card">

### Kaj smemo

Samo navedene tarče ACME. Ničesar ne spreminjamo. Javne vire samo beremo.

</div>
<div class="card">

### Potek

Trije krogi: 25, 40 in 40 minut, nato 10 minut skupnega pogovora.

</div>
</div>

[Praktične vaje](./vaje/)

Note:
*[≈2 min, nato začni prvi krog]*

Še pravila in potek. Dostop dobite s svojo osebno kodo na strani za prevzem. Večina bo uporabljala Kali v brskalniku; kdor ima svoj Kali, se lahko poveže prek WireGuarda.

Aktivno preverjamo samo navedene tarče ACME in ničesar ne spreminjamo, ne datotek, ne gesel, ne košaric, saj si tarče delimo. Shodan in ctlogs.dev odpirate v svojem običajnem brskalniku in samo berete; najdenih javnih naslovov ne pregledujte z Nmap. In resno: nepooblaščen vstop v tuj informacijski sistem je po kazenskem zakoniku (KZ-1, 221. člen) kaznivo dejanje. Tukaj smemo, ker je laboratorij naš.

Potek: trije krogi, 25 minut za sledi in po 40 minut za omrežja in aplikacije. V vsakem izberete eno od prvih treh vaj glede na izkušnje, nato nadaljujete z drugo vajo ali dodatnim izzivom. Če se zataknete, odprite namig in nato postopek. Ugotovitve zapišite po okviru z začetka. Na koncu imamo deset minut za skupni pogovor.

*Izvedba:* pokaži ali napiši IP za vajo 1.1, domeno za vajo 1.5 ter učna računa in ID košaric za vajo 3.5; gesel ne zapisuj na prosojnice. Omrežje ostane visitor do konca. Če kdo vpraša za `curl --noproxy '*'`: Kali tarče ACME že izvzame iz posrednika, možnost je varovalka za lastni Kali.
