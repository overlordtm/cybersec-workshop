terraform {
  required_version = ">= 1.8"
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.117.0"
    }
  }
}

provider "proxmox" {
  endpoint  = "https://${var.pve_host}:8006/"
  api_token = var.pve_api_token # set by lab.sh from infra/secrets/pve-token
  insecure  = false
  ssh {
    agent    = true
    username = "root"
  }
}
