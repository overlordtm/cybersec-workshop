# Workshop lab infrastructure

Lab environment for the cybersec-2xx workshops, hosted on `pve.digilab-g.rtfm.si`
(Hetzner dedicated server, Ryzen 5 3600 6C/12T, 64 GB RAM, 2× 512 GB NVMe ZFS mirror,
Proxmox VE 9, **one public IPv4**).

The lab emulates the fictional company **ACME** with several network segments and
deliberately exposed services. Participants attack it from Kali desktops in the lab
(through a browser, `https://lab.digilab-g.rtfm.si/`) or from their own laptops (WireGuard).

## Topology

```
                            Internet
                               │
          ┌────────────────────┴─────────────────────┐
          │ PVE host  vmbr0  135.181.74.56            │  DNAT → LAB-GW:
          │                                          │    tcp/80, tcp/443  Caddy → Guacamole
          │                                          │    udp/51820        WireGuard
          └────────────────────┬─────────────────────┘
              vmbr1 "transit"  172.31.255.0/30  (.1 host, .2 LAB-GW)
                               │
          ┌────────────────────┴─────────────────────┐
          │ OPNsense LAB-GW (VM 110)                 │  Caddy, WireGuard, Squid,
          │                                          │  DNS, DHCP, egress lockdown
          └──┬──────────────┬──────────────┬─────────┘
             │              │              │
     lab 10.20.0.0/24   wg 10.20.100.0/24  fakenet 198.51.100.0/24  ("the internet")
     .1   LAB-GW        .1 LAB-GW          .1      LAB-GW
     .10  Guacamole     .101-.199 peers    .10     ACME-FW (WAN)
     .11  Greenbone     .250 admin         .11-.15 ACME public IPs (1:1 NAT to DMZ)
     .101-.199 Kali                            │
                             ┌─────────────────┴────────────┐
                             │ OPNsense ACME-FW (VM 120)    │
                             └──┬────────────┬───────────┬──┘
                                │            │           │
                    acme-dmz 172.20.10.0/24  │   acme-iot 172.20.30.0/24
                                    acme-lan 172.20.20.0/24
                                             │
                                    .30 metasploitable2 (VM 145)
```

### Address plan

| Segment | Proxmox network | Subnet | Gateway | DHCP |
| --- | --- | --- | --- | --- |
| Public | `vmbr0` | 135.181.74.56/26 | Hetzner | — |
| Transit | `vmbr1` (Linux bridge, host has IP) | 172.31.255.0/30 | host .1 | — |
| Lab | SDN vnet `lab` (zone `LAB`) | 10.20.0.0/24 | LAB-GW .1 | LAB-GW (dnsmasq), reservations |
| WireGuard | — (tunnel `wg0`) | 10.20.100.0/24 | LAB-GW .1 | — |
| Fake internet | SDN vnet `fakenet` | 198.51.100.0/24 | LAB-GW .1 | — |
| ACME DMZ | SDN vnet `acmedmz` | 172.20.10.0/24 | ACME-FW .1 | — |
| ACME LAN | SDN vnet `acmelan` | 172.20.20.0/24 | ACME-FW .1 | — |
| ACME IoT | SDN vnet `acmeiot` | 172.20.30.0/24 | ACME-FW .1 | — |

**The SDN vnets have no subnet in Proxmox.** If a subnet is defined, the host gets an IP
on that vnet and routes between segments past both firewalls. The host has an IP only on
`vmbr0` and `vmbr1`. The host firewall drops everything arriving from `vmbr1` and the lab
vnets (IPv4 and IPv6), so the lab cannot reach SSH or the web UI of the host.

The host has routes to 10.20.0.0/16, 172.20.0.0/16 and 198.51.100.0/24 via LAB-GW, for
management only (LAB-GW allows the host to reach the ACME-FW GUI/SSH and Greenbone SSH).

## Egress and the Hetzner abuse risk

Hetzner sends abuse reports when scanning traffic leaves the server. Layers:

1. **LAB-GW does no outbound NAT.** Only LAB-GW's own traffic (172.31.255.2) leaves.
2. **The PVE host SNATs only 172.31.255.2** and drops anything to RFC1918, CGNAT,
   link-local and TEST-NET destinations on `vmbr0` — forwarded and host-originated
   (`infra/host/lab-nat.sh`).
3. Kali and ACME servers reach the internet only through **Squid on LAB-GW** (port 3128,
   ports 80/443 only, **domain allowlist**: Kali mirrors, GitHub, PyPI, Debian, Docker Hub,
   Greenbone's image registry, CVE/NVD/Exploit-DB/OWASP). Scanners that do not use the
   proxy cannot leave the lab.
4. WireGuard is a **split tunnel**: clients get only 10.20.100.1, 198.51.100.0/24 and
   172.20.0.0/16. Their own traffic never goes through the server.

## Firewall policy

### LAB-GW

| From → To | ACME (fakenet, 172.20/16) | LAB-GW | lab | internet |
| --- | --- | --- | --- | --- |
| lab (Kali, Guacamole, Greenbone) | public IPs; internal ranges only in `visitor`/`flat` | DNS, Squid, ping | (L2, see below) | Squid allowlist |
| WireGuard clients | public IPs; internal ranges only in `visitor`/`flat` | DNS, ping | ✗ | ✗ |
| fakenet (ACME) | — | DNS; Squid from 198.51.100.8/29 | ✗ | Squid allowlist |
| WAN | — | 80/443/51820 public; 22/8443 from host | ✗ | — |

No anti-lockout rule; the LAB-GW GUI and SSH listen on WAN only. Kali-to-Kali traffic is
blocked by the PVE firewall security group `kali` on every clone (RDP only from Guacamole).

### ACME-FW (demo of segmentation)

ACME's public block is 198.51.100.10–15. Each DMZ server has its own public IP (1:1 NAT):

| Public | DMZ | Host | Published ports |
| --- | --- | --- | --- |
| 198.51.100.10 | — | ACME-FW | ping only |
| .11 | 172.20.10.11 | www | 80, 443 |
| .12 | 172.20.10.12 | shop | 80, 443 |
| .13 | 172.20.10.13 | mail | 25, 110, 143, 587, 993 |
| .14 | 172.20.10.14 | ns1 | 53 tcp/udp |
| .15 | 172.20.10.15 | vpn | 22 |

Segmentation inside ACME (normal state, i.e. `internet` and `visitor` scenarios):

| From → To | DMZ | LAN | IoT | internet (fake) |
| --- | --- | --- | --- | --- |
| DMZ | — | ✗ | **✓ (intentional misconfiguration)** | DNS, update proxy only |
| LAN (office PCs) | service ports only (`dmz_ports`: 22, 25, 53, 80, 110, 143, 443, 587, 993) | — | ✗ | ✓ |
| IoT | ✗ | ✗ | — | DNS, update proxy only |

The DMZ → IoT hole is not visible from Kali. It is the "pivot" finding: whoever takes over a
DMZ server (e.g. `www`) can reach the camera, printer and HVAC.

## Scenarios

A scenario decides **where the participants are**, from ACME's point of view. There are
three modes, and exactly one is active at a time:

| Mode | Story | Participants (Kali and VPN) reach |
| --- | --- | --- |
| `internet` (default) | attacker on the internet | ACME's public IPs 198.51.100.10–15, published ports only |
| `visitor` | someone plugged a laptop into a socket in ACME's meeting room (office LAN); ACME is segmented | public IPs + **LAN** (all ports) + **DMZ** (service ports, as an office PC) — **no IoT** |
| `flat` | the same visitor, but ACME has no segmentation | public IPs + **all three segments, all ports** |

Switch it from your laptop or on the host:

```sh
./lab.sh scenario visitor          # or internet / flat / status
python3 /root/lab/opnsense/scenario.py visitor     # same, on the PVE host
```

The switch takes effect immediately for new connections and scans; connections that are
already open (e.g. a mounted SMB share) keep working until they close. Guacamole sessions
are not affected. `./lab.sh up` keeps the current mode; `./lab.sh reset` returns to `internet`.

### Which subnets are reachable

From Kali and Greenbone (10.20.0.0/24), and WireGuard (10.20.100.0/24):

| Destination | `internet` | `visitor` | `flat` |
| --- | --- | --- | --- |
| 198.51.100.1 (LAB-GW) | DNS 53, proxy 3128, ping | same | same |
| 198.51.100.10 (ACME-FW) | ping only | same | same |
| 198.51.100.11–15 (public servers) | published ports | same | same |
| 172.20.10.0/24 DMZ | ✗ (not routed) | service ports (`dmz_ports`), ping | all ports |
| 172.20.20.0/24 LAN | ✗ (not routed) | all ports | all ports |
| 172.20.30.0/24 IoT | ✗ (not routed) | ✗ | all ports |

Inside ACME, `flat` also opens DMZ ↔ LAN ↔ IoT completely (matters only for pivoting).

### What you see in nmap

Measured from `kali-01` with `nmap -sn 198.51.100.0/24 172.20.10.0/24 172.20.20.0/24 172.20.30.0/24`
(host discovery) and `nmap -Pn -p 22,53,80,139,443,445,502,554,9100 <host>` (ports):

**`internet`**
- Discovery finds only 198.51.100.1 and .10–.15. The 172.20.x.x ranges stay empty
  ("0 hosts up"): on the internet, private addresses are not routable.
- `198.51.100.11` (www): 80 open, everything else filtered.
- `172.20.x.x` with `-Pn`: every port filtered.

**`visitor`**
- Discovery also finds the internal hosts: DMZ .11–.15, LAN .10, .11, .12, .20, .30, and ACME-FW's
  own addresses .1 in each segment.
- `172.20.20.10` (files): 139 and 445 open → the SMB shares can be listed
  (`smbclient -N -L //172.20.20.10`).
- `172.20.10.11` (www, internal address): 80 open, as from the internet.
- `172.20.30.12` (hvac): all filtered. IoT is protected by segmentation.

**`flat`**
- Discovery: same hosts as `visitor`.
- `172.20.30.12` (hvac): 80 and **502 (Modbus)** open; the camera (80, 554) and the printer
  (80, 9100, SNMP 161/udp) also become visible.
- Everything else as in `visitor`.

The workshop story is the step from `visitor` to `flat`. The same scan from the same meeting
room socket suddenly shows the building controller and the cameras: that is exactly what
segmentation is for.

Notes for reading the output:
- In `visitor` mode, discovery may also report IoT addresses as up although all their
  ports are filtered. nmap's discovery probes get answered at the network level even though
  no service can be reached. Port results are what counts.
- Ports with no service behind them show as `filtered`, not `closed`, also where the firewall
  passes them (e.g. 443 on www). Don't use `closed` vs `filtered` in the workshop to explain
  firewall behaviour; open vs not open is reliable.

### Where the changes are applied

A scenario rule is a firewall rule whose description starts with `SCENARIO <modes>:`.
`scenario.py` turns a rule on when the chosen mode is in `<modes>` and off otherwise. The
rules are defined in `opnsense/labgw.py` and `opnsense/acmefw.py`. The firewall GUIs show them
under Firewall → Rules.

| Firewall | Rule | `internet` | `visitor` | `flat` |
| --- | --- | --- | --- | --- |
| LAB-GW, LAB | `SCENARIO visitor+flat: LAB to ACME internal` (lab → 172.20.0.0/16) | off | **on** | **on** |
| LAB-GW, WireGuard | `SCENARIO visitor+flat: VPN to ACME internal` | off | **on** | **on** |
| ACME-FW, WAN | `SCENARIO visitor: like a LAN PC (LAN)` (lab_nets → LAN, any) | off | **on** | off |
| ACME-FW, WAN | `SCENARIO visitor: like a LAN PC (DMZ services)` (→ DMZ, `dmz_ports`) | off | **on** | off |
| ACME-FW, WAN | `SCENARIO visitor: like a LAN PC (ping DMZ)` | off | **on** | off |
| ACME-FW, WAN | `SCENARIO flat: outside to all segments` (lab_nets → 172.20.10–30.0/24, any) | off | off | **on** |
| ACME-FW, DMZ | `SCENARIO flat: DMZ to all segments` | off | off | **on** |
| ACME-FW, LAN | `SCENARIO flat: LAN to all segments` | off | off | **on** |
| ACME-FW, IoT | `SCENARIO flat: IoT to all segments` | off | off | **on** |

Why both firewalls are involved: ACME-FW filters after the 1:1 NAT, so it cannot tell
"came in for the public IP 198.51.100.11" from "came in for 172.20.10.11". Without the LAB-GW
rule, participants could therefore reach the DMZ by its private addresses even in the
`internet` mode. LAB-GW plays the internet and only routes ACME's private ranges when a
scenario puts the participants inside ACME.

## ACME services

Most servers use a small Debian 13 LXC container (VMID 131–153, `infra/acme/hosts.csv`).
Metasploitable 2 uses its original Ubuntu VM (VMID 145), managed separately in OpenTofu.
Software whose *version* matters for the CVE exercise runs as a Docker container with host
networking inside its LXC. Website content is in Slovenian.

| Host | IP | Service | What participants find |
| --- | --- | --- | --- |
| www | 172.20.10.11 | Apache **2.4.49** (Docker) | CVE-2021-41773 in the banner; `robots.txt` → `/backup/config.php.bak` (password), `/admin/`, HTML comment, employee names |
| shop | 172.20.10.12 | OWASP Juice Shop v20.3.0 | exercise 3.3 (requests, forms, cookies) |
| mail | 172.20.10.13 | Postfix + Dovecot | SMTP/IMAP/POP3 banners; mailbox names = employees |
| ns1 | 172.20.10.14 | BIND, **AXFR allowed** | zone transfer reveals internal hosts |
| vpn | 172.20.10.15 | **OpenSSH 7.4p1** (Docker, Debian 9) | old version (CVE-2018-15473); password from www backup works |
| files | 172.20.20.10 | Samba, guest share `javno` | PDF with author metadata, device list with IPs |
| intranet | 172.20.20.11 | nginx, HTTP Basic auth | credentials over plain HTTP |
| nas | 172.20.20.12 | File Browser 2.23 (Docker) | default `admin` / `admin` |
| hr-pc | 172.20.20.20 | Samba share `Dokumenti` | open share on a workstation |
| metasploitable2 | 172.20.20.30 | Metasploitable 2 legacy Ubuntu VM | intentionally vulnerable services; `msfadmin` / `msfadmin` |
| cam01 | 172.20.30.10 | web login + RTSP (554) | default password on the page |
| printer | 172.20.30.11 | 9100, SNMP `public`, web | SNMP leaks location and contact |
| hvac | 172.20.30.12 | Modbus/TCP 502 (no auth), web | IoT that should never be reachable |

DNS: `ns1` is authoritative for `acme.lab`. LAB-GW forwards `acme.lab` to ns1's public
address, ACME-FW to its internal address; both allow private answers for `acme.lab`.

### Metasploitable 2 placement and lifecycle

[Metasploitable 2](https://docs.rapid7.com/metasploit/metasploitable-2/) represents an
unmaintained internal server, so it lives on the **office LAN** at
`172.20.20.30` (`metasploitable2.acme.lab`). This exposes its full set of services
in `visitor` and `flat`; it is unreachable from participants in `internet` mode.
The existing DMZ service allowlist would hide many of its services. No public IP,
NAT mapping or additional firewall rule is added. Its single NIC connects only to
`acmelan`; the existing LAB-GW egress controls still apply. Like other LAN hosts,
it can reach office peers and DMZ service ports; IoT opens only in `flat`.

`./lab.sh up` downloads the ZIP linked by Rapid7 from SourceForge on the PVE host,
extracts its VMDK, converts it to QCOW2, and uses libguestfs **offline, without
network access** to set its static address and remove VMware's persistent NIC
mapping. The guest is not upgraded or passed through the Debian LXC provisioning
scripts, preserving the deliberately vulnerable services and default credentials.
The VM uses legacy IDE disk and e1000 NIC emulation for the old Ubuntu kernel.

The prepared image is cached at `/var/lib/vz/import/metasploitable2-acme.qcow2`;
subsequent runs reuse it. VM 145 receives a `clean` snapshot and participates in
`./lab.sh reset` and `./lab.sh down`. The import cache remains after teardown,
like the OPNsense image. Access its console through Proxmox using
`msfadmin` / `msfadmin`; it has no cloud-init or guest agent.

After applying with `cd infra && ./lab.sh up`, switch to `visitor` and verify from
Kali with `nmap -sV -p 21,22,23,80,139,445,3306,5432,8180 172.20.20.30`.
Repeat in `internet` mode with `-Pn`: those ports should be filtered. Check
`dig metasploitable2.acme.lab` and verify that a workshop reset restores the VM.

## Participant access

| Access | Path | Credentials |
| --- | --- | --- |
| Browser (default) | `https://lab.digilab-g.rtfm.si/` → Caddy on LAB-GW (Let's Encrypt) → Guacamole (CT 111, 10.20.0.10:8080) → xrdp on Kali-NN | `udelezenec101…199` / password from `participants.csv` |
| WireGuard | `lab.digilab-g.rtfm.si:51820`, split tunnel | `infra/secrets/wireguard/udelezenec201…299.conf` |
| Greenbone (instructor) | `https://10.20.0.11/` from a hosted Kali browser | `admin` / password in `infra/secrets/greenbone-admin.pass` |

Guacamole uses file auth (`user-mapping.xml`, generated by `infra/guacamole/gen-users.py`).
Only active hosted participants get Guacamole accounts and Kali clones. WireGuard
participants get only a VPN identity/config, with no Guacamole account, desktop, or password.
Each hosted participant sees only their own Kali; the Kali user is `kali` with the same password,
stored in the connection, so the desktop opens directly. `admin` sees all Kalis and
retains a management WireGuard config (`wireguard/admin.conf`, .250). The
brute-force ban extension blocks an IP for 5 minutes after 5 failed logins.

OpenVPN is not set up; Guacamole over 443 covers networks that block UDP.

## VM inventory and resources

| VMID | Name | Type | Network | vCPU | RAM |
| --- | --- | --- | --- | --- | --- |
| 100 | kali-tmpl (template) | VM | lab | 2 | 3 GB |
| 110 | lab-gw (OPNsense 26.7) | VM | vmbr1, lab, fakenet | 2 | 2 GB |
| 111 | guacamole | LXC + Docker | lab | 2 | 2 GB |
| 112 | greenbone (Debian 13 + Community Containers, 64 GB disk) | VM | lab | 4 | 8 GB |
| 120 | acme-fw (OPNsense 26.7) | VM | fakenet, acmedmz, acmelan, acmeiot | 2 | 2 GB |
| 131–135, 141–144, 151–153 | ACME servers | LXC | acme* | 1 | 0.1–1 GB each (≈3 GB total) |
| 145 | metasploitable2 | VM | acmelan | 1 | 1 GB |
| 201–215 | kali-01..15 (linked clones) | VM | lab | 2 | 3 GB |

## Greenbone vulnerability scanner

Greenbone is implemented and provisioned by `./lab.sh up`, on the same `lab`
segment as Kali. Its scan access follows the active `internet`, `visitor` or
`flat` scenario automatically.

`./lab.sh up` also creates VM 112: Debian 13, 4 vCPU, 8 GB RAM and a 64 GB disk,
with **one NIC on `lab`, 10.20.0.11/24, gateway/DNS 10.20.0.1**. Ansible installs
Docker and the [official Greenbone Community Containers](https://greenbone.github.io/docs/latest/22.4/container/).
The vendored `greenbone/compose.yaml` binds the UI to the lab IP; the override sets
the UI hostname and a Docker subnet that does not overlap ACME. Container traffic
is masqueraded by Docker to 10.20.0.11, so scans traverse LAB-GW and ACME-FW exactly
as Kali scans do. No change to `scenario.py` is needed.

From a hosted Kali browser, open **https://10.20.0.11/** and accept the generated
self-signed certificate. Login: `admin`, password in `infra/secrets/greenbone-admin.pass`
on your laptop. Treat this as an instructor account; create separate Greenbone users
in the UI if participants need their own scans. Kali's PVE firewall allows only TCP
443 to this host. Greenbone SSH is restricted to the PVE host, and its UI is not
published through Caddy or made accessible to WireGuard clients.

Images and feed data download over HTTPS through the existing Squid proxy, using
the added `registry.community.greenbone.net` allowlist entry. Direct internet egress
stays blocked; rsync feed access is unnecessary. First provisioning can take hours
and needs several GB of downloads. Once it completes, check **Administration → Feed
Status** and **Configuration → Scan Configs** (the `Full and fast` config should be
available) before scanning. A running UI alone does not mean the feeds are ready.
The VM adds 8 GB of reserved RAM; allow room for it when choosing how many of the
3 GB Kali VMs to run on the 64 GB host.

For a scenario comparison, use explicit IP targets: public servers
`198.51.100.11–15`, DMZ `172.20.10.11–15`, LAN `172.20.20.10–12,172.20.20.20,172.20.20.30`, and
IoT `172.20.30.10–12`. Use a TCP port list that includes the demonstration services
(e.g. 22, 53, 80, 139, 443, 445, 502, 554, 9100), and TCP-based alive tests or
**Consider Alive** when comparing filtered hosts. Stop active scans before switching
with `./lab.sh scenario internet|visitor|flat`, then run a fresh scan and label its
report with the mode. The expected reachability is the same as the table above.
Reports already saved do not change, and existing firewall states can survive a switch.

The scanner's Docker volumes retain users, tasks, reports and feeds across `up`,
reboots and `reset`. It is deliberately excluded from the `clean` snapshots so
scenario reports remain available for comparison. `down` destroys its VM and data.
Normal `up` runs reuse installed images; the upstream images use rolling tags.
Update services and feeds explicitly during maintenance, with no scans running:

```sh
ssh root@pve.digilab-g.rtfm.si
ssh greenbone
cd /opt/greenbone
docker compose ps
docker compose pull
docker compose up -d
docker compose logs --tail=100 gvmd ospd-openvas
```

Wait for feed import to finish again after updating. When upgrading the stack,
review the [current upstream Compose file](https://greenbone.github.io/docs/latest/_static/compose.yaml)
against the vendored copy as well, preserving the lab bindings and override.

## Setup and teardown

Everything is driven from your laptop with `infra/lab.sh`:
**OpenTofu** creates the Proxmox resources, **Ansible** configures the host and what runs inside
the machines (it reuses the scripts in `host/`, `opnsense/`, `acme/`, `guacamole/`, `kali/`).

Requirements on the laptop: `tofu` (≥ 1.8), `ansible` with `ansible.posix`, `python3`,
`openssl`, `rsync`, and SSH access as `root@pve.digilab-g.rtfm.si` (key in your agent).

```sh
cd infra
./lab.sh up          # build/update using remembered counts (initial defaults: 15 hosted, 0 WG)
./lab.sh up 15 10    # 15 hosted Kali accounts + 10 participants using their own Kali via WG
./lab.sh up 20       # change hosted count to 20, keep remembered WG count
./lab.sh up 0 20     # WG-only workshop; removes existing hosted Kali clones
./lab.sh up 15 0     # hosted-only workshop; removes participant WG access
./lab.sh start       # start all Kali clones before the workshop (stop: ./lab.sh stop)
./lab.sh start 3 4   # start kali-03 and kali-04 only
./lab.sh status

./lab.sh reset       # between workshops: firewalls, Guacamole and ACME back to "clean",
                     # fresh Kali clones (participants keep their passwords)
./lab.sh kalis       # fresh Kali clones only

./lab.sh down        # destroy all lab VMs/containers/networks (keeps Kali template + host layer)
./lab.sh down --all  # also remove Kali template, vmbr1/NAT, host firewall lines, API token
```

### Applying the participant split to an existing lab

From the repository root:

```sh
cd infra
# Keep a private backup before the one-time CSV migration.
backup_dir=$(mktemp -d)
cp -a secrets "$backup_dir/secrets"
echo "Private backup: $backup_dir/secrets"
./lab.sh up 15 10    # choose hosted Kali and WireGuard participant counts
./lab.sh start
```

This example creates `udelezenec101`–`udelezenec115` for Guacamole and
`udelezenec201`–`udelezenec210` for WireGuard. Hosted account 101 connects to
`kali-01` (VM 201, 10.20.0.101); WG account 201 uses 10.20.100.101. The two
number ranges identify access types, not Proxmox VM IDs.

Existing `udelezenec01`–`NN` accounts migrate to the hosted `1xx` names with the
same passwords; the `admin` password is preserved. Tell hosted participants their
new usernames. Old shared participant VPN peers and their generated config files
are removed; distribute the new `secrets/wireguard/udelezenec2xx.conf` files only
to participants bringing their own Kali. Old participant VPN configs stop working.
Only the administrator keeps both access methods.

Counts are independent and remembered. Lowering the hosted count destroys excess
Kali VMs (including their desktop data); lowering the WG count revokes excess peers
and removes their generated configs locally and on the host. Inactive CSV rows and
VPN keys remain private for reuse if counts rise again. Use `active=yes` when
reading the CSV to distribute accounts. `./lab.sh reset` reapplies current accounts
after restoring snapshots, then recreates the hosted desktops.

For manual Ansible runs, pass both counts explicitly, e.g.
`ansible-playbook site.yml -e kali_count=15 -e wg_count=10` from `infra/ansible/`.
OpenTofu's `kali_count` controls only hosted VMs and must match the CSV's active
hosted accounts; `lab.sh up` keeps these in sync.

`./lab.sh up` from zero takes about 25 minutes with an existing Kali template, plus 30–60
minutes when the template has to be built and potentially hours for Greenbone's initial
feed setup. It runs, in order:

| Step | Tool | What |
| --- | --- | --- |
| 1 | `guacamole/gen-users.py` | participants and passwords (`secrets/participants.csv`, kept on re-runs) |
| 2 | `ansible/host.yml` | vmbr1 + NAT/egress rules, host firewall lines, helper tools, SSH key, API token for OpenTofu, OPNsense nano image (checksum + signature verified, unpacked into the import storage) |
| 3 | `tofu apply` | SDN zone and vnets, Debian 13 LXC template and scanner cloud image, LAB-GW/ACME-FW/Greenbone VMs, Guacamole and ACME containers, Kali firewall group (Kali clones only if the template exists) |
| 4 | `ansible/site.yml` | `keyctl` for the Docker containers (only `root@pam` may set it, not an API token), OPNsense bootstrap over the serial console, firmware + plugins, full config over the API (`labgw.py`, `acmefw.py`), WireGuard configs, Guacamole, Greenbone, ACME servers, `clean` snapshots (excluding Greenbone) |
| 5 | `ansible/kali-template.yml` | only if VM 100 is missing: build the Kali template from Kali's QEMU image |
| 6 | `tofu apply` | Kali clones |

All steps are idempotent: re-running `./lab.sh up` after a change only applies the change.
Typical changes:

| Change | Where | Then |
| --- | --- | --- |
| Firewall rules, Squid allowlist, WireGuard | `opnsense/labgw.py`, `opnsense/acmefw.py` | `./lab.sh up` |
| ACME service | `acme/hosts/NAME.sh`, `acme/files/NAME/` | `ssh root@pve 'FORCE=1 sh /root/lab/acme/provision.sh NAME'` after `./lab.sh up` (or recreate: `tofu -chdir=tofu apply -replace='proxmox_virtual_environment_container.ct["NAME"]'`, then `./lab.sh up`) |
| New ACME host | `acme/hosts.csv` + `acme/hosts/NAME.sh`; add the ID to `snapshot_cts` in `ansible/group_vars/all.yml` | `./lab.sh up` |
| Participant counts | `./lab.sh up KALI_COUNT WG_COUNT` (each 0–99) | Counts saved in `secrets/kali-count` and `secrets/wg-count` |

OpenTofu state is local (`infra/tofu/terraform.tfstate`, git-ignored). Keep it: without it
OpenTofu no longer knows what it created. The API token is in `secrets/pve-token`.

### Distributing credentials through the exercise site

Participants open `cybersec-201/vaje/dostop/` (linked from the exercises) and enter
one personal claim code. Hosted participants see their Guacamole login and browser
instructions; WireGuard participants download their own `.conf` and see setup,
connection, verification, and disconnect commands for their Kali VM. Admin access
is never exported.

After provisioning, export locally from `infra/`:

```sh
# One-time dependency setup; the virtual environment stays in ignored secrets/.
python3 -m venv secrets/credentials-venv
secrets/credentials-venv/bin/pip install -r requirements-credentials.txt

# Run after ./lab.sh up so the CSV and WireGuard configs are current.
CREDENTIALS_PYTHON=secrets/credentials-venv/bin/python ./lab.sh credentials
```

The exporter writes:

- **Public:** `cybersec-201/vaje/dostop/credentials.json`, containing only encrypted
  payloads and cryptographic metadata. Commit this file with the access page.
- **Private:** `infra/secrets/claim-codes.csv`, containing `user,access,claim_code,active`.
  Give each participant only their own active code and the page URL, e.g. on a
  printed slip or in a direct message. Keep the list and backups private.

From the repository root, build and publish through the existing Pages workflow:

```sh
npm run build
git add cybersec-201/vaje/dostop cybersec-201/vaje/VAJE.md vite.config.js
git add .gitignore infra/export-credentials.py infra/requirements-credentials.txt
git add infra/tests/test_credential_export.py infra/lab.sh infra/README.md
git commit -m "Add encrypted participant credential pickup"
git push
```

The existing GitHub Pages workflow publishes pushes to `main`; pushing a branch
requires merging it first. The claim page must be served over HTTPS (localhost
also works for development). No backend, analytics, or external script is required.
Codes are entered in a form, never in URLs. The page decrypts in browser memory,
without sending codes to the server or saving credentials to browser storage.
Downloaded configs and passwords explicitly copied to the clipboard remain under
the participant's control.

Codes use four random uppercase letters and four random digits, e.g. `ABCD-1234`
(about 32 bits of randomness). Duplicate codes are rejected, including codes retained
for inactive participants. Older long codes migrate automatically on export.
A PBKDF2-SHA256 derivation with a random per-export lookup salt, followed by
SHA-256, identifies each code’s blob, so checking guesses also requires the slow
derivation step; PBKDF2-SHA256 (600,000 iterations, random 16-byte salt) derives an AES-256-GCM
key, and each payload has a fresh 12-byte nonce and authenticated lookup ID. The
format is shared by the Python exporter and native browser Web Crypto code.
See [Web Crypto key derivation](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/deriveKey).
No participant usernames or access types appear unencrypted in the bundle.

Rerun `./lab.sh credentials` after changing accounts or WG configurations, then
commit and publish the new bundle. Existing claim codes are reused, while inactive
accounts disappear from the current bundle. `./lab.sh credentials --rotate` generates
new codes for all active participants; redistribute those codes after publishing.

**These are reusable claim codes, not one-time tokens.** Old bundles remain in Git
history and may have been downloaded. Changing a claim code or deleting a blob
cannot revoke credentials someone already has. For a leaked code, first change the
actual Kali/Guacamole password or revoke/regenerate the WG peer key, apply the lab
configuration, then export with `--rotate` and republish. Never publish
`participants.csv`, `claim-codes.csv`, raw `.conf` files, `wg-keys.json`, or secrets
backups. The existing `infra/secrets/` ignore rule covers the private inputs.

### Printing claim-code slips

From `infra/`, install or update the credential tools, then generate the PDF:

```sh
secrets/credentials-venv/bin/pip install -r requirements-credentials.txt
CREDENTIALS_PYTHON=secrets/credentials-venv/bin/python ./lab.sh claim-pdf
```

Output: `infra/secrets/claim-slips.pdf` (private and Git-ignored). Print on **A4,
100% / actual size**, single-sided, and cut along the dashed grid. Each page holds
**10 slips** (2 columns × 5 rows). Each slip contains the participant username,
access type, large claim code, short instructions, and the public access-page URL
with a QR code. The QR contains only the public URL; participants enter their code
on the page. Only active hosted Kali and WireGuard entries are printed; admin and
inactive entries are excluded. Codes are read as-is and are never regenerated by
this command. Rows are sorted by participant username.

The default page URL is
`https://overlordtm.github.io/cybersec-workshop/cybersec-201/vaje/dostop/`.
Override it if using a custom domain; optionally print one access type at a time:

```sh
CREDENTIALS_PYTHON=secrets/credentials-venv/bin/python ./lab.sh claim-pdf \
  --url https://example.org/cybersec-201/vaje/dostop/ \
  --access kali --output secrets/hosted-kali-slips.pdf
```

The underlying script also accepts an arbitrary CSV via `--input PATH`:
`secrets/credentials-venv/bin/python print-claim-codes.py --help`.
After changing accounts or rotating codes, first rerun `./lab.sh credentials` and
publish its encrypted bundle, then regenerate the PDF so the printed codes match.

### Secrets (`infra/secrets/`, git-ignored)

| File | Content |
| --- | --- |
| `claim-slips.pdf` | Private printable claim-code slips (10 per A4 page) |
| `claim-codes.csv` | Private per-participant claim codes for the encrypted credential page |
| `participants.csv` | `n,user,password,access,active` – `access` is `kali`, `wireguard`, or `admin`; only `active=yes` entries are provisioned. Hosted login password = Kali password; WG passwords are empty. Inactive credentials stay for reuse. |
| `wireguard/udelezenec2xx.conf`, `wireguard/admin.conf` | Active WireGuard client configs; no configs for hosted participants |
| `labgw-*`, `acmefw-*` | OPNsense root passwords and API keys |
| `pve-token`, `pve-lab.pub` | OpenTofu API token, the host's SSH key for lab machines |

### Repository layout

| Path | What it does |
| --- | --- |
| `lab.sh` | entry point (see above) |
| `tofu/` | OpenTofu: networks, images, routers, containers, Kali, Greenbone and `metasploitable2.tf` |
| `ansible/` | `host.yml`, `site.yml`, `kali-template.yml`, `reset.yml`, `teardown-host.yml` |
| `host/` | `lab-nat.sh` (NAT and egress drops on vmbr1), `serial-relay.py`, `opn` (shell API client) |
| `opnsense/` | `bootstrap.py` + `config-26.7-default.xml` (bootstrap config), `bootstrap-vm.sh` (serial injection), `firmware.sh`, `labgw.py`, `acmefw.py`, `scenario.py`, `opnapi.py` |
| `guacamole/` | Docker Compose file, `gen-users.py` |
| `kali/` | `build-template.sh` (from Kali's QEMU image), `prepare-template.sh` (inside the VM) |
| `acme/` | `hosts.csv`, `provision.sh`, `hosts/NAME.sh`, `files/NAME/` |
| `metasploitable2/` | `prepare-image.sh`: download and customize the legacy VM disk offline |

### Management access

```sh
ssh -L 8443:172.31.255.2:8443 -L 8444:198.51.100.10:8443 root@pve.digilab-g.rtfm.si
```
LAB-GW: `https://localhost:8443`, ACME-FW: `https://localhost:8444` (user `root`, passwords
in `secrets/`). From the host: `ssh lab-gw`, `ssh acme-fw`, `opn lab-gw GET /api/...`.

Scenario switch during the workshop: `./lab.sh scenario internet|visitor|flat|status`
(see [Scenarios](#scenarios)).

Local participant provisioning regression checks (no live infrastructure access):

```sh
python3 -m unittest discover -s infra/tests -v
```
