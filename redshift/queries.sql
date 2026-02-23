-- 1) Top acheteurs (par volume vendu)
SELECT
    buyerid,
    SUM(qtysold) AS total_qty_sold,
    SUM(total_price) AS total_revenue
FROM sales
GROUP BY buyerid
ORDER BY total_qty_sold DESC
LIMIT 10;

-- 2) Chiffre d'affaires total
SELECT
    SUM(total_price) AS chiffre_affaires_total
FROM sales;

-- 3) Ventes par événement
SELECT
    eventid,
    SUM(qtysold) AS total_qty_sold,
    SUM(total_price) AS total_revenue
FROM sales
GROUP BY eventid
ORDER BY total_revenue DESC;
