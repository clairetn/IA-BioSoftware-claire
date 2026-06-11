# TP — Dépôt GitHub et bonnes pratiques open source

## Contexte et objectifs

Un bon code ne vit pas seul : il vit dans un dépôt bien structuré, documenté, citable et archivé. Dans cette partie, vous allez transformer votre dépôt GitHub en un projet open source respectant les standards de la communauté scientifique et logicielle.

À la fin de cette partie, votre dépôt sera : lisible par des inconnus, contribuable par des tiers, citable dans des publications, et archivé de façon pérenne.

---

## Pré-requis

- Avoir terminé la partie code du TP
- Avoir un compte GitHub
- Avoir un compte [Zenodo](https://zenodo.org) (inscription gratuite, connexion via GitHub)
- Le dépôt GitHub du projet doit être **public**

---

## Étape 1 — Fichiers communautaires GitHub

GitHub reconnaît automatiquement un ensemble de fichiers placés à la racine du dépôt (ou dans `.github/`) et les met en avant dans l'interface. Ces fichiers signalent aux utilisateurs et contributeurs comment interagir avec le projet.

### 1.1 LICENSE

La licence définit ce que les autres ont le droit de faire avec votre code. Sans licence, le code est techniquement "tous droits réservés".

**Créer la licence depuis GitHub :**

1. Dans votre dépôt, cliquez sur "Add file" → "Create new file"
2. Nommez le fichier `LICENSE`
3. Cliquez sur "Choose a license template"
4. Sélectionnez **MIT** (permissive, recommandée pour la recherche)
5. Renseignez l'année et votre nom
6. Committez directement sur `main`

> **Pourquoi MIT ?** C'est la licence la plus permissive et la plus compatible avec les autres projets open source. Pour du code de recherche publique, elle est généralement recommandée. Si votre organisme a des consignes spécifiques (CNRS, Inria…), respectez-les.

---

### 1.2 `CODE_OF_CONDUCT.md`

Le code de conduite définit les règles de comportement attendues dans la communauté du projet.

**Depuis GitHub :**

1. "Add file" → "Create new file"
2. Nommez le fichier `CODE_OF_CONDUCT.md`
3. Cliquez sur "Choose a code of conduct template"
4. Sélectionnez **Contributor Covenant** (standard de l'industrie)
5. Remplacez `[INSERT CONTACT METHOD]` par une adresse email de contact
6. Committez

---

### 1.3 `CONTRIBUTING.md`

Ce fichier explique comment contribuer au projet : comment signaler un bug, proposer une fonctionnalité, soumettre une Pull Request.

Créez `.github/CONTRIBUTING.md` avec la structure suivante :

```markdown
# Guide de contribution

Merci de l'intérêt que vous portez à ce projet !

## Signaler un bug

Avant d'ouvrir une issue, vérifiez qu'elle n'existe pas déjà.
Utilisez le template "Bug report" et renseignez :
- La version utilisée
- Les étapes pour reproduire le problème
- Le comportement attendu vs observé

## Proposer une fonctionnalité

Ouvrez une issue avec le template "Feature request" en décrivant
le besoin et le comportement souhaité.

## Soumettre une Pull Request

1. Forkez le dépôt
2. Créez une branche depuis `main` : `git checkout -b feat/ma-fonctionnalite`
3. Faites vos modifications
4. Vérifiez que tous les checks passent : `pixi run all-checks`
5. Committez avec un message clair (voir Convention de commit ci-dessous)
6. Ouvrez une Pull Request vers `main`

## Convention de commit

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation uniquement
- `test:` ajout ou modification de tests
- `chore:` maintenance (dépendances, CI…)

Exemple : `feat: ajouter le support des fichiers CSV compressés`

## Environnement de développement

```bash
git clone https://github.com/votre-compte/votre-projet.git
cd votre-projet
pixi install
pixi run all-checks
```
```

---

### 1.4 Templates d'issues et de Pull Request

Les templates guident les contributeurs pour fournir les bonnes informations dès le départ.

Créez les fichiers suivants :

**`.github/ISSUE_TEMPLATE/bug_report.md`**

```markdown
---
name: Bug report
about: Signaler un comportement inattendu
labels: bug
---

## Description du bug
<!-- Description claire et concise -->

## Étapes pour reproduire
1. ...
2. ...

## Comportement attendu

## Comportement observé

## Environnement
- OS :
- Version Python :
- Version du projet :
```

**`.github/ISSUE_TEMPLATE/feature_request.md`**

```markdown
---
name: Feature request
about: Proposer une nouvelle fonctionnalité
labels: enhancement
---

## Problème à résoudre
<!-- Décrivez le besoin -->

## Solution proposée

## Alternatives envisagées
```

**`.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## Description
<!-- Décrivez les changements apportés -->

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Documentation
- [ ] Refactoring

## Checklist
- [ ] `pixi run all-checks` passe sans erreur
- [ ] Les tests couvrent les nouvelles fonctionnalités
- [ ] La documentation a été mise à jour
```

---

## Étape 2 — Métadonnées du logiciel

Ces fichiers permettent à des machines (moteurs de recherche, archives, gestionnaires de citations) de comprendre et référencer votre projet.

### 2.1 `CITATION.cff`

Le fichier CFF (Citation File Format) permet aux utilisateurs de citer votre logiciel facilement. GitHub l'affiche avec un bouton "Cite this repository".

Créez `CITATION.cff` à la racine :

```yaml
cff-version: 1.2.0
message: "Si vous utilisez ce logiciel, merci de le citer comme ci-dessous."
type: software
title: "Nom de votre projet"
abstract: "Description courte de ce que fait le projet."
authors:
  - family-names: "Votre Nom"
    given-names: "Votre Prénom"
    orcid: "https://orcid.org/0000-0000-0000-0000"  # Remplacez par votre ORCID
    affiliation: "Votre institution"
repository-code: "https://github.com/votre-compte/votre-projet"
license: MIT
version: "0.1.0"
date-released: "2025-01-01"
keywords:
  - bioinformatique
  - python
```

> **ORCID :** Si vous n'avez pas d'ORCID, c'est le moment de le créer sur [orcid.org](https://orcid.org). C'est l'identifiant persistant des chercheurs, reconnu par toutes les grandes institutions.

---

### 2.2 `codemeta.json`

CodeMeta est un standard de métadonnées pour les logiciels scientifiques, utilisé notamment par Software Heritage et Zenodo.

Le plus simple est de le générer via [codemeta.github.io](https://codemeta.github.io/codemeta-generator/).

Structure minimale à créer `codemeta.json` :

```json
{
  "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
  "@type": "SoftwareSourceCode",
  "name": "Nom du projet",
  "description": "Description courte",
  "version": "0.1.0",
  "dateCreated": "2025-01-01",
  "datePublished": "2025-01-01",
  "license": "https://spdx.org/licenses/MIT.html",
  "programmingLanguage": {
    "@type": "ComputerLanguage",
    "name": "Python",
    "version": "3.10"
  },
  "author": [
    {
      "@type": "Person",
      "givenName": "Prénom",
      "familyName": "Nom",
      "@id": "https://orcid.org/0000-0000-0000-0000"
    }
  ],
  "codeRepository": "https://github.com/votre-compte/votre-projet",
  "keywords": ["bioinformatique", "python"]
}
```

> **Cohérence :** Les informations dans `codemeta.json`, `CITATION.cff` et `pyproject.toml` doivent être identiques (version, auteurs, licence). Si vous modifiez l'une, modifiez les trois.

---

## Étape 3 — Pre-commit hooks

Les pre-commit hooks sont des scripts qui s'exécutent automatiquement avant chaque commit. Ils empêchent de commiter du code qui ne respecte pas les standards.

### 3.1 Installer pre-commit

```bash
pixi add --feature dev pre-commit
```

### 3.2 Créer `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: detect-private-key       # Bloque les clés privées
      - id: no-commit-to-branch      # Interdit de commiter directement sur main
        args: ["--branch", "main"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format

  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.365
    hooks:
      - id: pyright
```

### 3.3 Activer les hooks

```bash
pixi run -e dev pre-commit install
```

### 3.4 Tester sur tous les fichiers existants

```bash
pixi run -e dev pre-commit run --all-files
```

Ajoutez la commande dans `pixi.toml` :

```toml
[feature.dev.tasks]
pre-commit = "pre-commit run --all-files"
```

> **Test :** Essayez de commiter un fichier avec une ligne qui traîne un espace en fin de ligne. Le hook doit bloquer le commit et corriger automatiquement.

---

## Étape 4 — Intégration continue (CI) avec GitHub Actions

Les CI s'exécutent automatiquement sur chaque push et Pull Request. Elles garantissent que le code reste sain à tout moment.

Créez le répertoire `.github/workflows/`.

### 4.1 CI de qualité du code (`ci-quality.yml`)

Cette CI lance tous les contrôles qualité à chaque push.

```yaml
name: Quality checks

on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Pixi
        uses: prefix-dev/setup-pixi@v0.8.1
        with:
          pixi-version: latest
          environments: dev

      - name: Lint (Ruff)
        run: pixi run -e dev lint

      - name: Format check (Ruff)
        run: pixi run -e dev ruff format --check .

      - name: Type check (Pyright)
        run: pixi run -e dev typecheck

      - name: Safety check
        run: |
          pixi run -e dev pip freeze > requirements.txt
          pixi run -e dev safety check -r requirements.txt

      - name: Run tests with coverage
        run: pixi run -e dev coverage

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scan-ref: .
          scanners: secret,vuln,misconfig
          exit-code: 1
          severity: CRITICAL,HIGH
```

---

### 4.2 CI de release et changelog (`ci-release.yml`)

Cette CI se déclenche lors de la création d'un tag de version. Elle génère automatiquement le changelog et publie la release sur GitHub.

```yaml
name: Release

on:
  push:
    tags:
      - "v*.*.*"   # Se déclenche sur les tags comme v1.0.0, v0.2.1...

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write   # Nécessaire pour créer la release

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # Récupère tout l'historique pour le changelog

      - name: Install Pixi
        uses: prefix-dev/setup-pixi@v0.8.1
        with:
          environments: dev

      - name: Run all checks before release
        run: pixi run -e dev all-checks

      - name: Generate changelog
        uses: orhun/git-cliff-action@v3
        id: git-cliff
        with:
          config: cliff.toml
          args: --latest --strip header
        env:
          OUTPUT: CHANGELOG.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
          generate_release_notes: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Configuration de git-cliff** — Créez `cliff.toml` à la racine :

```toml
[changelog]
header = "# Changelog\n\n"
body = """
## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }} ([{{ commit.id | truncate(length=7, end="") }}]({{ commit.remote.link }}/commit/{{ commit.id }}))
{% endfor %}
{% endfor %}
"""
trim = true

[git]
conventional_commits = true
commit_parsers = [
  { message = "^feat", group = "Nouvelles fonctionnalités" },
  { message = "^fix", group = "Corrections de bugs" },
  { message = "^docs", group = "Documentation" },
  { message = "^test", group = "Tests" },
  { message = "^chore", group = "Maintenance" },
]
```

> **Pour créer une release :** taguez votre commit et poussez le tag.
> ```bash
> git tag v0.1.0
> git push origin v0.1.0
> ```

---

## Étape 5 — Archivage sur Zenodo

Zenodo est la plateforme d'archivage du CERN. Chaque dépôt GitHub peut y être archivé automatiquement à chaque release, et recevoir un DOI citable.

### 5.1 Connecter GitHub à Zenodo

1. Allez sur [zenodo.org](https://zenodo.org) et connectez-vous avec GitHub
2. Dans votre profil Zenodo → "GitHub"
3. Trouvez votre dépôt dans la liste et **activez le toggle**

Zenodo créera désormais automatiquement une archive à chaque nouvelle release GitHub.

### 5.2 Créer une première release pour obtenir le DOI

```bash
git tag v0.1.0
git push origin v0.1.0
```

La CI `ci-release.yml` va créer la release GitHub, puis Zenodo va automatiquement l'archiver et lui attribuer un DOI.

### 5.3 Mettre à jour `CITATION.cff` avec le DOI

Une fois le DOI obtenu sur Zenodo :

```yaml
# Ajoutez dans CITATION.cff
identifiers:
  - type: doi
    value: "10.5281/zenodo.XXXXXXX"
    description: "DOI de la version 0.1.0"
```

---

## Étape 6 — Archivage sur Software Heritage

Software Heritage est l'archive universelle du code source logiciel. Contrairement à Zenodo (snapshots de releases), Software Heritage archive l'intégralité de l'historique Git.

### 6.1 Déclencher l'archivage

1. Allez sur [save.softwareheritage.org](https://save.softwareheritage.org)
2. Renseignez l'URL de votre dépôt GitHub
3. Cliquez sur "Save"

L'archivage peut prendre quelques minutes. Vous recevrez un **SWHID** (Software Heritage Identifier), identifiant pérenne de votre code.

### 6.2 Format du SWHID

```
swh:1:dir:abc123...   # répertoire
swh:1:rev:def456...   # commit spécifique
swh:1:snp:ghi789...   # snapshot complet
```

### 6.3 Mettre à jour `codemeta.json` avec le SWHID

```json
{
  "identifier": "swh:1:dir:abc123def456..."
}
```

---

## Récapitulatif de la structure finale du dépôt

```
votre-projet/
├── .github/
│   ├── workflows/
│   │   ├── ci-quality.yml       # CI : lint, types, tests, sécurité
│   │   └── ci-release.yml       # CI : changelog + release automatique
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CONTRIBUTING.md
├── tests/
│   ├── __init__.py
│   └── test_script.py
├── .pre-commit-config.yaml
├── CHANGELOG.md                  # Généré automatiquement
├── CITATION.cff
├── cliff.toml
├── CODE_OF_CONDUCT.md
├── codemeta.json
├── LICENSE
├── pixi.toml
├── pyproject.toml
├── README.md
└── script.py
```

---

## Récapitulatif des livrables

| Étape | Livrable attendu |
|-------|-----------------|
| 1 | `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, templates d'issues et PR |
| 2 | `CITATION.cff` et `codemeta.json` cohérents avec `pyproject.toml` |
| 3 | `.pre-commit-config.yaml` actif, `pre-commit run --all-files` sans erreur |
| 4a | CI qualité qui passe au vert sur `main` |
| 4b | CI release fonctionnelle, release v0.1.0 créée avec changelog |
| 5 | DOI Zenodo obtenu, `CITATION.cff` mis à jour |
| 6 | SWHID obtenu, `codemeta.json` mis à jour |
