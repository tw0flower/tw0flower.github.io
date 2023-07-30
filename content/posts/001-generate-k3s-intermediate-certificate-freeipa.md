Title: Generating an intermediate certificate in FreeIPA and using it for k3s
Date: 2023-06-24 15:58
Status: draft

It is no secret that self-signed certificates should be avoided as they do not allow properly authenticating systems. k3s makes it very easy to just fire up with self-signed certificates, and it's really easy to just leave it as-is.

However, if your host is already registered to a FreeIPA server (this is the case if you have run `ipa-client-install`), the process of getting an intermediate certificate for your host that can be used by k3s is very easy. Better even, this intermediate CA will now be automatically renewed before it expires.

This guide assumes that you have already started the server and that the certificates have been generated. You *can* actually provision the certificates before starting the server *but* it means you would have to clean the in-use data directory which is not recommended and therefore really inconvenient. Therefore, I'd rather just start k3s and deal with rotating the keys, which is what this guide describes.

First, let's get the intermediate CA from FreeIPA.

    :::bash
    ipa-getcert request -k /etc/ssl/certs/$HOSTNAME.key -f /etc/ssl/certs/$HOSTNAME.pem

If the command succeeded you should see the two new files in the `/etc/ssl/certs` directory.

Now all we have to do is link this intermediate certificate to the right location for k3s to use, as per [the documentation](https://docs.k3s.io/cli/certificate#using-custom-ca-certificates). We use 3 files: the two files that make the intermediate CA we just got from FreeIPA and the root CA that was installed when you run `ipa-client-install`. This file is located in `/etc/ssl/certs/IPA_REALM.pem` where `IPA_REALM` is the name of the FreeIPA realm your server is registered in.

    :::bash
    mkdir -p /opt/k3s/server/tls
    ln -s /etc/ssl/certs/IPA_REALM.pem /var/lib/rancher/k3s/server/tls/root-ca.pem
    ln -s /etc/ssl/certs/$HOSTNAME.pem /opt/k3s/server/tls/intermediate-ca.pem
    ln -s /etc/ssl/certs/$HOSTNAME.key /opt/k3s/server/tls/intermediate-ca.key

We also 

Boom, now, let's generate this cert