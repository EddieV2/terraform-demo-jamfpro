terraform {
  cloud {
    organization = "vartan"
    workspaces {
      tags = ["jamfpro"]
    }
  }
}

terraform {
  required_providers {
    jamfpro = {
      source  = "deploymenttheory/jamfpro"
      version = "~> 0.1.12"
    }
  }
}

provider "jamfpro" {
  jamfpro_instance_fqdn                = var.JAMFPRO_INSTANCE_FQDN
  auth_method                          = var.JAMFPRO_AUTH_METHOD
  client_id                            = var.JAMFPRO_CLIENT_ID
  client_secret                        = var.JAMFPRO_CLIENT_SECRET
  enable_client_sdk_logs               = var.enable_client_sdk_logs
  client_sdk_log_export_path           = var.client_sdk_log_export_path
  hide_sensitive_data                  = var.jamfpro_hide_sensitive_data
  jamfpro_load_balancer_lock           = var.jamfpro_jamf_load_balancer_lock
  token_refresh_buffer_period_seconds  = var.jamfpro_token_refresh_buffer_period_seconds
  mandatory_request_delay_milliseconds = var.jamfpro_mandatory_request_delay_milliseconds
  #basic_auth_username           = var.jamfpro_basic_auth_username
  #basic_auth_password           = var.jamfpro_basic_auth_password
}

variable "JAMFPRO_INSTANCE_FQDN" {
  description = "The Jamf Pro FQDN (fully qualified domain name). Example: https://mycompany.jamfcloud.com"
  sensitive   = true
  default     = ""
}

variable "JAMFPRO_AUTH_METHOD" {
  description = "Auth method chosen for Jamf. Options are 'basic' or 'oauth2'."
  sensitive   = true
  default     = "oauth2"
}

variable "JAMFPRO_CLIENT_ID" {
  description = "The Jamf Pro Client ID for authentication."
  sensitive   = true
  default     = "de5d71ad-64cf-4f60-b326-cc0b6f052da0"
}

variable "JAMFPRO_CLIENT_SECRET" {
  description = "The Jamf Pro Client Secret for authentication."
  sensitive   = true
  default     = "oivLdBJPQIEpVkmk6DoReOLxUnraY6AWQxZ4zUX7v9KAJJrdHbzLZjK00dlM5KsD"
}

variable "jamfpro_basic_auth_username" {
  description = "The Jamf Pro username used for authentication."
  default     = ""
}

variable "jamfpro_basic_auth_password" {
  description = "The Jamf Pro password used for authentication."
  sensitive   = true
  default     = ""
}

variable "enable_client_sdk_logs" {
  description = "Enable client SDK logs."
  default     = false
}

variable "client_sdk_log_export_path" {
  description = "Specify the path to export http client logs to."
  default     = ""
}

variable "jamfpro_hide_sensitive_data" {
  description = "Define whether sensitive fields should be hidden in logs."
  default     = true
}

variable "jamfpro_custom_cookies" {
  description = "Custom cookies for the HTTP client."
  type = list(object({
    name  = string
    value = string
  }))
  default = []
}

variable "jamfpro_jamf_load_balancer_lock" {
  description = "Programmatically determines all available web app members in the load balancer and locks all instances of httpclient to the app for faster executions."
  default     = true
}

variable "jamfpro_token_refresh_buffer_period_seconds" {
  description = "The buffer period in seconds for token refresh."
  default     = 30
}

variable "jamfpro_mandatory_request_delay_milliseconds" {
  description = "A mandatory delay after each request before returning to reduce high volume of requests in a short time."
  default     = 50
}


resource "jamfpro_restricted_software" "restricted_software_001" {
  name                     = "tf-localtest-restrict-high-sierra"
  process_name             = "Install macOS High Sierra.app"
  match_exact_process_name = true
  send_notification        = true
  kill_process             = true
  delete_executable        = true
  display_message          = "This software is restricted and will be terminated."

  # site {
  #   id = 967
  # }

  scope { // scope entities will always be stated asending order. User sort() to sort the list if needed.
    all_computers      = true
  }
}