# Lab segments. No subnets on purpose: the host must not get an address on these vnets,
# otherwise it would route between segments around both firewalls.
# vmbr1 (transit host <-> LAB-GW) is managed by ansible/host.yml because of its NAT hooks.
resource "proxmox_sdn_zone_simple" "lab" {
  id    = "LAB"
  nodes = [var.node]
  ipam  = "pve"
}

locals {
  vnets = ["lab", "fakenet", "acmedmz", "acmelan", "acmeiot"]
}

resource "proxmox_sdn_vnet" "vnet" {
  for_each = toset(local.vnets)
  id       = each.key
  zone     = proxmox_sdn_zone_simple.lab.id
}

resource "proxmox_sdn_applier" "lab" {
  depends_on = [proxmox_sdn_vnet.vnet]
  lifecycle {
    replace_triggered_by = [proxmox_sdn_vnet.vnet]
  }
}
