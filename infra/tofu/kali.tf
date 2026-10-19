# Kali workstations: linked clones of the template, one per participant.
# Each gets MAC bc:24:11:20:00:NN -> DHCP reservation 10.20.0.(100+NN) on LAB-GW,
# user "kali" with the participant's password (same as the Guacamole login).
locals {
  participants = { for p in csvdecode(file(var.participants_csv)) : tonumber(p.n) => p if p.access == "kali" && p.active == "yes" }
  kalis        = { for n in range(1, var.kali_count + 1) : format("kali-%02d", n) => n }
}

resource "proxmox_virtual_environment_cluster_firewall_security_group" "kali" {
  name    = "kali"
  comment = "Kali workstations: no Kali-to-Kali traffic"

  rule {
    type    = "in"
    action  = "ACCEPT"
    source  = "10.20.0.10"
    proto   = "tcp"
    dport   = "3389"
    comment = "RDP from Guacamole"
  }
  rule {
    type    = "in"
    action  = "ACCEPT"
    source  = "10.20.0.1"
    proto   = "icmp"
    comment = "ping from LAB-GW"
  }
  rule {
    type    = "out"
    action  = "ACCEPT"
    dest    = "10.20.0.1"
    comment = "gateway: DNS, proxy, routing to ACME"
  }
  rule {
    type    = "out"
    action  = "DROP"
    dest    = "10.20.0.0/24"
    comment = "no other lab hosts"
  }
}

resource "proxmox_virtual_environment_vm" "kali" {
  for_each        = local.kalis
  depends_on      = [proxmox_sdn_applier.lab]
  node_name       = var.node
  vm_id           = 200 + each.value
  name            = each.key
  tags            = ["kali", "lab"]
  on_boot         = false
  started         = false
  stop_on_destroy = true

  clone {
    vm_id = var.kali_template_id
    full  = false
  }
  cpu {
    cores = 2
    type  = "x86-64-v2-AES"
  }
  memory { dedicated = 3072 }
  agent { enabled = true }

  network_device {
    bridge      = "lab"
    model       = "virtio"
    mac_address = format("BC:24:11:20:00:%02d", each.value)
    firewall    = true
  }

  initialization {
    datastore_id = "local-zfs"
    ip_config {
      ipv4 { address = "dhcp" }
    }
    user_account {
      username = "kali"
      password = local.participants[each.value].password
    }
  }

  lifecycle {
    # started/stopped with lab.sh start|stop
    ignore_changes = [started]
  }
}

resource "proxmox_virtual_environment_firewall_options" "kali" {
  for_each      = proxmox_virtual_environment_vm.kali
  node_name     = var.node
  vm_id         = each.value.vm_id
  enabled       = true
  input_policy  = "DROP"
  output_policy = "ACCEPT"
  dhcp          = true
  macfilter     = true
}

resource "proxmox_virtual_environment_firewall_rules" "kali" {
  for_each  = proxmox_virtual_environment_vm.kali
  node_name = var.node
  vm_id     = each.value.vm_id
  rule { security_group = proxmox_virtual_environment_cluster_firewall_security_group.kali.name }
}
