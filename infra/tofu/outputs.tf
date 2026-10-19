output "kalis" {
  value = { for k, v in proxmox_virtual_environment_vm.kali : k => "VMID ${v.vm_id}, 10.20.0.${v.vm_id - 100}" }
}

output "containers" {
  value = { for k, v in local.containers : k => "CT ${v.id}, ${v.ip}" }
}
