# Cybersec-201: praktične vaje

[Prosojnice](../) · [Prevzem dostopa](./dostop/)

ACME je izmišljeno podjetje s pripravljenimi učnimi tarčami. Po predstavitvi sledijo trije praktični krogi. V vsakem izberi eno od vaj 1–3 glede na svoje izkušnje. Če končaš prej, nadaljuj z drugo vajo ali dodatnim izzivom 4–5. **Ni treba rešiti vseh petnajstih vaj.**

| Sklop | Čas | Vaje |
| --- | --- | --- |
| 1. Digitalne sledi | 25 minut | 1.1–1.3 in dva dodatna izziva |
| 2. Omrežja | 40 minut | 2.1–2.3 in dva dodatna izziva |
| 3. Aplikacije | 40 minut | 3.1–3.3 in dva dodatna izziva |

Sledi deset minut skupnega pogovora. **Celoten praktični blok poteka v scenariju `visitor`.** Scenarij nastavi izvajalec pred začetkom; pri vajah ni treba čakati na preklop omrežja. Javni naslovi ACME so simulirani in delujejo samo v laboratoriju.

**Dostop:** s svojo osebno kodo odpri [prevzem dostopa](./dostop/). Uporabi pripravljeni Kali v brskalniku ali svoj Kali s povezavo WireGuard. V Kali odpri Firefox za splet in Terminal za ukaze. Javne iskalnike uporabljaj v svojem običajnem brskalniku.

Vsaka vaja najprej pokaže nalogo. Če potrebuješ pomoč, izberi **Prikaži namig**. Nato lahko z gumbom **Pokaži postopek** odpreš predlagane korake, ukaze in razlago rezultata. Pomoč se odpira za vsako vajo posebej.

Aktivno preverjamo samo navedene tarče ACME. Skupnih datotek, gesel in nastavitev ne spreminjamo. Za Shodan in javne certifikate pregledujemo že zbrane podatke; odkritih javnih naslovov ne pregledujemo z Nmap.

**Zapiši:** opažanje, dokaz in čas, omejitev sklepa, možen vpliv ter predlagan ukrep. Gesel in prijavnih žetonov ne vključuj v skupni zapis. Pri rezultatih loči dejansko meritev od pripravljenega primera. Ukaze kopiraj po eno vrstico; besedila v oglatih oklepajih zamenjaj z ustreznimi podatki.

## Vaja 1.1: Kaj o naslovu ve Shodan? — lahka

**Potrebuješ:** običajni brskalnik in resničen javni IP po želji.

V Shodanu poišči organizacijo, lokacijo in zaznane storitve izbranega naslova. Zapiši čas opažanja ter eno trditev, ki jo rezultat podpira, in eno, ki je ne moreš potrditi.

**Cilj:** kratek profil naslova z virom in časom.

### Namig

Pri vsaki storitvi poišči vrata, opis odziva in datum. Lokacija je podatek ponudnika; zapis storitve opisuje preteklo opažanje.

### Postopek

1. Odpri [Shodan](https://www.shodan.io/) in v iskalno polje vnesi IP. Naslovi ACME `198.51.100.x` niso primerni za javno iskanje.
2. Zapiši organizacijo in državo oziroma kraj. Manjkajoče podatke označi kot manjkajoče.
3. Izberi dve storitvi oziroma vse prikazane, če jih je manj. Zapiši vrata, opis in čas opažanja vsake storitve.
4. Sestavi ugotovitev: »Shodan je dne [datum] na [IP:vrata] zaznal [storitev].«
5. Dodaj omejitev: »Trenutne dosegljivosti nisem preveril; navedena lokacija ni dokaz fizične lokacije naprave.«

Če dostop omejuje račun ali naročnina, uporabi datiran posnetek izvajalca. Registracija in nakup nista del naloge. Oznaka CVE v zadetku sama ne dokazuje uspešne izrabe.

## Vaja 1.2: Sledi pozabljeni varnostni kopiji — srednja

**Tarča:** `http://www.acme.lab/` v Firefoxu na Kali.

Razišči stran, izvorno kodo in namige za iskalnike. Poišči datoteko, ki razkriva podatke za notranjo uporabo. Opiši posledice in potrebne ukrepe; pri tej vaji ne preverjaj prijave z najdenimi podatki.

**Cilj:** dokaz javno dostopne varnostne kopije.

### Namig

Poglej komentarje v izvorni kodi (`Ctrl+U`) in datoteko `robots.txt`. Prepoved indeksiranja ne prepreči dostopa. Če imenik nima seznama datotek, to še ne pomeni, da je prazen.

### Postopek

1. Odpri domačo stran in stran »O nas«. Zapiši javno navedene osebe, vloge in povezane storitve.
2. Z `Ctrl+U` odpri izvorno kodo. Komentar omenja poti `/admin/` in `/backup/`.
3. Odpri `http://www.acme.lab/robots.txt`. Tudi tam je navedena pot `/backup/`.
4. Odpri `http://www.acme.lab/backup/config.php.bak`. Po želji isto zahtevo izvedi v terminalu:

```sh
curl --noproxy '*' -sS http://www.acme.lab/backup/config.php.bak
```

5. Prepoznaj vrste razkritih podatkov: notranje ime, uporabniško ime in geslo. V skupni zapis ne prepisuj vrednosti gesla.
6. Predlagaj odstranitev kopije iz spletnega imenika, menjavo razkritega gesla in preverjanje njegove ponovne uporabe.

**Pričakovano:** strežnik vrne vsebino kopije. Samo dodajanje poti v `robots.txt` podatkov ne zaščiti.

## Vaja 1.3: DNS razkriva več, kot pričakujemo — zahtevna

**Tarča:** območje `acme.lab` na strežniku DNS `198.51.100.14`.

Preglej običajne zapise DNS in preveri, ali lahko preneseš celotno območje. Iz rezultatov sestavi seznam javnih in notranjih gostiteljev ter predlagaj popravek nastavitev.

**Cilj:** zemljevid infrastrukture z razlago izvora podatkov in omejitev.

### Namig

Uporabi `dig` in izrecno izberi strežnik z `@`. SOA in MX pokažeta osnovne podatke; AXFR zahteva prenos območja. Notranji naslov v DNS še ne pove, ali lahko dosežeš storitev.

### Postopek

1. Preglej osnovne zapise:

```sh
dig @198.51.100.14 acme.lab SOA
dig @198.51.100.14 acme.lab MX
dig @198.51.100.14 www.acme.lab A
```

2. Zahtevaj prenos območja:

```sh
dig @198.51.100.14 acme.lab AXFR
```

3. V izpisu loči simulirane javne naslove `198.51.100.x` od notranjih naslovov `172.20.x.x`.
4. Poišči imena za datotečni strežnik, intranet in IoT. Vlogo, sklepano samo iz imena, označi kot domnevo.
5. Zapiši dokaz: strežnik je našemu odjemalcu vrnil celotno območje z notranjimi imeni. Predlagaj omejitev prenosov na ustrezne strežnike in ločitev notranjih ter zunanjih podatkov.

**Pričakovano:** AXFR je dovoljen. To je neposredna poizvedba učnemu strežniku, ne pasivno iskanje v javnem indeksu.

## Vaja 1.4: Kaj razkrije dokument? — dodatni izziv

**Tarča:** PDF `http://www.acme.lab/dokumenti/cenik-2026.pdf`.

**Orodje:** ExifTool v Kali.

Preglej metapodatke dokumenta in jih poveži s podatki o ekipi ACME. Loči informacije, vidne na strani dokumenta, od njegovih skritih lastnosti.

**Cilj:** prepoznaš nenamerna razkritja v dokumentih in pojasniš zanesljivost sklepa o avtorju.

### Namig

Poišči polja za avtorja, naslov, program in datum. Ime v metapodatkih lahko izvira iz predloge dokumenta; ni nujno ime osebe, ki je dokument objavila.

### Postopek

1. Prenesi dokument in preglej metapodatke:

```sh
curl --noproxy '*' -fS -o /tmp/acme-cenik-2026.pdf http://www.acme.lab/dokumenti/cenik-2026.pdf
exiftool /tmp/acme-cenik-2026.pdf
```

2. Omeji izpis na zanimiva polja:

```sh
exiftool -Title -Author -Creator -Producer -CreateDate /tmp/acme-cenik-2026.pdf
```

3. Primerjaj avtorja »Maja Kovac« z osebo Maja Kovač na strani `http://www.acme.lab/o-nas.html`.
4. Zapiši ločeno: »PDF vsebuje navedbo avtorja« in »podatek je skladen z javno predstavljeno zaposleno«. Avtorstva s tem še nisi dokazal.
5. Predlagaj pregled in čiščenje metapodatkov pred objavo. Samo preimenovanje datoteke metapodatkov ne odstrani.

**Pričakovano:** pripravljeni dokument vsebuje učne metapodatke o avtorju in uporabljeni programski opremi.

## Vaja 1.5: Poddomene iz javnih certifikatov — dodatni izziv

**Potrebuješ:** običajni brskalnik in resnično domeno.

Iz javnih dnevnikov certifikatov sestavi seznam imen, ki bi lahko pripadala storitvam izbrane organizacije. Razvrsti jih po domnevnem namenu in označi zgodovinske podatke.

**Cilj:** odkriješ dodatne sledi brez aktivnega pregledovanja strežnikov.

### Namig

Pri iskanju v dnevnikih certifikatov vključi tudi poddomene. Certifikat lahko navaja več imen in je lahko že potekel. Nadomestni zapis `*.domena` ni seznam vseh dejanskih poddomen.

### Postopek

1. V običajnem brskalniku odpri [ctlogs.dev](https://ctlogs.dev/subdomains) in izberi iskanje poddomen (*subdomain finder*).
2. Vnesi dodeljeno domeno, na primer `izbrana-domena.si`. To je primer; nadomesti ga z domeno izvajalca. Učna domena `acme.lab` za to ni primerna.
3. Zapiši do pet različnih imen in pri vsakem datum prvega in zadnjega pojava v certifikatu (*First seen*, *Last seen*). Če jih je manj, zapiši vsa.
4. Imena razvrsti po domnevnem namenu, denimo pošta, trgovina ali razvojno okolje. Označi imena, ki se že dolgo niso pojavila v novem certifikatu.
5. Pojasni, zakaj certifikat ne potrjuje trenutne dosegljivosti, lastništva infrastrukture ali ranljivosti storitve.

Brez prijave ctlogs.dev prikaže prvih 100 imen in ne prikaže certifikatov, ki so potekli pred več kot 90 dnevi; za to vajo to zadošča. Če stran ni dosegljiva, poskusi [crt.sh](https://crt.sh/) z vzorcem `%.izbrana-domena.si` ali uporabi datiran izvoz izvajalca. Odkritih imen ne preverjaj z Nmap ali poskusi prijave.

## Vaja 2.1: Prepoznaj javne storitve — lahka

**Tarče:** samo simulirani javni naslovi ACME `198.51.100.11–15`.

**Orodje:** Nmap.

Na najmanj treh naslovih poišči odprta vrata in jih poveži z verjetnimi storitvami. Eno od spletnih storitev preveri tudi v brskalniku.

**Cilj:** tabela naslov → odprta vrata → verjetna vloga.

### Namig

Omeji naslove in seznam vrat. Pregled prisotnosti naprave ni isto kot pregled njenih storitev. Nmap lahko na podlagi številke vrat izpiše pričakovano ime storitve, ne da bi prepoznal dejanski program.

### Postopek

1. Zaženi omejen pregled TCP:

```sh
nmap -Pn -sT --open -p 22,25,53,80,110,143,443,587,993 198.51.100.11-15
```

2. Zapiši odprta vrata vsaj treh naslovov. `-Pn` preskoči odkrivanje prisotnosti, `-sT` preveri povezavo TCP, `--open` izbere odprta vrata in `-p` določi seznam vrat.
3. Poveži običajna vrata s storitvami: 22 SSH, 25/587 SMTP, 53 DNS, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS in 993 IMAPS.
4. V Firefoxu odpri `http://www.acme.lab/` in `http://shop.acme.lab/` ter primerjaj rezultat s pregledom.
5. Zapiši omejitev: ta ukaz ne pregleduje UDP in ne potrjuje ranljivosti odprtih storitev.

**Pričakovano:** na www in shop najdeš HTTP; na drugih naslovih objavljene delujoče storitve. Objavljena vrata 443 niso nujno odprta, če za njimi ne deluje storitev. Ker delamo v `visitor`, je to pregled javnih naslovov z notranjega izhodišča.

## Vaja 2.2: Kaj lahko preberemo brez prijave? — srednja

**Tarča:** `files.acme.lab` oziroma `172.20.20.10`. **Orodje:** `smbclient`.

Poišči deljene mape, preveri dostop brez prijave in preberi eno pripravljeno datoteko. Primerjaj dostop do map `javno` in `uprava`.

**Cilj:** ločiš vidnost imena mape od pravice do branja njene vsebine.

### Namig

Pri `smbclient` možnost `-L` izpiše mape, `-N` pa preskoči poziv za geslo. Izpis imena `uprava` še ne pomeni, da lahko odpreš njeno vsebino.

### Postopek

1. Izpiši deljene mape:

```sh
smbclient -N -L //172.20.20.10
```

2. Preveri seznam datotek in preberi pripravljeni seznam naprav:

```sh
smbclient -N //172.20.20.10/javno -c 'ls'
smbclient -N //172.20.20.10/javno -c 'get seznam-naprav.csv /tmp/acme-seznam-naprav.csv'
cat /tmp/acme-seznam-naprav.csv
```

3. Preveri razliko pri zaščiteni mapi:

```sh
smbclient -N //172.20.20.10/uprava -c 'ls'
```

4. Zapiši, katere informacije o notranjih napravah si lahko prebral brez uporabniške prijave. Predlagaj omejitev gostujočega dostopa in pregled vsebine deljenih map.

**Pričakovano:** mapa `javno` dovoli branje, `uprava` pa gostujoči dostop zavrne. Datoteko shraniš samo na svoj Kali. Morebitno opozorilo o starejšem protokolu pri prikazu delovne skupine presojaj ločeno od uspešnega izpisa map.

## Vaja 2.3: Ali različica dokazuje ranljivost? — zahtevna

**Tarča:** samo `198.51.100.11:80`, spletni strežnik ACME.

Ugotovi različico spletnega strežnika in pogoje za CVE-2021-41773. Preveri, ali zbrani dokazi upravičujejo trditev o uspešni izrabi.

**Cilj:** ločiš prizadeto različico od potrjenega vedenja konkretne namestitve.

### Namig

Primerjaj odziv storitve z Apachejevim obvestilom. Za dostop zunaj spletnega imenika so pomembna dovoljenja; za izvajanje ukazov so potrebni še dodatni pogoji.

### Postopek

1. Zberi podatke o različici:

```sh
nmap -Pn -sT -sV -p 80 198.51.100.11
curl --noproxy '*' -I http://198.51.100.11/
```

2. V [Apachejevem varnostnem obvestilu](https://httpd.apache.org/security/vulnerabilities_24.html) poišči CVE-2021-41773. Izpiši prizadeto različico 2.4.49, pogoj glede dovoljenj zunaj spletnega imenika in dodatni pogoj CGI za izvajanje ukazov. Ob nedostopnosti uporabi izsek izvajalca.
3. Na tej učni tarči lahko izvedeš en omejen preizkus poti do nenevarne datoteke `/etc/hostname`:

```sh
curl --noproxy '*' --path-as-is -i 'http://198.51.100.11/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/hostname'
```

4. Zapiši status in dejansko vsebino odgovora. Napaka ali zavrnitev ni prebrana datoteka. Drugih poti ne preizkušaj.
5. Sklep oblikuj glede na dokaze: »Zaznana je prizadeta različica; izraba s tem preizkusom ni potrjena.« Če preizkusa ne izvedeš, napiši »izraba ni preverjena«.

**Pričakovano:** privzeta konfiguracija učnega strežnika Apache preprečuje opisani dostop zunaj spletnega imenika. Negativen preizkus ne dokazuje, da strežnik nima drugih ranljivosti. Ukrep ostaja nadgradnja na podprto različico in pregled nastavitev.

## Vaja 2.4: Nmap zna več kot poiskati vrata — dodatni izziv

**Tarča:** Metasploitable 2, `172.20.20.30`. **Orodje:** Nmap s skriptami NSE.

Primerjaj prepoznavo storitve s preverjanjem njene nastavitve. Preveri anonimni dostop FTP in različice protokola SMB.

**Cilj:** ugotovitev podpreš z odzivom storitve, ne samo z oznako različice.

### Namig

Uporabi poimenovani skripti `ftp-anon` in `smb-protocols`. Prva preveri anonimno prijavo, druga pa podprte različice protokola SMB. Odsotnost izpisa skripte sama ne pomeni uspešno opravljenega negativnega testa.

### Postopek

1. Najprej prepoznaj storitve na izbranih vratih:

```sh
nmap -Pn -sT -sV -p 21,139,445 172.20.20.30
```

2. Preveri anonimno prijavo FTP:

```sh
nmap -Pn -sT -p 21 --script ftp-anon 172.20.20.30
```

3. Preveri podprte različice SMB:

```sh
nmap -Pn -sT -p 139,445 --script smb-protocols 172.20.20.30
```

4. Pri FTP zapiši, ali je anonimna prijava dovoljena. Pri SMB poišči starejši protokol, denimo `NT LM 0.12` oziroma SMBv1. Zapiši dejanski izpis, tudi če odstopa od pričakovanja.
5. Pojasni razliko med »vrata 21 so odprta«, »strežnik uporablja določeno različico programa« in »strežnik dovoli anonimno prijavo«. Predlagaj odstranitev nepotrebnega dostopa in zastarelih protokolov.

Za razlago izpisov sta na voljo dokumentaciji [ftp-anon](https://nmap.org/nsedoc/scripts/ftp-anon.html) in [smb-protocols](https://nmap.org/nsedoc/scripts/smb-protocols.html). Na skupni tarči ne zapisuj datotek in ne zaganjaj celotne zbirke skript.

## Vaja 2.5: Ali ugotovitev pregledovalnika drži? — dodatni izziv

**Potrebuješ:** končano poročilo Greenbone oziroma njegov izsek, ki ga pripravi izvajalec. **Tarče za preverjanje:** samo storitve ACME, navedene v izbrani ugotovitvi.

Izberi eno ugotovitev ter jo preveri z drugim orodjem. Opiši dokaz, pogoje, vpliv in ukrep. Med vajo ne zaganjaj novega pregleda Greenbone.

**Cilj:** presodiš, koliko ugotovitev pregledovalnika dejansko dokazuje.

### Namig

Poišči naslov tarče, vrata, opis zaznave in dokaz. Nato preveri, ali ugotovitev temelji na različici ali na neposrednem odzivu. Ocena resnosti in Quality of Detection odgovarjata na različni vprašanji.

### Postopek

1. V poročilu izberi eno ugotovitev, ki jo izvajalec označi za to vajo. Zapiši naslov, vrata, zaznano težavo in način zaznave.
2. Pri sumu na ranljivost strežnika Apache ponovi prepoznavo različice:

```sh
nmap -Pn -sT -sV -p 80 198.51.100.11
curl --noproxy '*' -I http://198.51.100.11/
```

3. Če je izbrana ugotovitev dovoljen prenos območja DNS, preveri neposredno vedenje:

```sh
dig @198.51.100.14 acme.lab AXFR
```

4. Primerjaj svoj rezultat z dokazom iz poročila. Pri Apacheju je ujemanje različice namig; pri uspešnem AXFR je vrnjeno območje neposreden dokaz nastavitve.
5. Zapiši vpliv in ukrep ter pojasni, s katerim preverjanjem bi po popravku potrdil izboljšavo. Ne izmišljaj številčne ocene resnosti ali zanesljivosti, če v izseku ni navedena.

**Če dejansko poročilo ni na voljo:** uporabi učni primer »Pregledovalnik je na `198.51.100.11:80` iz odziva zaznal Apache 2.4.49 in navedel CVE-2021-41773«. To je ponazoritev za presojo, ne rezultat izvedenega pregleda. V zapisu izrecno označi, da si preverjal učni primer.

## Vaja 3.1: Preberi svojo spletno zahtevo — lahka

**Tarča:** `http://shop.acme.lab/` v Firefoxu na Kali.

V trgovini poišči izdelek in ugotovi, katera zahteva je prenesla tvoj iskalni niz. Prepoznaj metodo, pot, podatke in odgovor.

**Cilj:** pokažeš povezavo med svojim dejanjem in konkretno zahtevo HTTP.

### Namig

Odpri razvijalska orodja pred iskanjem. V zavihku Omrežje oziroma Network počisti seznam in poišči niz, ki si ga vnesel. Za iskanje izberi kratek izmišljen izraz, denimo `jabolko`.

### Postopek

1. Odpri trgovino, pritisni `F12` in izberi Omrežje oziroma Network.
2. Počisti seznam zahtev in v trgovini poišči `jabolko`.
3. Poišči zahtevo do `/rest/products/search` z iskalnim parametrom `q`. Izberi jo in preglej URL ter glave.
4. Zapiši metodo `GET`, pot, parameter in status odgovora. Poglej tudi odgovor JSON z rezultati iskanja; prazni rezultati so še vedno veljaven odgovor.
5. Izberi po eno glavo zahteve in odgovora ter opiši njen namen. Po želji preglej shrambo brskalnika; odsotnost prijavnega piškotka ne pomeni, da aplikacija ne uporablja sej.

**Pričakovano:** prepoznaš zahtevo, ki jo sproži tvoje iskanje. Ne ustvarjaj naročil in ne spreminjaj izdelkov.

## Vaja 3.2: Base64 ne skrije prijave — srednja

**Tarča:** `http://intranet.acme.lab/`. **Učna prijava:** uporabnik `zaposleni`, geslo `acme123`.

V lastni prijavni zahtevi poišči način zapisa prijavnih podatkov in ga dekodiraj. Pojasni razliko med kodiranjem ter zaščito prenosa.

**Cilj:** razumeš, zakaj HTTP Basic brez HTTPS ne zaščiti prijavnih podatkov med prenosom.

### Namig

V glavah zahteve poišči `Authorization: Basic`. Dekodiraš samo niz za besedo `Basic`. V lokalnem CyberChefu izberi `From Base64`; uporabiš lahko tudi orodje `base64` v terminalu.

### Postopek

1. V Firefoxu odpri `F12` → Network, nato odpri intranet in vnesi pripravljena učna podatka. Če si že prijavljen, osveži stran in izberi novo zahtevo.
2. V surovih glavah zahteve poišči `Authorization: Basic …` in kopiraj samo kodirani del.
3. V CyberChefu uporabi `From Base64`. Druga možnost je ukaz, pri katerem niz prilepiš ob pozivu, da ne ostane v zgodovini ukazov:

```sh
printf 'Prilepi učni niz Base64: '
IFS= read -r acme_basic
printf '%s' "$acme_basic" | base64 --decode
unset acme_basic
```

4. Pričakovani dekodirani rezultat je `zaposleni:acme123`. Rezervni niz `dWNlbmVjOnVjbm8=` pomeni `ucenec:ucno`; če uporabiš njega, zapiši, da ni dokaz zajema intraneta.
5. Zapiši: Base64 je povratno kodiranje brez skrivnega ključa. HTTPS zaščiti prenos; lastna razvijalska orodja tudi pri HTTPS vidijo podatke pred šifriranjem.

Ogled lastne zahteve v brskalniku sam po sebi ne dokazuje prisluškovanja druge osebe. Resničnih gesel ne prenašaj v javna spletna orodja.

## Vaja 3.3: Od razkritja do dostopa SSH — zahtevna

**Tarči:** `http://www.acme.lab/` in `vpn.acme.lab:22`. **Učni račun:** `peter.horvat`.

Poišči razkrit prijavni podatek in preveri, ali je ponovno uporabljen pri oddaljenem dostopu. Zberi minimalen dokaz prijave ter se odjavi. Vajo lahko začneš brez rezultatov vaje 1.2.

**Cilj:** povežeš razkritje podatka in potrjeno ponovno uporabo gesla.

### Namig

Spletna stran vsebuje namige do varnostne kopije. ACME uporablja obliko imen `ime.priimek`; za to vajo je določen uporabnik `peter.horvat`. Podatek v kopiji še ni dokaz, da isto geslo deluje pri SSH.

### Postopek

1. Preglej izvorno kodo domače strani in `robots.txt`. Odpri `/backup/config.php.bak`; prepoznaj razkrito učno geslo.
2. Poskusi eno prijavo v določen račun:

```sh
ssh peter.horvat@vpn.acme.lab
```

3. Ob prvi povezavi primerjaj prstni odtis z odtisom izvajalca. Geslo vnesi ob pozivu.
4. Za dokaz izvedi:

```sh
whoami
hostname
exit
```

5. Zapiši, ali je prijava uspela. Če je, poveži spletno razkritje s ponovno uporabo gesla na drugi storitvi. Predlagaj odstranitev kopije, menjavo gesla ter ločene prijavne podatke oziroma ključe SSH.

**Pričakovano:** razkrito geslo omogoči prijavo učnega uporabnika. Prijava ne dokazuje skrbniških pravic ali dostopa do IoT. Po dokazu se odjavi.

## Vaja 3.4: SQL injection pri prijavi — dodatni izziv

**Tarča:** samo prijava v Juice Shop, `http://shop.acme.lab/rest/user/login`. **Orodje:** ZAP in njegov brskalnik ali terminal Kali.

Primerjaj neuspešno običajno prijavo s spremenjeno zahtevo, ki vpliva na poizvedbo SQL. Pojasni, zakaj strežnik sprejme prijavo brez pravilnega gesla.

**Cilj:** dokažeš obhod prijave in razložiš vlogo parametriziranih poizvedb.

### Namig

Prijavna zahteva pošilja JSON s poljema `email` in `password`. Narekovaj lahko zaključi niz v poizvedbi, oznaka komentarja pa izloči nadaljnji pogoj. Spremeni telo zahteve, ne prijavnega žetona.

### Postopek

1. V brskalniku, odprtem iz ZAP, poskusi prijavo z izmišljenim računom in napačnim geslom. V zgodovini poišči `POST /rest/user/login` ter odpri zahtevo za urejanje in ponovno pošiljanje. Brskalnik ZAP že uporablja njegov lokalni posrednik.
2. Shrani opažanje neuspešne prijave. Nato v telesu zahteve uporabi:

```json
{"email":"admin@juice-sh.op'-- ","password":"napacno-ucno-geslo"}
```

3. Pošlji zahtevo. Če želiš primerjavo opraviti v terminalu, najprej izvedi običajno prijavo:

```sh
curl --noproxy '*' -sS -i -H 'Content-Type: application/json' --data-binary '{"email":"neobstojeci@acme.lab","password":"napacno-ucno-geslo"}' http://shop.acme.lab/rest/user/login
```

4. Nato pošlji spremenjeno telo; vsebino med oznakama `JSON` kopiraj skupaj z ukazom:

```sh
curl --noproxy '*' -sS -i -H 'Content-Type: application/json' --data-binary @- http://shop.acme.lab/rest/user/login <<'JSON'
{"email":"admin@juice-sh.op'-- ","password":"napacno-ucno-geslo"}
JSON
```

5. Primerjaj odgovora. Pri običajni prijavi pričakujemo zavrnitev, pri spremenjeni pa odgovor z objektom `authentication`, učnim administratorskim računom v `umail` in prijavnim žetonom. Status 200 sam ne zadostuje. Žetona ne vključuj v skupni zapis in ga ne uporabljaj za spreminjanje podatkov.
6. Pojasni, da znak `'` zaključi vrednost e-poštnega naslova v sestavljeni poizvedbi, `-- ` pa preostanek spremeni v komentar. Parametrizirana poizvedba loči podatke od navodil SQL.

**Pričakovano:** obhod prijave.

## Vaja 3.5: Čigava je ta košarica? — dodatni izziv

**Tarča:** `http://shop.acme.lab/`, izziv »View Basket«.

**Potrebuješ:** učna računa A in B ter ID njunih košaric. Račune lahko narediš sam.

Preveri, ali lahko račun A prebere pripravljeno košarico računa B. Ohrani identiteto A in spremeni samo identifikator zahtevanega vira.

**Cilj:** dokažeš napako IDOR oziroma BOLA — manjkajoče preverjanje pravic do posameznega objekta.

### Namig

V zgodovini zahtev poišči `GET /rest/basket/…`. ID košarice ni nujno enak ID uporabnika. Če hkrati zamenjaš prijavni žeton z žetonom B, nisi dokazal napake pri pravicah A.

### Postopek

1. Z učnim računom A se prijavi prek brskalnika, odprtega iz ZAP, in odpri njegovo košarico. Za to vajo ne uporabljaj administratorske prijave iz vaje 3.4.
2. Poišči uspešno zahtevo `GET /rest/basket/[ID_A]` in jo odpri za ponovno pošiljanje. Zapiši vsebino košarice A.
3. Spremeni samo pot v `/rest/basket/[ID_B]`, kjer je `[ID_B]` identifikator pripravljene košarice B. Glavo `Authorization` z žetonom računa A ohrani.
4. Pošlji zahtevo in primerjaj vsebino. Poišči izdelek v košarici B. Običajni vmesnik lahko še vedno kaže košarico A; pomemben je odgovor na spremenjeno zahtevo.
5. Pomožna oblika zahteve je:

```http
GET /rest/basket/[ID_B] HTTP/1.1
Host: shop.acme.lab
Authorization: Bearer [ZETON_RACUNA_A]
```

6. Zapiši dokaz: isti račun A je prejel vsebino košarice B. Predlagaj preverjanje lastništva košarice na strežniku; skrivanje gumba v vmesniku ali težje uganljiv ID ne nadomestita preverjanja pravic.

**Pričakovano:** Juice Shop v20.3.0 vrne drugo košarico. Preveri vsebino in identiteto, ne le statusa ali skupnega obvestila o rešenem izzivu. Med vajo v košarici ničesar ne spreminjaj.

## Moj zapis in skupni pogovor

| Polje | Moj zapis |
| --- | --- |
| Vaja in čas | |
| Opažanje | |
| Dokaz, vir in izhodišče | |
| Kaj ostaja nepotrjeno | |
| Možen vpliv | |
| Predlagan ukrep | |
| Kako preverimo izboljšavo | |

Izberi eno ugotovitev za pogovor. Kateri trije ukrepi bi ACME najbolj pomagali? Kaj bi dodatno preveril pred trditvijo, da je storitev ranljiva?
