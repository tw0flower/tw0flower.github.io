Title: Using Ansible to set mappers when setting up LDAP federation
Date: 2023-07-29
Status: published

**TL;DR**

Look up the [Keycloak's API JavaDoc](https://www.keycloak.org/docs-api/22.0.1/javadocs/index.html), search for "MapperConfig" to find your mapper's config class, lowercase all fields and replace the underscores by commas (e.g. LDAP_FULL_NAME_ATTRIBUTE -> ldap.full.name.attribute). For the group mapper the two following classes are needed: [GroupMapperConfig](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/storage/ldap/mappers/membership/group/GroupMapperConfig.html) and [LdapMapCommonGroupMapperConfig](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/models/map/storage/ldap/config/LdapMapCommonGroupMapperConfig.html). This is because GroupMapperConfig inherits from LdapMapCommonGroupMapperConfig.

Here is a full working example:

    :::yaml
    community.general.keycloak_user_federation:
        auth_keycloak_url: "https://keycloak.example.com"
        auth_client_id: admin-cli
        auth_realm: master
        auth_username: admin
        auth_password: not_a_great_password
        realm: master
        name: LDAPFederation
        provider_id: ldap
        config:
        bindCredential: the_ldap_password
        bindDn: uid=keycloak,cn=accounts, dc=ldap,dc=example,dc=com
        connectionUrl: ldap://ldap.example.com
        editMode: "READ_ONLY"
        usernameLDAPAttribute: uid
        userObjectClasses: "inetuser"
        usersDn: "cn=users,cn=accounts,dc=ldap,dc=example,dc=com"
        vendor: other
        mappers:
        - name: group
            providerId: group-ldap-mapper
            providerType: "org.keycloak.storage.ldap.mappers.LDAPStorageMapper"
            config:
            memberof.ldap.attribute: memberOf
            membership.attribute.type: DN
            membership.ldap.attribute: member
            membership.user.ldap.attribute: uid
            mode: READ_ONLY
            user.roles.retrieve.strategy: GET_GROUPS_BY_MEMBEROF_ATTRIBUTE
            default.ldap.groups.path: /
            groups.dn: cn=groups,cn=accounts,dc=ldap,dc=example,dc=com

---

As of today, if you take a look at the Ansible documentation for the community.general.keycloak_user_federation module, you will find a rather elusive description of how mappers should be defined. In particular, the `config` field's description says this:

>A list of dicts defining mappers associated with this Identity Provider.

Not a great start. The documentation does not tell you how to find how to set fields. In search for answers, I looked at the examples and found this:

    :::yaml
    - name: Create LDAP user federation
      community.general.keycloak_user_federation:
        auth_keycloak_url: https://keycloak.example.com/auth
        auth_realm: master
        auth_username: admin
        auth_password: password
        realm: my-realm
        name: my-ldap
        ...
        mappers:
        - name: "full name"
            providerId: "full-name-ldap-mapper"
            providerType: "org.keycloak.storage.ldap.mappers.LDAPStorageMapper"
            config:
                ldap.full.name.attribute: cn
                read.only: true
                write.only: false

This describes how to configure a full name mapper, one of the mappers that Keycloak supports and probably one of the most straightforward. The example works, but it does not really explain where the config fields come from. The documentation does say this though:

>The names of module options are snake_cased versions of the camelCase ones found in the Keycloak API and its documentation at https://www.keycloak.org/docs-api/8.0/rest-api/index.html

So I went to check the [Keycloak's API JavaDoc](https://www.keycloak.org/docs-api/22.0.1/javadocs/index.html) and found the specific [page](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/storage/ldap/mappers/membership/group/GroupLDAPStorageMapper.html) that pertains to the LDAP group mapper.

The `getConfig` method tells us that the config type is [CommonLDAPGroupMapperConfig](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/storage/ldap/mappers/membership/CommonLDAPGroupMapperConfig.html), and there bingo! The fields match some of the ones we have in the UI. But not all. Fortunately, a quick look at the direct known subclasses tells us that the [GroupMapperConfig](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/storage/ldap/mappers/membership/group/GroupMapperConfig.html) inherits from the GroupMapperClass. With the fields from this new class in addition, we have everything we need.

A look at the [FullNameLDAPStorageMapper](https://www.keycloak.org/docs-api/22.0.1/javadocs/org/keycloak/storage/ldap/mappers/FullNameLDAPStorageMapper.html) class tells us how to convert the attributes from the JavaDoc to something that the Ansible module will process. **LDAP_FULL_NAME_ATTRIBUTE** becomes **ldap.full.name.attribute**, **READ_ONLY** becomes **read.only**, etc.

This is not camelCase, so the above quotation does not apply and I don't think this is actually explained anywhere in the documentation. 

The process I described can be applied for any group mapper, but here is a working example for the group mapper.

    :::yaml
    - name: Create LDAP user federation
      community.general.keycloak_user_federation:
        auth_keycloak_url: https://keycloak.example.com/auth
        auth_realm: master
        auth_username: admin
        auth_password: password
        realm: my-realm
        name: my-ldap
        ...
        mappers:
        - name: "full name"
            providerId: "full-name-ldap-mapper"
            providerType: "org.keycloak.storage.ldap.mappers.LDAPStorageMapper"
            config:
                ldap.full.name.attribute: cn
                read.only: true
                write.only: false
