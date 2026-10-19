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
     .10  Guacamole     .101-.115 peers    .10     ACME-FW (WAN)
     .11  Greenbone     .250 admin         .11-.15 ACME public IPs (1:1 NAT to DMZ)
     .101-.120 Kali                            │
                             ┌─────────────────┴────────────┐
                             │ OPNsense ACME-FW (VM 120)    │
                             └──┬────────────┬───────────┬──┘
                                │            │           │
                    acme-dmz 172.20.10.0/24  │   acme-iot 172.20.30.0/24
                                    acme-lan 172.20.20.0/24
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
management only (LAB-GW allows the host to reach the ACME-FW GUI/SSH and nothing else).

## Egress and the Hetzner abuse risk

Hetzner sends abuse reports when scanning traffic leaves the server. Layers:

1. **LAB-GW does no outbound NAT.** Only LAB-GW's own traffic (172.31.255.2) leaves.
2. **The PVE host SNATs only 172.31.255.2** and drops anything to RFC1918, CGNAT,
   link-local and TEST-NET destinations on `vmbr0` — forwarded and host-originated
   (`infra/host/lab-nat.sh`).
3. Kali and ACME servers reach the internet only through **Squid on LAB-GW** (port 3128,
   ports 80/443 only, **domain allowlist**: Kali mirrors, GitHub, PyPI, Debian, Docker Hub,
   CVE/NVD/Exploit-DB/OWASP). Scanners that do not use the proxy cannot leave the lab.
4. WireGuard is a **split tunnel**: clients get only 10.20.100.1, 198.51.100.0/24 and
   172.20.0.0/16. Their own traffic never goes through the server.

## Firewall policy

### LAB-GW

| From → To | ACME (fakenet, 172.20/16) | LAB-GW | lab | internet |
| --- | --- | --- | --- | --- |
| lab (Kali, Guacamole) | ✓ | DNS, Squid, ping | (L2, see below) | Squid allowlist |
| WireGuard clients | ✓ | DNS, ping | ✗ | ✗ |
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

- DMZ → IoT: **allowed (intentional misconfiguration)**; DMZ → LAN: ✗.
- LAN → anywhere: ✓. IoT → DNS and the update proxy only.
- **Scenario switches** (disabled rules; enable live in ACME-FW → Firewall → Rules):
  - `SCENARIO visitor` – lab and VPN reach ACME LAN ("someone plugged into a meeting room socket").
  - `SCENARIO flat (from outside)`, `SCENARIO flat (DMZ)`, `SCENARIO flat (IoT)` – no segmentation.

## ACME services

One small Debian 13 LXC container per server (VMID 131–153, `infra/acme/hosts.tsv`).
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
| cam01 | 172.20.30.10 | web login + RTSP (554) | default password on the page |
| printer | 172.20.30.11 | 9100, SNMP `public`, web | SNMP leaks location and contact |
| hvac | 172.20.30.12 | Modbus/TCP 502 (no auth), web | IoT that should never be reachable |

DNS: `ns1` is authoritative for `acme.lab`. LAB-GW forwards `acme.lab` to ns1's public
address, ACME-FW to its internal address; both allow private answers for `acme.lab`.

## Participant access

| Access | Path | Credentials |
| --- | --- | --- |
| Browser (default) | `https://lab.digilab-g.rtfm.si/` → Caddy on LAB-GW (Let's Encrypt) → Guacamole (CT 111, 10.20.0.10:8080) → xrdp on Kali-NN | `udelezenecNN` / password from `participants.csv` |
| WireGuard | `lab.digilab-g.rtfm.si:51820`, split tunnel | `infra/secrets/wireguard/udelezenecNN.conf` |

Guacamole uses file auth (`user-mapping.xml`, generated by `infra/guacamole/gen-users.py`).
Each participant sees only their own Kali; the Kali user is `kali` with the same password,
stored in the connection, so the desktop opens directly. `admin` sees all Kalis. The
brute-force ban extension blocks an IP for 5 minutes after 5 failed logins.

OpenVPN is not set up; Guacamole over 443 covers networks that block UDP.

## VM inventory and resources

| VMID | Name | Type | Network | vCPU | RAM |
| --- | --- | --- | --- | --- | --- |
| 100 | kali-tmpl (template) | VM | lab | 2 | 3 GB |
| 110 | lab-gw (OPNsense 26.7) | VM | vmbr1, lab, fakenet | 2 | 2 GB |
| 111 | guacamole | LXC + Docker | lab | 2 | 2 GB |
| 112 | greenbone (planned) | VM | lab | 4 | 8 GB |
| 120 | acme-fw (OPNsense 26.7) | VM | fakenet, acmedmz, acmelan, acmeiot | 2 | 2 GB |
| 131–153 | ACME servers | LXC | acme* | 1 | 0.1–1 GB each (≈3 GB total) |
| 201–215 | kali-01..15 (linked clones) | VM | lab | 2 | 3 GB |

## Repository layout and how to rebuild

Everything runs on the PVE host from `/root/lab` (copies of these files). Secrets
(`infra/secrets/`, git-ignored) hold OPNsense root passwords and API keys, participant
passwords and WireGuard configs.

| Path | What it does |
| --- | --- |
| `host/lab-nat.sh`, `host/interfaces.vmbr1` | transit bridge, DNAT/SNAT, egress drops (hooked into `vmbr1`) |
| `host/serial-relay.py` | VM serial console ↔ log file + FIFO (used to bootstrap OPNsense) |
| `host/opn` | tiny OPNsense API client for the shell |
| `opnsense/bootstrap.py` | turns a stock `config.xml` into a reachable bootstrap config (profiles `lab-gw`, `acme-fw`) |
| `opnsense/install.sh` | creates an OPNsense VM from the nano image and injects the bootstrap config |
| `opnsense/labgw.py`, `opnsense/acmefw.py` | full firewall configuration over the API (idempotent) |
| `guacamole/` | Docker Compose file and user generator |
| `kali/prepare-template.sh`, `kali/clones.sh` | template preparation (inside the VM) and clones |
| `acme/deploy.sh`, `acme/hosts.tsv`, `acme/hosts/`, `acme/files/` | ACME servers |

Order: host network → SDN vnets → `install.sh` + `labgw.py` → Guacamole → Kali template →
`install.sh` + `acmefw.py` → `acme/deploy.sh` → `kali/clones.sh` → snapshot `clean`.

Management GUIs (from your laptop):
`ssh -L 8443:172.31.255.2:8443 -L 8444:198.51.100.10:8443 root@pve.digilab-g.rtfm.si`,
then `https://localhost:8443` (LAB-GW) and `https://localhost:8444` (ACME-FW).

## Operations

- **Clean state:** snapshot ACME containers and both firewalls as `clean`; roll back between workshops.
- **Kali:** recreate clones before each workshop with `kali/clones.sh 1 15`.
- **New participants:** `guacamole/gen-users.py` (keeps existing passwords), copy
  `participants.csv` to `/root/lab/`, rerun `labgw.py` (WireGuard peers), redeploy Guacamole's
  `user-mapping.xml`, run `clones.sh`.
- **Later:** wrap the Proxmox layer in OpenTofu (`bpg/proxmox`) and call these scripts from it.
