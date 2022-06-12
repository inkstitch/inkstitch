---
title: "Installation manuelle sous Windows"
permalink: /fr/developers/inkstitch/windows-manual-setup/
last_modified_at: 2019-09-16
toc: false
---

Ceci décrit l'installation manuelle pour qui souhaite debuguer des extentions Ink/Stitch sous Windows.
Une description générique et plus complète de ces environements est disponible sur [installation manuelle](/developers/inkstitch/manual-setup/).
Cette description ne concerne que la partie python dans un environement Windows.
L'installation décrite vous permettra de debuguer le code en exécutant l'extension puis d'éditer le code et de ré-executer le code.

#### 1. Vous devez avoir un environnement Python (2.7 est recommandé).

Inkscape, qui est l'application de base à l'intérieur de laquelle Ink/Stitch est exécutée installe un environement Python.
Cet environnement ne contient pas tout ce qui est necessaire pour les extensions Ink/Stitch
Utilser cet environnement pour créer un environement virtuel sous Windows n'est pas une solution simple (pour inkscape 0.92.4).  Il est plus facile d'installer un nouveau python à partir duquel créer un environement virtuel.

Il vous est suggéré d'utiliser python 2.7. S'il n'est pas déjà installé, téléchargez le et installez le.

Une fois installé, vérifiez votre variable de chemin d'environnement. Lorsque l'environnement virtuel s'exécute,
la variable de chemin n'est plus importante. Jusqu'à ce que vous y soyez, le plan le plus simple est de veiller à ce que les chemins python 2.7 (exe, lib, DLL) soient en premier dans le chemin.


#### 2. Vous souhaiterez peut être un client git

Un client git est necessaire si vous souhaitez participer sur github
Dans ce cas, téléchargez un client git, et clonez le repertoire principal d'inkstitch, par exemple dans c:\inkstitch, qui est le répertoire utilisé dans les exemples.
Aucune description specifique de comment obtenir le client, ou installer le clone n'est donné. Une manière simple est d'utiliser PyCharm.


#### 3. Vous devez créer un environement virtuel Python 2.7 pour Ink/Stitch
Ce point est clé. Cet environement sera utilisé par inkscape pour excuter les extensions. A nouveau, aucune description spécifique de comment télécharger et installer cet environement virtuel ne sont donnés. A nouveau une manière simple de faire  est d'utiliser PyCharm et le fichier  "requirements.txt" qui vient avec Ink/Stitch

#### 4. Actions spéciales nécéssaires pour l'environnement virtuel Python

Le fichier requirements.txt qui vient avec  Ink/Stitch ne dit pas tout, il reste des choses à faire.
Sous Linux, il y a plus d'outils dans l'environement que ce qu'il est standard d'avoir sous Windows.

Normalement, vous ne compilez pas de module sous Windows, ce qui crée des problèmes spécifiques pour certain paquets.
Pour résoudre cela, nous proposons de télécharger des fichiers wheel tout prêt (".whl" files). 
Ces fichiers peuvent être installés par python, mais sont prêts pour un environement spécifique.
Pour  Windows 64, avec un  Python 64 bit,  téléchargez les fichiers suivants (il peut y avoir des fichiers plus récents, utilisez les, mais  "cp27" and "amd64" sont les noms à rechercher:

    libxml2_python-2.9.3-cp27-none-win_amd64.whl
    lxml-4.4.1-cp27-cp27m-win_amd64.whl
Installez le fichier wheel lixxml2 dans l'environement virtuel de la manière qui vous est habituelle.
Puis installez le fichier lxml.
Le fichier lxml necessite une installation particulière pour s'assurer qu'il n'y a pas de collision avec libxml2 qu'il utilise.
La commande pip, doit être le pip de l'ennvironement virtuel, d'où l'hypothese que vous lancez cette commande en ligne de commande, depuis le repertoire qui contient cette commande pip.

    SET STATIC_DEPS=true
    .\pip install lxml-4.4.1-cp27-cp27m-win_amd64.whl
    set STATIC_DEPS=
    
Vous ne pouvez pas installer wx, à la place installez wxPython normalement. Pour plus de sécurité, installez aussi scour.

#### 5. shapely est spécialement difficile
Si OSGeo4W64 n'est pas installé, vous devrez le faire.
Shapely necessite deux DLLS qui proviennent de ce programme  (geos_c.dll and geos.dll).
Après l'installation, avec les bonnes déclaration de chemins, cela va marcher. Cependant, OSGeo4W64 peut interferrer avec d'autre programmes (comme illustrator).
Une solution peut être d'installer ces deux fichiers au bon endroit dans votre environement virtuel.
Si vous utilisez pyinstaller, cet endroit doit être D:\Temp\BoxIssue\inkstitch-master\Lib\site-packages\shapely\DLLs.

Une fois ces DLLS en place, vous pouvez installer shapely.



#### 6. Pour pouvoir exécuter Inks/Stitch dans l'environement virtuel, vous devez définir  PYTHONPATH

Ink/Stitch contient un sous-module, pyembroidery, dont la localisation n'est pas automatiquement reconnue.Vous devez donc la déclarer.
Ceci se fait en donnant à PYTHONPATH la valeur du chemin où se trouve  pyembroidery (le repertoire racine de pyembroidery).
Sans utiliser les "" autour du chemin, même s'il contient des espaces, ce qui est inhabituel dans les environnements Windows.

Si vous voulez plus de repertoires dans le chemin, par exemple inkstitch, ajoutez un point virgule et le chemin. Je n'ai pas fait cela, mais ça devrait marcher.

    SET PYTHONPATH=D:\Path\To\pyembroidery

#### 7. Pour eviter d'exécuter les make files d'Ink/Stitch 
Théoriquement, vous pouriez maintenant préparer les fichiers inx à l'aide de make. A la place téléchargez et installez la dernière release d'Ink/Stitch.
Cela installera tous les fichiers inx et fichiers locaux nécessaires.
Une fois cela fait, copiez l'ensemble de votre clone Ink/Stitch là où se trouve l'extension inkstitch.
Ainsi le fichier inkstitch.py de votre clone écrase le fichier inkstitch.py dans le répertoire de l'extension.

Ceci signifie que lorsque inkscape lance l'extension Ink/Stitch, c'est votre fichier inkstitch.py qui est utilisé.

Cela signifie aussi que chaque fois que vous changez le code, vous devez copier ces changements là.


#### 8. Réglages  inkscape  pour utiliser votre environement virtuel Python:
Cela se fait en allant dans le fichier de préférences inkscape (preferences.xml) qui est dans votre dossier de Roaming (C:\Users\xxxxxx\AppData\Roaming\inkscape).

xxxxxx est dans ce cas votre nom d'utilisateur Windows.  Fermez  inkscape, et éditez ce fichier. 
Recherchez un groupe avec id="extensions", et ajoutez votre chemin python directement dessous, en donnant explicitement le chemin d'accès du fichier
python.exe :

     id="extensions"
     python-interpreter="d:/path/to/virtualenv/Scripts/python.exe"
     
Chaque fois que inkscape lancera une extensionn il utilisera votre environement virtuel.
Si votre version d'inkscape est trop ancienne, cela peut poser un problème. Téléchargez et installez une version plus récentes
     

#### 9. Dire à  Ink/Stitch d'activer le debugage à distance
Il est suggérré d'utiliser pydev comme debuggeur. A nouveau nous ne donnons ici aucune instruction sur la manière de l'installer.
Il est activé chaque fois qu'une extension Ink/Stitch est éxécutée, à condition que vous ayez un fichier nommé "DEBUG" dans le répertoire où l'exension Ink/Stitch est installée.
Donc allez dans le répertoire d'extensions inkscape et créez un fichier (ou un dossier) nommé  "DEBUG" dans le même dossier que inkstitch.py

#### 10.   Debuger necessite maintenant un debugeur à distance.
Démarrez votre debugueur à distance. Ecoutez le port 5678. Démarrez inkscape, depuis un endroit où votre PYTHONPATH est actif.
Je fais cela en ligne de commande. Depuis inkscape, appellez l'extension Ink/Stitch que vous voulez debuger. Ink/Stitch appelera le debugger.
Toutes les erreurs que vous pourriez voir avant cela proviennent d'inkscape et de la chain d'import appelée par by Ink/Stitch.

Installez tout module dit manquant.
Si quelque chose ne va tounours pas, la meilleure manière de débuger en attendant que le debugger à distance fonctionne est probablement d'éditer le fichier inkex.py du dossier d'extension d'inkscape:

    C.\Program Files\inkscape\share\extensions\inkex.py
