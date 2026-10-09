# Cybersec-101: vaje in rešitve za izvajalca

Pripravljeno 9. oktobra 2026, posodobljeno 11. in 13. oktobra 2026. Vse domene pod .example, dialogi, podatki trgovin in rezultati razkritja v tem dokumentu so **izmišljeni učni primeri** in ne predstavljajo ugotovitev o resničnih ponudnikih. Vaje 1. sklopa od 13. oktobra 2026 uporabljajo javno dostopne spletne kvize. Vsak sklop ima tri vaje.

Besedilo »Rešitve za izvajalca« razkrij šele po razpravi. Udeleženci ne delijo gesel, obnovitvenih kod ali QR-kod za 2FA. Uporaba osebnega računa je prostovoljna. Kjer vaja uporablja lastno napravo, zaslona ne projiciramo in ga ne kažemo sosedu.

## Vaja 1.1: Spletni kviz in lažni IBAN

### Del A: kviz

Samostojno ali v paru, na telefonu ali prenosniku. **Izberi en kviz:**

| Kviz | Jezik | Obseg | Posebnost |
| --- | --- | --- | --- |
| [Spletni detektiv](https://spletnidetektiv.si/) (SI-CERT) | slovenščina | 4 vprašanja, nato še 4 dodatna | Več pravilnih odgovorov; razlaga po vsakem vprašanju. |
| [Phishing Quiz](https://phishingquiz.withgoogle.com/) (Google Jigsaw) | angleščina, nemščina in drugi | 8 e-poštnih sporočil | Na začetku vpiši **izmišljeno** ime in e-pošto; kviz to izrecno zahteva. |

1. Reši kviz do konca.
2. Zapiši en primer, ki te je presenetil, in en namig za naprej.

### Del B: sporočilo »dobavitelja«

Delaš v računovodstvu. Dobavitelj Dobavitelj d. o. o. vam pošilja račune že dve leti, običajno ti piše Maja Kovač z naslova maja.kovac@dobavitelj.example. Danes v isti niti prejmeš:

> **Od:** Maja Kovač &lt;maja.kovac@dobavltelj.example&gt;<br>
> **Odgovori na:** placila@dobavitelj-racuni.example<br>
> **Zadeva:** RE: Račun 2026-0412
>
> Pozdravljeni,
>
> zaradi revizije pri banki smo zamenjali IBAN. Račun 2026-0412 (4.870,00 €) prosim nakažite še danes na nov račun SI56 XXXX XXXX XXXX XXX. Stari račun bo jutri zaprt. Ves dan sem na sestankih in po telefonu nedosegljiva, zato mi potrdilo pošljite kar po e-pošti.
>
> Lep pozdrav, Maja

1. Poišči čim več znakov, da gre lahko za prevaro.
2. Zapiši, kaj narediš, preden račun plačaš, in koga pokličeš.

**Rešitve za izvajalca:**

- **Spletni detektiv** pokrije kupca, ki preplača in prosi za nakazilo razlike, lažne nagradne igre na Facebooku, »nagrado«, ki te vpiše v plačljiv SMS-klub, zgodbo o dediščini oziroma prenosu premoženja, ponovno uporabo gesla, priponke in izsiljevalsko kodo, posodobitve ter plačilo mimo platforme Airbnb. Zgodbe so starejše (harfa, Sirija), vzorci pa so še vedno aktualni.
- **Jigsaw** uči premik miške nad povezavo, branje domene, lažna povabila k deljenju dokumentov in lažna obvestila o prijavi. Na telefonu predogled povezave dobimo z dolgim pritiskom.
- Obema kvizoma manjkata sprememba IBAN (BEC) in bančni klic. BEC pokrijeta prosojnica »Vrivanje v poslovno komunikacijo (BEC)« in del B te vaje, bančni klic pa prosojnica »Prevare prek sporočil in telefonskih klicev«.
- **Del B, znaki:** domena pošiljatelja je `dobavltelj.example` (»l« namesto »i«), ne `dobavitelj.example`; odgovor gre na tretjo domeno (Reply-To); sprememba IBAN; nujnost (»še danes«, »stari račun bo jutri zaprt«); izogibanje telefonu; zahteva po potrdilu samo po e-pošti. Nit »RE:« in pravi znesek računa nista dokaz pristnosti: napadalec lahko bere prevzet predal in pozna resnične račune. Tudi če bi bila domena pravilna, bi zahtevo preverili.
- **Del B, varen postopek:** ne odgovorimo in ne plačamo. Majo ali dobavitelja pokličemo na številko iz pogodbe, prejšnjih računov ali imenika, ne iz podpisa v tem sporočilu. Spremembo IBAN potrdi še druga oseba po notranjem postopku. Obvestimo IT. Če se izkaže, da je dobaviteljev predal prevzet, obvestimo tudi dobavitelja. Če je bilo že plačano, takoj pokličemo banko, nato policijo; incident lahko prijavimo SI-CERT.
- Pri pogovoru poudari, da sporočilo nima povezave ne priponke, zato ga filtri pogosto ne ustavijo. Isti vzorec velja za lažnega direktorja (»nujno, zaupno, ne kliči me«) in za zahtevo za spremembo IBAN za plačo.

**Uspeh:** udeleženec zna povedati en nov namig in varen postopek ob spremembi IBAN.

## Vaja 1.2: Preberi naslov in preveri trgovino

Obe orodji sta v angleščini. Kdor angleško ne bere dobro, dela v paru.

### Del A: komu res pripada naslov?

Odpri [SafeToOpen Phishing Quiz](https://safetoopen.com/en/phishing-quiz/). Ima 12 sporočil in spletnih strani, nekatere so pristne, druge lažne. Vse znamke so izmišljene. Registracija ni potrebna; stran beleži le končni rezultat in državo.

**Namig:** gostitelj je med »https://« in prvo naslednjo poševnico (/). Lastnika pove konec gostitelja, ne začetek. `banka.example.prijava-varno.example` pripada `prijava-varno.example`.

### Del B: lažna spletna trgovina

Na prenosniku odpri [Online Shop Scam Game](https://goodthings-online-shop-scam-game.ai.studio/) (Good Things Foundation Australia). Klikni »Start the game«, razišči trgovino in označi vse, kar se ti zdi sumljivo. Nato klikni »Spot the scams« in primerjaj.

**Rešitve za izvajalca:**

- **Del A:** ključna lekcija je, da lastnika pove domena, ne ime znamke drugje v naslovu, ključavnica HTTPS ali videz strani. Kviz vključuje tudi podobne znake (npr. »rn« namesto »m«, cirilične črke), ki jih s prostim očesom skoraj ne vidimo. Zato je pri dvomu bolje odpreti aplikacijo ali zaznamek kot brati naslov.
- **Del B:** pogovor usmeri na skupne znake: predobra cena, umetna nujnost (odštevalnik, »samo še 2 kosa«), manjkajoči podatki podjetja in pogoji vračila, ocene brez možnosti preverjanja, plačilo, ki ga ni mogoče reklamirati. Dodaj slovenski vidik: podjetje preverimo v [AJPES](https://www.ajpes.si/), SI-CERT pa opozarja na lažne »slovenske družinske butike« z zgodbami, ustvarjenimi z UI.
- Pred izvedbo oba kviza preizkusi v brskalniku. SafeToOpen je komercialni ponudnik razširitve za brskalnik; razširitve na delavnici ne nameščamo.

**Uspeh:** udeleženec zna pri naslovu poiskati lastnika in navesti tri znake lažne trgovine.

## Vaja 1.3: Ali prepoznaš ponaredek?

### Del A: Which Face Is Real

Odpri [whichfaceisreal.com](https://www.whichfaceisreal.com/). Vsakič vidiš dva obraza: eden je fotografija, drugi je ustvarjen z umetno inteligenco. Klikni resničnega. Odigraj 10 krogov in štej pravilne odgovore.

### Del B: deepfake video (na projektorju)

Izvajalec predvaja enega od posnetkov:

- [This is not Morgan Freeman – A Deepfake Singularity](https://www.youtube.com/watch?v=oxXpB9pSETo) (Diep Nep): zelo prepričljiv obraz in glas.
- [You Won't Believe What Obama Says In This Video!](https://www.youtube.com/watch?v=cQ54GDm1eL0) (BuzzFeed, 2018): klasičen primer z razkritjem, kdo v resnici govori.

### Del C: pogovor

1. Koliko pravilnih odgovorov ste imeli pri obrazih?
2. Bi video prepoznali, če vam ga ne bi napovedali?
3. Kaj torej naredimo, ko nas »znan obraz« prosi za denar?

**Rešitve za izvajalca:**

- Pri obrazih je večina rezultatov blizu ugibanja ali le malo boljša. Which Face Is Real uporablja starejšo tehnologijo (StyleGAN); današnji ponaredki so še boljši. Bistvo je ugotovitev, da po videzu ne moremo zanesljivo presoditi.
- Pravilen odgovor na tretje vprašanje je postopek s prosojnice »Kako preverimo nenavadno zahtevo«: ustavi se, preveri po kanalu, ki ga izbereš sam, šele nato ukrepaj.
- Domač primer: maja 2024 je vlada [opozorila na lažni posnetek](https://www.gov.si/novice/2024-05-15-opozorilo-o-laznih-spletnih-vsebinah-povezanih-z-vlado/), ki je zlorabil podobo in glas predsednika vlade.
- Oba videa sta demonstraciji, ne prevari. Pred izvedbo preveri, da se predvajata brez prijave in oglasov, ki bi motili.

**Uspeh:** udeleženci sami ugotovijo, da prepoznavanje po videzu ni zanesljivo, in povedo postopek preverjanja.

## Vaja 2.1: Preveri razkritje in obnovitev e-pošte

E-pošta je ključ do drugih računov, zato začnemo pri njej.

### Del A: razkritje

Odpri [Have I Been Pwned](https://haveibeenpwned.com/). Po želji vnesi **svoj** naslov, ne naslova drugega udeleženca. Gesla ne vnašamo. Poišči prizadeto storitev, leto in vrste podatkov.

### Del B: obnovitev in seje

V svojem glavnem e-poštnem računu odpri varnostni pregled:

- Google: [myaccount.google.com/security-checkup](https://myaccount.google.com/security-checkup)
- Microsoft: [account.microsoft.com/security](https://account.microsoft.com/security)
- Apple: Nastavitve → tvoje ime → Prijava in varnost

Preveri tri stvari: ali sta obnovitvena telefonska številka in e-pošta še tvoji, katere naprave so prijavljene in ali je dvostopenjsko preverjanje že vključeno. Neznano napravo odjavi.

**Učni primer brez osebnih podatkov:** iz izmišljene storitve »Učna trgovina« so leta 2024 odtekli e-poštni naslovi in zgoščene vrednosti gesel. Uporabnik ima isto geslo še danes tudi za e-pošto. Kot obnovitvena številka je v e-pošti vpisana njegova stara številka, ki je ne uporablja več. Kaj mora narediti in v kakšnem vrstnem redu?

**Rešitev učnega primera:**

1. **Najprej e-pošta:** z zaupanja vredne naprave zamenja geslo za e-pošto z novim, edinstvenim geslom. E-pošta je prva, ker lahko z njo ponastavi vse druge račune.
2. **Pregled računa:** odjavi neznane naprave ter preveri obnovitveni e-naslov in pravila za preusmeritev pošte.
3. **Obnovitvena številka:** staro zamenja s trenutno. Operater lahko neuporabljeno številko dodeli komu drugemu, ta pa bi z njo lahko ponastavil geslo.
4. **Dvostopenjsko preverjanje:** ga vključi in shrani rezervne kode. Številko posodobi prej, sicer bi kode SMS prihajale na staro številko.
5. **Drugi računi:** geslo zamenja povsod, kjer je bilo enako, tudi v Učni trgovini, ali račun tam zapre.

Pri pogovoru pojasni: zgoščena vrednost ni geslo v berljivi obliki, a šibka in pogosta gesla napadalci iz nje hitro razbijejo. Zato razkritje jemljemo resno, tudi če gesla niso odtekla »v čistopisu«.

**Uspeh:** udeleženec razlikuje med zgodovinskim razkritjem in trenutnim vdorom ter ve, ali je pošto mogoče obnoviti brez trenutnega telefona.  
**Viri:** [HIBP: pogosta vprašanja](https://haveibeenpwned.com/FAQs), [Google: varnostni pregled](https://myaccount.google.com/security-checkup).

## Vaja 2.2: Pripravi trezor gesel

Vsi uporabimo [Bitwarden](https://bitwarden.com/), ker deluje na vseh sistemih in brskalnikih in ga v vaji 2.3 zaščitimo z dvostopenjsko prijavo. Za račun potrebuješ dostop do e-pošte.

1. Na [bitwarden.com](https://bitwarden.com/) ustvari račun. Razširitev za brskalnik namesti prek uradne strani in preveri izdajatelja.
2. Izberi dolgo glavno frazo, ki je drugje ne uporabljaš. Ne uporabi javnih primerov s prosojnic.
3. Nastavi samodejno zaklepanje.
4. Z generatorjem pripravi tri različna gesla za spodnje učne vnose.
5. Zakleni in ponovno odkleni trezor.
6. Zapiši, kako dostopaš do trezorja, če izgubiš telefon.

| Ime vnosa | Uporabniško ime | Učni naslov |
| --- | --- | --- |
| Učna pošta | ucenec@example.com | posta.example |
| Učna trgovina | ucenec@example.com | trgovina.example |
| Učno omrežje | ucenec | omrezje.example |

Ti naslovi niso spletne storitve in se vanje ne prijavljamo. Za demonstracijo samodejnega izpolnjevanja izvajalec uporabi svoj poskusni račun pri vnaprej izbrani storitvi.

**Uspeh:** trije različni vnosi, uspešen odklep in razumljiv načrt obnovitve.  
**Viri:** [Bitwarden: razširitev](https://bitwarden.com/help/getting-started-browserext/), [glavno geslo](https://bitwarden.com/help/master-password/).

## Vaja 2.3: Dodaj ključ za dostop ali drugi dejavnik

Izberi eno pot. Pot A je priporočena, ker obstoječe geslo ostane, zato dostopa ne moreš izgubiti.

**Pot A — ključ za dostop (passkey):**

1. Na telefonu odpri [g.co/passkeys](https://g.co/passkeys) (Google) ali varnostne nastavitve računa Microsoft.
2. Ustvari ključ za dostop in ga potrdi z odklepom telefona.
3. Na prenosniku odpri zasebno okno in se prijavi z možnostjo »ključ za dostop«; prijavo potrdi s telefonom (QR-koda, Bluetooth mora biti vklopljen).
4. Preveri, da se ključ pokaže na seznamu v nastavitvah računa.

**Pot B — aplikacija za kode (za Bitwarden iz vaje 2.2):**

1. Namesti **2FAS Auth** prek [uradne strani ponudnika](https://2fas.com/) ali uporabi svojo potrjevalno aplikacijo.
2. V spletnem trezorju Bitwarden: Nastavitve → Varnost → Dvostopenjska prijava → aplikacija za preverjanje pristnosti.
3. Dodaj QR-kodo v aplikacijo in potrdi s trenutno kodo.
4. **Pred odjavo** shrani obnovitveno kodo na papir ali drugo mesto zunaj trezorja.
5. Odjavi se in prijavi znova s kodo.

**Ne projiciramo osebnih QR-kod.** Kdor QR-kodo ali skrivni ključ kopira, lahko ustvarja iste kode. Ob težavi ne izklapljamo zaščite brez razumevanja posledic.

**Uspeh:** nova prijava deluje in udeleženec zna opisati obnovitev.  
**Viri:** [FIDO Alliance: ključi za dostop](https://fidoalliance.org/passkeys/), [Google: ključi za dostop](https://support.google.com/accounts/answer/13548313), [2FAS: pomoč](https://2fas.com/support/), [Bitwarden: koda za obnovitev 2FA](https://bitwarden.com/help/two-step-recovery-code/).

## Vaja 3.1: Pospravi brskalnik

Na prenosniku v brskalniku, ki ga največ uporabljaš:

1. **Posodobitev:** Chrome ali Edge: Nastavitve → O brskalniku; Firefox: Pomoč → O Firefoxu.
2. **Razširitve:** odpri seznam razširitev (v Chromu `chrome://extensions`, v Firefoxu `about:addons`). Odstrani tiste, ki jih ne poznaš ali ne uporabljaš.
3. **Obvestila spletnih strani:** Chrome: Nastavitve → Zasebnost in varnost → Nastavitve spletnega mesta → Obvestila; Firefox: Nastavitve → Zasebnost in varnost → Dovoljenja → Obvestila. Odstrani strani, ki jih ne poznaš.
4. Chrome: zaženi **Preverjanje varnosti** v razdelku Zasebnost in varnost.
5. **Po želji:** Firefox: uradni **uBlock Origin**; Chrome: **uBlock Origin Lite** iz [projekta razvijalca](https://github.com/gorhill/uBlock). Odpri običajno stran in preveri, ali deluje.

**Rešitev za izvajalca:** lažna opozorila »Vaš računalnik je okužen« pogosto prihajajo kot obvestila strani, ki ji je uporabnik nekoč kliknil »Dovoli«. Preklic obvestil jih ustavi. Števec blokatorja ni število preprečenih okužb. Ne nameščamo več blokatorjev hkrati.

**Uspeh:** brskalnik je posodobljen, udeleženec pozna vse svoje razširitve in strani z dovoljenjem za obvestila.  
**Viri:** [Google: obvestila v Chromu](https://support.google.com/chrome/answer/3220216), [Mozilla: obvestila](https://support.mozilla.org/en-US/kb/push-notifications-firefox), [uBlock Origin](https://github.com/gorhill/uBlock), [uBlock Origin Lite](https://github.com/gorhill/uBlock/tree/master/platform/mv3).

## Vaja 3.2: Pripravi telefon na izgubo

Vaja uporablja telefon in prenosnik skupaj.

1. **Zaklep zaslona:** preveri, da imaš PIN (najmanj 6 številk) ali geslo in kratek čas samodejnega zaklepa.
2. **Posodobitve:** preveri, ali čaka posodobitev in ali so samodejne posodobitve vključene. Velike posodobitve med delavnico ne nameščamo.
3. **Iskanje naprave:** Android: v Nastavitvah poišči »Find Hub« oziroma »Poišči napravo« in preveri, da je vklopljeno. iPhone: Nastavitve → tvoje ime → Najdi → Najdi moj iPhone.
4. **Preizkus s prenosnika:** odpri [android.com/find](https://www.android.com/find) ali [icloud.com/find](https://www.icloud.com/find), se prijavi in telefonu **predvajaj zvok**. Ne izberi »Izbriši«. Na koncu se odjavi, če prenosnik ni tvoj.
5. Zapiši, koga pokličeš ob izgubi: operaterja (zapora SIM) in banko.

**Rešitev za izvajalca:** iskanje deluje samo, če je vklopljeno vnaprej. Prijava na prenosniku pogosto sproži dodatno preverjanje na telefonu, kar je dobra ponovitev drugega sklopa. Pri izgubi brez telefona pride prav obnovitev iz vaje 2.1.

**Uspeh:** telefon zazvoni na ukaz s prenosnika.  
**Viri:** [Google: izgubljena naprava Android](https://support.google.com/android/answer/6160491), [Apple: izgubljena naprava](https://support.apple.com/en-us/104978), [Google: posodobitve Androida](https://support.google.com/android/answer/7680439), [Apple: posodobitve iOS](https://support.apple.com/en-us/118575).

## Vaja 3.3: Preglej dovoljenja aplikacij

Izberi tri nameščene aplikacije. Pri vsaki zapiši namen in potrebna dovoljenja.

- Android: Nastavitve → Aplikacije → izbrana aplikacija → Dovoljenja.
- iPhone: Nastavitve → Zasebnost in varnost → Lokacija, Mikrofon ali Kamera.

Preglej en nepotreben dostop in ga zavrni ali omeji na čas uporabe, če sistem to ponuja. Preizkusi pomembno funkcijo aplikacije. Če se ustavi, razmisli o manjšem dovoljenju ali vrni prejšnjo nastavitev.

| Aplikacija | Namen | Dovoljenje | Moja izbira | Ali še deluje? |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

**Primer:** zemljevid potrebuje lokacijo za navigacijo, aplikacija za videoklic mikrofon za pogovor, preprosta svetilka praviloma ne potrebuje stikov. Primeri so učni; preverimo funkcije konkretne aplikacije.

**Uspeh:** en utemeljen poseg in preizkus delovanja.  
**Vira:** [Google: dovoljenja](https://support.google.com/android/answer/9431959), [Apple: dovoljenja](https://support.apple.com/guide/iphone/control-access-to-information-in-apps-iph251e92810/ios).

## Dodatna vaja za hitrejše: varnejši DNS

Ni del osnovnega urnika. Primerna za udeležence, ki končajo prej in nimajo upravljane naprave.

- **Android 9+:** Nastavitve → »Zasebni DNS« → ime ponudnika **dns.quad9.net**; preveri na [on.quad9.net](https://on.quad9.net/).
- **Firefox:** Nastavitve → Zasebnost in varnost → DNS prek HTTPS → ponudnik po meri **https://dns.quad9.net/dns-query**.

Pred spremembo zapiši prejšnjo nastavitev; če povezava odpove, jo vrni. Šifriranje poizvedbe in filtriranje nevarnih domen sta ločeni funkciji (ilustracija dns.svg). Quad9 filtrira znane zlonamerne domene; Cloudflare 1.1.1.1 je brez filtra, 1.1.1.2 s filtrom. Noben filter ne pozna vseh prevar. VPN, prijavni portal ali službeno omrežje lahko vplivajo na rezultat.  
**Viri:** [Quad9: Android](https://docs.quad9.net/Setup_Guides/Android/Android_9%2B_(Encrypted)/), [Mozilla: DoH](https://support.mozilla.org/en-US/kb/firefox-dns-over-https), [Cloudflare: možnosti resolverja](https://developers.cloudflare.com/1.1.1.1/setup/).

## Za doma: preizkusi varnostno kopijo

1. Ustvari izmišljeno datoteko `vaja-kopija.txt` z besedilom »To je učni dokument«.
2. Z obstoječim postopkom jo kopiraj na drug nosilec ali v obstoječo odobreno shrambo. Zapiši datum kopije.
3. Iz kopije jo **obnovi v drugo mapo** in odpri. Izvirnika ne briši.
4. Zapiši načrt 3–2–1 za svoje pomembne podatke: izvirnik, prva kopija, druga kopija, lokacija zunaj doma.
5. Preveri, katera kopija bi ostala dosegljiva, če je glavni računalnik okužen ali izgubljen. Ali je vsaj ena kopija brez povezave (odklopljen disk)? Kje imaš obnovitveni ključ, če je kopija šifrirana?

**Uspeh:** obnovljena izmišljena datoteka se odpre; načrt ni le mapa na istem disku. Pri oblačni storitvi posebej preveri koš, zgodovino različic in trajanje hrambe. Sinhronizacija se lahko odzove tudi na izbris. Ne nalagamo resničnih službenih dokumentov v neodobrene storitve.

**Brez dodatnega nosilca ali računa:** na papirju pripravi načrt in pri izvajalcu spremljaj obnovitev testne datoteke. To je priprava načrta, ne dokaz, da dejanska kopija deluje.

## Za doma: zemljevid digitalnega doma

Nariši usmerjevalnik, svoj računalnik, telefon, eno pametno napravo (IoT) in gosta. Zapiši:

- Kdo sme v glavno omrežje in kdo le v gostujoče?
- Ali poznaš razliko med geslom Wi-Fi in skrbniškim geslom?
- Kdo posodablja usmerjevalnik in koliko časa je pametna naprava podprta?
- Ali kamera potrebuje dostop od zunaj in kako je ta zaščiten?

**Rešitev:** gostje in pametne naprave naj imajo ločen dostop, kjer je to podprto in smiselno. Preveri dejansko izolacijo, privzeta gesla, posodobitve in nepotrebno oddaljeno upravljanje. Brez dovoljenja ne spreminjaj službenega ali skupnega omrežja; za domači usmerjevalnik uporabi navodila proizvajalca oziroma operaterja.

## Mini kviz za ponovitev

| Trditev | Odgovor in razlog |
| --- | --- |
| HTTPS dokazuje, da je trgovec pošten. | Ne. Šifrira povezavo do strani. |
| Geslo z istim začetkom in drugim imenom storitve je neodvisno. | Ne. Različico je mogoče predvideti. |
| Mapa »backup« na istem disku me zaščiti pred okvaro tega diska. | Ne. Okvara prizadene tudi mapo. |
| Posodobitve lahko odpravijo varnostne ranljivosti. | Da. Zato jih redno nameščamo iz zaupanja vrednega vira. |
| Po kliku na sumljivo povezavo je najbolje to čim prej povedati odgovorni osebi. | Da. Hitra prijava pomaga omejiti škodo. |

Pri izvedbi naj par najprej pove odgovor, nato razlog. Zadnji primer preverja odnos do prijave, ne kaznuje napake.

## Zaključni osebni načrt

**Danes bom:** __________________  
**Do datuma:** __________________  
**Uspeh preverim tako:** __________________  
**Kontakt ob sumu prevare:** __________________

Pri bančnih podatkih ali nakazilu takoj kontaktiramo banko, pri službenem računu IT, incidente pa lahko prijavimo [SI-CERT](https://www.cert.si/prijava-incidenta/). Ob oškodovanju se obrnemo tudi na policijo.
