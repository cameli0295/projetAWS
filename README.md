# Projet Data Cloud AWS – ETL & Visualisation

Ce dépôt contient les livrables techniques du projet AWS Data Cloud.

## Arborescence livrable

```text
Projet_Data_AWS/
├── iam/
│   └── policy.json
├── s3_structure/
│   ├── raw_sales_example.csv
│   └── screenshots/
├── glue/
│   ├── glue_job.py
│   └── screenshots/
├── redshift/
│   ├── create_tables.sql
│   ├── copy_commands.sql
│   └── queries.sql
├── quicksight/
│   └── dashboards/
└── README.md
```

## Étape 1 – IAM

- Utilisateurs à créer dans AWS IAM :
  - `data_admin`
  - `data_engineer`
  - `data_analyst`
  - `data_viewer`
  - `auditor`
- Groupe IAM : `data-project-group`
- Policy personnalisée : `iam/policy.json`

## Étape 2 – S3

Bucket recommandé : `data-project-m2-master`

Arborescence à créer dans S3 :

```text
data-project-m2-master/
├── raw/
│   └── sales_raw.csv
├── processed/
│   └── sales_cleaned/
└── analytics/
    └── redshift_ready/
```

## Étape 3 – AWS Glue ETL

Script PySpark fourni : `glue/glue_job.py`

Transformations implémentées :
- Suppression des lignes nulles sur les colonnes critiques
- Cast des types (`qtysold`, `pricepaid`, etc.)
- Renommage des colonnes en `snake_case`
- Suppression des doublons
- Ajout de `total_price = qtysold * pricepaid`
- Export en Parquet vers `s3://data-project-m2-master/processed/sales_cleaned/`

## Étape 4 – Amazon Redshift Serverless

Scripts SQL :
- Création de table : `redshift/create_tables.sql`
- Chargement S3 -> Redshift : `redshift/copy_commands.sql`
- Requêtes analytiques : `redshift/queries.sql`

## Étape 5 – Amazon QuickSight

Visualisations attendues (à produire dans AWS Console) :
1. Top 10 acheteurs (`SUM(qtysold)`)
2. Chiffre d'affaires par événement (`SUM(total_price)`)
3. KPI volume total de ventes et CA global

> Ajouter les captures/exports dans `quicksight/dashboards/`.

## Remarque

Les captures d'écran demandées dans le sujet doivent être réalisées directement dans les consoles AWS (IAM, S3, Glue, Redshift, QuickSight) puis déposées dans les dossiers `screenshots/` et `quicksight/dashboards/`.
