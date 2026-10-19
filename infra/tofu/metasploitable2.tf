# Intentionally vulnerable legacy server on the office LAN. Disk customized offline
# by ansible/host.yml; IDE and e1000 work with the original Ubuntu 8.04 kernel.
resource "proxmox_virtual_environment_vm" "metasploitable2" {
  depends_on      = [proxmox_sdn_applier.lab]
  node_name       = var.node
  vm_id           = 145
  name            = "metasploitable2"
  tags            = ["lab", "acme", "vulnerable"]
  on_boot         = true
  started         = true
  stop_on_destroy = true
  startup { order = 3 }
  operating_system { type = "l26" }
  cpu {
    cores = 1
    type  = "qemu32"
  }
  memory { dedicated = 1024 }
  bios       = "seabios"
  machine    = "pc"
  boot_order = ["ide0"]
  disk {
    interface    = "ide0"
    datastore_id = "local-zfs"
    import_from  = "local:import/metasploitable2-acme.qcow2"
    size         = 8
    file_format  = "raw"
  }
  network_device {
    bridge   = "acmelan"
    model    = "e1000"
    firewall = false
  }
}

output "metasploitable2" {
  value = "VM 145, metasploitable2.acme.lab (172.20.20.30); msfadmin/msfadmin; reachable in visitor/flat"
}
