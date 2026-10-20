# Cybersec-201: načrt izvedbe

Predstavitev poda splošen uvod v digitalne sledi, omrežja in aplikacijsko varnost. Pojme poveže z resničnimi dogodki in širšim izborom orodij, nato pripravi udeležence na praktično delo v izmišljenem podjetju ACME. Namenjena je radovednim udeležencem z različnimi tehničnimi izkušnjami.

## Potek

Predstavitev odpre naslovna prosojnica po vzoru Cybersec-101, sledi ji prosojnica z okvirom dela (opažanje → dokaz → omejitev → vpliv → ukrep), nato prvi vsebinski sklop. Prijave uredimo pred začetkom; organizacijske informacije, ACME in pravila vaj so na koncu predstavitve, tik pred praktičnim delom. Najprej izvedemo vse tri vsebinske sklope s primeri iz prakse, nato praktično delo. Podrobni postopki in večina prikazov orodij sodijo k vajam; osrednji prikaz predavanja je primerjava visitor/flat pri segmentaciji. Čas naslovnice je vključen v prvi sklop.

| Del | Predstavitev s prikazi | Praktično delo in pogovor | Skupaj |
| --- | --- | --- | --- |
| Uvod in 1. Digitalne sledi | 12 minut | — | 12 minut |
| 2. Omrežja | 15 minut | — | 15 minut |
| 3. Aplikacije in sklep | 14 minut | — | 14 minut |
| ACME, pravila in potek vaj | 4 minute | — | 4 minute |
| Vaje: Digitalne sledi | — | 25 minut | 25 minut |
| Vaje: Omrežja | — | 40 minut | 40 minut |
| Vaje: Aplikacije | — | 40 minut | 40 minut |
| Primerjava ugotovitev in zaključek | — | 10 minut | 10 minut |
| **Skupaj** | **45 minut** | **115 minut** | **160 minut** |

## Prosojnice

Predstavitev vsebuje 34 prosojnic: naslovno, okvir dela, šest za digitalne sledi, enajst za omrežja, dvanajst za aplikacije, sklepno ter dve za ACME in pravila vaj. Štirje resnični dogodki imajo vidne povezave do primarnih virov ter pojasnila v opombah. Izmišljeni izpisi, poti API in številke košaric so označeni kot ponazoritve.

| Št. | Naslov | Namen |
| --- | --- | --- |
| 1 | OSINT, omrežna in aplikacijska varnost | Naslovnica z geslom, fotografijo, avtorjem in datumom po vzoru Cybersec-101. |
| 2 | Od sledi do ukrepa | Okvir dela za vse ugotovitve; ustreza zapisu pri vajah. |
| 3 | 1. sklop · Digitalne sledi | Splošen pogled na javne sledi ter razlikovanje OSINT in forenzike. |
| 4 | Kaj razkrijejo objavljeni dokumenti? | Metapodatki, kaj z njimi naredi napadalec in čiščenje pred objavo. |
| 5 | Philadelphia, 2020: majica poveže spletne sledi | Povezovanje posnetkov, spletne ocene in profilov z dodatno potrditvijo. |
| 6 | Iskanje omejimo na uporabne sledi | Iskalni operatorji, arhivi, certifikati in iskanje lastnih sledi. |
| 7 | Shodan: kaj je bilo zaznano in kdaj? | Storitev, odziv, čas opažanja in popis lastne izpostavljenosti. |
| 8 | Orodja za sledi, povezave in forenziko | Zbiranje, povezovanje podatkov, pregled nosilcev in pomnilnika. |
| 9 | 2. sklop · Omrežja | Vloge sistemov in upravičene omrežne poti. |
| 10 | Nmap: od vrat do storitve | Vrata, storitev in omejitve izpisa. |
| 11 | DNS: kaj razkrije imenik omrežja? | Kaj je DNS; prenos območja, notranja imena, prevzem poddomene, odprt razreševalnik. |
| 12 | SMB: deljene mape in kako jih zlorabijo | Kaj je SMB, štiri pogoste zlorabe in ukrepi. |
| 13 | Kako segmentacija spremeni dostop? | Ista meritev ACME v visitor in flat; vprašanje o poti DMZ → IoT. |
| 14 | Target, 2013: od dobavitelja do občutljivih sistemov | Dobaviteljev dostop in izolacija občutljivih sistemov. |
| 15 | WannaCry, 2017: ko izpad IT prekine zdravstveno oskrbo | Operativne posledice napada in več plasti obrambe. |
| 16 | IoT: pozabljeni računalniki v omrežju | Kaj je IoT; privzeta gesla, SNMP, Modbus, nevzdrževane naprave. |
| 17 | Zastarela storitev: kaj pove različica? | Od prepoznave različice do preverjanja vedenja. |
| 18 | Pregledovalniki ranljivosti: kako beremo ugotovitev | Dokaz, resnost, zanesljivost zaznave in ukrep; pregled s prijavo in brez nje. |
| 19 | Omrežna orodja: pregled, preizkus in zaznava | Pregled, zajem prometa, preverjanje in stalno spremljanje. |
| 20 | 3. sklop · Aplikacije | HTTP na generični zahtevi in odgovoru. |
| 21 | ZAP: zahtevo spremenimo in ponovimo | Ogled, sprememba in ponovitev zahteve. |
| 22 | Razkrite datoteke: kaj ostane na javnem strežniku? | Kopije, .git, izvozi, .env; kako jih napadalec najde. |
| 23 | Prijava: geslo in zaščita prenosa | Privzeta gesla, gesla iz drugih vdorov in zaščita prenosa. |
| 24 | Eno razkritje, več vrat | Veriga razkritje → ponovna uporaba gesla → dostop; priprava na vajo 3.3. |
| 25 | SQL injection: vnos spremeni poizvedbo | Mešanje podatkov in navodil SQL. |
| 26 | XSS: vnos postane skripta v brskalniku | Vnos, ki ni zaupanja vreden, brskalnik izvede kot kodo. |
| 27 | Prijava še ne pomeni pravice do vseh podatkov | Avtentikacija in avtorizacija; pravice do posameznega objekta: IDOR/BOLA. |
| 28 | Equifax, 2017: znana ranljivost, veliko razkritje | Resnični primer povezave komponent, skrivnosti in dostopov. |
| 29 | Zastarele komponente: preverimo pogoje | Različica, pogoji in preverjanje konfiguracije. |
| 30 | Varnost preverjamo tudi med razvojem programske opreme | Pregled kode, odvisnosti, slik in nastavitev. |
| 31 | Katero orodje uporabimo? | Ročni preizkusi, pregled strežnika in preizkusi po predlogah. |
| 32 | Od ugotovitve do ukrepa | Okvir na eni verigi, ponovno preverjanje ukrepa in prijava napake zunaj laboratorija. |
| 33 | ACME: izmišljeno podjetje za vaje | Segmenti, naslovi in položaj udeleženca v scenariju visitor; dosegljiv LAN kot prva ugotovitev. |
| 34 | Pravila in potek vaj | Dostop, dovoljene tarče, pravni okvir, potek krogov in podatki za vaje. |

Vsak resnični dogodek dobi približno minuto. Podrobni ukazi so pri vajah; Shodan pojasnimo s pripravljenim posnetkom, pregledovalnike ranljivosti pa splošno, brez izseka poročila. Prikaz segmentacije (približno tri minute) je priporočen v živo, z rezervo na prosojnici; dodatni kratek prikaz IDOR je neobvezen. S tem ostane predstavitev v okviru 45 minut, čas za praktično delo pa se ne spremeni.

Pri Targetu ohranimo negotovosti zgodnje analize. Pri WannaCry notranjo segmentacijo predstavimo kot splošen nauk, ne kot edini vzrok iz poročila. Pri Equifaxu navedbe pripišemo FTC ob poravnavi. Pri primeru iz Philadelphie ločimo javne vire od uradnih evidenc in podatkov, pridobljenih s sodnim pozivom.

## Vaje

V vsakem krogu udeleženec izbere eno od prvih treh vaj glede na izkušnje. Če konča prej, nadaljuje z drugo vajo ali dodatnim izzivom. Vseh petnajst vaj ni obveznih in ne sestavljajo zaporedne verige.

| Sklop | Lahka | Srednja | Zahtevna | Dodatni izziv 4 | Dodatni izziv 5 |
| --- | --- | --- | --- | --- | --- |
| Digitalne sledi | Shodanov profil IP | Sledi spletni kopiji | Prenos območja DNS | Metapodatki PDF | Imena iz certifikatov |
| Omrežja | Javne storitve ACME | Dostop do map SMB | Presoja različice Apache | Izbrani skripti NSE | Preverjanje ugotovitve Greenbone |
| Aplikacije | Lastna zahteva HTTP | HTTP Basic in Base64 | Razkritje in dostop SSH | SQL injection pri prijavi | IDOR: druga košarica |

Vaje 1.1–1.3 in 3.1–3.3 ohranijo dogovorjeni namen. AXFR ostane vaja 1.3, čeprav tehnična razlaga spada med omrežja. Vaja 2.2 je samostojen pregled SMB. Segmentacija je skupni prikaz v predstavitvi in ne samostojna vaja; vaji 3.3 ustreza prosojnica »Eno razkritje, več vrat«.

Vsaka vaja v `vaje/VAJE.md` vsebuje nalogo ter ločeni podpoglavji `### Namig` in `### Postopek`. Stran najprej pokaže samo nalogo in gumb »Prikaži namig«. Po odprtju namiga je na voljo »Pokaži postopek«. Tam so koraki, ukazi in pričakovani rezultati. Povezave ter QR-kode iz skritih delov se razkrijejo skupaj z vsebino.

## Omrežni scenariji

Za živi prikaz segmentacije oziroma SNMP izvajalec med predstavitvijo preklopi `visitor → flat → visitor`. Sicer uporabi izpis obeh stanj na prosojnici. Pred praktičnim blokom potrdi `visitor` in ga ohrani do konca. Vaje ne zahtevajo preklopov, zato jih lahko udeleženci rešujejo različno hitro.

Javne naslove ACME lahko pregledamo tudi v visitor, vendar je to meritev z notranjega izhodišča. Notranji IoT ostane omejen. Skupni preklop flat ni dokaz ločene napake DMZ → IoT. Obstoječe povezave lahko preživijo preklop; v prikazu uporabljamo nove meritve.

Priprava prikazov, PDF, poročila in učnih računov ter pričakovani izidi so v `EXERCISES.md`. Navodila za dostop pred dogodkom so v `NAVODILO.md`.
