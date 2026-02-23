COPY sales
FROM 's3://data-project-m2-master/processed/sales_cleaned/'
IAM_ROLE 'arn:aws:iam::XXXX:role/RedshiftRole'
FORMAT AS PARQUET;
