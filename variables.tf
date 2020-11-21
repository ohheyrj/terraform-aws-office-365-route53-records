variable "zone_id" {
  description = "Route53 Zone ID"
}

variable "domain_name" {
  type        = string
  description = "The full domain name that is being setup"
}

variable "verify_id" {
  description = "The unique ID Microsoft provides to verify your domain, e.g. MS=ms########. Only the numbers are required."
  default     = ""
}

variable "enable_s4b" {
  type        = bool
  description = "Create Route53 records for Skype for Business."
  default     = true
}

variable "enable_exchange" {
  type        = bool
  description = "Create Route53 records for exchange."
  default     = true
}

variable "enable_spf" {
  type        = bool
  description = "Create Route53 SPF record for O365."
  default     = true
}

variable "enable_basic_mdm" {
  type        = bool
  description = "Create Route53 basic MDM records."
  default     = true
}