# Cybersec-201: Uvod v kibernetske operacije za radovedne

## Kratek povzetek

Delavnica je namenjena radovednim udeležencem brez poklicnega znanja informatike, tehnično spretnejšim uporabnikom in operativnim ekipam. Prvi sklop bo predstavil zbiranje javno dostopnih informacij in raziskovanje digitalnih sledi. Drugi sklop bo povezal osnove omrežij, segmentacijo in pregled izpostavljenih storitev. V tretjem sklopu bodo udeleženci v pripravljenem učnem okolju spoznali Kali Linux, dekodiranje podatkov in pregled spletnih zahtev ter ugotovitve povezali z obrambo. Delavnica traja 150 minut, od tega 36 minut predstavitve in 114 minut praktičnega dela.

## Načrt izvedbe

Vse tri predstavitve izvedemo pred praktičnim delom. Vaje so na ločeni strani `vaje/`; prosojnice ne vsebujejo nalog. Udeleženec v vsakem sklopu izbere eno od treh težavnosti, ob hitrem napredku pa lahko nadaljuje z drugo. Devet vaj ni obvezen zaporedni seznam.

| Del | Predstavitev | Praktično delo in pogovor | Skupaj |
| --- | --- | --- | --- |
| Uvod in orientacija v Kali | 5 minut | — | 5 minut |
| 1. Javno dostopne informacije in digitalne sledi | 8 minut | — | 8 minut |
| 2. Segmentacija omrežij in pregled ranljivosti | 12 minut | — | 12 minut |
| 3. Kali Linux in razmišljanje napadalca | 11 minut | — | 11 minut |
| Praktični krog 1: digitalne sledi | — | 30 minut | 30 minut |
| Praktični krog 2: omrežje in segmentacija | — | 35 minut | 35 minut |
| Praktični krog 3: zahteve in preverjanje | — | 35 minut | 35 minut |
| Dokončanje zapisov in rezerva | — | 4 minute | 4 minute |
| Skupni pogovor in zaključek | — | 10 minut | 10 minut |
| **Skupaj** | **36 minut** | **114 minut** | **150 minut** |

## Prosojnice po vrsti

Osnutek sledi slogu cybersec-101: kratke alineje, jasen poudarek in govorčeve opombe z razlago ter prikazi. Podrobnosti ostanejo v opombah in navodilih. Naslovi ustrezajo datoteki `slides.md`.

| Št. | Naslov | Namen |
| --- | --- | --- |
| 1 | Cybersec-201: Uvod v kibernetske operacije za radovedne | Predstavitev zgodbe ACME in cilja delavnice. |
| 2 | Eno podjetje, trije pogledi | Trije sklopi pred skupnim praktičnim blokom. |
| 3 | Naše učno okolje | Prijava v pripravljeni Kali, Firefox, terminal in dovoljene tarče. |
| 4 | 1. sklop: Javno dostopne informacije | OSINT, javne objave in metapodatki. |
| 5 | Iskalniki za infrastrukturo | Shodan, Censys, SecurityTrails in crt.sh; en stavek o vsakem. |
| 6 | Iskalniki za razkritja in zgodovino | DeHashed, IntelX, HIBP, VirusTotal in Wayback Machine; en stavek o vsakem. |
| 7 | Od sledi do ugotovitve | Viri, čas opažanja, povezovanje in omejitve sklepanja. |
| 8 | 2. sklop: Od naslova do storitve | IP, podomrežje, vrata in protokol na primeru ACME. |
| 9 | Ista vtičnica, drugačna dosegljivost | DMZ, LAN, IoT in razlika med tremi scenariji. |
| 10 | Nmap: kaj odgovarja? | Kratek prikaz pripravljenega izpisa odkrivanja in storitev. |
| 11 | Greenbone: od pregleda do poročila | Štiriminutna demonstracija končanega poročila in ene ugotovitve. |
| 12 | Različica → CVE → preverjanje | Razlika med zaznano različico in potrjeno ranljivostjo. |
| 13 | 3. sklop: Kako razmišlja preizkuševalec | Zaporedje preizkušanja, povezana razkritja in obrambni ukrepi. |
| 14 | Kaj potuje v spletni zahtevi? | Kratek prikaz lastne zahteve v Firefoxu na Juice Shop. |
| 15 | Kodiranje ni šifriranje | Base64, kodiranje URL in kratek prikaz CyberChef. |
| 16 | Piškotek predstavlja sejo | Namen in omejitve zastavic piškotkov. |
| 17 | Od ugotovitve do zaščite | Oblika zapisa ugotovitve in povezava z obrambo. |

## Praktični del po vseh treh sklopih

| Sklop | Lahka raven | Srednja raven | Zahtevna raven |
| --- | --- | --- | --- |
| 1 | Poišči pripravljen javni IP v Shodanu. | Razišči spletne sledi in izpostavljeno kopijo ACME. | Razišči DNS in razkritje notranjih imen. |
| 2 | Prepoznaj javne storitve ACME. | Primerjaj storitve v segmentiranem in ravnem omrežju. | Presodi zaznano različico in pogoje ranljivosti Apache. |
| 3 | Preglej lastno spletno zahtevo v Juice Shop. | Dekodiraj lastno prijavno glavo HTTP Basic. | Poveži razkritje poverilnic z minimalnim dokazom dostopa SSH. |

Vsaka vaja se začne samostojno; zahtevnejša vaja ne zahteva uspeha pri prejšnji. Končni zapis vsebuje opažanje, dokaz, omejitev, vpliv in predlagan ukrep. Navodila in namigi za udeležence so v `vaje/VAJE.md`, priprava ter pričakovani izidi za izvajalca pa v `EXERCISES.md`.

### Usklajevanje omrežnih scenarijev

Scenarij velja za vse udeležence hkrati. Prvi krog in javni pregled v drugem krogu potekata v `internet`. Drugi krog vključuje skupne prehode `internet → visitor → flat → visitor`. Izvajalec napove vsak prehod in počaka na zaključek primerjalnih meritev. Tretji krog ostane v `visitor`. Obstoječe povezave lahko preživijo preklop, zato primerjamo nove povezave in preglede odprtih vrat, ne le zaznanih gostiteljev.

## Priprava izvajalca

- Pred dogodkom preveri prijave prek Guacamole, Kali, Firefox in WireGuard za dodatni način dostopa. Namestitev VM ali zagon USB nista pogoj za udeležbo.
- Predhodna navodila `NAVODILO.md` še opisujejo obvezno lokalno namestitev; pred pošiljanjem jih uskladi z dostopom prek brskalnika.
- Namesti Greenbone, posodobi podatkovne vire in pripravi končan pregled izbrane tarče ACME. Pripravi izvoz poročila in posnetke kot rezervo. Med predstavitvijo ne čakaj na nov pregled.
- Izberi resničen javni IP z uporabnim Shodanovim zapisom, preveri dostop brez nepričakovanih omejitev in pripravi datiran posnetek rezultata. Naslovi 198.51.100.x so simulacija in niso tarče za Shodan.
- Javne iskalnike udeleženci odpirajo v lastnem brskalniku; dostop iz Kali omejuje proxy. Računi pri plačljivih ponudnikih niso pogoj za delavnico.
- Preveri orodja Nmap, dig, curl, SSH in lokalni CyberChef ter odzive ACME. Vnaprej preveri tudi prikaz zahtev in piškotkov trenutne različice Juice Shop.
- Za zahtevno vajo 3 pripravi samostojni namig o uporabniškem imenu; udeleženci ne potrebujejo predhodne SMB vaje. Potrdi delovanje starega SSH z uporabljenim odjemalcem.
- Apache 2.4.49 ima v trenutni pripravi omejen dostop zunaj DocumentRoot. Ne načrtuj zagotovljene uspešne izrabe ali prehoda do IoT prek njega.
- Vaje ne spreminjajo skupnih gesel, nastavitev aplikacij ali naprav. Greenbone preglede vodi izvajalec, da ne obremenimo skupnih tarč z več sočasnimi pregledi.
- Metapodatke ohranimo v razlagi; samostojna vaja s fotografijo ali PDF ni del tega osnutka in bi zahtevala preverjeno pripravljeno datoteko.
