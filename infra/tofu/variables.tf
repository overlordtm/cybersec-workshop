variable "pve_host" {
  type    = string
  default = "pve.digilab-g.rtfm.si"
}

variable "pve_api_token" {
  type      = string
  sensitive = true
}

variable "node" {
  type    = string
  default = "pve"
}

variable "kali_template_id" {
  description = "VM built by ansible/kali-template.yml"
  type        = number
  default     = 100
}

variable "kali_count" {
  description = "Number of Kali clones (participants udelezenec101..199)"
  type        = number
  default     = 15
  validation {
    condition     = var.kali_count >= 0 && var.kali_count <= 99 && floor(var.kali_count) == var.kali_count
    error_message = "kali_count must be an integer between 0 and 99."
  }
}

variable "participants_csv" {
  description = "n,user,password,access,active — created by guacamole/gen-users.py"
  type        = string
  default     = "../secrets/participants.csv"
}

variable "ssh_public_key" {
  description = "Key the PVE host uses to manage lab machines"
  type        = string
  default     = "../secrets/pve-lab.pub"
}

variable "opnsense_version" {
  description = "Must match opnsense_version in ansible/group_vars/all.yml"
  type        = string
  default     = "26.7"
}

