# Cybersec-201

**Uvod v kibernetske operacije za radovedne**

![Udeleženec in trije segmenti podjetja ACME](./images/acme.svg)

<small>Andraž Vrhovec · Koofr d.o.o. · oktober 2026</small>

Note:
ACME je izmišljeno podjetje s pripravljeno infrastrukturo. Današnja zgodba: poiščemo sled, preverimo dokaz in predlagamo zaščito. Uvodne štiri prosojnice skupaj pet minut.

---

## Eno podjetje, trije pogledi

<div class="cards">
<div class="card"><h3>01 · Sledi</h3><p>Kaj je že objavljeno?</p></div>
<div class="card"><h3>02 · Omrežje</h3><p>Kaj lahko dosežemo?</p></div>
<div class="card"><h3>03 · Preverjanje</h3><p>Kaj lahko dokažemo?</p></div>
</div>

**36 minut predstavitve s prikazi; preostanek za praktično delo in pogovor.**

Note:
Vse tri predstavitve pred praktičnim blokom. Prosojnic je več zaradi razdelitve pojmov, ne zaradi daljšega predavanja. Navodila za vaje so na posebni strani.

---

## Kali je že pripravljen

![Brskalnik prek Guacamole odpre pripravljeni Kali](./images/access.svg)

Firefox za splet · terminal za ukaze · orodja za preverjanje

Note:
Pokaži prijavo na https://lab.digilab-g.rtfm.si/, Firefox in terminal. Vsak ima svoje namizje. Lokalna namestitev ni pogoj; WireGuard je dodatna možnost. Javne iskalnike odpiramo v lastnem običajnem brskalniku.

---

## Dogovor o preverjanju

<div class="cards">
<div class="card"><h3>ACME</h3><p>Aktivne zahteve in pregledi samo na določenih učnih tarčah.</p></div>
<div class="card"><h3>Javni viri</h3><p>Pregled že zbranih podatkov ponudnikov.</p></div>
<div class="card"><h3>Dokazi</h3><p>Zapišemo vir, čas in meje sklepanja.</p></div>
</div>

Note:
Pojasni razliko med iskanjem že indeksiranih podatkov in aktivnim pregledom strežnika. Lab omejuje internetni promet. Ne spreminjamo skupnih gesel, datotek ali nastavitev.

---

## 1. sklop · Digitalne sledi

<p class="eyebrow">OD OBJAVE DO POVEZAVE</p>

![Spletna stran, dokument in repozitorij kot viri sledi](./images/traces.svg)

Note:
Za celoten prvi sklop osem minut. OSINT je zbiranje in povezovanje javno dostopnih informacij. Uporablja se v preiskovanju, novinarstvu in informacijski varnosti.

---

## Kaj izda spletna stran?

<div class="cards">
<div class="card"><h3>Ljudje</h3><p>Imena, kontakti in vloge v podjetju.</p></div>
<div class="card"><h3>Storitve</h3><p>Trgovina, pošta in oddaljeni dostop.</p></div>
<div class="card"><h3>Zgodovina</h3><p>Stare strani, komentarji in pozabljene datoteke.</p></div>
</div>

**Posamezna objava je košček širše slike.**

Note:
Na primeru ACME omeni javne kontakte in povezavo do trgovine. Ni treba odkrivati vseh odgovorov vaj. Spletni komentar in robots.txt nista mehanizma zaščite.

---

## Metapodatki: podatki o podatkih

<div class="example"><div class="example-label">IZMIŠLJEN PRIMER · METAPODATKI DOKUMENTA</div><pre><code>Title:    Predstavitev podjetja
Author:   Maja Kovač
Creator:  LibreOffice
Created:  2026-09-14</code></pre></div>

Fotografija lahko doda še model naprave in lokacijo GPS.

Note:
Primer je ponazoritev, ne zajem dejanske datoteke. EXIF ali metapodatki PDF lahko manjkajo, so odstranjeni ali spremenjeni. Avtor dokumenta ni avtomatično oseba, ki ga je objavila.

---

## Isto ime še ne pomeni iste osebe

![Več neodvisnih virov vodi do previdnega sklepa](./images/traces.svg)

**Preverimo čas, kontekst in neodvisno potrditev.**

Note:
Psevdonim se lahko pojavi na več družbenih omrežjih, ne da bi pripadal isti osebi. Podatki v javnem repozitoriju imajo zgodovino; odstranitev iz zadnje različice ni nujno odstranitev iz zgodovine.

---

## Iskanje z manj šuma

<div class="example"><div class="example-label">PONAZORITEV POIZVEDB · IZMIŠLJENA DOMENA</div><pre><code>site:podjetje.example
site:podjetje.example filetype:pdf
site:podjetje.example inurl:backup</code></pre></div>

Domena · vrsta datoteke · del spletnega naslova

Note:
Operatorji pomagajo omejiti rezultate. Ne zagotavljajo popolnosti ali svežine. Izmišljena domena je primer sintakse; učna domena acme.lab ni indeksirana v javnem iskalniku.

---

## Iskalniki za infrastrukturo

<div class="cards">
<div class="card"><h3><a href="https://www.shodan.io/">Shodan</a></h3><p>Išče internetno izpostavljene naprave in njihove storitve.</p></div>
<div class="card"><h3><a href="https://censys.com/">Censys</a></h3><p>Povezuje podatke o gostiteljih, spletnih storitvah in certifikatih.</p></div>
<div class="card"><h3><a href="https://securitytrails.com/">SecurityTrails</a></h3><p>Pomaga raziskovati DNS, poddomene in zgodovino infrastrukture.</p></div>
</div>

Note:
Vsako orodje predstavi z enim stavkom, brez treh dodatnih prikazov. Nekatere funkcije so odvisne od računa ali naročnine.

---

## Kako beremo zapis v Shodanu?

<div class="example"><div class="example-label">PONAZORITEV · NI ŽIV REZULTAT SHODANA</div><pre><code>IP             [izbrani javni naslov]
Organizacija   [podatek ponudnika]
80 / HTTP      [opažena storitev]
Opaženo        [datum pri storitvi]</code></pre></div>

**Čas opažanja šteje. Geolokacija je ocena.**

Note:
Na pripravljenem dejanskem zapisu lahko pokažeš iste štiri elemente. Ne uporabljaj simuliranega naslova 198.51.100.x kot živega zadetka. Oznaka CVE pri rezultatu ne potrjuje izrabe. Shodan že zbrane podatke ponudi v pregled; ne naročamo novega pregleda javne tarče.

---

## Razkritja in izpostavljeni računi

<div class="cards">
<div class="card"><h3><a href="https://dehashed.com/">DeHashed</a></h3><p>Omogoča raziskovanje razkritih identitetnih in poverilnih podatkov.</p></div>
<div class="card"><h3><a href="https://intelx.io/">IntelX</a></h3><p>Išče po indeksiranih dokumentih, arhivih in razkritjih.</p></div>
<div class="card"><h3><a href="https://haveibeenpwned.com/">Have I Been Pwned</a></h3><p>Pomaga preveriti pojav e-poštnega naslova v znanih razkritjih.</p></div>
</div>

Note:
Orodja samo omenimo. Ne odpiramo resničnih razkritih gesel in ne iščemo podatkov drugih udeležencev. Zgodovinsko razkritje ni dokaz trenutnega vdora; obseg dostopa je odvisen od ponudnika.

---

## Certifikati, povezave in zgodovina

<div class="cards">
<div class="card"><h3><a href="https://crt.sh/">crt.sh</a></h3><p>Išče domenska imena v javnih dnevnikih certifikatov.</p></div>
<div class="card"><h3><a href="https://www.virustotal.com/">VirusTotal</a></h3><p>Povezuje opažanja o datotekah, naslovih in domenah.</p></div>
<div class="card"><h3><a href="https://web.archive.org/">Wayback Machine</a></h3><p>Prikazuje arhivirane različice spletnih strani.</p></div>
</div>

Note:
Omeni, da zgodovinski certifikat ne potrjuje trenutno delujoče storitve. V javne storitve za analizo ne nalagamo zaupnih dokumentov. Arhiviran posnetek je sled preteklega stanja.

---

## Znano ime ≠ dosegljiva naprava

![Ime DNS vodi do notranjega IP; dosegljivost je ločeno vprašanje](./images/dns.svg)

**DNS razkrije naslov. Omrežje določi pot.**

Note:
Zaključi OSINT: ločimo odkrito ime, podatek o naslovu in preizkušeno storitev. Neposredno preverjanje DNS je aktivna zahteva in ga omejimo na dogovorjeno učno tarčo.

---

## 2. sklop · Od omrežja do storitve

![DMZ, LAN in IoT podjetja ACME](./images/acme.svg)

Javno objavljeno · notranje dosegljivo · ločeno z omejitvami

Note:
Dvanajst minut za drugi sklop, od tega štiri za demonstracijo Greenbone. Na shemi niso prikazane vse upravljavske naprave, temveč učni segmenti ACME.

---

## Naslov IP in podomrežje

<div class="cards">
<div class="card"><h3>198.51.100.11</h3><p>Simulirani javni naslov spletnega strežnika ACME.</p></div>
<div class="card"><h3>172.20.20.10</h3><p>Notranji naslov datotečnega strežnika.</p></div>
<div class="card"><h3>172.20.20.0/24</h3><p>Skupina naslovov pisarniškega omrežja LAN.</p></div>
</div>

**Za pot med omrežji potrebujemo usmerjanje in dovoljen promet.**

Note:
/24 poenostavljeno predstavi kot skupino naslovov z istimi prvimi tremi deli. Ne računamo mask. 198.51.100.0/24 je dokumentacijski razpon; v labu igra vlogo interneta.

---

## Vrata so vstop do storitve

![En strežnik lahko ponuja SSH, HTTP in HTTPS](./images/ports.svg)

Številka vrat je namig; odziv storitve poda več dokazov.

Note:
Shema je splošna ponazoritev, ne izpis dejanskih vrat www. Omeni še DNS 53, SMB 445 in poštne storitve. TCP in UDP sta različna načina prenosa; pregled TCP ne popiše storitev UDP.

---

## Zakaj DMZ, LAN in IoT?

<div class="cards">
<div class="card"><h3>DMZ</h3><p>Storitve, ki jih mora videti zunanji svet.</p></div>
<div class="card"><h3>LAN</h3><p>Delovne naprave, datoteke in notranje aplikacije.</p></div>
<div class="card"><h3>IoT</h3><p>Kamere, tiskalniki in krmilniki naprav.</p></div>
</div>

**Ločitev zmanjša doseg napake ali ukradenega računa.**

Note:
VLAN loči omrežja, pravila požarnega zidu pa določajo prehode. Ime segmenta samo po sebi ni zaščita. Primer doma: gostujoče omrežje ne sme avtomatično dostopati do vseh naprav.

---

## Segmentacijo določajo dovoljene poti

![Obiskovalec lahko doseže dovoljeno storitev, ne pa IoT](./images/segmentation.svg)

Dovolimo potreben promet; preostale poti omejimo.

Note:
Ne gre le za blokiranje interneta. Pomemben je tudi promet med notranjimi segmenti. V ACME obstaja namerna napaka DMZ → IoT; njen vpliv bi se pokazal iz ustreznega izhodišča v DMZ.

---

## Ista vtičnica, tri stanja

| Položaj | Dosegljivo iz Kali |
| --- | --- |
| `internet` | objavljene javne storitve |
| `visitor` | LAN in dovoljene storitve DMZ |
| `flat` | vsi trije segmenti, tudi IoT |

**Rezultat vedno opremimo s podatkom o izhodišču.**

Note:
Scenarij velja globalno za vse. Preklopi spremenijo nove povezave; obstoječe lahko ostanejo. Udeleženci bodo primerjavo izvedli šele v praktičnem bloku.

---

## Nmap: tri različna vprašanja

<div class="cards">
<div class="card"><h3>Naprava</h3><p>Ali dobim odgovor na preverjanje prisotnosti?</p></div>
<div class="card"><h3>Vrata</h3><p>Ali lahko dosežem določeno storitev?</p></div>
<div class="card"><h3>Program</h3><p>Kaj odziv pove o vrsti in različici storitve?</p></div>
</div>

Note:
Odkrivanje gostiteljev samo zase ni dovolj. V tem labu so odprte storitve zanesljivejši učni dokaz kot razlikovanje closed/filtered. Zenmap lahko pokaže rezultate grafično, če je pripravljen.

---

## Kako preberemo rezultat?

<div class="example"><div class="example-label">PONAZORITEV IZPISA NMAP · JAVNI WWW ACME</div><pre><code>Nmap scan report for 198.51.100.11
PORT     STATE     SERVICE
80/tcp   open      http
443/tcp  filtered  https</code></pre></div>

**»open« potrdi dosegljiva vrata; ne potrdi ranljivosti.**

Note:
Izpis je ponazoritev vedenja, opisanega v README, ne sveža meritev. Pokaži IP, protokol TCP in stanje posameznih vrat. Pri 443 je lahko za pravilom tudi odsotna delujoča storitev; ne poenostavljaj v trditev, da je vzrok vedno požarni zid.

---

## Greenbone sestavi širši pregled

<div class="cards">
<div class="card"><h3>Obseg</h3><p>Katere tarče in katere teste smo vključili?</p></div>
<div class="card"><h3>Ugotovitve</h3><p>Katere težave je orodje zaznalo in na podlagi česa?</p></div>
<div class="card"><h3>Odprava</h3><p>Kateri ukrep predlaga in kako ga preverimo?</p></div>
</div>

**Kratek prikaz končanega pregleda ACME.**

Note:
Za naslednji dve prosojnici in preklop v Greenbone skupaj štiri minute. Odpri pripravljen pregled. Če pokažeš zagon novega, ne čakaj na zaključek. Namestitev in osvežitev podatkovnih virov morata biti opravljeni pred dogodkom.

---

## V poročilu odpremo eno ugotovitev

<div class="cards">
<div class="card"><h3>Dokaz</h3><p>Odziv, zaznana različica ali rezultat preizkusa.</p></div>
<div class="card"><h3>Resnost</h3><p>Kako velike bi bile posledice opisane težave?</p></div>
<div class="card"><h3>Zanesljivost</h3><p>Kako zanesljivo orodje prepozna konkretno stanje?</p></div>
</div>

**Preverimo pogoje, vpliv in predlagano odpravo.**

Note:
Pokaži dejansko poročilo, CVSS oziroma prikaz resnosti in Quality of Detection. Ne izmišljaj številčnih ocen pred izvedbo pregleda. Resnost ni isto kot verjetnost napada; tudi visoka zanesljivost prepoznave različice ne potrjuje vseh pogojev izrabe. Rezervno uporabi izvoženo poročilo.

---

## Različica → CVE → preverjanje

<div class="example"><div class="example-label">UČNI PRIMER ACME</div><pre><code>Opažanje:      Apache 2.4.49
Znana težava:  CVE-2021-41773
Pogoj:         ustrezno dovoljen dostop do poti
Sklep:         različica še ne potrdi izrabe</code></pre></div>

<small>[Apache: varnostna obvestila](https://httpd.apache.org/security/vulnerabilities_24.html)</small>

Note:
Apache v labu privzeto zavrača dostop zunaj DocumentRoot. Razloži razliko med starim programom, znano ranljivostjo in potrjenim vedenjem konkretne namestitve. Negativen poskus prav tako ne dokazuje odsotnosti vseh ranljivosti.

---

## 3. sklop · Razmišljanje preizkuševalca

![Razkrita poverilnica lahko zaradi ponovne uporabe vodi do dostopa](./images/chain.svg)

**Majhna razkritja se lahko povežejo v večji problem.**

Note:
Enajst minut za tretji sklop. Shema prikazuje možne povezave, ne zagotovljenega uspeha vsakega napada. Kali je zbirka orodij; razumevanje odzivov ostane naša naloga.

---

## Kaj se zgodi po kliku?

![Brskalnik pošlje zahtevo, strežnik vrne odgovor](./images/http.svg)

Zahteva: metoda, cilj, glave, telo · odgovor: status, glave, vsebina

Note:
Zgornja puščica predstavlja zahtevo, spodnja odgovor. Poveži s klikom na iskanje v trgovini. Zahteva ne vsebuje nujno telesa; podatki so lahko tudi v naslovu ali glavah.

---

## Zahteva pod povečevalnim steklom

<div class="example"><div class="example-label">IZMIŠLJEN PRIMER HTTP · NI ZAJEM JUICE SHOP</div><pre><code>POST /prijava HTTP/1.1
Host: trgovina.example
Content-Type: application/json

{&quot;uporabnik&quot;:&quot;ucenec&quot;,&quot;geslo&quot;:&quot;ucno&quot;}</code></pre></div>

Metoda in pot → glave → prazna vrstica → telo

Note:
Razloži štiri dele na kratko. Podatki so namerno izmišljeni, pot /prijava ni obljuba API Juice Shop. Ob HTTPS brskalnik še vedno vidi svoje podatke pred šifriranjem prenosa.

---

## Odgovor pove, kaj se je zgodilo

<div class="cards">
<div class="card"><h3>200 · OK</h3><p>Strežnik je zahtevo uspešno obdelal.</p></div>
<div class="card"><h3>401 · Unauthorized</h3><p>Zahteva potrebuje ustrezno prijavo.</p></div>
<div class="card"><h3>403 · Forbidden</h3><p>Strežnik zavrne dostop do vira.</p></div>
</div>

Status beremo skupaj z vsebino in kontekstom.

Note:
Status 200 sam zase ne dokazuje uspešne prijave; aplikacija lahko vrne sporočilo o napaki znotraj uspešnega odziva HTTP. Razloži še, da preusmeritev ni nujno napaka, brez dodatne tabele kod.

---

## Firefox pokaže lastni promet

<div class="cards">
<div class="card"><h3>Omrežje</h3><p>Zahteve, metode, odzivi in časi.</p></div>
<div class="card"><h3>Glave in telo</h3><p>Kaj je brskalnik dejansko poslal.</p></div>
<div class="card"><h3>Shramba</h3><p>Piškotki in drugi podatki aplikacije.</p></div>
</div>

**Kratek prikaz na pripravljeni trgovini ACME.**

Note:
Odpri F12 → Network v Firefoxu na shop.acme.lab. Pokaži eno lastno iskanje. Ne ustvarjaj računov in ne spreminjaj naročil. ZAP ali Burp prestrezata in omogočata dodatno obdelavo prometa; za začetno razumevanje zadostujejo razvijalska orodja.

---

## Kodiranje ni šifriranje

![Pretvorba Base64 je povratna in ne potrebuje skrivnega ključa](./images/encoding.svg)

**Base64 spremeni zapis. Šifriranje uporabi ključ.**

Note:
Prikazani učni niz se dekodira v ucenec:ucno. Omeni še kodiranje URL za posebne znake. Sprememba zapisa ne pomeni skrivnosti.

---

## CyberChef: sestavimo pretvorbo

<div class="cards">
<div class="card"><h3>Vhod</h3><p>dWNlbmVjOnVjbm8=</p></div>
<div class="card"><h3>Postopek</h3><p>From Base64</p></div>
<div class="card"><h3>Izhod</h3><p>ucenec:ucno</p></div>
</div>

Vhodni podatek → izbrana operacija → preverljiv rezultat

Note:
Kratek prikaz lokalnega CyberChef na Kali. Vnaprej preveri zagon. Uporabljaj le pripravljene izmišljene podatke. Pri več operacijah vrstni red vpliva na rezultat; avtomatsko zaznana pretvorba še ni dokaz pomena.

---

## HTTP Basic in zaščita prenosa

<div class="cards">
<div class="card"><h3>Basic</h3><p>Uporabnik in geslo sta zapisana z Base64.</p></div>
<div class="card"><h3>HTTP</h3><p>Prenos nima zaščite TLS.</p></div>
<div class="card"><h3>HTTPS</h3><p>TLS šifrira promet med brskalnikom in strežnikom.</p></div>
</div>

**Lastna orodja brskalnika podatke vidijo tudi pri HTTPS.**

Note:
Poveži z učnim intranetom, ne razkrivaj vseh odgovorov vaj. Lastni ogled zahteve ni dokaz prisluškovanja tretje osebe. HTTPS varuje prenos, ne zagotavlja poštenosti storitve in ne popravi vseh napak aplikacije.

---

## Piškotek lahko predstavlja sejo

| Zaščita | Namen |
| --- | --- |
| `Secure` | pošiljanje piškotka prek HTTPS |
| `HttpOnly` | omejitev dostopa JavaScript |
| `SameSite` | omejitev pošiljanja med spletnimi mesti |

**Vrednost prijavne seje obravnavamo kot skrivnost.**

Note:
Niso vsi piškotki prijavni. Odsotnost zastavice na nenevarni nastavitvi ni samodejno ranljivost. Nekatere aplikacije prijavne žetone hranijo drugače; pokaži samo dejansko stanje pripravljene različice.

---

## Od dokaza do izboljšave

<div class="cards">
<div class="card"><h3>Opažanje in dokaz</h3><p>Kaj, kje in kdaj smo preverili?</p></div>
<div class="card"><h3>Vpliv in omejitve</h3><p>Kaj ugotovitev pomeni in česa še ne vemo?</p></div>
<div class="card"><h3>Ukrep in potrditev</h3><p>Kaj spremenimo in kako preverimo izboljšavo?</p></div>
</div>

**Poišči sled. Preveri dokaz. Predlagaj zaščito.**

Note:
Zaključi predstavitev. Navodila za praktični blok so na ločeni strani vaje/. Skupni zaključni pogovor izvedi po vseh vajah: primerjava dokazov in izbor treh najkoristnejših ukrepov za ACME. Vsebinsko 35 prosojnic skupaj, brez navodil za naloge.
