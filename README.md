# Projet Métaheuristiques

Ce projet a été réalisé dans le cadre du cours de métaheuristiques du MPRO (Master Parisiende Recherche Opérationnelle).
Il présente une implémentation d'une métaheuristique pour la résolution d'un problème de couverture minimum de réseau.

## Auteurs

Guillaume CROGNIER
Quentin PEÑA

## Paramétrage

L'ensemble des paramètres réglables se situe au début du fichier main.py.

Le paramètre INST représente l'instance du problème que l'on souhaite résoudre. 
Il peut prendre comme valeur un entier N pour générer une grille NxN ou une chaine de caractères correspond au chemin d'accès à un fichier de données.

Le paramètre (R_CAPT, R_COM) représente les rayons de captation et de communication.
C'est un couple d'entiers positifs.



## Usage

Pour lancer l'algorithme, exécuter le fichier main.py.

```python
python main.py
```

## Fichiers

Les fichiers plot_cap.sci et plot_sol.sci sont des fichiers d'instructions SCILAB et sont modifiés à chaque exécution de l'algorithme.
Le premier contient le code pour tracer dans un repère l'ensemble des capteurs et leurs rayons de communication.
Le second contient le code pour tracer dans un repère l'ensemble des cibles (+) et des capteurs (X) ainsi que les rayons de captation.
Ces fichiers offrent un moyen efficace de visualiser les solutions obtenues, notamment pour les instances à partir de fichiers de données.