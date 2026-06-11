# Python

## Contexte et objectifs

Dans la partie précédente, vous avez obtenu un script Python généré par une IA. Ce script est fonctionnel, mais il ne respecte pas forcement les standards modernes de développement logiciel. Votre mission est de le mettre aux normes en appliquant les bonnes pratiques en développement logiciel : environnement reproductible, qualité du code, sécurité, tests, et documentation.

À la fin du TP, votre projet devra pouvoir être repris par n'importe quel développeur et exécuté de façon fiable, sûre et documentée.

---

## Pré-requis

- Avoir installé [pixi](https://pixi.sh) sur votre machine
- Avoir un compte GitHub

---

## Étape 0 — Lecture du script fourni pour identifier les améliorations

Avant de commencer, prenez quelques minutes pour :

1. Identifier les dépendances utilisées (imports)
2. Repérer les problèmes évidents : 
   1. absence de typage, docstrings manquantes, noms de variables peu explicites, absence de gestion d'erreurs, etc.

> **Note :** Ne modifiez pas encore le code. Cette étape est une phase d'observation.

---

## Étape 1 — Environnement reproductible avec Pixi

L'objectif est de garantir que n'importe qui puisse exécuter votre projet dans les mêmes conditions, quelle que soit sa machine. Dans ce TP, nous allons utiliser Pixi.

### 1.1 Initialiser le projet Pixi

```bash
pixi init
```

Cette commande crée un fichier `pixi.toml` à la racine du projet.

### 1.2 Ajouter les dépendances

Ajoutez les dépendances nécessaires à votre script. Par exemple, si votre script utilise `pandas` et `requests` :

```bash
pixi add python pandas requests
```

Ajoutez également les outils de développement dans un environnement dédié :

```bash
pixi add --feature dev ruff pyright pytest pytest-cov safety trivy
```

### 1.3 Déclarer les environnements dans `pixi.toml`

```toml
[environments]
default = { features = ["default"] }
dev = { features = ["default", "dev"] }
```

> **Vérification :** Supprimez votre environnement local et relancez `pixi install`. Le projet doit fonctionner sans aucune installation manuelle supplémentaire.

---

## Étape 2 — Enrichir le `pyproject.toml`

Pixi utilise un fichier `pyproject.toml` pour centraliser la configuration des outils. Créez-le ou enrichissez-le avec les sections suivantes.

### 2.1 Métadonnées du projet

```toml
[project]
name = "mon-projet"
version = "0.1.0"
description = "Description courte du script"
authors = [{ name = "Prénom Nom", email = "email@exemple.fr" }]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.10"
keywords = ["bioinformatique", "données", "automatisation"]
```

### 2.2 Configuration de Ruff

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "D", "N"]
ignore = ["D203", "D212"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"
```

### 2.3 Configuration de Pyright

```toml
[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "basic"
```

### 2.4 Configuration de Pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=. --cov-report=term-missing --cov-report=xml"
```

---

## Étape 3 — Contrôle du typage avec Pyright

Le typage statique permet de détecter des erreurs avant l'exécution du code.

### 3.1 Annoter le script

Ajoutez des annotations de types à toutes les fonctions du script :

**Avant (généré par IA, sans types)**
```python
def process_data(data, threshold):
    results = []
    for item in data:
        if item > threshold:
            results.append(item)
    return results
```

**Après (avec types)**

```python
def process_data(data: list[float], threshold: float) -> list[float]:
    """Filtre les éléments supérieurs au seuil donné.

    Args:
        data: Liste de valeurs numériques à filtrer.
        threshold: Seuil de filtrage.

    Returns:
        Liste des éléments strictement supérieurs au seuil.
    """
    results: list[float] = []
    for item in data:
        if item > threshold:
            results.append(item)
    return results
```

### 3.2 Lancer Pyright

```bash
pixi run -e dev pyright script.py
```

Corrigez toutes les erreurs remontées avant de passer à l'étape suivante.

---

## Étape 4 — Qualité d'écriture du code avec Ruff

Ruff est un linter **et** un formateur ultra-rapide pour Python. Il remplace à lui seul Black, isort, flake8 et pydocstyle.

### 4.1 Lancer le linter

```bash
pixi run -e dev ruff check .
```

### 4.2 Corriger automatiquement ce qui peut l'être

```bash
pixi run -e dev ruff check --fix .
```

### 4.3 Formater le code

```bash
pixi run -e dev ruff format .
```

### 4.4 Points à vérifier manuellement

Ruff ne peut pas tout corriger automatiquement. Vérifiez que :

- **Chaque fonction** dispose d'une docstring au format Nympy
- **Les noms de variables** sont explicites (`df` → `dataframe_resultats`, `x` → `valeur_seuil`)
- **Aucun `# type: ignore`** n'est utilisé sans justification commentée

> **Vérification :** `ruff check .` doit se terminer sans aucune erreur ni avertissement.

---

## Étape 5 — Contrôle des dépendances avec Safety

Safety vérifie si vos dépendances ont des vulnérabilités connues (CVE).

### 5.1 Scanner les dépendances

```bash
pixi run -e dev safety check 
```

### 5.2 Interpréter les résultats

- **Aucune vulnérabilité** : vous pouvez passer à la suite
- **Vulnérabilités détectées** : mettez à jour les packages concernés dans `pixi.toml` en spécifiant une version corrigée

```bash
pixi add "pandas>=2.1.0"  # exemple si pandas <2.1.0 est vulnérable
```

> **Livrable :** Capture d'écran ou sortie de `safety check` sans vulnérabilité critique.

---

## Étape 6 — Détection des failles de sécurité avec Trivy

Trivy analyse le code source et les fichiers de configuration pour détecter des secrets exposés, des mauvaises configurations ou des dépendances vulnérables.

### 6.1 Scanner le répertoire du projet

```bash
trivy fs --scanners secret,vuln,misconfig .
```

### 6.2 Points particuliers à surveiller

- **Secrets exposés** : clés API, mots de passe, tokens dans le code ou dans les fichiers de config
- **Vulnérabilités** dans les dépendances (croisement avec Safety)
- **Mauvaises configurations** : fichiers Docker, CI, etc.

### 6.3 Corriger les problèmes détectés

Si Trivy détecte des secrets dans le code :

1. Supprimez-les immédiatement du code
2. Utilisez des variables d'environnement ou un fichier `.env` (ajouté au `.gitignore`)
3. Si le secret a déjà été commité, utilisez `git filter-repo` pour purger l'historique

```python
# Mauvaise pratique
API_KEY = "sk-abc123xyz"

# Bonne pratique
import os
API_KEY = os.environ.get("API_KEY")
```

> **Livrable :** Sortie de Trivy sans vulnérabilité critique ni secret exposé.

---

## Étape 7 — Tests unitaires avec Pytest

Les tests garantissent que votre code fait ce qu'il est censé faire et continuera de le faire après des modifications.

### 7.1 Créer la structure de tests

```
projet/
├── script.py
├── tests/
│   ├── __init__.py
│   └── test_script.py
```

### 7.2 Écrire des tests unitaires

Pour chaque fonction du script, écrivez au minimum :

- Un test avec des données nominales (cas normal)
- Un test avec des valeurs limites (liste vide, zéro, valeur négative…)
- Un test vérifiant qu'une exception est levée si les entrées sont invalides

```python
# tests/test_script.py
import pytest
from script import process_data

def test_process_data_nominal() -> None:
    """Vérifie le comportement nominal de process_data."""
    result = process_data([1.0, 5.0, 3.0], threshold=2.0)
    assert result == [5.0, 3.0]

def test_process_data_empty_list() -> None:
    """Vérifie que process_data gère une liste vide."""
    result = process_data([], threshold=2.0)
    assert result == []

def test_process_data_all_below_threshold() -> None:
    """Vérifie qu'aucun élément n'est retourné si tous sont sous le seuil."""
    result = process_data([0.5, 1.0, 1.9], threshold=2.0)
    assert result == []

def test_process_data_invalid_input() -> None:
    """Vérifie qu'une erreur est levée pour une entrée invalide."""
    with pytest.raises(TypeError):
        process_data("pas une liste", threshold=2.0)  # type: ignore[arg-type]
```

### 7.3 Lancer les tests

```bash
pixi run -e dev pytest
```

---

## Étape 8 — Couverture de tests avec pytest-cov

La couverture mesure quelle proportion du code est exercée par vos tests.

### 8.1 Lancer les tests avec rapport de couverture

```bash
pixi run -e dev pytest --cov=. --cov-report=term-missing
```

### 8.2 Interpréter le rapport

```
---------- coverage: platform linux, python 3.10 ----------
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
script.py      42      6    86%   45, 67-72
-----------------------------------------
TOTAL          42      6    86%
```

- Les lignes listées sous "Missing" ne sont pas couvertes par les tests
- Ajoutez des tests pour couvrir ces cas

> **Objectif minimum :** 80% de couverture sur `script.py`.

### 8.3 Générer un rapport HTML (optionnel)

```bash
pixi run -e dev pytest --cov=. --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

---

## Étape 9 — Commandes Pixi

Pixi permet de définir des commandes personnalisées pour centraliser et documenter les tâches courantes du projet.

### 9.1 Ajouter les commandes dans `pixi.toml`

```toml
[feature.dev.tasks]
lint = "ruff check ."
format = "ruff format ."
typecheck = "pyright script.py"
safety-check = "safety check -r requirements.txt"
test = "pytest"
coverage = "pytest --cov=. --cov-report=term-missing"
all-checks = { depends-on = ["lint", "typecheck", "test"] }
```

### 9.2 Utiliser les commandes

```bash
pixi run lint          # Lancer le linter
pixi run format        # Formater le code
pixi run typecheck     # Vérifier les types
pixi run test          # Lancer les tests
pixi run coverage      # Tests + couverture
pixi run all-checks    # Tout en une commande
```

> **Vérification :** `pixi run all-checks` doit se terminer sans erreur.

---

## Étape 10 — README

Le README est le premier document qu'un utilisateur ou un développeur lit. Il doit permettre de comprendre et d'utiliser le projet en quelques minutes.

### Structure minimale attendue

```markdown
# Nom du projet

Description courte (1-2 phrases) de ce que fait le script.

## Prérequis

- [Pixi](https://pixi.sh) installé
- Python 3.10+

## Installation

```bash
git clone https://github.com/votre-compte/votre-projet.git
cd votre-projet
pixi install
```

## Utilisation

```bash
pixi run python script.py --input data.csv --output results.csv
```

## Commandes disponibles

| Commande                  | Description                        |
|---------------------------|------------------------------------|
| `pixi run lint`           | Vérification de la qualité du code |
| `pixi run format`         | Formatage automatique              |
| `pixi run typecheck`      | Vérification du typage             |
| `pixi run test`           | Lancement des tests unitaires      |
| `pixi run coverage`       | Rapport de couverture de tests     |
| `pixi run all-checks`     | Tous les contrôles en une commande |

## Structure du projet

```bash
.
├── script.py          # Script principal
├── tests/             # Tests unitaires
├── pyproject.toml     # Configuration des outils
├── pixi.toml          # Environnement et dépendances
└── README.md          # Ce fichier
```

---

## Récapitulatif des livrables

| Étape | Livrable attendu |
|-------|-----------------|
| 1 | `pixi.toml` avec dépendances de prod et de dev |
| 2 | `pyproject.toml` avec sections ruff, pyright, pytest |
| 3 | Code annoté, `pyright` sans erreur |
| 4 | `ruff check .` et `ruff format .` sans erreur |
| 5 | `safety check` sans vulnérabilité critique |
| 6 | `trivy fs .` sans secret exposé ni vulnérabilité critique |
| 7 | Suite de tests couvrant les cas nominaux et limites |
| 8 | Couverture ≥ 80% sur le script principal |
| 9 | Commandes Pixi fonctionnelles (`pixi run all-checks` passe) |
| 10 | README complet permettant de lancer le projet from scratch |

---
