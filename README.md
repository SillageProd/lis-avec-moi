# Lis avec moi

Petite app pour aider les enfants (4 à 8 ans) à lire les mots et les lettres vus à l'école.
Elle s'installe sur iPad et iPhone depuis Safari : **Partager → Sur l'écran d'accueil**.

- Jusqu'à 6 profils, sans mot de passe.
- Mode **Timer** (30 s à 5 min) et mode **Normal** (25, 50, 75, 100 mots ou tous).
- L'adulte valide chaque mot avec **V** (juste) ou **X** (faux).
- Les résultats et le graphique des progrès restent sur l'appareil.

## Changer les mots

Les mots viennent d'un Google Sheet partagé « Tous les utilisateurs disposant du lien » :
un mot ou une lettre par ligne, dans la colonne A. L'app relit la liste à chaque ouverture.
Le lien se change dans **Espace parents**.

## Fichiers

- `index.html`, `sw.js`, `manifest.webmanifest`, `icone-*.png` : l'app en ligne (GitHub Pages).
- `source/` : la version de travail et le script `build.py` qui produit les fichiers ci-dessus.

## Synchroniser l'iPad et l'iPhone

Les profils et les résultats peuvent être partagés entre appareils grâce à un petit script Google
(`source/synchro.gs`, aussi disponible sur le site : `synchro.gs.txt`) installé dans un Google Sheet
privé. Les étapes sont expliquées dans **Espace parents → Synchroniser l'iPad et l'iPhone**.
Si le même prénom a été créé sur deux appareils, les deux profils sont regroupés automatiquement.
