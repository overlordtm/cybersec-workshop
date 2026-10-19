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

Predstavitev vsebuje 35 prosojnic: štiri uvodne, deset za prvi sklop, enajst za drugi, devet za tretji ter eno sklepno. Več prosojnic omogoča postopno razlago posameznih pojmov; čas predstavitve ostaja 36 minut s kratkimi prikazi. Devet avtorskih shem prikazuje poti skozi lab, povezovanje sledi, DNS, storitve, segmentacijo, HTTP, Base64 in verigo razkritij. Ponazoritve izpisov so izrecno označene; niso posnetki živega laboratorija. Pisava in velikosti naslovov sledijo cybersec-101.

| Št. | Naslov | Namen in prikaz |
| --- | --- | --- |
| 1 | Cybersec-201 | ACME je izmišljeno podjetje s pripravljeno infrastrukturo. |
| 2 | Eno podjetje, trije pogledi | Vse tri predstavitve pred praktičnim blokom. |
| 3 | Kali je že pripravljen | Pokaži prijavo na https://lab.digilab-g.rtfm.si/, Firefox in terminal. |
| 4 | Dogovor o preverjanju | Pojasni razliko med iskanjem že indeksiranih podatkov in aktivnim pregledom strežnika. |
| 5 | 1. sklop · Digitalne sledi | Za celoten prvi sklop osem minut. |
| 6 | Kaj izda spletna stran? | Na primeru ACME omeni javne kontakte in povezavo do trgovine. |
| 7 | Metapodatki: podatki o podatkih | Primer je ponazoritev, ne zajem dejanske datoteke. |
| 8 | Isto ime še ne pomeni iste osebe | Psevdonim se lahko pojavi na več družbenih omrežjih, ne da bi pripadal isti osebi. |
| 9 | Iskanje z manj šuma | Operatorji pomagajo omejiti rezultate. |
| 10 | Iskalniki za infrastrukturo | Vsako orodje predstavi z enim stavkom, brez treh dodatnih prikazov. |
| 11 | Kako beremo zapis v Shodanu? | Na pripravljenem dejanskem zapisu lahko pokažeš iste štiri elemente. |
| 12 | Razkritja in izpostavljeni računi | Orodja samo omenimo. |
| 13 | Certifikati, povezave in zgodovina | Omeni, da zgodovinski certifikat ne potrjuje trenutno delujoče storitve. |
| 14 | Znano ime ≠ dosegljiva naprava | Zaključi OSINT: ločimo odkrito ime, podatek o naslovu in preizkušeno storitev. |
| 15 | 2. sklop · Od omrežja do storitve | Dvanajst minut za drugi sklop, od tega štiri za demonstracijo Greenbone. |
| 16 | Naslov IP in podomrežje | /24 poenostavljeno predstavi kot skupino naslovov z istimi prvimi tremi deli. |
| 17 | Vrata so vstop do storitve | Shema je splošna ponazoritev, ne izpis dejanskih vrat www. |
| 18 | Zakaj DMZ, LAN in IoT? | VLAN loči omrežja, pravila požarnega zidu pa določajo prehode. |
| 19 | Segmentacijo določajo dovoljene poti | Ne gre le za blokiranje interneta. |
| 20 | Ista vtičnica, tri stanja | Scenarij velja globalno za vse. |
| 21 | Nmap: tri različna vprašanja | Odkrivanje gostiteljev samo zase ni dovolj. |
| 22 | Kako preberemo rezultat? | Izpis je ponazoritev vedenja, opisanega v README, ne sveža meritev. |
| 23 | Greenbone sestavi širši pregled | Za naslednji dve prosojnici in preklop v Greenbone skupaj štiri minute. |
| 24 | V poročilu odpremo eno ugotovitev | Pokaži dejansko poročilo, CVSS oziroma prikaz resnosti in Quality of Detection. |
| 25 | Različica → CVE → preverjanje | Apache v labu privzeto zavrača dostop zunaj DocumentRoot. |
| 26 | 3. sklop · Razmišljanje preizkuševalca | Enajst minut za tretji sklop. |
| 27 | Kaj se zgodi po kliku? | Zgornja puščica predstavlja zahtevo, spodnja odgovor. |
| 28 | Zahteva pod povečevalnim steklom | Razloži štiri dele na kratko. |
| 29 | Odgovor pove, kaj se je zgodilo | Status 200 sam zase ne dokazuje uspešne prijave; aplikacija lahko vrne sporočilo o napaki znotraj uspešnega odziva HTTP. |
| 30 | Firefox pokaže lastni promet | Odpri F12 → Network v Firefoxu na shop.acme.lab. |
| 31 | Kodiranje ni šifriranje | Prikazani učni niz se dekodira v ucenec:ucno. |
| 32 | CyberChef: sestavimo pretvorbo | Kratek prikaz lokalnega CyberChef na Kali. |
| 33 | HTTP Basic in zaščita prenosa | Poveži z učnim intranetom, ne razkrivaj vseh odgovorov vaj. |
| 34 | Piškotek lahko predstavlja sejo | Niso vsi piškotki prijavni. |
| 35 | Od dokaza do izboljšave | Zaključi predstavitev. |

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
