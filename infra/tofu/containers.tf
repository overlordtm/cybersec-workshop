# LXC containers: Guacamole in the lab and one container per ACME server (acme/hosts.csv).
# Software inside is installed by ansible/site.yml.
locals {
  ssh_key = trimspace(file(var.ssh_public_key))
  acme    = { for h in csvdecode(file("${path.module}/../acme/hosts.csv")) : h.name => h }
  containers = merge(
    {
      guacamole = { id = 111, segment = "lab", ip = "10.20.0.10", gw = "10.20.0.1", memory = 2048,
      cores = 2, disk = 8, docker = true, domain = "lab.internal", tags = ["lab"] }
    },
    { for name, h in local.acme : name => {
      id     = tonumber(h.id), segment = h.segment, ip = h.ip, gw = "${join(".", slice(split(".", h.ip), 0, 3))}.1",
      memory = tonumber(h.memory_mb), cores = 1, disk = 4, docker = h.docker == "yes",
      domain = "acme.lab", tags = ["acme", h.segment]
    } }
  )
}

resource "proxmox_virtual_environment_container" "ct" {
  for_each      = local.containers
  depends_on    = [proxmox_sdn_applier.lab, proxmox_virtual_environment_vm.router]
  node_name     = var.node
  vm_id         = each.value.id
  tags          = each.value.tags
  unprivileged  = true
  start_on_boot = true
  started       = true

  operating_system {
    template_file_id = proxmox_download_file.debian13.id
    type             = "debian"
  }
  cpu { cores = each.value.cores }
  memory {
    dedicated = each.value.memory
    swap      = 256
  }
  disk {
    datastore_id = "local-zfs"
    size         = each.value.disk
  }
  # keyctl (needed by Docker) may only be set by root@pam, not by an API token:
  # ansible/site.yml adds it with `pct set` for the Docker containers.
  features {
    nesting = true
  }
  startup { order = each.value.tags[0] == "lab" ? 2 : 3 }

  network_interface {
    name     = "eth0"
    bridge   = each.value.segment
    firewall = false
  }

  lifecycle {
    ignore_changes = [features]
  }

  initialization {
    hostname = each.key
    ip_config {
      ipv4 {
        address = "${each.value.ip}/24"
        gateway = each.value.gw
      }
    }
    dns {
      domain  = each.value.domain
      servers = [each.value.gw]
    }
    user_account { keys = [local.ssh_key] }
  }
}
