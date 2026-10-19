# Cybersec-201: načrt izvedbe

Delavnica povezuje digitalne sledi, omrežne storitve in aplikacijske ranljivosti na infrastrukturi izmišljenega podjetja ACME. Pri vsakem primeru razložimo težavo, orodje, dokaz in ukrep. Namenjena je radovednim udeležencem z različnimi tehničnimi izkušnjami.

## Potek

Uvodnih prosojnic ni. Prijave uredimo pred začetkom; predstavitev se začne neposredno s prvim sklopom. Najprej izvedemo vse tri vsebinske sklope s kratkimi prikazi, nato praktično delo.

| Del | Predstavitev s prikazi | Praktično delo in pogovor | Skupaj |
| --- | --- | --- | --- |
| 1. Digitalne sledi | 7 minut | — | 7 minut |
| 2. Omrežja | 14 minut | — | 14 minut |
| 3. Aplikacije | 14 minut | — | 14 minut |
| Vaje: Digitalne sledi | — | 25 minut | 25 minut |
| Vaje: Omrežja | — | 40 minut | 40 minut |
| Vaje: Aplikacije | — | 40 minut | 40 minut |
| Primerjava ugotovitev in zaključek | — | 10 minut | 10 minut |
| **Skupaj** | **35 minut** | **115 minut** | **150 minut** |

## Prosojnice

Predstavitev vsebuje 23 prosojnic: pet za digitalne sledi, osem za omrežja, devet za aplikacije in eno sklepno. Izpisi, številke košaric ter poenostavljeni primeri so označeni; niso predstavljeni kot meritve živega okolja.

| Št. | Naslov | Namen |
| --- | --- | --- |
| 1 | 1. sklop · Digitalne sledi | Neposreden začetek: kaj o ACME povedo javni viri? |
| 2 | Kaj razkrijejo stran in dokumenti? | Povezava učnih metapodatkov z javnimi podatki o ekipi. |
| 3 | Iskanje omejimo na uporabne sledi | Iskalni operatorji, arhivi in certifikati. |
| 4 | Shodan: kaj je bilo zaznano in kdaj? | En pripravljen dejanski zadetek; vir, storitev in čas. |
| 5 | Povežimo podatke, preverimo sklep | Razlika med opažanjem in utemeljenim sklepom. |
| 6 | 2. sklop · Omrežja | IP, vrata in TCP/UDP na eni shemi ACME. |
| 7 | Nmap: od vrat do storitve | Omejen pregled in branje rezultata. |
| 8 | DNS: kdo lahko prenese celotno območje? | AXFR, notranja imena in ukrep. |
| 9 | SMB: kdo lahko bere deljene datoteke? | Vidnost mape in pravica do njene vsebine. |
| 10 | Kako segmentacija spremeni dostop? | Skupni prikaz iste meritve v visitor in flat. |
| 11 | IoT: dostop do naprav in njihovih podatkov | SNMP, kamera in Modbus; po prikazu vrnemo visitor. |
| 12 | Zastarela storitev: kaj pove različica? | Od prepoznave do preverjanja pogojev. |
| 13 | Greenbone: preverimo eno ugotovitev | Končano poročilo, dokaz in odprava. |
| 14 | 3. sklop · Aplikacije | HTTP na eni zahtevi in odgovoru Juice Shop. |
| 15 | ZAP: zahtevo spremenimo in ponovimo | Zgodovina, urejanje in primerjava odgovora. |
| 16 | Razkrite datoteke: kopija na javni strani | Posledice razkritja prijavnih podatkov. |
| 17 | Prijava: geslo in zaščita prenosa | Privzeta prijava, HTTP Basic ter kratka razlaga Base64. |
| 18 | SQL injection: vnos spremeni poizvedbo | Mehanizem napake in parametrizirane poizvedbe. |
| 19 | XSS: vnos postane skripta v brskalniku | DOM XSS, varen prikaz besedila in obdelava izhoda. |
| 20 | Prijava še ne pomeni pravice do vseh podatkov | Glavni aplikacijski prikaz: View Basket z računoma A in B. |
| 21 | Zastarele komponente: preverimo pogoje | Apache 2.4.49 brez obljube uspešne izrabe. |
| 22 | Katero orodje uporabimo? | ZAP, Firefox, Burp, curl, ffuf, Nikto in sqlmap glede na vprašanje. |
| 23 | Od ugotovitve do ukrepa | Prehod na vaje in podlaga za sklepni pogovor. |

Prikazi so časovno omejeni: Shodan približno minuto, segmentacija približno dve minuti, SNMP kratek izsek, Greenbone približno dve minuti, ZAP z IDOR skupaj največ pet minut. Drugi primeri uporabljajo pripravljene izseke; vseh orodij ne prikazujemo v živo.

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

V predstavitvi izvajalec za prikaz segmentacije in SNMP preklopi `visitor → flat → visitor`. Za rezervo pripravi izpise obeh stanj. Pred praktičnim blokom potrdi `visitor` in ga ohrani do konca. Vaje ne zahtevajo preklopov, zato jih lahko udeleženci rešujejo različno hitro.

Javne naslove ACME lahko pregledamo tudi v visitor, vendar je to meritev z notranjega izhodišča. Notranji IoT ostane omejen. Skupni preklop flat ni dokaz ločene napake DMZ → IoT. Obstoječe povezave lahko preživijo preklop; v prikazu uporabljamo nove meritve.

Priprava prikazov, PDF, poročila in učnih računov ter pričakovani izidi so v `EXERCISES.md`. Navodila za dostop pred dogodkom so v `NAVODILO.md`.
