# Logo — Clinique Espoir

## Le signe : « l'étreinte »

Il est dérivé du logo existant de la Clinique de l'Espoir : le ruban bleu qui s'enroule,
la virgule turquoise en bas à gauche, et une forme rouge au centre. On garde la structure
et les trois couleurs ; on remplace le « e » rouge par **une tête de profil**, tenue par
le ruban. Le signe dit alors ce que la clinique fait : tenir quelqu'un.

L'anneau ouvert sert aussi de puce dans les listes du site.

Couleurs, reprises de l'original : ruban `#2B4B9B`, tête `#C0392F`, virgule `#0E9BA8`.
En réserve : ruban blanc, tête `#F2A79E`, virgule `#5FD3DE`.

## Fichiers

| Fichier | Usage |
|---|---|
| `espoir-mark.svg` | Le signe seul, bleu enseigne `#2B4B9B`. Fond clair. |
| `espoir-mark-blanc.svg` | Le signe seul, blanc. Fond bleu ou sombre. |
| `espoir-badge.svg` | Pastille bleue à coins arrondis. Favicon, avatar, application. |
| `espoir-lockup.svg` | Signe + « Espoir الأمل » + ligne d'identification. Fond clair. |
| `espoir-lockup-blanc.svg` | Le même, en réserve. |

## Règles

- **Couleur** : bleu `#2B4B9B` sur fond clair, blanc sur fond bleu ou sur `#10222F`.
  Pas d'autre couleur, pas de dégradé, pas d'ombre portée.
- **Air** : laisser autour du signe au moins la hauteur de sa ligne de base.
- **Taille minimale** : 18 px pour le signe, 22 px pour la pastille, 120 px pour le logotype.
- **Ne pas** : étirer, incliner, changer l'épaisseur de l'arche, poser le signe sur une
  photographie chargée, ni remplacer la typographie du logotype.

## Typographie du logotype

« Espoir » en **Bricolage Grotesque** 700, approche resserrée (−0,038 em).
La ligne « CLINIQUE PSYCHIATRIQUE · EL MENZAH 9 » en **Archivo** 500, interlettrage +0,1 em.
« الأمل » en **Noto Kufi Arabic**. Les trois polices sont dans `assets/fonts/`.

Les fichiers `*-lockup*.svg` contiennent du texte vivant : pour l'impression ou pour un
usage hors du site, ouvrez-les dans un éditeur vectoriel et vectorisez le texte.

## Les pistes écartées

`logos.html` (à la racine du projet) présente les quatre pistes étudiées, chacune testée
en grand, en pastille, en 18 px et en réserve. Pour en adopter une autre, dites-le : le
signe est défini à un seul endroit, dans le `<g id="mark">` en haut de `index.html`.
