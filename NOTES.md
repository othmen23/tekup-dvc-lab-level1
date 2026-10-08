# Niveau 1 : fondamentaux DVC

## Exercice 1.1 : versioning et remote
- Iris n'a que 150 lignes : jeu suréchantillonné à 600 lignes (tirage avec remise + bruit gaussien 0.05) pour respecter le seuil de 500 lignes.
- `dvc add data/iris.csv` crée `data/iris.csv.dvc` (pointeur md5) et `data/.gitignore`.
- Remote local : `dvc remote add -d storage ../dvc-remote-level1`, puis `dvc push` : 1 file pushed.
- `rm -rf .dvc/cache data/iris.csv` puis `dvc pull` : 1 file fetched and 1 file added. `wc -l` donne 601 lignes avant et après.

## Exercice 1.2 : voyage dans le temps
- 4 versions (v1 à v4) : 6ad7e1c, 19ad830, 8339424, 429270b (`git log --oneline -- data/iris.csv.dvc`).
- `git checkout 6ad7e1c -- data/iris.csv.dvc` puis `dvc checkout` : en-tête d'origine (colonne `target`), 601 lignes. La branche reste sur main.
- `git checkout main -- data/iris.csv.dvc` puis `dvc checkout` : colonnes `species` et `petal_area` de retour (v4).

## Questions de contrôle

**1. Pourquoi DVC ajoute-t-il le fichier de données au .gitignore automatiquement ?**
Pour que Git ne suive jamais le gros fichier : seul le petit pointeur `.dvc` entre dans l'historique. Sans cela, un `git add .` committerait la donnée brute, difficile à retirer ensuite.

**2. Taille du dépôt si on committe le CSV brut et qu'on le modifie 20 fois ?**
Git conserve chaque version : environ 21 copies du fichier (≈ 13,6 Ko x 21 ≈ 286 Ko ici). La compression delta aide peu. Avec un jeu de 2 Go, cela ferait environ 42 Go dans chaque clone. Avec DVC, Git ne garde que 21 pointeurs de quelques centaines d'octets.

**3. Que contient le cache DVC ? Que se passe-t-il si on le supprime sans `dvc push` ?**
`.dvc/cache` contient les fichiers de données réels, stockés par hash md5, pour toutes les versions. Supprimé avant un push, les données sont perdues : les `.dvc` pointent vers des hashes sans contenu et `dvc pull` échoue. Ici les données avaient été poussées, donc `dvc pull` les a restaurées depuis le remote.
