Title: How I used to self-host my services and plans for the future
Date: 2023-02-05 10:20
Category: Project

I became interested in self-hosting a while ago, when I was still a student. Let's be honest, my main motivation at first was to set-up a seedbox to download the last Game of Thrones episode released this week for me while I was attending my morning class at the university.

History will not say if I succeeded in this endeavour or not. However, what history will tell is that I soon began hosting much more than just smallish projects. Before I knew it I was administering a cloud storage solution, then an e-mail server, then again my own git server, because why not?

# The FreeBSD era

The Raspberry Pi that I was using in the first place soon became very limited in its abilities to hold the load - it was one of the first versions and even running Nextcloud was a stretch. So I migrated everything to a dedicated server in a datacenter. And I moved from Debian to FreeBSD in the process, because that's the operating system I was using at my internship at the time. I did things the right way and administered everything with FreeBSD's containerization system: the [jails](https://docs.freebsd.org/en/books/handbook/jails/).

Due to FreeBSD's nature I had to do everything myself. If a package was not available in binary format, I built it using my own [poudriere](https://github.com/freebsd/poudriere). If a web service was not available in the repositories, I set up the jail with the necessary packages myself. It was extremely difficulty with my lack of experience at the time, but so rewarding. Most common Linux programs do not offer any FreeBSD support. And sometimes they didn't even built in a FreeBSD environment. So I had to find workarounds all the time.

Even though my system was perfectly functional, containerized, and manageable with the scripts I had written, I wanted to experiment with Docker. Which was not officially available on the BSD systems. And so I migrated again.

# Debian and Docker

So