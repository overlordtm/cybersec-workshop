# Cybersec-201: priprava in opombe za izvajalca

Ta datoteka ni udeleženski priročnik in se ne vključuje v stran z vajami. Udeleženska navodila so v `vaje/VAJE.md`. Osnutek temelji na datotekah infrastrukture; odzive živega okolja je treba pred dogodkom potrditi.

## Pred dogodkom

- Preveri vsak dodeljen Kali in dostop prek Guacamole; udeleženci dobijo svoje prijave.
- Določi javni IP za Shodan, preveri prikaz z udeleženskim dostopom in pripravi datiran posnetek. Ne uporabljaj javnega naslova gostitelja lab kot implicitne tarče aktivnega preverjanja.
- Preveri lokalni CyberChef in zapiši način zagona oziroma naslov na tablo. Za rezervni niz `dWNlbmVjOnVjbm8=` je rezultat `ucenec:ucno`.
- Greenbone namesti in posodobi pred dogodkom. Preglej izbrano tarčo ter pripravi poročilo z dokazom zaznave, resnostjo, Quality of Detection in predlogom odprave. Izvozi rezervno poročilo. Hkratnih pregledov vseh udeležencev ne načrtuj.
- Za vajo 2.3 pripravi izsek Apachejevega obvestila o CVE-2021-41773 in nedestruktivno zahtevo do `/etc/hostname`. Potrdi njen obseg pred izvedbo. Privzeta konfiguracija www zavrača dostop zunaj DocumentRoot; uspešna izraba ni pričakovani cilj.
- Preveri SSH od trenutnega Kali do starega strežnika in pripravi preverjen prstni odtis ključa za udeležence. Morebitno izjemo združljivosti omeji na to tarčo in posamezen ukaz; ne spreminjaj globalnih nastavitev.
- Uskladi predhodna navodila NAVODILO.md pred pošiljanjem: trenutni dokument še zahteva lokalni Kali.

## Potek scenarijev

Vsi časi so od začetka praktičnega bloka, po 36 minutah predstavitve.

| Čas | Scenarij | Dejavnost |
| --- | --- | --- |
| 0–30 min | internet | prvi krog |
| 30–40 min | internet | javni pregled in priprava drugega kroga |
| 40–50 min | visitor | prva notranja meritev |
| 50–60 min | flat | primerjalna meritev |
| 60–65 min | visitor | primerjava in ukrepi |
| 65–100 min | visitor | tretji krog |
| 100–104 min | visitor | dokončanje zapisov in rezerva |
| 104–114 min | visitor | skupni pogovor |

Preklop: `./infra/lab.sh scenario internet|visitor|flat`. Vsak preklop jasno napovej in preveri stanje. Že odprte povezave se lahko ohranijo; uporabljaj nove preglede. Ne izvajaj ponastavitve med delom udeležencev.

## Pričakovani izidi

| Vaja | Dokaz uspeha in omejitve |
| --- | --- |
| 1.1 | Udeleženec navede vir, čas in opažene storitve. Organizacija/geolokacija sta podatka ponudnika; trenutna dosegljivost ni preverjena. |
| 1.2 | Komentar in robots.txt vodita do `/backup/config.php.bak`. Kopija razkriva uporabnika, geslo in notranje ime. Robots.txt ne ščiti dostopa. |
| 1.3 | AXFR razkrije tudi LAN in IoT. Poznavanje notranjih imen in IP ne zagotavlja dostopa. |
| 2.1 | www in shop HTTP, mail poštna vrata, ns1 DNS, vpn SSH; dejanski odprti porti veljajo več kot načrt objav NAT. |
| 2.2 | SMB na files je v visitor dosegljiv, IoT storitve postanejo dosegljive v flat. Primerjaj odprta vrata, ne le odkritih gostiteljev. |
| 2.3 | Različica Apache 2.4.49 je namig. Privzeta omejitev dostopa izven DocumentRoot preprečuje pričakovano pot izrabe. Neuspeh enega testa ni dokaz odsotnosti vseh ranljivosti. |
| 3.1 | Zahteva z iskalnim nizom, metoda, pot in status. Ne predpisuj piškotkov ali poti API brez predhodnega preverjanja dejanske različice. |
| 3.2 | Authorization Basic se dekodira v učna podatka zaposleni:acme123. HTTP nima TLS; lastna orodja brskalnika vidijo podatke tudi pri HTTPS. |
| 3.3 | Najdeno geslo za peter.horvat deluje na SSH. Minimalen dokaz whoami/hostname, nato odjava. To ne dokazuje višjih pravic ali dosegljivosti IoT. |

Pri ocenjevanju šteje jasen zapis dokazov, omejitev in ukrepa. Udeleženec lahko dobro reši presojo tudi brez uspešne izrabe. Gesel in sejnih žetonov ne projiciraj ali vključuj v skupne zapiske.
