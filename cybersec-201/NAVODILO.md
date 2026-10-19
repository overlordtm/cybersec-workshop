# Priprava na delavnico kibernetske varnosti

Pozdravljeni!

Za udeležbo na delavnici kibernetske varnosti boste potrebovali **virtualizacijsko okolje in operacijski sistem Kali Linux**.

Prosimo, da oboje namestite **pred začetkom delavnice**, saj bomo Kali Linux uporabljali pri praktičnih vajah.

## 1. Namestitev virtualizacijskega okolja

Izberete lahko eno izmed spodnjih virtualizacijskih okolij. **Priporočamo Oracle VirtualBox**, saj je brezplačen, enostaven za uporabo in na voljo za različne operacijske sisteme.

### Možnost A: Oracle VirtualBox (priporočeno)

VirtualBox je brezplačno odprtokodno virtualizacijsko okolje, ki deluje na Windows, Linux in macOS.

**Postopek namestitve:**

1. Obiščite uradno spletno stran: [VirtualBox Downloads](https://www.virtualbox.org/wiki/Downloads)
2. Prenesite namestitveno datoteko za svoj operacijski sistem.
3. Zaženite namestitveni program in sledite navodilom.
4. Po končani namestitvi zaženite VirtualBox.

### Možnost B: VMware Workstation Pro

VMware Workstation Pro je brezplačno virtualizacijsko okolje, ki omogoča uporabo virtualnih računalnikov.

**Postopek namestitve:**

1. Obiščite [uradno stran za prenos VMware](https://knowledge.broadcom.com/external/article/368667/download-and-license-vmware-desktop-hyper.html).
2. Za prenos boste potrebovali brezplačen uporabniški račun Broadcom.
3. Prenesite VMware Workstation Pro (Windows/Linux) oziroma VMware Fusion Pro (macOS).
4. Zaženite namestitveni program in sledite navodilom.

### Možnost C: Microsoft Hyper-V (Windows Pro/Enterprise)

Hyper-V je Microsoftovo virtualizacijsko okolje, ki je že vključeno v določene različice operacijskega sistema Windows.

**Pomembno:** Hyper-V ni na voljo v različicah Windows 10/11 Home. Za uporabo potrebujete Windows Pro ali Enterprise.

**Postopek namestitve:**

1. Odprite meni Start in poiščite **Turn Windows features on or off** (Vklop ali izklop funkcij sistema Windows).
2. Na seznamu poiščite in označite **Hyper-V**.
3. Kliknite OK in počakajte na zaključek namestitve.
4. Ponovno zaženite računalnik.
5. V meniju Start poiščite in zaženite **Hyper-V Manager**.

Podrobnejša navodila: [Microsoft – Namestitev Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/install-hyper-v?pivots=windows)

## 2. Namestitev Kali Linux

Kali Linux je operacijski sistem, namenjen preizkušanju kibernetske varnosti.

Za delavnico bomo uporabili **že pripravljeno virtualno napravo (Pre-built Virtual Machine)**, zato klasična namestitev operacijskega sistema ni potrebna.

**Postopek:**

1. Obiščite uradno spletno stran: [Kali Virtual Machines](https://www.kali.org/get-kali/#kali-virtual-machines)
2. Prenesite pripravljeno virtualno napravo za izbrano virtualizacijsko okolje (VirtualBox, VMware ali Hyper-V).
3. Sledite ustreznim navodilom za uvoz virtualne naprave:
    - **VirtualBox:** [Navodila za namestitev](https://www.kali.org/docs/virtualization/import-premade-virtualbox/)
    - **VMware:** [Navodila za namestitev](https://www.kali.org/docs/virtualization/import-premade-vmware/)
    - **Hyper-V:** [Navodila za namestitev](https://www.kali.org/docs/virtualization/import-premade-hyper-v/)
4. Zaženite virtualno napravo Kali Linux.

**Privzeti prijavni podatki:**
- Uporabniško ime: `kali`
- Geslo: `kali`

## 3. Priporočene sistemske zahteve

Za nemoteno delo priporočamo:

- **Procesor:** Intel ali AMD s podporo za virtualizacijo (Intel VT-x / AMD-V).
- **Pomnilnik (RAM):** najmanj 8 GB (priporočeno 16 GB).
- **Prostor na disku:** vsaj 30 GB prostega prostora.
- **Internetna povezava:** potrebna za prenos in uporabo določenih orodij.

**Pred delavnico preverite, da se Kali Linux uspešno zažene in da se lahko prijavite v sistem.**

Če imate težave z zagonom virtualne naprave, preverite, ali je v nastavitvah BIOS/UEFI omogočena strojna virtualizacija (Intel VT-x oziroma AMD-V).

---

**Prosimo, da namestitev opravite pred začetkom delavnice, da bomo lahko čim več časa namenili praktičnemu delu.**

Če boste pri namestitvi ali zagonu naleteli na težave, jih bomo poskusili odpraviti pred začetkom delavnice.

Na voljo bo tudi nekaj **rezervnih virtualnih naprav (VM)**, ki jih boste lahko uporabljali, če vaš računalnik ni dovolj zmogljiv za poganjanje Kali Linuxa ali če vam namestitve ne bo uspelo dokončati.

Se vidimo na delavnici!