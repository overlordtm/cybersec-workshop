# OPNsense nano image: downloaded, signature-checked and unpacked into the import storage by
# ansible/host.yml (Proxmox cannot decompress files of type "import").
locals {
  opnsense_image = "local:import/OPNsense-${var.opnsense_version}-nano-amd64.raw"
}

resource "proxmox_download_file" "debian13" {
  node_name           = var.node
  datastore_id        = "local"
  content_type        = "vztmpl"
  url                 = "http://download.proxmox.com/images/system/debian-13-standard_13.6-1_amd64.tar.zst"
  overwrite_unmanaged = true
}
