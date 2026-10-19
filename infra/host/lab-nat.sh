#!/bin/sh
# NAT and forwarding between the public interface (vmbr0) and the lab transit (vmbr1).
# Called from /etc/network/interfaces (post-up/post-down on vmbr1). Idempotent.
set -e

PUB_IF=vmbr0
PUB_IP=135.181.74.56
TR_IF=vmbr1
LABGW=172.31.255.2

# Ports forwarded from the public IP to LAB-GW
TCP_PORTS="80,443,1194"
UDP_PORTS="51820"

# Destinations that must never leave through vmbr0 (Hetzner abuse reports)
NOEGRESS="10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 100.64.0.0/10 192.0.2.0/24 198.51.100.0/24 203.0.113.0/24 169.254.0.0/16"

chain() { # table chain parent position
    iptables -t "$1" -N "$2" 2>/dev/null || iptables -t "$1" -F "$2"
    iptables -t "$1" -C "$3" -j "$2" 2>/dev/null || iptables -t "$1" -I "$3" "$4" -j "$2"
}

unchain() { # table chain parent
    iptables -t "$1" -D "$3" -j "$2" 2>/dev/null || true
    iptables -t "$1" -F "$2" 2>/dev/null || true
    iptables -t "$1" -X "$2" 2>/dev/null || true
}

if [ "$1" = down ]; then
    unchain nat LAB-PRE PREROUTING
    unchain nat LAB-POST POSTROUTING
    unchain filter LAB-FWD FORWARD
    unchain filter LAB-IN INPUT
    unchain filter LAB-OUT OUTPUT
    exit 0
fi

# DNAT public ports to LAB-GW
chain nat LAB-PRE PREROUTING 1
iptables -t nat -A LAB-PRE -i $PUB_IF -d $PUB_IP -p tcp -m multiport --dports $TCP_PORTS -j DNAT --to-destination $LABGW
iptables -t nat -A LAB-PRE -i $PUB_IF -d $PUB_IP -p udp -m multiport --dports $UDP_PORTS -j DNAT --to-destination $LABGW

# SNAT only LAB-GW itself (Squid, updates)
chain nat LAB-POST POSTROUTING 1
iptables -t nat -A LAB-POST -o $PUB_IF -s $LABGW -j SNAT --to-source $PUB_IP

# Forwarding policy for the transit
chain filter LAB-FWD FORWARD 1
iptables -A LAB-FWD -o $TR_IF -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A LAB-FWD -i $TR_IF -o $PUB_IF -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A LAB-FWD -i $PUB_IF -o $TR_IF -d $LABGW -p tcp -m multiport --dports $TCP_PORTS -m conntrack --ctstate DNAT -j ACCEPT
iptables -A LAB-FWD -i $PUB_IF -o $TR_IF -d $LABGW -p udp -m multiport --dports $UDP_PORTS -m conntrack --ctstate DNAT -j ACCEPT
for net in $NOEGRESS; do
    iptables -A LAB-FWD -i $TR_IF -o $PUB_IF -d "$net" -j DROP
done
iptables -A LAB-FWD -i $TR_IF -o $PUB_IF -s $LABGW -j ACCEPT
iptables -A LAB-FWD -i $TR_IF -j DROP
iptables -A LAB-FWD -o $TR_IF -j DROP

# The lab must not reach the host itself (SSH, web UI); allow ping for debugging
chain filter LAB-IN INPUT 1
iptables -A LAB-IN -i $TR_IF -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A LAB-IN -i $TR_IF -p icmp --icmp-type echo-request -j ACCEPT
iptables -A LAB-IN -i $TR_IF -j DROP

# The host itself must not send lab or private destinations out to Hetzner either
chain filter LAB-OUT OUTPUT 1
for net in $NOEGRESS; do
    iptables -A LAB-OUT -o $PUB_IF -d "$net" -j DROP
done
