# TP — Qualité du code R

## Contexte et objectifs

Dans la partie précédente, vous avez obtenu un script Python généré par une IA. Ce script est fonctionnel, mais il ne respecte pas forcement les standards modernes de développement en R. Votre mission est de le structurer comme un **package R**, d'y appliquer les outils de qualité, de sécurité et de test, puis de le documenter.

À la fin du TP, votre projet R devra pouvoir être installé, exécuté et audité par n'importe quel développeur R.

> **Pourquoi un package R et pas juste un script ?**
> En R, la structure de package est le standard universel pour distribuer du code reproductible. Elle impose une organisation claire, permet la génération automatique de documentation, et est attendue par les outils de qualité comme `lintr`, `styler`, `covr` et `testthat`.

---

## Pré-requis

- R ≥ 4.2 installé
- RStudio ou VSCode avec l'extension R
- Les packages de développement de base :

```r
install.packages(c("devtools", "usethis", "renv"))
```

---

## Étape 0 — Découverte du script fourni

Avant de commencer, prenez 10 minutes pour relire le script pour : 

1. Identifier les dépendances utilisées (`library()` ou `require()`)
2. Repérer les problèmes évidents : absence de documentation, noms de variables peu lisibles, fonctions trop longues, absence de gestion d'erreurs

> **Note :** Ne modifiez pas encore le code. Cette étape est une phase d'observation.

---

## Étape 1 — Structurer le projet comme un package R

### 1.1 Créer la structure du package

```r
usethis::create_package("nom_du_projet")
```

Cette commande génère la structure minimale d'un package R :

```
nom_du_projet/
├── R/                  # Vos fonctions R
├── DESCRIPTION         # Métadonnées du package
├── NAMESPACE           # Exports (géré automatiquement par roxygen2)
└── nom_du_projet.Rproj
```

### 1.2 Déplacer le script dans `R/`

Découpez le script fourni en **fonctions** et placez-les dans des fichiers thématiques dans `R/` :

```
R/
├── load_data.R       # Fonctions de chargement des données
├── process_data.R    # Fonctions de traitement
├── visualize.R       # Fonctions de visualisation
└── utils.R           # Fonctions utilitaires
```

> **Règle d'or :** Un fichier R ne doit contenir que des définitions de fonctions. Les appels directs (`library()`, lecture de fichiers, boucles en dehors de fonctions) n'ont pas leur place dans `R/`. Créez un script `run.R` à la racine pour l'exécution.

---

## Étape 2 — Environnement reproductible avec renv

`renv` enregistre les versions exactes des packages utilisés dans un fichier `renv.lock`, garantissant que le projet fonctionnera identiquement sur une autre machine.

### 2.1 Initialiser renv

```r
renv::init()
```

Cette commande :

- Détecte les packages utilisés dans votre projet
- Crée un environnement isolé dans `renv/`
- Génère `renv.lock` avec les versions exactes

### 2.2 Installer les dépendances de développement

```r
renv::install(c("lintr", "styler", "oysteR", "testthat", "covr", "roxygen2"))
```

### 2.3 Mettre à jour le lockfile

```r
renv::snapshot()
```

### 2.4 Fichiers à commiter / ignorer

Commitez :

- `renv.lock` — indispensable pour la reproductibilité
- `renv/activate.R` — script d'activation automatique
- `.Rprofile` — active renv au démarrage du projet

Ne commitez **pas** (ajoutez à `.gitignore`) :

- `renv/library/` — les packages installés localement (trop volumineux)

```
# .gitignore
renv/library/
renv/staging/
```

> **Vérification :** Supprimez votre dossier `renv/library/`, relancez R dans le projet, et exécutez `renv::restore()`. Tous les packages doivent se réinstaller automatiquement.

---

## Étape 3 — Fichier `DESCRIPTION`

Le fichier `DESCRIPTION` est le fichier central d'un package R. Il contient les métadonnées et déclare les dépendances.

### 3.1 Éditer `DESCRIPTION`

```
Package: nomduprojet
Title: Description courte (une ligne, sans point final)
Version: 0.1.0
Authors@R:
    person(
      given = "Prénom",
      family = "Nom",
      role = c("aut", "cre"),
      email = "email@exemple.fr",
      comment = c(ORCID = "0000-0000-0000-0000")
    )
Description: Description longue du package sur une ou plusieurs
    phrases. Chaque ligne de continuation commence par 4 espaces.
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
RoxygenNote: 7.3.1
Depends:
    R (>= 4.2.0)
Imports:
    dplyr (>= 1.1.0),
    ggplot2 (>= 3.4.0)
Suggests:
    testthat (>= 3.0.0),
    covr,
    lintr,
    styler
```

**Différence `Imports` vs `Suggests` :**

- `Imports` : packages nécessaires pour que le code fonctionne
- `Suggests` : packages utilisés uniquement pour les tests et le développement

### 3.2 Créer le fichier `LICENSE`

```r
usethis::use_mit_license()
```

---

## Étape 4 — Documentation avec roxygen2

`roxygen2` génère automatiquement la documentation R (fichiers `.Rd`) et le `NAMESPACE` à partir de commentaires spéciaux dans votre code.

### 4.1 Format des commentaires roxygen2

Chaque fonction doit être documentée avec le bloc suivant **juste au-dessus** de sa définition :

```r
#' Filtre les valeurs supérieures à un seuil
#'
#' @description
#' Prend un vecteur numérique et retourne uniquement les valeurs
#' strictement supérieures au seuil fourni.
#'
#' @param data Vecteur numérique à filtrer.
#' @param threshold Valeur numérique du seuil de filtrage.
#'
#' @return Vecteur numérique contenant uniquement les valeurs
#'   supérieures au seuil.
#'
#' @examples
#' process_data(c(1, 5, 3, 8), threshold = 4)
#'
#' @export
process_data <- function(data, threshold) {
  if (!is.numeric(data)) {
    stop("`data` doit être un vecteur numérique.", call. = FALSE)
  }
  data[data > threshold]
}
```

**Tags essentiels :**

| Tag | Description |
|-----|-------------|
| `@param` | Décrit un paramètre de la fonction |
| `@return` | Décrit la valeur retournée |
| `@examples` | Exemples exécutables |
| `@export` | Rend la fonction accessible aux utilisateurs du package |
| `@importFrom` | Importe une fonction d'un autre package |

### 4.2 Générer la documentation

```r
devtools::document()
```

> **Vérification :** Le répertoire `man/` doit se peupler de fichiers `.Rd`, et `NAMESPACE` doit lister vos fonctions exportées.

---

## Étape 5 — Contrôle qualité du code avec lintr et styler

### 5.1 Formatage automatique avec styler

`styler` reformate automatiquement votre code selon le [Tidyverse Style Guide](https://style.tidyverse.org).

```r
# Formater un fichier
styler::style_file("R/process_data.R")

# Formater tout le package
styler::style_pkg()
```

**Ce que styler corrige automatiquement :**

- Espaces autour des opérateurs (`x<-1` → `x <- 1`)
- Indentation (2 espaces)
- Lignes trop longues
- Parenthèses et accolades

### 5.2 Analyse statique avec lintr

`lintr` détecte les problèmes que styler ne corrige pas : mauvaises pratiques, code mort, `T`/`F` au lieu de `TRUE`/`FALSE`, etc.

Créez un fichier de configuration `.lintr` à la racine :

```
linters: linters_with_defaults(
  line_length_linter(120),
  object_name_linter(styles = c("snake_case")),
  assignment_linter(),
  commented_code_linter()
)
encoding: "UTF-8"
```

Lancer lintr :

```r
# Analyser tout le package
lintr::lint_package()

# Analyser un fichier
lintr::lint("R/process_data.R")
```

### 5.3 Workflow recommandé

Toujours styler **avant** lintr : styler corrige le formatage, lintr signale ce qui reste à corriger manuellement.

```r
styler::style_pkg()
lintr::lint_package()
```

> **Vérification :** `lintr::lint_package()` doit retourner 0 warning.

---

## Étape 6 — Contrôle des dépendances avec oysteR

`oysteR` interroge la base de données OSS Index de Sonatype pour détecter les vulnérabilités connues dans les dépendances de votre projet.

### 6.1 Auditer les dépendances

```r
library(oysteR)

# Auditer les packages installés dans l'environnement renv
audit <- audit_description(here::here("DESCRIPTION"))
get_vulnerabilities(audit)
```

### 6.2 Interpréter les résultats

- Si `get_vulnerabilities()` retourne un dataframe vide : aucune vulnérabilité détectée
- Si des vulnérabilités sont listées : mettez à jour les packages concernés dans `DESCRIPTION` en spécifiant une version minimale corrigée, puis relancez `renv::snapshot()`

> **Livrable :** Capture d'écran ou sortie de `get_vulnerabilities()` vide.

---

## Étape 7 — Tests unitaires avec testthat

### 7.1 Initialiser testthat

```r
usethis::use_testthat()
```

Cette commande crée le répertoire `tests/testthat/` et ajoute `testthat` aux `Suggests` du `DESCRIPTION`.

### 7.2 Structure des tests

```
tests/
├── testthat/
│   ├── test-load_data.R
│   ├── test-process_data.R
│   └── test-utils.R
└── testthat.R
```

### 7.3 Écrire les tests

Créez un fichier de test par fichier source (`test-process_data.R` pour `R/process_data.R`) :

```r
# tests/testthat/test-process_data.R

test_that("process_data retourne les valeurs au-dessus du seuil", {
  result <- process_data(c(1, 5, 3, 8), threshold = 4)
  expect_equal(result, c(5, 8))
})

test_that("process_data retourne un vecteur vide si tout est sous le seuil", {
  result <- process_data(c(1, 2, 3), threshold = 10)
  expect_length(result, 0)
})

test_that("process_data lève une erreur pour une entrée non numérique", {
  expect_error(
    process_data("pas un vecteur", threshold = 4),
    "`data` doit être un vecteur numérique."
  )
})

test_that("process_data gère un vecteur vide", {
  result <- process_data(numeric(0), threshold = 4)
  expect_length(result, 0)
})
```

**Fonctions d'assertion courantes :**

| Fonction | Usage |
|----------|-------|
| `expect_equal(x, y)` | Égalité de valeur |
| `expect_identical(x, y)` | Égalité stricte (type inclus) |
| `expect_length(x, n)` | Longueur d'un vecteur |
| `expect_error(expr, message)` | Vérifie qu'une erreur est levée |
| `expect_warning(expr)` | Vérifie qu'un warning est levé |
| `expect_true(expr)` / `expect_false(expr)` | Valeur logique |
| `expect_s3_class(x, class)` | Classe d'un objet |

### 7.4 Lancer les tests

```r
devtools::test()
```

---

## Étape 8 — Couverture de tests avec covr

### 8.1 Calculer la couverture

```r
library(covr)

# Couverture de tout le package
cov <- package_coverage()
print(cov)
```

### 8.2 Rapport visuel

```r
# Rapport HTML interactif
report(cov)

# Couverture par fonction
function_coverage("process_data", cov)
```

### 8.3 Vérifier un seuil minimum

```r
# Échoue si la couverture est inférieure à 80%
percent_coverage(cov) >= 80
```

> **Objectif minimum :** 80% de couverture sur les fonctions du package.

---

## Étape 9 — README

Le README d'un package R doit permettre à un utilisateur de l'installer et l'utiliser en quelques minutes.

### 9.1 Générer un README avec usethis

```r
usethis::use_readme_rmd()
```

Cela crée un `README.Rmd` (R Markdown) qui peut contenir du code R exécutable. Éditez-le puis générez le `README.md` :

```r
devtools::build_readme()
```

> **Important :** Committez toujours les deux fichiers `README.Rmd` **et** `README.md`. Le `.Rmd` est la source, le `.md` est affiché par GitHub.

### 9.2 Structure minimale attendue

````markdown
# nomduprojet

Description courte (1-2 phrases).

## Installation

```r
# Installer depuis GitHub
devtools::install_github("votre-compte/nom_du_projet")
```

## Utilisation

```r
library(nomduprojet)

# Exemple minimal
result <- process_data(c(1, 5, 3, 8), threshold = 4)
print(result)
```

## Développement

Cloner le projet et restaurer l'environnement :

```r
renv::restore()
```

Lancer les vérifications :

```r
styler::style_pkg()        # Formatage
lintr::lint_package()      # Qualité du code
devtools::test()           # Tests unitaires
covr::package_coverage()   # Couverture
devtools::check()          # Vérification complète du package
```
````

---

## Étape 10 — Vérification finale du package

`devtools::check()` (alias de `R CMD check`) est la vérification complète d'un package R. C'est le standard utilisé par CRAN.

```r
devtools::check()
```

Cette commande vérifie :
- La cohérence du `DESCRIPTION` et du `NAMESPACE`
- La documentation de toutes les fonctions exportées
- L'absence d'erreurs et de warnings dans le code
- Que tous les exemples dans la documentation s'exécutent correctement
- Que les tests passent

> **Objectif :** `0 errors | 0 warnings | 0 notes`

---

## Récapitulatif de la structure finale du projet

```
nom_du_projet/
├── R/
│   ├── load_data.R
│   ├── process_data.R
│   └── utils.R
├── man/                        # Généré par roxygen2
├── tests/
│   ├── testthat/
│   │   ├── test-load_data.R
│   │   └── test-process_data.R
│   └── testthat.R
├── renv/
│   └── activate.R
├── .lintr
├── .Rprofile
├── DESCRIPTION
├── LICENSE
├── NAMESPACE                   # Généré par roxygen2
├── README.Rmd
├── README.md                   # Généré par devtools::build_readme()
├── renv.lock
└── run.R                       # Script d'exécution principal
```

---

## Récapitulatif des livrables

| Étape | Livrable attendu |
|-------|-----------------|
| 1 | Structure de package R correcte, fonctions dans `R/` |
| 2 | `renv.lock` commité, `renv::restore()` fonctionnel |
| 3 | `DESCRIPTION` complet avec dépendances correctement classées |
| 4 | Toutes les fonctions documentées avec roxygen2, `man/` généré |
| 5 | `styler::style_pkg()` appliqué, `lintr::lint_package()` sans warning |
| 6 | `oysteR` sans vulnérabilité critique |
| 7 | Tests couvrant les cas nominaux, limites et erreurs |
| 8 | Couverture ≥ 80% |
| 9 | README complet avec installation et utilisation |
| 10 | `devtools::check()` : 0 errors, 0 warnings |
