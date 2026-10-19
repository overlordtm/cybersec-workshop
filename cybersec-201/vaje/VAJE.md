# Cybersec-201: praktične vaje

[Prosojnice](../) · **Vse vaje izvajamo po predstavitvi vseh treh sklopov.**

ACME nas prosi za pregled izpostavljenosti. V vsakem krogu izberi **eno raven**: lahko za prvi stik, srednjo za nekaj izkušenj ali zahtevno za poznavalce. Če končaš prej, nadaljuj z drugo ravnjo istega sklopa. Ni treba rešiti vseh devetih vaj.

| Krog | Čas | Omrežni scenarij |
| --- | --- | --- |
| 1. Digitalne sledi | 30 minut | internet |
| 2. Omrežje in segmentacija | 35 minut | skupni prehodi po navodilu izvajalca |
| 3. Zahteve in preverjanje | 35 minut | visitor |

Štiri minute namenimo dokončanju zapisov in deset minut skupnemu pogovoru. Scenarija ne spreminjaš sam; izvajalec ga preklopi za vse hkrati.

**Dostop:** s svojo osebno kodo odpri [prevzem dostopa](./dostop/). Tam dobiš prijavo v Kali prek brskalnika ali WireGuard konfiguracijo za svojo Kali VM in navodila za povezavo. Pri dostopu prek brskalnika se Kali odpre kot oddaljeno namizje. Za terminal poišči aplikacijo Terminal, za splet Firefox. Ukaze kopiraj po eno vrstico; besedila v oglatih oklepajih zamenjaj s svojim podatkom.

Aktivno preverjamo samo spodaj navedene učne tarče ACME. Shodan uporabljamo za pregled že zbranih podatkov o IP, ki ga določi izvajalec. Skupnih gesel, datotek in nastavitev ne spreminjamo. Če rezultat odstopa od navodil, ga zapiši in pokliči izvajalca.

**Pri vsaki vaji zapiši:** opažanje, dokaz in čas, omejitev sklepa, možen vpliv ter en ukrep. Razkritih gesel in vrednosti sej ne vključuj v skupni zapis.

## Vaja 1.1: Kaj o naslovu ve Shodan? — lahka

**Potrebuješ:** svoj običajni brskalnik in resničen javni IP, ki ga poda izvajalec. Simulirani naslovi ACME `198.51.100.x` za to vajo niso primerni.

1. Odpri [Shodan](https://www.shodan.io/) in poišči dodeljeni IP. Če iskanje omejuje dostop, uporabi posnetek rezultata, ki ga pripravi izvajalec; registracija ali nakup nista del vaje.
2. Poišči zapisano organizacijo in geografsko lokacijo. Manjkajoče podatke označi kot manjkajoče.
3. Zapiši dve opaženi storitvi oziroma vsa opažanja, če jih je manj. Poišči čas zadnjega opažanja pri posamezni storitvi.
4. Loči trditev »Shodan je takrat zaznal storitev« od trditve »storitev je zdaj dosegljiva«.
5. Zapiši eno ugotovitev, ki jo rezultat podpira, in eno, za katero dokaz ne zadostuje.

**Cilj:** kratek profil IP z virom in časom. Geolokacija ni dokaz fizične lokacije, oznaka ranljivosti pa ni potrditev uspešne izrabe. Na izbrani javni IP ne pošiljaj lastnih pregledov ali prijav.

## Vaja 1.2: Sledi pozabljeni varnostni kopiji — srednja

**Tarča:** `http://www.acme.lab/` v Firefoxu znotraj Kali. Deluje v scenariju `internet`.

1. Preglej spletno stran in izpiši javno navedena imena, kontakte ter povezane storitve.
2. Odpri izvorno kodo strani (`Ctrl+U`). Poišči komentar, ki namiguje na neobjavljene poti.
3. Odpri `/robots.txt` na isti spletni strani. Kaj razkriva? Ali preprečuje odpiranje navedenih poti?
4. Sledi namigom do varnostne kopije. Če pot nima seznama datotek, poskusi ime `config.php.bak` v imeniku, omenjenem v namigu.
5. Zapiši vrste razkritih podatkov in izvor vsakega. V skupni zapis ne prepisuj gesla.
6. Predlagaj takojšen ukrep in pojasni, zakaj samo odstranitev datoteke morda ne zadošča.

**Cilj:** dokaz javno dostopne kopije in razlaga posledic. Pri tej vaji ne preverjamo prijave z najdenimi podatki.

## Vaja 1.3: DNS razkriva več, kot pričakujemo — zahtevna

**Tarča:** območje `acme.lab` na učnem strežniku DNS `198.51.100.14`. Uporabi terminal Kali.

1. Preglej običajne zapise:

```sh
dig @198.51.100.14 acme.lab SOA
dig @198.51.100.14 acme.lab MX
dig @198.51.100.14 www.acme.lab A
```

2. Preveri, ali strežnik dovoli prenos območja:

```sh
dig @198.51.100.14 acme.lab AXFR
```

3. Iz rezultatov sestavi seznam javnih in notranjih gostiteljev. Razvrsti jih po domnevni vlogi in označi, kaj sklepaš samo iz imena.
4. Izberi notranjo napravo ter pojasni, ali zapis DNS dokazuje obstoj, trenutno delovanje ali dosegljivost njene storitve.
5. Predlagaj omejitev prenosov območja in ločevanje notranjih ter zunanjih podatkov DNS.

**Cilj:** zemljevid z viri in omejitvami, ne le izpis ukaza. Prenos območja je neposredna poizvedba učnemu strežniku; ta postopek uporabljamo samo na navedeni tarči.

## Vaja 2.1: Prepoznaj javne storitve — lahka

**Scenarij:** začetek drugega kroga, `internet`. **Tarče:** samo pet učnih javnih naslovov `.11–.15`.

V terminal prilepi:

```sh
nmap -Pn -sT --open -p 22,25,53,80,110,143,443,587,993 198.51.100.11-15
```

`-Pn` preskoči predhodno odkrivanje gostitelja, `-sT` preveri povezavo TCP, `--open` prikaže odprta vrata, `-p` omeji seznam vrat. Pregled lahko traja nekaj časa; pusti ga dokončati.

1. Za najmanj tri naslove zapiši odprta vrata.
2. Poveži vrata z verjetno storitvijo: 22 SSH, 25/587 pošta SMTP, 53 DNS, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 993 IMAPS.
3. V Firefoxu odpri `http://www.acme.lab/` in `http://shop.acme.lab/`. Primerjaj z rezultati pregleda.
4. Zapiši, zakaj znana številka vrat še ni dokaz dejanskega programa in zakaj zaprta ali filtrirana vrata ne pomenijo, da naprave ni.

**Cilj:** tabela naslov → odprta vrata → verjetna vloga. Ne pričakuj, da je vsaka objavljena številka vrat tudi odprta; za njo mora delovati storitev.

## Vaja 2.2: Kaj spremeni segmentacija? — srednja

**Scenarija:** `visitor` in `flat`, ki ju preklopi izvajalec. Začni ob napovedi `visitor` in pred preklopom shrani rezultat.

1. Izvedi enak omejen pregled v obeh scenarijih:

```sh
nmap -Pn -sT --open -p 80,445,502,554,9100 172.20.20.10 172.20.30.10-12
```

2. Pripravi tabelo naslov → vrata v `visitor` → vrata v `flat`.
3. Pred preklopom napovej, katere storitve bodo postale dosegljive. Po napovedi izvajalca za `flat` ponovi ukaz.
4. Prepoznaj datotečni strežnik, kamero, tiskalnik in krmilnik klime. Namigi: SMB 445, RTSP 554, tiskanje 9100, Modbus 502.
5. Predlagaj pravilo za promet obiskovalcev do IoT. Zapiši tudi morebitno upravičeno izjemo za skrbništvo.

**Cilj:** primerjava dosegljivih storitev in utemeljeno pravilo. Odkrivanje gostiteljev samo zase ni dovolj. Ne spreminjaj nastavitev naprav in ne pošiljaj ukazov Modbus ali tiskalnih opravil.

Če končaš prej, razmisli, zakaj ločen VLAN brez omejitev prometa ne doseže istega cilja. Ob koncu izvajalec vrne `visitor`; nove meritve opravi z novimi povezavami.

## Vaja 2.3: Ali različica dokazuje ranljivost? — zahtevna

**Tarča:** samo `198.51.100.11:80`. Deluje v vseh treh scenarijih.

1. Zberi osnovna dokaza:

```sh
nmap -Pn -sT -sV -p 80 198.51.100.11
curl -I http://198.51.100.11/
```

2. V [Apachejevem varnostnem obvestilu](https://httpd.apache.org/security/vulnerabilities_24.html) poišči CVE-2021-41773. Ob nedostopnosti uporabi izsek, ki ga pripravi izvajalec.
3. Izpiši prizadeto različico, pogoje za dostop zunaj korenskega imenika in dodatne pogoje za izvajanje ukazov.
4. Sestavi največ eno nedestruktivno preverjanje dostopa do `/etc/hostname` na učni tarči. Pred izvedbo pokaži zahtevo izvajalcu, da potrdi omejitev poti. Ne preverjaj gesel, zasebnih ključev ali izvajanja ukazov.
5. Primerjaj odziv s pogoji obvestila. Če preverjanja ne izvedeš, jasno napiši »ujemanje različice; izraba ni preverjena«.
6. Če je na voljo izsek Greenbone, primerjaj njegovo dokazilo s svojim. Kaj je neposredno izmerjeno in kaj sklep iz različice?

**Cilj:** razvrsti ugotovitev kot sum na podlagi različice, potrjeno vedenje ali nepotrjen poskus. Neuspel poskus sam zase ne dokazuje, da je strežnik v celoti varen.

## Vaja 3.1: Preberi svojo spletno zahtevo — lahka

**Tarča:** `http://shop.acme.lab/` v Firefoxu na Kali. **Scenarij:** `visitor`.

1. Odpri trgovino in s tipko `F12` odpri razvijalska orodja. Izberi zavihek Omrežje oziroma Network.
2. Osveži stran, nato v trgovini poišči izdelek z izmišljenim iskalnim nizom `jabolko`.
3. Poišči zahtevo, ki vsebuje tvoj niz. Če je seznam nepregleden, ga počisti in iskanje ponovi.
4. Zapiši metodo, pot, status odgovora in mesto, kamor je brskalnik poslal niz: naslov, glave ali telo.
5. Preglej eno glavo zahteve in eno glavo odgovora ter s svojimi besedami opiši namen.
6. Po želji v shrambi brskalnika poišči piškotek in njegove zastavice. Če piškotka ni, zapiši to opažanje; ne predpostavljaj, da vsaka prijava uporablja piškotek.

**Cilj:** znaš pokazati zahtevo, ki jo je sprožilo tvoje dejanje. Ne ustvarjaj skupnih uporabniških računov in ne spreminjaj izdelkov ali naročil.

## Vaja 3.2: Base64 ne skrije prijave — srednja

**Tarča:** `http://intranet.acme.lab/`. **Scenarij:** `visitor`. Uporabi samo učna podatka: uporabnik `zaposleni`, geslo `acme123`.

1. Odpri razvijalska orodja Firefox → Omrežje. Nato odpri intranet in se prijavi z učnima podatkoma. Če se pogovorno okno ne pojavi, si morda že prijavljen; osveži stran in preglej novo zahtevo.
2. V lastni zahtevi poišči glavo `Authorization` s predpono `Basic`. Preglej glave v surovi obliki, če jih vmesnik skrije.
3. V lokalnem CyberChef v Kali uporabi operacijo `From Base64` na delu za besedo `Basic`. Če orodja ne najdeš, prosi izvajalca za lokalni naslov.
4. Primerjaj rezultat z učnima podatkoma. Zakaj napadalec za dekodiranje ne potrebuje skrivnega ključa?
5. Zapiši razliko med ogledom lastne zahteve v brskalniku in možnostjo opazovanja prometa med prenosom.
6. Predlagaj zaščito prenosa in pojasni, kaj bi razvijalska orodja še vedno pokazala tudi pri HTTPS.

**Rezervni učni niz:** `dWNlbmVjOnVjbm8=`. Če uporabiš samo ta niz, to označi; ni dokaz zajema prijave v intranet.

**Cilj:** razložiš razliko med kodiranjem in šifriranjem. Uporabljaj samo pripravljene izmišljene podatke, brez nalaganja resničnih poverilnic v spletna orodja.

## Vaja 3.3: Od razkritja do dostopa SSH — zahtevna

**Tarči:** `http://www.acme.lab/` in `vpn.acme.lab:22`. **Scenarij:** `visitor`; naloga ne zahteva rezultatov prejšnjih vaj.

ACME je v navodilih za oddaljeni dostop navedel obliko uporabniških imen `ime.priimek`. Za ta primer je uporabnik `peter.horvat`. Ne preizkušaj drugih računov ali seznamov gesel.

1. Na spletni strani samostojno razišči izvorno kodo, `robots.txt` in navedeno varnostno kopijo. Po potrebi uporabi namig: `/backup/config.php.bak`.
2. Zapiši hipotezo, zakaj bi bila razkrita poverilnica lahko uporabna še drugje. Pred preverjanjem loči hipotezo od dokaza.
3. Preveri eno prijavo v določen učni račun:

```sh
ssh peter.horvat@vpn.acme.lab
```

4. Geslo vnesi ob pozivu, ne v ukazno vrstico. Ob prvem povezovanju primerjaj prstni odtis z odtisom, ki ga poda izvajalec. Ob opozorilu o spremenjenem ključu se ustavi in ga vprašaj.
5. Za minimalen dokaz izvedi samo:

```sh
whoami
hostname
exit
```

6. Opiši verigo dokazov, neposreden vpliv in vsaj dva ukrepa: odstranitev razkritja, preklic oziroma menjava poverilnice, ločena gesla ali sprememba načina prijave.

**Cilj:** potrjen ali jasno omejen sklep o ponovni uporabi poverilnice. Ne nameščaj orodij, ne dviguj pravic, ne pregleduj tujih datotek in ne nadaljuj v druge segmente. Če stari SSH ni združljiv z odjemalcem, pokliči izvajalca; splošnih varnostnih nastavitev odjemalca ne izklapljaj.

## Moj zapis in skupni pogovor

| Polje | Moj zapis |
| --- | --- |
| Vaja in scenarij | |
| Opažanje | |
| Dokaz, vir in čas | |
| Kaj ostaja nepotrjeno | |
| Možen vpliv | |
| Predlagan ukrep | |
| Kako preverimo izboljšavo | |

Izberi eno ugotovitev za skupni pogovor. Kateri trije ukrepi bi ACME najbolj pomagali? Kaj bi morali dodatno preveriti, preden bi trdili, da je neka storitev ranljiva?
