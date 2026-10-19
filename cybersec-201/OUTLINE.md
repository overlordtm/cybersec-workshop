# Cybersec-201: načrt izvedbe

Predstavitev poda splošen uvod v digitalne sledi, omrežja in aplikacijsko varnost. Pojme poveže z resničnimi dogodki in širšim izborom orodij, nato pripravi udeležence na praktično delo v izmišljenem podjetju ACME. Namenjena je radovednim udeležencem z različnimi tehničnimi izkušnjami.

## Potek

Predstavitev odpre naslovna prosojnica po vzoru Cybersec-101, nato neposredno sledi prvi vsebinski sklop. Prijave uredimo pred začetkom; ločenega organizacijskega uvoda ni. Najprej izvedemo vse tri vsebinske sklope s primeri iz prakse, nato praktično delo. Podrobni postopki in večina prikazov orodij sodijo k vajam; v predavanju ostane največ en kratek prikaz. Čas naslovnice je vključen v prvi sklop.

| Del | Predstavitev s prikazi | Praktično delo in pogovor | Skupaj |
| --- | --- | --- | --- |
| 1. Digitalne sledi | 10 minut | — | 10 minut |
| 2. Omrežja | 12 minut | — | 12 minut |
| 3. Aplikacije | 13 minut | — | 13 minut |
| Vaje: Digitalne sledi | — | 25 minut | 25 minut |
| Vaje: Omrežja | — | 40 minut | 40 minut |
| Vaje: Aplikacije | — | 40 minut | 40 minut |
| Primerjava ugotovitev in zaključek | — | 10 minut | 10 minut |
| **Skupaj** | **35 minut** | **115 minut** | **150 minut** |

## Prosojnice

Predstavitev vsebuje 32 prosojnic: naslovno, osem za digitalne sledi, enajst za omrežja, enajst za aplikacije in eno sklepno. Pet resničnih dogodkov ima vidne povezave do primarnih virov ter pojasnila v opombah. Izmišljeni izpisi, poti API in številke košaric so označeni kot ponazoritve. Viri so zbrani tudi v `SOURCES.md`.

| Št. | Naslov | Namen |
| --- | --- | --- |
| 1 | OSINT, omrežna in aplikacijska varnost | Naslovnica z geslom, fotografijo, avtorjem in datumom po vzoru Cybersec-101. |
| 2 | 1. sklop · Digitalne sledi | Splošen pogled na javne sledi ter razlikovanje OSINT in forenzike. |
| 3 | Kaj razkrijejo stran in dokumenti? | Metapodatki, povezovanje podatkov in omejitve sklepa. |
| 4 | Philadelphia, 2020: majica poveže spletne sledi | Povezovanje posnetkov, spletne ocene in profilov z dodatno potrditvijo. |
| 5 | Iskanje omejimo na uporabne sledi | Iskalni operatorji, arhivi in certifikati. |
| 6 | Strava, 2018: vzorec gibanja razkrije lokacijo | Resnični primer sklepanja iz javnih lokacijskih vzorcev. |
| 7 | Shodan: kaj je bilo zaznano in kdaj? | Storitev, odziv in čas opažanja. |
| 8 | Orodja za sledi, povezave in forenziko | Zbiranje, povezovanje podatkov, pregled nosilcev in pomnilnika. |
| 9 | Povežimo podatke, preverimo sklep | Razlika med podatkom in potrjenim sklepom. |
| 10 | 2. sklop · Omrežja | Vloge sistemov in upravičene omrežne poti. |
| 11 | Nmap: od vrat do storitve | Vrata, storitev in omejitve izpisa. |
| 12 | DNS: kdo lahko prenese celotno območje? | Prenos območja in notranja imena. |
| 13 | SMB: kdo lahko bere deljene datoteke? | Vidnost mape in pravica do vsebine. |
| 14 | Kako segmentacija spremeni dostop? | Splošna shema omejitve dosega; laboratorij je ponazoritev. |
| 15 | Target, 2013: od dobavitelja do občutljivih sistemov | Dobaviteljev dostop in izolacija občutljivih sistemov. |
| 16 | WannaCry, 2017: ko izpad IT prekine zdravstveno oskrbo | Operativne posledice napada in več plasti obrambe. |
| 17 | IoT: dostop do naprav in njihovih podatkov | Upravljanje naprav, SNMP in Modbus. |
| 18 | Zastarela storitev: kaj pove različica? | Od prepoznave različice do preverjanja vedenja. |
| 19 | Greenbone: preverimo eno ugotovitev | Dokaz, resnost, zanesljivost zaznave in ukrep. |
| 20 | Omrežna orodja: pregled, preizkus in zaznava | Pregled, zajem prometa, preverjanje in stalno spremljanje. |
| 21 | 3. sklop · Aplikacije | HTTP na generični zahtevi in odgovoru. |
| 22 | ZAP: zahtevo spremenimo in ponovimo | Ogled, sprememba in ponovitev zahteve. |
| 23 | Razkrite datoteke: kopija na javni strani | Kopije, dnevniki, nastavitve in posledice razkritja. |
| 24 | Prijava: geslo in zaščita prenosa | Privzeta gesla, ponovna uporaba in zaščita prenosa. |
| 25 | SQL injection: vnos spremeni poizvedbo | Mešanje podatkov in navodil SQL. |
| 26 | XSS: vnos postane skripta v brskalniku | Nezaupanja vreden vnos postane izvajalna vsebina. |
| 27 | Prijava še ne pomeni pravice do vseh podatkov | Pravice do posameznega objekta: IDOR/BOLA. |
| 28 | Equifax, 2017: znana ranljivost, veliko razkritje | Resnični primer povezave komponent, skrivnosti in dostopov. |
| 29 | Zastarele komponente: preverimo pogoje | Različica, pogoji in preverjanje konfiguracije. |
| 30 | Varnost preverjamo tudi pred objavo | Pregled kode, odvisnosti, slik in nastavitev. |
| 31 | Katero orodje uporabimo? | Ročni preizkusi, pregled strežnika in preizkusi po predlogah. |
| 32 | Od ugotovitve do ukrepa | Povezava ugotovitve, ukrepa in ponovnega preverjanja; prehod na vaje. |

Vsak resnični dogodek dobi približno minuto. Podrobni ukazi so pri vajah; Shodan in Greenbone pojasnimo s pripravljenim izsekom. Po želji izvedemo en kratek prikaz segmentacije ali IDOR, največ dve minuti. S tem ohranimo 35 minut predstavitve in obstoječi čas za praktično delo.

Pri Targetu ohranimo negotovosti zgodnje analize. Pri WannaCry notranjo segmentacijo predstavimo kot splošen nauk, ne kot edini vzrok iz poročila. Pri Equifaxu navedbe pripišemo FTC ob poravnavi. Pri primeru iz Philadelphie ločimo javne vire od uradnih evidenc in podatkov, pridobljenih s sodnim pozivom.

## Vaje

V vsakem krogu udeleženec izbere eno od prvih treh vaj glede na izkušnje. Če konča prej, nadaljuje z drugo vajo ali dodatnim izzivom. Vseh petnajst vaj ni obveznih in ne sestavljajo zaporedne verige.

| Sklop | Lahka | Srednja | Zahtevna | Dodatni izziv 4 | Dodatni izziv 5 |
| --- | --- | --- | --- | --- | --- |
| Digitalne sledi | Shodanov profil IP | Sledi spletni kopiji | Prenos območja DNS | Metapodatki PDF | Imena iz certifikatov |
| Omrežja | Javne storitve ACME | Dostop do map SMB | Presoja različice Apache | Izbrani skripti NSE | Preverjanje ugotovitve Greenbone |
| Aplikacije | Lastna zahteva HTTP | HTTP Basic in Base64 | Razkritje in dostop SSH | SQL injection pri prijavi | IDOR: druga košarica |

Vaje 1.1–1.3 in 3.1–3.3 ohranijo dogovorjeni namen. AXFR ostane vaja 1.3, čeprav tehnična razlaga spada med omrežja. Vaja 2.2 je samostojen pregled SMB. Segmentacija je skupni prikaz v predstavitvi in ne samostojna vaja.

Vsaka vaja v `vaje/VAJE.md` vsebuje nalogo ter ločeni podpoglavji `### Namig` in `### Postopek`. Stran najprej pokaže samo nalogo in gumb »Prikaži namig«. Po odprtju namiga je na voljo »Pokaži postopek«. Tam so koraki, ukazi in pričakovani rezultati. Povezave ter QR-kode iz skritih delov se razkrijejo skupaj z vsebino.

## Omrežni scenariji

Če izvajalec izbere živi prikaz segmentacije oziroma SNMP, pred vajami preklopi `visitor → flat → visitor`. Sicer uporabi splošno shemo in pripravljena izpisa obeh stanj. Pred praktičnim blokom potrdi `visitor` in ga ohrani do konca. Vaje ne zahtevajo preklopov, zato jih lahko udeleženci rešujejo različno hitro.

Javne naslove ACME lahko pregledamo tudi v visitor, vendar je to meritev z notranjega izhodišča. Notranji IoT ostane omejen. Skupni preklop flat ni dokaz ločene napake DMZ → IoT. Obstoječe povezave lahko preživijo preklop; v prikazu uporabljamo nove meritve.

Priprava prikazov, PDF, poročila in učnih računov ter pričakovani izidi so v `EXERCISES.md`. Navodila za dostop pred dogodkom so v `NAVODILO.md`.
