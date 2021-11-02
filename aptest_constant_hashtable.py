__author__ = 'Pradeep Mondal P'


#    Either a dictionary or a list
#   Dictionary is suggestable
#   all upper letter constants must have lower case word here..


aptest_constant_dictionary = {

########################################################  basic  constants #############################################
########################################################################################################################
    "login_amc_" : True,
    "logout_amc_"   : True,
    "apply_changes_"    : True,

    "do_pending_changes_"   : True,
    "save_apply_pending_changes_"   : True,
    "restore_tier_configuration_"   : True,
    "restore_tier_auth_server_" : True,
    "import_tier_configur_" : True ,

    "login_amc_restore_tier_configuration_" : True,
    "configure_smtp_server_create_ldap_unpw_server_enable_otp_" : True,
    "ssh_appliance_"    : True,

    "disabling_ntp_service_"    : True,
    "disabling_ntp_service_change_appliance_time_"  : True,
    "enable_ntp_service_"   : True,

    "set_dns_server_"   : True,
    "connecting_mct_backend_network_"   : True,

    "enable_epc_" : True ,


    ################################################# Certificates #####################################################
    ####################################################################################################################
    "import_root_certificate_authentication_server_" : True ,


################################################# AMC  login ###########################################################
########################################################################################################################
    "login_amc_using_newly_created_ldap_user_super_admin_"  : True,
    "logging_amc_using_newly_created_local_user_super_admin_"   : True,
    "logging_amc_using_newly_created_ad_user_super_admin_"  : True,
    # "logging_amc_using_newly_created_ad_user_system_admin_" : True,

# ............................... AMC login using otp ..............................................
    "login_amc_using_newly_created_local_user_super_admin_otp_" : True,

################################################# EW  login ###########################################################
########################################################################################################################
    "login_cram_unpw_radius_ad_affinity_enabled_realm_affinity_user_": True ,

    ######################################## Authentication Servers ####################################################
    ####################################################################################################################
    "enable_user_initiated_password_change_" : True ,


################################################ AD  server ############################################################
########################################################################################################################
    "create_ad_server_" : True,
    "configure_ad_ldap_adtree_directory_server_ssl_enabled_" : True ,
    "configure_ad_ldap_adtree_server_ssl_enabled_" : True ,
    "create_ad_ldap_adtree_directory_server_ssl_enabled_" : True ,
    "create_ad_ldap_adtree_server_ssl_enabled_" : True ,
    "configure_ad_ldap_adtree_authentication_server_ssl_enabled_" : True ,

    "create_directory_authentication_server_" : True ,
    "create_directory_server_authentication_" : True ,
    "create_authentication_server_" : True ,
    "setup_ad_authentication_server_" : True ,
    "create_ad_server_" : True ,

    "create_new_ads_auth_server_enabling_one_time_password_"    : True,
    "set_ad_authentication_server_primary_authentication_module_"   : True,
    "set_primary_auth_module_ads_auth_server_"  : True,
    "create_ad_authentication_server_configure_otp_" : True ,

################################################ LDAP server ###########################################################
########################################################################################################################
    "create_new_ldap_authentication_server_"    : True,
    "add_ldap_unpw_auth_server_static_group_matching_" : True ,
    "create_ldap_unpw_auth_server_static_group_matching_" : True ,
    "CREATE_LDAP_AUTHENTICATION_SERVER_CONFIGURE_OTP_"  : True,
    "CONFIGURE_SMTP_SERVER_CREATE_LDAP_UNPW_SERVER_ENABLE_OTP_" : True,
    "set_ldap_authentication_server_primary_authentication_module_"  : True,
    "set_primary_auth_module_ldap_auth_server_" : True,
    "create_new_ldap_auth_server_enabling_one_time_password_"   : True,

################################################# local auth server ####################################################
########################################################################################################################
    "create_local_auth_server_" : True,
    "create_local_auth_server_enabling_password_expiry_"    : True,
    "create_local_authentication_server_"   : True,
    "create_new_local_auth_server_" : True,
    "set_local_authentication_server_primary_authentication_module_save_changes_"   : True,
    "create_new_local_auth_server_enabling_one_time_password_"  : True,
    "create_local_auth_server_setting_set_passwordexpiretime_greater_passwordexpirealerttime_"  : True,
    "set_primary_auth_module_local_auth_server_secondary_auth_module_ads_"  : True,

################################################### Ad Tree server #####################################################
########################################################################################################################
    "set_primary_auth_module_adtree_auth_server_"   : True,
    "configure_adtree_auth_server_" : True,
    "create_adtree_auth_server_"    : True,
    "set_primary_auth_module_ad_tree_"  : True ,
    "configure_ad_tree_authentication_server_"  : True ,
    "create_ad_tree_authentication_server_" : True ,


########################################### Radius Token Authentication Server #########################################
########################################################################################################################
    "create_radius_token_authentication_server_invalid_radius_identifier_nas_ip_address_"   : True,
    "create_radius_unpw_authentication_server_invalid_radius_identifier_nas_ip_address_"    : True,
    "add_cram_radius_auth_server_filter_id_group_matching_" : True ,
    "add_unpw_radius_auth_server_filter_id_group_matching_" : True ,
    "create_unpw_radius_auth_server_filter_id_group_matching_" : True ,

####################################### Radius Authentication Server ###################################################
########################################################################################################################
    "create_new_radius_authentication_server_"  : True,
    "create_radius_authentication_server_" : True ,
    "set_radius_authentication_server_primary_authentication_module_"   : True,

############################################# LDAP CERT AUTH server ####################################################
########################################################################################################################
    "select_ldap_cert_" : True,

######################################################## Realms ########################################################
########################################################################################################################
    "create_realm_associate_authentication_server_" : True ,


#.................................................... Stacked Realm ....................................................
    "create_translated_realm_stacked_authentication_cram_radius_unpw_radius_without_affinity_" : True ,
    "create_translated_realm_stacked_authentication_cram_radius_unpw_radius_affinity_ad_unpw_" : True ,
    "create_translated_realm_stacked_authentication_cram_radius_unpw_radius_affinity_ldap_unpw_" : True ,


# ................................................  AD server realm ....................................................

    "create_realm_associate_ad_authentication_server_" : True ,
    "create_realm_associate_otp_enabled_ad_authentication_server_" : True ,


# .............................................  Local auth server realm ...............................................

# ..............................................  AD Tree server realm .................................................

# ..........................................  Radius Auth server realm .................................................


#........................................... LDAP Auth Server Realm ....................................................

    "create_realm_ldap_authentication_server_" : True ,

######################################################### ADMIN ########################################################
########################################################################################################################

# ........................................................  Roles .......................................................
    "create_new_security_admin_role_"   : True,
    "create_new_system_admin_role_" : True,
    "create_new_super_admin_role_"  : True,
    "create_new_role_view_permissions_" : True,

# ...................................................  AD user admin....................................................
    "create_new_ad_user_security_admin_"    : True,
    "create_new_ad_user_super_admin_"   : True,
    "create_new_ads_user_super_admin_"  : True,
    "create_new_ad_user_system_admin_"  : True ,

# ................................................. AD ADTREE user admin ................................................
    "create_new_adtree_user_super_admin_"   : True,

# .................................................. LDAP user admin ....................................................
    "create_new_ldap_user_super_admin_" : True,

# ................................................. Local auth user admin ..............................................
    "create_new_local_user_super_admin_"    : True,
    "create_local_user_super_admin_"    : True,
    "set_primary_auth_module_local_auth_server_"    : True,

# .................................................. Radius user admin .................................................
    "create_new_radius_user_security_admin_"    : True,
    "create_new_radius_user_super_admin_"   : True ,

    "make_created_user_amc_admin_"  : True,
    "create_new_radius_user_system_admin_"   : True,

################################################# USERS ################################################################
########################################################################################################################

# ....................................................Local user.........................................................
    "create_new_local_user_"    : True,
    "login_amc_using_newly_created_local_user_super_admin_" : True,
    "create_local_user_without_clearing_password_reset_button_"  : True,
    "create_local_user_clearing_password_reset_button_" : True,


# .............................................AD user .................................................................
    "add_ad_user_using_directory_browse_option_"    : True,
    "add_ads_user_using_directory_search_"  : True,
    "create_user_" : True ,

    "add_ad_user_manually_set_realm_management_console_"    : True,
    "add_ads_user_using_directory_search_feature_"  : True,

# ................................................LDAP user ............................................................
    "add_ldap_user_manually_set_realm_management_console_"  : True,
    "add_ldap_user_using_directory_search_" : True,
    "add_ldap_user_using_directory_search_feature_" : True ,


# ..................................................AD Tree user .......................................................
    "add_adtree_user_manually_" : True,
    "add_adtree_user_using_directory_search_"   : True,


# ..................................................... Radius User ....................................................
    "add_radius_user_manually_set_realm_management_console_"    : True,
    "add_radius_user_manually_" : True,

##################################################### Groups ###########################################################
########################################################################################################################
    "create_group_entry_testgroup_qa_testgroup_" : True ,
    "create_user_group_" : True ,

# .......................................local user group ...........................................

    "add_new_local_group_created_new_user_"  : True,


# .......................................AD user group ...........................................
    "create_ad_user_group_" : True ,


#............................................... Profiles ..............................................................
    "create_device_profile_" : True ,


#..................................................... ZONE ............................................................
    "create_standard_zone_using_device_profile_" : True ,
    "enforce_epc_zone_realm_" : True ,


#.................................................... Resources ........................................................
    "create_resource_" : True ,
    "create_hostname_ip_address_resource_" : True ,
    "create_uqdn_resource_" : True ,
    "create_url_resource_workplace_shortcut_" : True ,
    "create_ip_range_resource_" : True ,
    "create_subnet_resource_" : True ,
    "create_server_farm_resource_" : True ,
    "create_domain_resource_" : True ,


#.................................................. Workplace  .........................................................
    "create_workplace_shortcut_" : True ,
    "create_workplace_shortcut_resource_" : True ,
    "create_resource_workplace_shortcut_" : True ,
    "create_hostname_ip_address_resource_workplace_shortcut_" : True ,
    "create_uqdn_resource_workplace_shortcut_" : True ,
    "create_ip_range_resource_workplace_shortcut_" : True ,
    "create_subnet_resource_workplace_shortcut_" :True ,
    "create_server_farm_resource_workplace_shortcut_" : True ,
    "create_domain_resource_workplace_shortcut_" : True ,


#.........................................    ACL  .....................................................................
    "create_allow_acl_" : True ,
    "create_deny_acl_" : True ,
    "create_deny_acl_test_group_dn_" : True ,
    "add_acl_allow_testgroup_shortname_resource_" : True ,
    "add_acl_allow_testgroup_resource_" : True ,
    "add_acl_deny_testgroup_shortname_resource_" : True ,
    "create_allow_acl_test_group_dn_" : True ,
    "add_acl_deny_testgroup_resource_" : True ,

    "create_allow_acl_create_acl_deny_test_group_dn_" : True ,

    "disable_permit_rule_default_resources_" : True ,
    "delete_existing_acl_" : True ,
    "delete_existing_acls_" : True ,

    "create_permit_acl_user_resource_" : True ,
    "create_permit_acl_group_uqdn_resource_" : True ,

    "create_permit_acl_user_workplace_ct_" : True ,
    "create_permit_acl_group_workplace_ct_" : True ,

    "create_acl_allow_test_group_qa_test_group_dn_" : True ,
    "create_permit_acl_user_hostname_ip_address_resource_" : True ,
    "create_permit_acl_user_ip_range_resource_" : True ,
    "create_permit_acl_group_url_resource_" : True ,
    "create_permit_acl_group_subnet_resource_" : True ,
    "create_permit_acl_user_server_farm_resource_" : True ,
    "create_permit_acl_user_domain_resource_" : True ,

}
