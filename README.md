[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/dt_Da3ef)
# 🎯Jeu de fléchettes

| Type       | Description                        |
| ---------- | ---------------------------------- |
| Durée      | 2x45 minutes + Travail à la maison |
| Rendu      | Sur GitHub                         |
| Format     | Travail individuel                 |
| Évaluation | Sur les critères de `criteria.yml` |

Prenez bien connaissance des [critères d'évaluation](criteria.yml) et veuillez bien lire la donnée en entier avant de commencer.

## Première partie

Le programme `dart` retourne le nombre de points obtenu au jeu de fléchettes considérant la position de la fléchette reçue en coordonnées cartésiennes (`x`,  `y`). Le centre de coordonnées concorde avec le centre des cercles.

Ainsi la position `(0, 0)` rapporte le maximum de points. L'exemple suivant illustre ce cas. Le programme est appelé avec les arguments `0 0` (soit la fléchette au centre de la cible) et retourne `100`, le nombre de points obtenus :

```shell
$ ./dart 0 0
100
```

La cible se compose de trois cercles concentriques définissant les zones nommées **A**, **B** et **C**. Par extension, la zone **D** est celle située à l'extérieur du cercle **C**.

Le type de variable utilisé pour stocker chaque coordonnée est `double` afin de maximiser la précision de la mesure. Rappelez-vous qu'il s'agit d'un nombre à virgule flottante stocké sur 64 bits.

Par défaut les diamètres de ces cercles sont les suivants :

- A = 2 cm
- B = 10 cm
- C = 20 cm

Le nombre de points obtenu dépend naturellement de l'endroit où atterrit la fléchette:

- Zone **A**: 100 points
- Zone **B**: 25 points
- Zone **C**: 5 points
- Zone **D**: 0 point

La figure ci-dessous illustre la cible avec les zones et les points associés.

![target](assets/target.png)

Pour résoudre les cas de litiges, une fléchette qui tomberait à la frontière d'un cercle appartient à la zone **intérieure** de ce cercle.

N'oubliez pas de faire des `commit` intermédiaires fréquents et de régulièrement pousser vos travaux sur GitHub. En cas de difficultés, demandez de l'aide aux assistants ou au professeur en donnant le numéro du commit qui pose problème.

Pour l'implémentation de votre programme, servez-vous des exemples vus en classe. Le programme recevra la coordonnée `x` sur l'argument `argv[1]` et la coordonnée `y` sur l'argument `argv[2]`. Utilisez la fonction `sscanf` pour convertir les chaînes de caractères reçues en des `double`.

Les valeurs de retour du programme sont :

- `1` Si pas assez d'arguments fournis au programme (i.e. `./dart 1`) ;
- `2` Si la valeur passée n'est pas valide (i.e. `./dart foo`) ;
- `0` Si le programme se termine correctement.

## Deuxième partie

Cette deuxième partie est nécessaire pour obtenir la note de 6.

Le programme doit être modifié pour accepter des arguments supplémentaires optionnels. Ces arguments optionnels permettent de spécifier le nombre de points obtenu dans chaque zone. Dans le cas suivant, une fléchette qui atterrit dans la zone D fait perdre des points :

```shell
$ ./dart 100 100 100 25 5 -5
-5
```

Le type pour stocker les points est `int`. On a donc au niveau des arguments.

```text
$ ./dart 1 2 3 4 5 6
         | | | | | '-- Nombre de points en dehors de la zone de jeu (int)
         | | | | '---- Nombre de points dans la zone C (int)
         | | | '------ Nombre de points dans la zone B (int)
         | | '-------- Nombre de points dans la zone A (int)
         | '---------- Coordonnée Y (double)
         '------------ Coordonnée X (double)
```

Il est possible d'omettre certaines valeurs : ainsi `./dart 100 100 3 1` ne spécifie que les points obtenus dans les zones `A` et `B`. Les autres grandeurs conservent leurs valeurs par défaut.

## Compilation et tests

Comme d'habitude, des tests ont été écrits pour vérifier que votre programme fonctionne comme demandé. Ils s'exécutent désormais avec `pytest`.

Utilisez la commande `make` pour compiler votre programme :

```shell
make
```

Pour seulement compiler votre programme, utilisez :

```shell
make build
```

Pour seulement lancer les tests, c'est cette commande :

```shell
make test
```

Enfin, pour supprimer l'exécutable créé et tout nettoyer :

```shell
make clean
```

Voici le résultat complet que vous devez obtenir si tout fonctionne :

```shell
$ make clean test
Cleaning...
rm -f dart *.o a.out
Compilation...
cc -std=c99 -g -Wall -Werror -pedantic dart.c -o dart -lm
Run tests...
EXEC=./dart pytest -q
...............................
31 passed in 0.42s
```

> **NOTE**
> Si la batterie de tests s'exécute sans erreurs, vous avez 13 points. Si en revanche, vous livrez votre programme avec aucun test fonctionnel, vous aurez 0 point !

## 🏆 Version

Pour obtenir des points supplémentaires, il faut que le programme accepte comme premier argument, et de manière optionnelle, la chaîne de caractère `-v`.  Si le premier argument vaut cette valeur, les autres arguments seront ignorés et le programme se comporte alors comme suit :

```c
$ ./dart -v
Dart (c)2020 Nom Prénom <firstname.lastname@heig-vd.ch>
Version 1.0.0
```

Pour comprendre ce qui se passe dans `argv[0]` essayer ceci:

```c
printf("%c %c %d\n", argv[0][0], argv[0][1], argv[0][2]);
```
