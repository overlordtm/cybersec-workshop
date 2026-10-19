# Dedicated scanner VM: only one NIC, on the same segment as Kali. Docker NAT
# gives scans source 10.20.0.11, covered by both firewalls' existing scenario rules.
resource "proxmox_download_file" "greenbone_debian" {
  node_name           = var.node
  datastore_id        = "local"
  content_type        = "import"
  url                 = "https://cloud.debian.org/images/cloud/trixie/latest/debian-13-genericcloud-amd64.qcow2"
  file_name           = "greenbone-debian-13.qcow2"
  overwrite_unmanaged = true
}

resource "proxmox_virtual_environment_vm" "greenbone" {
  depends_on      = [proxmox_sdn_applier.lab]
  node_name       = var.node
  vm_id           = 112
  name            = "greenbone"
  tags            = ["lab", "scanner"]
  on_boot         = true
  started         = true
  stop_on_destroy = true
  startup { order = 2 }
  operating_system { type = "l26" }
  cpu {
    cores = 4
    type  = "x86-64-v2-AES"
  }
  memory { dedicated = 8192 }
  scsi_hardware = "virtio-scsi-single"
  boot_order    = ["scsi0"]
  disk {
    interface    = "scsi0"
    datastore_id = "local-zfs"
    import_from  = proxmox_download_file.greenbone_debian.id
    size         = 64
    iothread     = true
    discard      = "on"
  }
  network_device {
    bridge   = "lab"
    model    = "virtio"
    firewall = true
  }
  initialization {
    datastore_id = "local-zfs"
    dns { servers = ["10.20.0.1"] }
    ip_config {
      ipv4 {
        address = "10.20.0.11/24"
        gateway = "10.20.0.1"
      }
    }
    user_account {
      username = "root"
      keys     = [local.ssh_key]
    }
  }
  serial_device { device = "socket" }
  vga { type = "serial0" }
}

resource "proxmox_virtual_environment_firewall_options" "greenbone" {
  node_name     = var.node
  vm_id         = proxmox_virtual_environment_vm.greenbone.vm_id
  enabled       = true
  input_policy  = "DROP"
  output_policy = "ACCEPT"
  macfilter     = true
}

resource "proxmox_virtual_environment_firewall_rules" "greenbone" {
  node_name = var.node
  vm_id     = proxmox_virtual_environment_vm.greenbone.vm_id
  rule {
    type   = "in"
    action = "ACCEPT"
    source = "172.31.255.1"
    proto  = "tcp"
    dport  = "22"
  }
  rule {
    type   = "in"
    action = "ACCEPT"
    source = "10.20.0.0/24"
    proto  = "tcp"
    dport  = "443"
  }
  rule {
    type    = "out"
    action  = "ACCEPT"
    dest    = "10.20.0.1"
    comment = "DNS, proxy and gateway"
  }
  rule {
    type    = "out"
    action  = "DROP"
    dest    = "10.20.0.0/24"
    comment = "Scan ACME, isolate other lab hosts"
  }
}

output "greenbone" {
  value = "VM 112, https://10.20.0.11/ (from Kali); admin password: secrets/greenbone-admin.pass"
}
