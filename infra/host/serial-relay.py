#!/usr/bin/env python3
"""Relay a Proxmox VM serial socket to a log file and an input FIFO.

Usage: serial-relay.py VMID
  output -> /root/serial/VMID.log   input <- /root/serial/VMID.in (FIFO)
"""
import os, selectors, socket, sys, time

vmid = sys.argv[1]
d = "/root/serial"
os.makedirs(d, exist_ok=True)
fifo = f"{d}/{vmid}.in"
if not os.path.exists(fifo):
    os.mkfifo(fifo)

while True:
    try:
        s = socket.socket(socket.AF_UNIX)
        s.connect(f"/var/run/qemu-server/{vmid}.serial0")
        break
    except OSError:
        time.sleep(1)

log = open(f"{d}/{vmid}.log", "ab", buffering=0)
fin = os.open(fifo, os.O_RDWR | os.O_NONBLOCK)
sel = selectors.DefaultSelector()
sel.register(s, selectors.EVENT_READ)
sel.register(fin, selectors.EVENT_READ)
while True:
    for key, _ in sel.select():
        if key.fileobj is s:
            data = s.recv(65536)
            if not data:
                sys.exit(0)
            log.write(data)
        else:
            data = os.read(fin, 65536)
            for b in data:  # slow down: the FreeBSD console drops fast pastes
                s.send(bytes([b]))
                time.sleep(0.002)
