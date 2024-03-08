resource "jamfpro_policies" "jamfpro_policy_001" {
  general {
    name                        = "[policy]-test-001"
    enabled                     = false
    trigger                     = "EVENT" // "USER_INITIATED" for self self trigger , "EVENT" for an event trigger
    trigger_checkin             = false
    trigger_enrollment_complete = false
    trigger_login               = false
    trigger_logout              = false
    trigger_network_state_changed = false
    trigger_startup             = false
    frequency                   = "Once per computer"
    retry_event                 = "none"
    retry_attempts              = -1
    notify_on_each_failed_retry = false
    location_user_only          = false
    target_drive                = "/"
    offline                     = false

    network_limitations {
      minimum_network_connection = "No Minimum"
      any_ip_address             = false
    }

    override_default_settings {
      target_drive         = "/"
      distribution_point   = "default"
      force_afp_smb        = false
      sus                  = "default"
    }

    site {
      id   = -1
      name = "None"
    }
  }
    scripts {
    script {
      id        = data.jamfpro_script.jamfpro_script_001_data.id
      name = data.jamfpro_script.jamfpro_script_001_data.name
      priority  = "After"
      parameter4 = "Macintosh HD"
      parameter5 = "APFS"
      parameter6 = ""
      parameter7 = ""
      parameter8 = "100"
      parameter9 = ""
      parameter10 = ""
      parameter11 = ""
    }
  }

  self_service {
    use_for_self_service        = true
    self_service_display_name   = ""
    install_button_text         = "Install"
    reinstall_button_text       = ""
    self_service_description    = ""
    force_users_to_view_description = false

    self_service_icon {
      id        = 0
    }

    feature_on_main_page        = false
  }
  
  

}



# resource "jamfpro_policies" "example_policy" {
#   count    = 1
#   general {
#     name                          = "[policy]-test-v0.1-${format("%03d", count.index + 1)}"
#     enabled                       = false
#     trigger                       = "EVENT" // "EVENT" / "USER_INITIATED"
#     trigger_checkin               = false
#     trigger_enrollment_complete   = false
#     trigger_login                 = false
#     trigger_logout                = false
#     trigger_network_state_changed = false
#     trigger_startup               = false
#     frequency                     = "Once per computer" // "Once per computer", "Once per user per computer", "Once per user", "Once every day", "Once every week", "Once every month", "Ongoing",
#     retry_event                   = "none"  // "none" / "check-in" / "trigger"
#     retry_attempts                = -1
#     notify_on_each_failed_retry   = false
#     location_user_only            = false
#     offline                       = false
#     target_drive = "/"

#     category {
#       id   = -1
#       name = "No category assigned"
#     }

#     network_limitations {
#       any_ip_address   = true
#       minimum_network_connection = "No Minimum"
#     }

#     override_default_settings {
#       target_drive         = "/"
#       distribution_point   = "default"
#       force_afp_smb        = false
#       sus                  = "default"
#     }
#     site {
#     }
#   }

#   scope {
#     all_computers    = false
#   }

#   self_service {
#     use_for_self_service        = false
#     self_service_display_name   = ""
#     install_button_text         = "Install"
#     reinstall_button_text       = ""
#     self_service_description    = ""
#     force_users_to_view_description = false

#     self_service_icon {
#       id        = 0
#     }

#     feature_on_main_page        = false
#   }

#   disk_encryption {
#     action = "apply"
#     disk_encryption_configuration_id = 1
#     auth_restart = true
#   }
# /*
#   scripts {
#     script {
#       id        = 3859
#       name = "[scpt]-add-apfs-volume-to-startup-container-v8.0"
#       priority  = "After"
#       parameter4 = "Macintosh HD"
#       parameter5 = "APFS"
#       parameter6 = ""
#       parameter7 = ""
#       parameter8 = "100"
#       parameter9 = ""
#       parameter10 = ""
#       parameter11 = ""
#     }
#   }
# */
# /*
#   account_maintenance {
#     /*
#     accounts {
#       account {
#         action                    = "Create"   // "Create", "Reset", "Delete", "DisableFileVault"
#         username                  = "username"
#         realname                  = "Real Name"
#         password                  = "password"
#         archive_home_directory    = false     // Set to true or false
#         archive_home_directory_to = "" // "/path/to/archive"
#         home                      = "/Users/username/"
#         hint                      = "Password Hint"
#         picture                   = "/path/to/picture"
#         admin                     = false      // Set to true or false
#         filevault_enabled         = false     // Set to true or false
#       }
#     }
#     */
#     /*
#     directory_bindings {
#       binding {
#         id    = 1234               // Specify the unique identifier
#         name  = "Binding Name"     // This is a computed field
#       }
#     }
# */
# /*
#     management_account {
#       action                   = "doNotChange"  // Default value
#       managed_password         = ""             // Default value
#       managed_password_length  = 0              // Default value
#     }


#     open_firmware_efi_password {
#       of_mode      = "none"     // Default value
#       of_password  = ""         // Default value
#     }

#   }
#   */
# /*
#   maintenance {
#     recon                    = false
#     reset_name               = false
#     install_all_cached_packages = false
#     heal                     = false
#     prebindings              = false
#     permissions              = false
#     byhost                   = false
#     system_cache             = false
#     user_cache               = false
#     verify                   = false
#   }
# */
# /*
#   files_processes {
#     search_by_path          = ""
#     delete_file             = false
#     locate_file             = ""
#     update_locate_database  = false
#     spotlight_search        = ""
#     search_for_process      = ""
#     kill_process            = false
#     run_command             = ""
#   }
# */
# /*
#   user_interaction {
#     message_start           = ""
#     allow_user_to_defer     = false
#     allow_deferral_until_utc = ""
#     allow_deferral_minutes  = 0
#     message_finish          = ""
#   }
# */
# /*
#   reboot {
#     message                     = "This computer will restart in 15 minutes. Please save anything you are working on and log out by choosing Log Out from the bottom of the Apple menu."
#     startup_disk                = "Currently Selected Startup Disk (No Bless)"
#     specify_startup             = "MDM Restart with Kernel Cache Rebuild" // "Standard Restart" / "MDM Restart with Kernel Cache Rebuild"
#     no_user_logged_in           = "Restart Immediately" // Restart Immediately / "Restart if a package or update requires it"
#     user_logged_in              = "Restart Immediately" // Restart Immediately / "Restart if a package or update requires it"
#     minutes_until_reboot        = 10
#     start_reboot_timer_immediately = true
#     file_vault_2_reboot         = true
#   }
# */



# }
