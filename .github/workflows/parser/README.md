# How To Use Manually

This script is triggered on push to main in the github actions.
It converts markdown files to cobra pdf subjects.

## Virtual env

First, cd your way to the script's directory

```bash
cd .github/workflows/parser
```

I strongly suggest making a virtual env for ease of use.

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Running

You only need to give it the path of the markdown file you want to convert.
*No more title, version, campus bullshit. erm.*

```bash
python3 cc_subjects.py <PATH-TO-MD>
```

Important note. The pdf will be generated in the parent directory of the markdown file. Exemple:

```
├── nom_du_sujet
│   ├── Sujet.pdf // Généré
│   └── subject
│       └── sujet.md
│
```
