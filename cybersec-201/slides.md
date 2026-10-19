# OSINT, omrežna in aplikacijska varnost

<!-- .slide: class="title-slide" -->

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

![Prenosnik, telefon in odprt zvezek na mizi](../cybersec-101/images/devices-desk.jpg)

Andraž Vrhovec, Koofr d.o.o.

oktober 2026

Note:
Kratka naslovnica po vzoru Cybersec-101. Pozdravi udeležence in preidi na način dela. Dostop in pravila vaj so na koncu predstavitve; čas naslovnice je vključen v prvi sklop.

---

## Od sledi do ukrepa

**Pri vsaki ugotovitvi danes odgovorimo na isto zaporedje vprašanj.**

<div class="case-chain"><span>Kaj sem opazil?</span><b>→</b><span>Kakšen je dokaz in kdaj je nastal?</span><b>→</b><span>Česa še ne vem?</span><b>→</b><span>Kaj to omogoča?</span><b>→</b><span>Kaj spremenimo?</span></div>

Enaka polja izpolnite v zapisu pri vajah.

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

Note:
Okvir za celo delavnico, približno minuto. Polja ustrezajo obrazcu »Moj zapis« na strani z vajami: opažanje, dokaz z virom in časom, kar ostaja nepotrjeno, možen vpliv in predlagan ukrep. Poudari tretji korak: omejen, pošteno zapisan sklep je dober rezultat, tudi če preverjanje ne uspe. Na ta okvir se vrnemo pri sklepni prosojnici.

---

## 1. sklop · Digitalne sledi

**Kaj o nas in organizacijah povedo podatki, ki jih puščamo za sabo?**

![Spletna stran, dokument in repozitorij kot viri sledi](./images/traces.svg)

**OSINT** je zbiranje in povezovanje javno dostopnih informacij. Objave, dokumenti, fotografije in storitve puščajo povezljive sledi.

Note:
Za prvi sklop skupaj dvanajst minut, vključno z naslovnico in okvirom. Začnemo neposredno z vsebino, brez organizacijskega uvoda. OSINT je zbiranje in povezovanje javno dostopnih informacij; digitalna forenzika pa preiskovanje podatkov na napravah, v datotekah in zajemih. Področji se dopolnjujeta, vendar dostop do zasebnega nosilca ni OSINT. Predstavitev najprej razloži splošne vzorce in resnične dogodke, nato jih v vajah povežemo z izmišljenim podjetjem ACME.

---

## Kaj razkrijejo stran in dokumenti?

<div class="example">
<div class="example-label">IZMIŠLJEN PRIMER · METAPODATKI DOKUMENTA</div>

```plaintext
Title:    Interni cenik 2026
Author:   Maja Kovac
Creator:  LibreOffice 7.0
Created:  2026-09-14
```

</div>

Ime avtorja lahko povežemo z javnim seznamom zaposlenih.

**Podatka se ujemata. Avtorstvo še ni dokazano.**

Note:
Metapodatki so podatki o podatkih: avtor, program in čas nastanka; pri fotografijah lahko tudi GPS. Ime lahko izvira iz predloge ali drugega računalnika. Razloži razliko med navedbo avtorja in dokazom avtorstva. V poslovnem okolju lahko dokument razkrije zaposlenega, stare različice programov ali notranje poti. Za vajo je primer pripravljen v PDF ACME; v predstavitvi ni treba odpirati datoteke ali razlagati poti do nje.

---

## Philadelphia, 2020: majica poveže spletne sledi

<p class="case-tag">RESNIČEN PRIMER · POVEZOVANJE JAVNIH VIROV</p>

<div class="case-chain"><span>Majica na posnetku</span><b>→</b><span>Ocena nakupa na Etsyju</span><b>→</b><span>Povezani spletni profili</span></div>

FBI je spletne sledi dopolnil s primerjavo tetovaže in uradnimi evidencami.

**Nauk:** več drobnih objav skupaj lahko razkrije identiteto.

<small>Vir: [sodna izjava FBI, 2020, str. 9–11](https://storage.courtlistener.com/recap/gov.uscourts.paed.572055/gov.uscourts.paed.572055.1.1.pdf#page=9)</small>

Note:
Približno minuto za zgodbo iz preiskave požiga policijskih vozil v Philadelphii maja 2020. Po sodni izjavi so preiskovalci prepoznali model majice na fotografijah, našli oceno na Etsyju in isto uporabniško ime povezali s profilom Poshmark ter nato LinkedIn. Dodatno so primerjali tetovažo na javnem videu in pridobili uradne podatke ter prodajne evidence. Javni del ponazori OSINT; uradne evidence in podatki, pridobljeni s sodnim pozivom, niso javni viri. Posamezna majica ali uporabniško ime sama ne dokazujeta identitete. Poznejši izid zadeve je dokumentiran v objavi DOJ iz julija 2022. Ne reproduciraj kontaktov ali zasebnih podatkov iz sodne vloge.

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

Tudi DNS je javni vir: zapisi razkrivajo imena, napačno nastavljen strežnik pa celotno območje.

**Čas objave in izvor podatka sta del ugotovitve.**

Note:
Iskalni operatorji omejijo domeno, vrsto datoteke ali del naslova. Arhiv pokaže preteklo objavo, javni dnevniki certifikatov domenska imena. DNS omeni zato, ker je vaja 1.3 (AXFR) v krogu digitalnih sledi, tehnična razlaga prenosa območja pa pride šele v sklopu Omrežja; poizvedba na strežnik je že neposreden stik s tarčo, ne pasivno iskanje. Noben vir ne zagotavlja popolnosti ali trenutnega delovanja. Robots.txt je navodilo iskalniku, ne nadzor dostopa. Ne izvajaj vseh poizvedb v živo; uporabi pripravljen primer. Učna domena acme.lab ni javno indeksirana.

---

## Strava, 2018: vzorec gibanja razkrije lokacijo

<p class="case-tag">RESNIČEN PRIMER · JAVNO OBJAVLJENI PODATKI</p>

<div class="case-chain"><span>Športne aktivnosti</span><b>→</b><span>Javni zemljevid gostote</span><b>→</b><span>Razvidne vojaške lokacije</span></div>

Običajen podatek dobi nov pomen, ko ga povežemo s krajem in ponavljanjem.

**Nauk:** presojamo tudi posledice skupne objave številnih posameznih sledi.

<small>Vir: [ameriško obrambno ministrstvo, 29. 1. 2018](https://www.defense.gov/News/News-Stories/Article/Article/1426579/dod-studying-implications-of-wearable-devices-giving-too-much-info/)</small>

Note:
Približno minuto za primer. Pentagon je januarja 2018 opisal varnostno vprašanje zemljevida Strava, ki je prikazoval poti teka in kolesarjenja ter lahko razkrival vojaške lokacije. Ne trdi, da so bile vse lokacije prej neznane ali da zemljevid gostote sam razkriva identiteto vsake osebe. Varnostni sklep: javni lokacijski podatki lahko pokažejo vzorce, čeprav posamezna objava deluje neškodljivo. Primer ne zahteva vdora v aplikacijo ali iskanja dejanskih posameznikov med predavanjem.

---

## Shodan: kaj je bilo zaznano in kdaj?

<div class="example">
<div class="example-label">PONAZORITEV ZADETKA · DOKUMENTACIJSKI NASLOV, NI ŽIV REZULTAT</div>

```plaintext
IP             203.0.113.25
Organizacija   Primer Gostovanje d.o.o.   ← podatek ponudnika
Lokacija       Ljubljana, SI              ← ocena iz baze naslovov
80/tcp         nginx 1.18.0               ← odziv ob opažanju
Zadnjič        2026-09-30                 ← ne pomeni »zdaj«
```

</div>

Preberemo storitev, odziv in čas zadnjega opažanja.

**Oznaka CVE je namig za preverjanje.**

Note:
Shodan in Censys indeksirata opažene spletne storitve ter odzive; to ni isti korak kot lasten aktivni pregled. 203.0.113.25 je dokumentacijski naslov (RFC 5737), zadetek je sestavljen. Če je mogoče, namesto njega pokaži datiran posnetek resničnega zadetka, ki ga pripraviš za vajo 1.1. Organizacija in lokacija sta podatka ponudnika, čas je ključen. Oznaka CVE je izhodišče za preverjanje. Živi prikaz je dodatna možnost, če ostane čas; ne zahteva računa udeležencev. Vaja 1.1 omogoča podrobnejši samostojen pregled.

---

## Orodja za sledi, povezave in forenziko

| Kaj raziskujemo? | Primeri orodij |
| --- | --- |
| Spletne storitve in domene | [Shodan](https://www.shodan.io/), [Censys](https://censys.com/), [crt.sh](https://crt.sh/) |
| Javno objavljene naslove in imena | [theHarvester](https://github.com/laramies/theHarvester) |
| Povezave med podatki | [Maltego](https://www.maltego.com/), [SpiderFoot](https://github.com/smicallef/spiderfoot) |
| Rekurzivno odkrivanje domen in storitev | [BBOT](https://github.com/blacklanternsecurity/bbot) |
| Metapodatke in nosilce | [ExifTool](https://exiftool.org/), [Autopsy](https://www.autopsy.com/) |
| Zajem delovnega pomnilnika | [Volatility](https://volatilityfoundation.org/) |

**Vir podatka določa, kaj lahko iz njega sklepamo.**

Note:
To je orientacijski zemljevid, ne seznam orodij za namestitev. theHarvester zbira podatke iz virov, Maltego prikaže in raziskuje povezave, SpiderFoot avtomatizira zbiranje iz več virov. BBOT rekurzivno odkriva dodatne domene in storitve ter povezuje module za raziskovanje izpostavljenosti; glede na izbiro modulov uporablja pasivne vire ali aktivne poizvedbe. ExifTool bere metapodatke, Autopsy preiskuje nosilce, Volatility analizira zajeme pomnilnika. Zajem zasebnega nosilca ali pomnilnika ni javni vir; ne enači forenzike z OSINT. Ne trdi, da so bila ta orodja uporabljena v opisani preiskavi. Možnosti in način dela so odvisni od podatkov, virov in nastavitev. Uradne povezave so na imenih orodij v preglednici.

---

## Povežimo podatke, preverimo sklep

| Sled | Kaj izvemo? | Kaj še manjka? |
| --- | --- | --- |
| Ime v dokumentu | Navedeni avtor | Potrditev avtorstva |
| Ime v certifikatu | Objavljeno domensko ime | Trenutno stanje storitve |
| Zapis v Shodanu | Preteklo opažanje | Nova meritev |

**Vir + čas + neodvisna potrditev → utemeljen sklep.**

Note:
Zaključi prvi sklop z razločevanjem med opažanjem in sklepom. Enako ime na dveh straneh še ne dokazuje iste osebe. Philadelphia ponazori povezovanje vizualnih sledi in spletnih profilov, Strava pa sklepanje iz javnih lokacijskih vzorcev. Tudi graf povezav iz orodja ne nadomesti presoje izvora. Navodila in ukazi za ACME ostanejo na strani z vajami.

---

## 2. sklop · Omrežja

**Kaj sme doseči uporabnik, naprava ali zunanji izvajalec?**

| Del okolja | Primer storitve | Vprašanje o dostopu |
| --- | --- | --- |
| Javni strežniki | Spletna stran, pošta | Kaj mora biti dosegljivo od zunaj? |
| Notranji sistemi | Dokumenti, zbirke podatkov | Kdo jih potrebuje za delo? |
| Naprave in upravljanje | Kamera, klima, skrbniški vmesnik | Od kod je dostop upravičen? |

IP določi naslov · vrata označijo storitev · TCP in UDP ločimo.

Note:
Za Omrežja skupaj petnajst minut, vključno s prikazom segmentacije. IP je naslov omrežnega vmesnika; vrata so številka v transportnem protokolu, na kateri je storitev dosegljiva. 53/tcp in 53/udp sta različni meritvi. Splošno vprašanje je, katere poti so potrebne za delo in katere samo širijo posledice vdora. Zunanji in notranji dostop nista enakovredna. Za predstavo lahko omeniš domače omrežje gostov, službeni prenosnik in kamero, nato poslovni primer izvajalca in plačilnega okolja.

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
Na kratkem označenem izpisu razloži tri vprašanja: prisotnost naprave, dosegljiva vrata in prepoznana storitev. -Pn preskoči odkrivanje prisotnosti, -sT preveri povezavo TCP, -sV prepoznava storitev. Ime brez -sV lahko temelji le na številki vrat. Odprta storitev ni samodejno napaka. Ukaz uporablja laboratorijski naslov samo kot konkreten primer sintakse; izvedba ukaza je del vaj, ne obvezni prikaz predavanja.

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
AXFR je prenos območja, uporaben za izmenjavo med ustreznimi strežniki DNS. Če je dovoljen neustreznim odjemalcem, lahko razkrije zemljevid notranjih imen. Izpis je sintetična ponazoritev; 192.0.2.53 ni živa tarča. Razkrito ime ne dokazuje dosegljive storitve. Tehnični preizkus je pripravljen v vaji 1.3. Tudi običajni zapisi lahko razkrivajo imena, zato je omejitev AXFR samo del ureditve podatkov DNS.

---

## SMB: kdo lahko bere deljene datoteke?

| Opažanje | Kaj dokazuje? |
| --- | --- |
| Vidim ime deljene mape | Mapa je navedena v seznamu |
| Brez prijave odprem datoteko | Gost ima pravico do branja |
| Zaposleni vidi podatke drugega oddelka | Dovoljenja zahtevajo pregled |

**smbclient** preveri dostop; **enum4linux-ng** zbere širši pregled.

**Ukrep:** pravice uskladimo z vlogo uporabnika in namenom podatkov.

Note:
Deljene mape so vsakdanji vir preširokega dostopa. Javno branje ni nujno napaka, če gre za res javne podatke; vsebino in namen moramo poznati. Vidnost imena in branje vsebine sta različna dokaza. Podatki o napravah, kopije dokumentov ali izvozi baz pogosto pristanejo v napačni mapi. Vaja 2.2 na ACME primerja javno in uprava; ukazi so pri nalogi, zato jih na tej prosojnici ne izvajamo.

---

## Kako segmentacija spremeni dostop?

<div class="example">
<div class="example-label">ACME · ISTA MERITEV IZ VTIČNICE V SEJNI SOBI, DVA SCENARIJA</div>

```plaintext
nmap -Pn -sT -p 80,502 172.20.30.12        # krmilnik klime

visitor (segmentirano)     flat (brez segmentacije)
80/tcp   filtered          80/tcp   open   http
502/tcp  filtered          502/tcp  open   mbap (Modbus)
```

</div>

**Segmentacija omeji dovoljene poti in s tem doseg napadenega sistema.**

Za razpravo: kam lahko pride nekdo, ki prevzame spletni strežnik v DMZ?

Note:
Segmentacija loči okolja glede na njihove vloge in s pravili omeji promet med njimi. Ločen VLAN brez omejitev prometa ne zadostuje. Cilj je tudi omejiti posledice, ko je ena naprava že napadena. To je osrednji prikaz delavnice, približno tri minute. Priporočeno v živo: z ./infra/lab.sh scenario flat preklopi, z istega Kali ponovi ukaz (nova povezava), nato takoj ./infra/lab.sh scenario visitor in preveri status. Preklop velja za vse, zato ga izvedi samo med predstavitvijo, nikoli med vajami. Če laboratorij ni na voljo, uporabi izpis s prosojnice; ustreza meritvam iz infra/README.md. V visitor lahko nmap -sn naslov IoT označi kot dosegljiv, čeprav so vsa vrata filtrirana; šteje rezultat vrat. Vprašanje o DMZ: ACME namerno dovoljuje promet DMZ → IoT. S Kali ga ne vidimo; pokaže se šele, ko nekdo prevzame strežnik v DMZ. Odgovora ne razkrij takoj, vrni se nanj pri Targetu. Razpravo nadaljuj z resničnima primeroma Target in WannaCry.

---

## Target, 2013: od dobavitelja do občutljivih sistemov

<p class="case-tag">RESNIČEN PRIMER · ANALIZA AMERIŠKEGA SENATA IZ 2014</p>

<div class="case-chain"><span>Zlorabljen dostop dobavitelja</span><b>→</b><span>Premik med notranjimi sistemi</span><b>→</b><span>Podatki plačilnih kartic</span></div>

Analiza opozarja na nezadostno ločitev občutljivih delov omrežja.

**Nauk:** dostop zunanjega izvajalca naj vodi le do storitev, ki jih potrebuje.

<small>Vir: [odbor ameriškega senata, 2014, povzetek](https://www.commerce.senate.gov/wp-content/uploads/media/doc/2014%200325%20Target%20Kill%20Chain%20Analysis.pdf#page=2)</small>

Note:
Približno minuto. Poročilo senata povzema takrat javno dostopne ugotovitve in analize; ne gre za popolno končno forenzično rekonstrukcijo. V njem opisana pot od dobaviteljevega dostopa do občutljivih sistemov nakazuje pomanjkljivo izolacijo. Ne poenostavi v zgodbo, da so napadalci vdrli v sam krmilnik klime. Segmentacija bi lahko omejila nadaljnji premik; trditev, da bi sama zagotovo preprečila celoten vdor, ni upravičena. Potrebni so tudi omejene pravice računov, spremljanje ter odziv na opozorila. Tu odgovori na vprašanje s prosojnice o segmentaciji: tudi ACME ima eno preširoko pot, DMZ → IoT. Kdor prevzame spletni strežnik, doseže kamero, tiskalnik in klimo, čeprav jih obiskovalec v sejni sobi ne vidi.

---

## WannaCry, 2017: ko izpad IT prekine zdravstveno oskrbo

<p class="case-tag">RESNIČEN PRIMER · NHS V ANGLIJI</p>

Napad je povzročil odpovedi pregledov in operacij ter preusmerjanje pacientov.

NAO je pri okuženih organizacijah izpostavil neposodobljene ali nepodprte sisteme Windows.

**Varnostni nauk:** popravki zmanjšajo možnost okužbe; omejene omrežne poti omejijo širjenje in posledice.

<small>Vir: [National Audit Office, poročilo o WannaCry in NHS](https://www.nao.org.uk/reports/investigation-wannacry-cyber%20attack-and-the-nhs/)</small>

Note:
Približno minuto. NAO opisuje posledice za oskrbo in pomanjkljivosti pri popravkih ter zunanjih požarnih zidovih. Prizadetost storitve ni isto kot okužba vsake naprave; motnje so imeli tudi odvisni ali preventivno odklopljeni sistemi. Notranja segmentacija je naš splošni varnostni nauk, ne ugotovitev poročila o edinem vzroku. Omejene poti lahko zmanjšajo širjenje, ne nadomestijo pa popravkov in načrta obnovitve.

---

## IoT: dostop do naprav in njihovih podatkov

| Naprava | Storitev | Kaj preverimo? |
| --- | --- | --- |
| Kamera | HTTP, RTSP 554/tcp | Izpostavljenost vmesnika |
| Tiskalnik | SNMP 161/udp | Podatke s skupnostjo `public` |
| Klima | Modbus 502/tcp | Dosegljivost krmilnika |

<div class="example">
<div class="example-label">VZOREC UKAZA · V VAJAH (VISITOR) IoT NI DOSEGLJIV</div>

```plaintext
snmpwalk -v2c -c public [IP-tiskalnika] 1.3.6.1.2.1.1
```

</div>

**Ukrep:** dostop omejimo na potrebne upravljavske poti.

Note:
Splošni primeri naprav: tiskalnik razkriva kontakt in lokacijo prek slabo omejenega SNMP, kamera izpostavlja spletno upravljanje, krmilnik uporablja protokol brez ustreznega preverjanja uporabnika. Dostopnost vrat sama še ne dokazuje možnosti spremembe nastavitev. Ukaz je vzorec z nadomestnim naslovom. Ker vaje potekajo v visitor, udeleženci naprav IoT ne dosežejo; to je namerna posledica segmentacije s prejšnje prosojnice. V predavanju ni treba vzpostavljati povezav; uporabi pripravljen izsek. Če vseeno pokažeš SNMP v labu (tiskalnik 172.20.30.11), ga izvedi skupaj s prikazom segmentacije v flat in nato vrni visitor. Wireshark vidi lasten oziroma dosegljiv promet, ne samodejno vsega prometa preklopljenega omrežja.

---

## Zastarela storitev: kaj pove različica?

![Zaznana različica, pogoji in potrditev vedenja so ločeni koraki](./images/verification.svg)

**Nmap prepozna storitev. Naslednji preizkus preveri konkreten pogoj.**

Note:
Zastarela različica je razlog za preverjanje in načrtovanje nadgradnje. Oglas različice lahko zavaja, paket pa lahko vsebuje prenesene varnostne popravke. Nmap poda namig, izbrana skripta preveri konkretno lastnost, proizvajalčevo obvestilo pojasni pogoje. Metasploit lahko pomaga pri nadzorovanem preverjanju znane ranljivosti, vendar izbira modula ni dokaz. V delavnici je za stare storitve pripravljen Metasploitable 2, podrobnosti so v vajah.

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
Greenbone je primer pregledovalnika ranljivosti, Nessus je druga razširjena možnost. Poročilo povezuje obseg, dokaz, resnost in odpravo. Visoka resnost ni isto kot verjetnost napada, Quality of Detection ne potrjuje vseh pogojev izrabe. Inventar in prava konfiguracija pregleda sta ključna: pregled ne more preveriti neznane oziroma izpuščene tarče. V predavanju razloži pripravljen izsek; preklop v živo je neobvezen, podroben pregled pa sodi v vajo 2.5.

---

## Omrežna orodja: pregled, preizkus in zaznava

| Namen | Primeri orodij |
| --- | --- |
| Odkrijemo storitve in izpostavljenost | [Nmap](https://nmap.org/), [Masscan](https://github.com/robertdavidgraham/masscan) |
| Razumemo omrežni promet | [Wireshark](https://www.wireshark.org/docs/), [tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html) |
| Poiščemo znane težave | [Greenbone](https://greenbone.github.io/docs/latest/), [Nessus](https://www.tenable.com/products/nessus) |
| Preverimo izbrano znano ranljivost | [Metasploit](https://www.rapid7.com/products/metasploit/) |
| Spremljamo dogajanje in opozorila | [Zeek](https://zeek.org/), [Suricata](https://suricata.io/), [Wazuh](https://wazuh.com/platform/overview/) |

**Enkraten pregled in stalno spremljanje odgovarjata na različni vprašanji.**

Note:
Pokaži širino področja, brez zagona vseh orodij. Masscan je namenjen hitremu iskanju odprtih vrat, ne nadomešča podrobne prepoznave Nmap. Wireshark in tcpdump delata z vidnim oziroma zajetim prometom. Greenbone in Nessus pomagata pri pregledu ranljivosti; Metasploit pri nadzorovanem preverjanju izbranih znanih ranljivosti. Zeek iz prometa izdela podatke o dogodkih, Suricata omogoča zaznavanje in opozarjanje. Wazuh zbira in analizira dnevnike sistemov ter aplikacij, spremlja spremembe datotek in povezuje varnostne dogodke; združuje zmožnosti SIEM in XDR. Pregled, izraba in zaznava niso zamenljivi izrazi. Orodja v tem pregledu niso vsa del vaj ali nameščena v predlogi Kali; uradne povezave so na imenih orodij v preglednici.

---

## 3. sklop · Aplikacije

**Kaj se zgodi z našim vnosom?**

<div class="example">
<div class="example-label">POENOSTAVLJEN PRIMER SPLETNE APLIKACIJE</div>

```plaintext
GET /api/izdelki?q=jabolko HTTP/1.1
Host: trgovina.example

HTTP/1.1 200 OK
Content-Type: application/json

{"status":"success","data":[...]}
```

</div>

Metoda in pot → podatki → obdelava → odgovor.

Note:
Za Aplikacije skupaj štirinajst minut, vključno s sklepno prosojnico »Od ugotovitve do ukrepa«. Razloži HTTP na eni zahtevi in odgovoru; primer je generičen, ne obljuba konkretne poti API. Vnos je lahko v URL, telesu ali glavah. Status beremo skupaj z vsebino. HTTPS zaščiti prenos, vendar ne odpravi napak v poslovni logiki ali preverjanju pravic. Pri praktičnih nalogah isti model uporabimo na Juice Shop.

---

## ZAP: zahtevo spremenimo in ponovimo

![Brskalnik pošlje zahtevo prek lokalnega ZAP do aplikacije](./images/zap.svg)

**Ohranimo izhodišče, spremenimo en podatek in primerjamo odgovor.**

Note:
Prestrezni posrednik omogoča pogled na lastne zahteve, spremembo podatka in ponovitev. Loči opazovanje, ročno preverjanje in samodejni aktivni pregled. ZAP in Burp Suite sta primera; za prvi pogled zadoščajo tudi razvijalska orodja Firefox. Za prikaz izberi eno spremenjeno zahtevo, denimo ID košarice, in ga omeji na približno dve minuti. Nastavitve brskalnika ter posrednika so izvajalska priprava, ne vsebina splošne razlage.

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
Pogosta razkritja so varnostne kopije, izvozi baz, dnevniki, datoteke nastavitev in javno objavljen repozitorij .git. Robots.txt ali odsotnost povezave ne uveljavita pravic dostopa. Razkrite skrivnosti prekličemo ali zamenjamo, ne le odstranimo datoteke. curl preveri konkretno pot, ffuf oziroma Gobuster odkrivata poti po seznamu. Učni primer ACME ostane pri vajah; v predavanju ne prikazuj resničnih razkritih gesel.

---

## Prijava: geslo in zaščita prenosa

| Primer | Težava | Ukrep |
| --- | --- | --- |
| Upravljavski vmesnik | Privzeti ali ponovno uporabljeni podatki | Ločene, ustrezno zaščitene prijave |
| Notranji portal | HTTP Basic brez TLS | HTTPS in omejen dostop |

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
Razlikuj tri težave: privzeto geslo, ponovno uporabo skrivnosti in nezaščiten prenos. Niz Base64 je izmišljen; CyberChef pokaže, da za pretvorbo ne potrebujemo skrivnega ključa. Lastni brskalnik podatke vidi tudi pri HTTPS. MFA zmanjša tveganje nekaterih zlorab računov, ni pa nadomestilo za preverjanje pravic do posameznega vira. Praktična primera sta NAS in intranet ACME; ni ju treba odpirati med splošno razlago.

---

## Eno razkritje, več vrat

![Javna kopija razkrije geslo, ponovljeno geslo odpre drugo storitev; ukrepi prekinejo vsak člen](./images/chain.svg)

**Geslo iz ene napake odpre drugo storitev, če ga ponovno uporabimo.**

Note:
Približno minuto. Zgornja vrsta je veriga: razkrita poverilnica v javni kopiji, isto geslo pri drugi storitvi, nato dostop s pravicami tega računa. Spodnja vrsta pokaže, da vsak ukrep prekine en člen: odstranitev kopije in menjava gesla, ločene prijave ali ključi SSH, omejene pravice in beleženje prijav. Odstranitev datoteke brez menjave gesla ne zadostuje, ker je geslo morda že kopirano. Povezava med dvema ugotovitvama je pogosto pomembnejša od vsake posebej. Vaja 3.3 preveri točno to verigo na ACME; vrednosti gesla ne razkrivaj.

---

## SQL injection: vnos spremeni poizvedbo

<div class="example">
<div class="example-label">POENOSTAVLJENA POIZVEDBA · UČNI PRIMER</div>

```plaintext
SELECT ... WHERE uporabnik = '[vnos]'
             AND password = ...

Vnos: ana'--

SELECT ... WHERE uporabnik = 'ana'-- ...
```

</div>

**Napaka:** aplikacija podatke združi z navodili SQL.

**Ukrep:** parametrizirane poizvedbe ločijo podatke od kode.

Note:
Poenostavljeni primer prikazuje mešanje podatkov in navodil SQL; ni izpis konkretnega produkcijskega sistema. Narekovaj zaključi vrednost, komentar lahko izloči nadaljnji pogoj. Glavni ukrep so parametrizirane poizvedbe. sqlmap avtomatizira preverjanje nekaterih vektorjev SQL injection, ZAP in Burp pomagata pri ročnem spreminjanju zahtev. V vaji 3.4 je konkreten postopek za prijavo Juice Shop; ni treba razlagati njegove privzete domene na tej prosojnici.

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
XSS pomeni cross-site scripting. Aplikacija nevarno obravnava nezaupanja vreden vnos kot izvajalno vsebino v brskalniku. Posledice so odvisne od konteksta in pravic: dejanja v imenu uporabnika ali branje dosegljivih podatkov. textContent je ustrezen za navadno besedilo; dovoljen HTML potrebuje ustrezno sanitizacijo. Kontekstno kodiranje izhoda in CSP sta različna ukrepa. DOM XSS se lahko izvede brez ustrezne sledi v strežniškem odgovoru. Za neobvezen prikaz uporabimo lokalni učni primer, ne shranjenega XSS na skupni tarči.

---

## Prijava še ne pomeni pravice do vseh podatkov

<div class="example">
<div class="example-label">PONAZORITEV ID-JEV · PRIJAVNI ŽETON OSTAJA OD A</div>

```plaintext
Račun A → GET /api/kosarice/7   → košarica A
Račun A → GET /api/kosarice/12  → košarica B
```

</div>

**IDOR / BOLA:** strežnik ne preveri pravice do zahtevanega objekta.

**Ukrep:** pri vsaki zahtevi preverimo lastništvo in dovoljene pravice.

Note:
IDOR pomeni insecure direct object reference, BOLA broken object level authorization. Aplikacija prepozna uporabnika, ne preveri pa njegove pravice do objekta. Primer ni omejen na trgovino: enako velja za račun, zdravstveni dokument, naročilo ali datoteko. Težje ugibljiv ID ne nadomesti preverjanja lastništva. Kratek neobvezen prikaz na Juice Shop uporablja dejansko pot /rest/basket/:id, pripravljena navadna računa in nespremenjen žeton A. V predavanju zadošča pojasnilo zahteve in odgovora; navodila so pri vaji 3.5.

---

## Equifax, 2017: znana ranljivost, veliko razkritje

<p class="case-tag">RESNIČEN PRIMER · OČITKI FTC OB PORAVNAVI</p>

<div class="case-chain"><span>Nenameščen popravek</span><b>→</b><span>Vstop in dostop do drugih sistemov</span><b>→</b><span>Podatki približno 147 milijonov ljudi</span></div>

FTC je očital tudi neustrezno segmentacijo in prijavne podatke v nezaščiteni datoteki.

**Nauk:** upravljanje komponent, skrivnosti in notranjih dostopov deluje skupaj.

<small>Vir: [FTC, objava poravnave iz leta 2019 o vdoru 2017](https://www.ftc.gov/news-events/news/press-releases/2019/07/equifax-pay-575-million-part-settlement-ftc-cfpb-states-related-2017-data-breach)</small>

Note:
Približno minuto. FTC je ob poravnavi opisal neizveden popravek, nezaščitene administrativne podatke in neustrezno ločitev baz. Navedbe predstavljamo kot očitke regulatorja, ne kot lastno forenzično analizo ali kazensko obsodbo. Primer poveže aplikacijsko vstopno točko in nadaljnji dostop. Ključna sta inventar komponent in preverjanje izvedbe popravkov; pregledovalnik z neustreznim obsegom ni dovolj.

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

**Različica + nastavitev + dejanski odziv → utemeljen sklep.**

<small>[Apache: varnostna obvestila](https://httpd.apache.org/security/vulnerabilities_24.html)</small>

Note:
Zgodovinski primer Apache 2.4.49 pokaže, zakaj sama oznaka CVE še ne potrdi vseh poti izrabe. Za dostop do datotek so pomembna dovoljenja, za izvajanje kode še CGI. V nasprotju s tem je Equifax primer, kjer je znana neodpravljena ranljivost pomenila dejansko vstopno točko. Negativen preizkus ene poti ne potrjuje popolne varnosti. Ukrep je podprta različica in preverjena konfiguracija. Posebnost privzete nastavitve ACME ostane razložena pri vaji 2.3.

---

## Varnost preverjamo tudi pred objavo

| Področje | Primeri orodij | Namen |
| --- | --- | --- |
| Izvorno kodo | [Semgrep](https://semgrep.dev/docs/) | Nevarne vzorce v kodi |
| Knjižnice | [Dependency-Check](https://owasp.org/www-project-dependency-check/), [Trivy](https://trivy.dev/) | Znane ranljivosti komponent |
| Slike zabojnikov in nastavitve | [Trivy](https://trivy.dev/) | Ranljive pakete, skrivnosti, napačne nastavitve |
| Posodobitve knjižnic | [Renovate](https://github.com/renovatebot/renovate) | Samodejni predlogi posodobitev |

**Pregled kode in komponent dopolni preizkus delujoče aplikacije.**

Note:
Razširi pogled z zunanjega preizkušanja na razvoj in vzdrževanje. Pregled kode, sestave programske opreme in delujočega sistema pokriva različne razrede težav. Semgrep je primer statične analize; OWASP Dependency-Check in Trivy preverjata odvisnosti, Trivy ima tudi preglede skrivnosti in konfiguracij. Zaznava skrivnosti ne pomeni samodejne potrditve, da ključ še velja. Renovate poišče nove različice odvisnosti in odpre predloge sprememb (pull requeste); posodobitve preverimo s testi in pregledom sprememb. Tako poleg odkrivanja težav predstavimo tudi redno vzdrževanje komponent. Pregled se lahko vključi v razvojni proces, vendar potrebuje obravnavo ugotovitev. Orodij ne nameščamo za današnje vaje. Uradne povezave so na imenih orodij v preglednici.

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
Ta pregled obsega več možnosti, kot jih bomo uporabili pri vajah. Nikto preverja spletni strežnik, Nuclei izvaja preizkuse po predlogah; rezultati so odvisni od obsega in nastavitev. ZAP in Burp združujeta ogled prometa z dodatnimi ročnimi in samodejnimi preizkusi. sqlmap je specializiran za SQL injection. Poslovni pomen objekta in razmerje med uporabnikoma pogosto zahtevata ročni preizkus. Predstavitev orodja ni navodilo za njegov zagon med delavnico.

---

## Od ugotovitve do ukrepa

**Kaj smo opazili? → Kaj to omogoča? → Kaj spremenimo?**

| Dokaz | Ukrep | Ponovno preverjanje |
| --- | --- | --- |
| Gost prebere interno datoteko | Uredimo dovoljenja | Gostujoče branje je zavrnjeno |
| Račun A vidi košarico B | Preverimo lastništvo | Zahteva A za B je zavrnjena |

**Ukrep je končan, ko ponovno preverjanje pokaže spremembo.**

Note:
Zaključi splošni pregled z vprašanjem, kaj bi pri posameznem resničnem dogodku prekinilo verigo in kakšen dokaz bi potrebovali za preverjanje ukrepa. Vrni se na okvir z začetka: zadnji korak »Kaj spremenimo?« dopolni ponovna meritev. Primeri so ilustracije vzorcev, ne rekonstrukcije v laboratoriju.

---

## ACME: izmišljeno podjetje za vaje

![Udeleženec prek požarnega zidu do treh segmentov ACME: DMZ, LAN in IoT](./images/acme.svg)

<small>Javni naslovi 198.51.100.11–15 · DMZ 172.20.10.0/24 · LAN 172.20.20.0/24 · IoT 172.20.30.0/24</small>

**Vaš položaj (`visitor`):** prenosnik v vtičnici sejne sobe. Dosežete javne naslove, LAN in storitve DMZ, IoT pa ne.

Note:
Približno dve minuti. ACME je izmišljen; javni naslovi 198.51.100.x so dokumentacijski in delujejo samo v laboratoriju, imena pod acme.lab razreši laboratorijski DNS. DMZ: www, shop (Juice Shop), mail, ns1, vpn. LAN: files, intranet, nas, hr-pc in Metasploitable 2 (172.20.20.30) kot primer nevzdrževanega notranjega strežnika. IoT: kamera, tiskalnik, klima. Scenarij visitor ostane nastavljen ves praktični blok; s prikaza segmentacije vemo, zakaj IoT ni dosegljiv. Notranjih naslovov ne iščemo na javnem internetu.

---

## Pravila in potek vaj

<div class="cards">
<div class="card">

### Dostop

S svojo kodo odpri [prevzem dostopa](./vaje/dostop/). Kali v brskalniku ali svoj Kali prek WireGuard. V Kali uporabljaš Firefox in Terminal.

</div>
<div class="card">

### Kaj smemo

Samo navedene tarče ACME. Ničesar ne spreminjamo. Javne vire samo beremo. Napad na tuje sisteme je kaznivo dejanje.

</div>
<div class="card">

### Potek

Trije krogi: 25, 40 in 40 minut. Izberi 1 od 3 vaj, nato dodatni izziv. Namig → postopek → zapis.

</div>
</div>

[Praktične vaje](./vaje/) · podatke za vaje 1.1, 1.5 in 3.5 poda izvajalec

Note:
Približno dve minuti, nato začnemo prvi krog. Kali dostopa do spleta samo prek posrednika Squid; tarče ACME so v no_proxy izvzete. Ukazi v vajah z curl --noproxy '*' zagotovijo neposredno povezavo tudi pri lastnem Kali ali drugačnih nastavitvah lupine; teh možnosti ni treba odstranjevati. Shodan in crt.sh udeleženci odpirajo v svojem običajnem brskalniku in javnih naslovov ne pregledujejo z Nmap. Pravna plat: v Sloveniji je nepooblaščen vstop v informacijski sistem kaznivo dejanje po KZ-1; vaje so dovoljene, ker smo lastniki laboratorija. Napiši na tablo ali pokaži IP za vajo 1.1, domeno za vajo 1.5 ter učna računa in ID košaric za vajo 3.5. Ne zapisuj gesel na prosojnice. Časovnica: 45 minut predstavitve, nato 25 minut digitalnih sledi, po 40 minut omrežij in aplikacij ter 10 minut pogovora. Vaje ostajajo samostojne, z namigi in postopki; omrežje je ves čas visitor.
