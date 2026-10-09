# Digitalna samoobramba: vaje

Navodila za udeležence delavnice Cybersec-101. V vsakem sklopu so tri vaje.

- **Gesel, obnovitvenih kod in QR-kod za dvostopenjsko prijavo ne deli** z nikomer, tudi s sosedom ne.
- Uporaba osebnega računa je prostovoljna.
- Kjer delaš na svoji napravi, zaslona ne kaži drugim.
- Vse domene pod `.example`, učni vnosi in podatki v vajah so izmišljeni.

Povezave lahko odpreš s klikom ali skeniraš QR-kodo s telefonom.

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

**Cilj:** znaš povedati en nov namig iz kviza in varen postopek ob spremembi IBAN.

## Vaja 1.2: Preberi naslov in preveri trgovino

Obe orodji sta v angleščini. Če angleško ne bereš dobro, delaj v paru.

### Del A: komu res pripada naslov?

Odpri [SafeToOpen Phishing Quiz](https://safetoopen.com/en/phishing-quiz/). Ima 12 sporočil in spletnih strani, nekatere so pristne, druge lažne. Vse znamke so izmišljene. Registracija ni potrebna. Razširitve za brskalnik, ki jo stran ponuja, ne nameščaj.

**Namig:** gostitelj je med »https://« in prvo naslednjo poševnico (/). Lastnika pove konec gostitelja, ne začetek. `banka.example.prijava-varno.example` pripada `prijava-varno.example`.

### Del B: lažna spletna trgovina

Na prenosniku odpri [Online Shop Scam Game](https://goodthings-online-shop-scam-game.ai.studio/) (Good Things Foundation Australia). Klikni »Start the game«, razišči trgovino in označi vse, kar se ti zdi sumljivo. Nato klikni »Spot the scams« in primerjaj.

**Cilj:** pri naslovu znaš poiskati lastnika in navesti tri znake lažne trgovine.

## Vaja 1.3: Ali prepoznaš ponaredek?

### Del A: Which Face Is Real

Odpri [whichfaceisreal.com](https://www.whichfaceisreal.com/). Vsakič vidiš dva obraza: eden je fotografija, drugi je ustvarjen z umetno inteligenco. Klikni resničnega. Odigraj 10 krogov in štej pravilne odgovore.

### Del B: deepfake video

Posnetek si ogledamo skupaj na projektorju. Če ga želiš pozneje pogledati še enkrat:

- [This is not Morgan Freeman – A Deepfake Singularity](https://www.youtube.com/watch?v=oxXpB9pSETo) (Diep Nep)
- [You Won't Believe What Obama Says In This Video!](https://www.youtube.com/watch?v=cQ54GDm1eL0) (BuzzFeed, 2018)

### Del C: pogovor

1. Koliko pravilnih odgovorov je bilo pri obrazih?
2. Bi bil ponaredek v videu opazen, če ga ne bi napovedali?
3. Kaj torej narediš, ko te »znan obraz« prosi za denar?

**Cilj:** znaš povedati, kako zahtevo preveriš brez zanašanja na videz.

## Vaja 2.1: Preveri razkritje in obnovitev e-pošte

E-pošta je ključ do drugih računov, zato začnemo pri njej.

### Del A: razkritje

Odpri [Have I Been Pwned](https://haveibeenpwned.com/). Po želji vnesi **svoj** naslov, ne naslova drugega udeleženca. Gesla ne vnašaj. Poišči prizadeto storitev, leto in vrste podatkov.

### Del B: obnovitev in seje

V svojem glavnem e-poštnem računu odpri varnostni pregled:

- Google: [myaccount.google.com/security-checkup](https://myaccount.google.com/security-checkup)
- Microsoft: [account.microsoft.com/security](https://account.microsoft.com/security)
- Apple: Nastavitve → tvoje ime → Prijava in varnost

Preveri tri stvari: ali sta obnovitvena telefonska številka in e-pošta še tvoji, katere naprave so prijavljene in ali je dvostopenjsko preverjanje že vključeno. Neznano napravo odjavi.

**Učni primer brez osebnih podatkov:** iz izmišljene storitve »Učna trgovina« so leta 2024 odtekli e-poštni naslovi in zgoščene vrednosti gesel. Uporabnik ima isto geslo še danes tudi za e-pošto. Kot obnovitvena številka je v e-pošti vpisana njegova stara številka, ki je ne uporablja več. Kaj mora narediti in v kakšnem vrstnem redu?

**Cilj:** razlikuješ med starim razkritjem in trenutnim vdorom ter veš, ali je pošto mogoče obnoviti brez trenutnega telefona.  
**Več:** [HIBP: pogosta vprašanja](https://haveibeenpwned.com/FAQs)

## Vaja 2.2: Pripravi trezor gesel

Vsi uporabimo [Bitwarden](https://bitwarden.com/), ker deluje na vseh sistemih in brskalnikih. V vaji 2.3 ga zaščitimo z dvostopenjsko prijavo. Za račun potrebuješ dostop do e-pošte.

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

Ti naslovi niso spletne storitve in se vanje ne prijavljamo. Samodejno izpolnjevanje pokaže izvajalec.

**Cilj:** trije različni vnosi, uspešen odklep in razumljiv načrt obnovitve.  
**Več:** [Bitwarden: razširitev](https://bitwarden.com/help/getting-started-browserext/), [Bitwarden: glavno geslo](https://bitwarden.com/help/master-password/)

## Vaja 2.3: Dodaj ključ za dostop ali drugi dejavnik

Izberi eno pot. Pot A je priporočena, ker obstoječe geslo ostane, zato dostopa ne moreš izgubiti.

**Pot A — ključ za dostop (passkey):**

1. Na telefonu odpri [g.co/passkeys](https://g.co/passkeys) (Google) ali varnostne nastavitve računa Microsoft.
2. Ustvari ključ za dostop in ga potrdi z odklepom telefona.
3. Na prenosniku odpri zasebno okno in se prijavi z možnostjo »ključ za dostop«. Prijavo potrdi s telefonom (QR-koda, Bluetooth mora biti vklopljen).
4. Preveri, da se ključ pokaže na seznamu v nastavitvah računa.

**Pot B — aplikacija za kode (za Bitwarden iz vaje 2.2):**

1. Namesti **2FAS Auth** prek [uradne strani ponudnika](https://2fas.com/) ali uporabi svojo potrjevalno aplikacijo.
2. V spletnem trezorju Bitwarden: Nastavitve → Varnost → Dvostopenjska prijava → aplikacija za preverjanje pristnosti.
3. Dodaj QR-kodo v aplikacijo in potrdi s trenutno kodo.
4. **Pred odjavo** shrani obnovitveno kodo na papir ali drugo mesto zunaj trezorja.
5. Odjavi se in prijavi znova s kodo.

**Svoje QR-kode za 2FA ne kaži nikomur.** Kdor QR-kodo ali skrivni ključ kopira, lahko ustvarja iste kode. Ob težavi zaščite ne izklapljaj, ampak pokliči izvajalca.

**Cilj:** nova prijava deluje in znaš opisati obnovitev.  
**Več:** [FIDO Alliance: ključi za dostop](https://fidoalliance.org/passkeys/), [Google: ključi za dostop](https://support.google.com/accounts/answer/13548313), [2FAS: pomoč](https://2fas.com/support/), [Bitwarden: koda za obnovitev 2FA](https://bitwarden.com/help/two-step-recovery-code/)

## Vaja 3.1: Pospravi brskalnik

Na prenosniku v brskalniku, ki ga največ uporabljaš:

1. **Posodobitev:** Chrome ali Edge: Nastavitve → O brskalniku; Firefox: Pomoč → O Firefoxu.
2. **Razširitve:** odpri seznam razširitev (v Chromu `chrome://extensions`, v Firefoxu `about:addons`). Odstrani tiste, ki jih ne poznaš ali ne uporabljaš.
3. **Obvestila spletnih strani:** Chrome: Nastavitve → Zasebnost in varnost → Nastavitve spletnega mesta → Obvestila; Firefox: Nastavitve → Zasebnost in varnost → Dovoljenja → Obvestila. Odstrani strani, ki jih ne poznaš.
4. Chrome: zaženi **Preverjanje varnosti** v razdelku Zasebnost in varnost.
5. **Po želji:** Firefox: uradni **uBlock Origin**; Chrome: **uBlock Origin Lite** iz [projekta razvijalca](https://github.com/gorhill/uBlock). Odpri običajno stran in preveri, ali deluje. Ne nameščaj več blokatorjev hkrati.

**Cilj:** brskalnik je posodobljen, poznaš vse svoje razširitve in strani z dovoljenjem za obvestila.  
**Več:** [Google: obvestila v Chromu](https://support.google.com/chrome/answer/3220216), [Mozilla: obvestila](https://support.mozilla.org/en-US/kb/push-notifications-firefox), [uBlock Origin Lite](https://github.com/gorhill/uBlock/tree/master/platform/mv3)

## Vaja 3.2: Pripravi telefon na izgubo

Vaja uporablja telefon in prenosnik skupaj.

1. **Zaklep zaslona:** preveri, da imaš PIN (najmanj 6 številk) ali geslo in kratek čas samodejnega zaklepa.
2. **Posodobitve:** preveri, ali čaka posodobitev in ali so samodejne posodobitve vključene. Velike posodobitve med delavnico ne nameščaj.
3. **Iskanje naprave:** Android: v Nastavitvah poišči »Find Hub« oziroma »Poišči napravo« in preveri, da je vklopljeno. iPhone: Nastavitve → tvoje ime → Najdi → Najdi moj iPhone.
4. **Preizkus s prenosnika:** odpri [android.com/find](https://www.android.com/find) ali [icloud.com/find](https://www.icloud.com/find), se prijavi in telefonu **predvajaj zvok**. Ne izberi »Izbriši«. Na koncu se odjavi, če prenosnik ni tvoj.
5. Zapiši, koga pokličeš ob izgubi: operaterja (zapora SIM) in banko.

**Cilj:** telefon zazvoni na ukaz s prenosnika.  
**Več:** [Google: izgubljena naprava Android](https://support.google.com/android/answer/6160491), [Apple: izgubljena naprava](https://support.apple.com/en-us/104978), [Google: posodobitve Androida](https://support.google.com/android/answer/7680439), [Apple: posodobitve iOS](https://support.apple.com/en-us/118575)

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

**Primer:** zemljevid potrebuje lokacijo za navigacijo, aplikacija za videoklic mikrofon za pogovor, preprosta svetilka praviloma ne potrebuje stikov.

**Cilj:** en utemeljen poseg in preizkus delovanja.  
**Več:** [Google: dovoljenja](https://support.google.com/android/answer/9431959), [Apple: dovoljenja](https://support.apple.com/guide/iphone/control-access-to-information-in-apps-iph251e92810/ios)

## Za hitrejše: varnejši DNS

Ni del osnovnega urnika. Primerno, če končaš prej in nimaš upravljane (službene) naprave.

- **Android 9+:** Nastavitve → »Zasebni DNS« → ime ponudnika **dns.quad9.net**; preveri na [on.quad9.net](https://on.quad9.net/).
- **Firefox:** Nastavitve → Zasebnost in varnost → DNS prek HTTPS → ponudnik po meri **https://dns.quad9.net/dns-query**.

Pred spremembo zapiši prejšnjo nastavitev; če povezava odpove, jo vrni. Šifriranje poizvedbe in filtriranje nevarnih domen sta ločeni funkciji. Quad9 filtrira znane zlonamerne domene, vendar noben filter ne pozna vseh prevar. VPN, prijavni portal ali službeno omrežje lahko vplivajo na rezultat.

**Več:** [Quad9: Android](https://docs.quad9.net/Setup_Guides/Android/Android_9%2B_(Encrypted)/), [Mozilla: DNS prek HTTPS](https://support.mozilla.org/en-US/kb/firefox-dns-over-https)

## Za doma: preizkusi varnostno kopijo

1. Ustvari izmišljeno datoteko `vaja-kopija.txt` z besedilom »To je učni dokument«.
2. Z obstoječim postopkom jo kopiraj na drug nosilec ali v obstoječo odobreno shrambo. Zapiši datum kopije.
3. Iz kopije jo **obnovi v drugo mapo** in odpri. Izvirnika ne briši.
4. Zapiši načrt 3–2–1 za svoje pomembne podatke: izvirnik, prva kopija, druga kopija, lokacija zunaj doma.
5. Preveri, katera kopija bi ostala dosegljiva, če je glavni računalnik okužen ali izgubljen. Ali je vsaj ena kopija brez povezave (odklopljen disk)? Kje imaš obnovitveni ključ, če je kopija šifrirana?

Pri oblačni storitvi preveri koš, zgodovino različic in trajanje hrambe. Sinhronizacija se lahko odzove tudi na izbris. Resničnih službenih dokumentov ne nalagaj v neodobrene storitve.

**Cilj:** obnovljena izmišljena datoteka se odpre; načrt ni le mapa na istem disku.

## Za doma: zemljevid digitalnega doma

Nariši usmerjevalnik, svoj računalnik, telefon, eno pametno napravo (IoT) in gosta. Zapiši:

- Kdo sme v glavno omrežje in kdo le v gostujoče?
- Ali poznaš razliko med geslom Wi-Fi in skrbniškim geslom?
- Kdo posodablja usmerjevalnik in koliko časa je pametna naprava podprta?
- Ali kamera potrebuje dostop od zunaj in kako je ta zaščiten?

Brez dovoljenja ne spreminjaj službenega ali skupnega omrežja. Za domači usmerjevalnik uporabi navodila proizvajalca oziroma operaterja.

## Moj načrt

**Danes bom:** __________________  
**Do datuma:** __________________  
**Uspeh preverim tako:** __________________  
**Kontakt ob sumu prevare:** __________________

Pri bančnih podatkih ali nakazilu takoj pokliči banko, pri službenem računu IT. Incidente lahko prijaviš [SI-CERT](https://www.cert.si/prijava-incidenta/). Ob oškodovanju se obrni tudi na policijo.
