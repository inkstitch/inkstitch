---
title: Installer Ink/Stitch  sur un téléphone ou une tablette Android 
permalink: /fr/tutorials/inkstistch-on-android/
last_modified_at: 2025-01-06
language: fr
excerpt: "Installer Ink/Stitch sous Android avecTermux"
image: "/assets/images/tutorials/android/android_inkstitch.png"

tutorial-type:
  - Text
after_footer_scripts:
  - /assets/js/copy_code.js
classes:
  - wide
---
![Le simulateur sur un ecran de  telephone](/assets/images/tutorials/android/android_inkstitch_full.png)

Notez que  ce tutoriel est pour le fun. On peut douter de l'utilité d'utiliser Ink/Stitch sur un téléphone. Il se peut qu'il y ait des crashs fréquents et nous ne fournissons pas d'assistance pour cela.
{: .notice--warning }

Ce tutoriel est un peu technique et à destination des utilisateurs expérimentés. Nous utiliseront Termux
This tutorial is a bit technical and directed to experienced users. Nous utiliserons Termux pour configurer un bureau Linux sur lequel nous pourrons utiliser Inkscape et Ink/Stitch.
Sur cette page, vous trouverez une procédure d'installation simple. Des informations plus détaillées peuvent être trouvées ici : [Termux](https://github.com/LinuxDroidMaster/Termux-Desktops), [Termux X11](https://github.com/termux/termux-x11)

Nous tenons à remercier [LinuxDroidMaster](https://github.com/LinuxDroidMaster) pour le travail acharné sur le script qui nous permet de réaliser ce travail.
## Installation

Dans notre exemple, nous allons utiliser proot, arch linux et xfce desktop. Lisez la documentation mentionnée ci-dessus pour décider ce que vous souhaitez utiliser.
{: .notice--info }

* Nous commençons par installer [Termux](https://termux.dev/), s'il n'est pas déjà utilisé.

* Dans Termux, installez les packages pour exécuter Linux pour Termux et Android. Exécutez ces commandes dans la ligne de commande Termux

```
pkg update
pkg upgrade
```

```
pkg install x11-repo termux-x11-nightly tur-repo pulseaudio proot-distro wget git vim
```

* Téléchargez et installez l'application termux-x11 pour Android à partir de [termux-x11 nightly release](https://github.com/termux/termux-x11/releases/tag/nightly). Utilisez le fichier `debug-universal.apk`.

* Pour installer Linux avec proot-distro, utilisez la commande suivante

```
proot-distro install archlinux
```

* Connexion au conteneur archlinux

```
proot-distro login archlinux
```
* Nous sommes maintenant à l'intérieur de l'installation d'Arch. Mettons à jour le système

```
pacman -Syu
```

* Installer sudo

```
pacman -S sudo
```

* Créer un utilisateur

```
useradd -m -G wheel username
passwd username
```

Insérer la ligne suivante dans `/etc/sudoers`

```
username ALL=(ALL) ALL
```

* Installer xfce et inkscape. Vous pouvez bien sûr choisir un autre environnement de bureau si vous le souhaitez.

```
pacman -S xfce4 inkscape
```



* Quitter le conteneur Arch Linux

```
exit
```

* De retour dans termux, récupérez le script pour exécuter le xfce

```
wget https://raw.githubusercontent.com/LinuxDroidMaster/Termux-Desktops/main/scripts/proot_arch/startxfce4_arch.sh
```

Rendre le script exécutable

```
chmod +x startxfce4_arch.sh
```

Modifiez le script pour l'adapter à votre nom d'utilisateur

```
vim startxfce4_arch.sh
```

Remplacez le nom d'utilisateur `droidmaster` par votre propre nom d'utilisateur dans cette ligne

```
proot-distro login archlinux --shared-tmp -- /bin/bash -c 'export PULSE_SERVER=127.0.0.1 && export XDG_RUNTIME_DIR=${TMPDIR} && su - droidmaster -c "env DISPLAY=:0 startxfce4"'
```

Sur de nombreux téléphones, vous pouvez rencontrer un écran noir lorsque le script est en cours d'exécution.
Si cela vous arrive, remplacez `termux-x11 :0 >/dev/null &` par

```
termux-x11 :0 -legacy-drawing >/dev/null &
```

Enregistrez et quittez vim

* Exécutez le script et il démarrera le xfce

```
./startxfce4_arch.sh
```

* Nous avons déjà installé Inkscape.Ouvrez-le  puis fermez-le à nouveau.

  [Téléchargez Ink/Stitch for arm64](https://github.com/inkstitch/inkstitch-linux-arm64/releases/latest) et installez comme d'habitude  (copie dans le dossier des extensions).
