# OPNsense VMs from the nano image. They are created stopped; ansible/site.yml injects the
# bootstrap config.xml over the serial console, boots them and configures them over the API.
locals {
  routers = {
    lab-gw  = { id = 110, nets = ["vmbr1", "lab", "fakenet"] }
    acme-fw = { id = 120, nets = ["fakenet", "acmedmz", "acmelan", "acmeiot"] }
  }
}

resource "proxmox_virtual_environment_vm" "router" {
  for_each        = local.routers
  depends_on      = [proxmox_sdn_applier.lab]
  node_name       = var.node
  vm_id           = each.value.id
  name            = each.key
  tags            = ["lab", "router"]
  on_boot         = true
  started         = false
  stop_on_destroy = true

  operating_system { type = "other" }
  cpu {
    cores = 2
    type  = "x86-64-v2-AES"
  }
  memory { dedicated = 2048 }
  scsi_hardware = "virtio-scsi-single"
  boot_order    = ["scsi0"]
  startup { order = 1 }

  disk {
    interface    = "scsi0"
    datastore_id = "local-zfs"
    import_from  = local.opnsense_image
    size         = 16
    iothread     = true
    discard      = "on"
  }

  dynamic "network_device" {
    for_each = each.value.nets
    content {
      bridge   = network_device.value
      model    = "virtio"
      firewall = false
    }
  }

  serial_device { device = "socket" }
  vga { type = "serial0" }

  lifecycle {
    # started by ansible after bootstrap; the temporary config disk (scsi1) comes and goes
    ignore_changes = [started, disk]
  }
}
