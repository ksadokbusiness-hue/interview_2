# Exercice – cash net journalier

Tu rejoins l'équipe Trading Data. Message reçu de la Product Owner (Teams, ce matin) :

> « Hello, la trésorerie ne retrouve pas le cash net par produit en EUR sur plusieurs jours récents, les écarts sont énormes. Le job met aussi une éternité à tourner. Tu peux jeter un œil ? Je suis en comité toute la session, mais je réponds à tes questions. »

## Mise en place
Les données sont des fichiers CSV dans `data/` (ouvrables avec n'importe quel outil : DuckDB, pandas, Excel, éditeur).
```
pip install -r requirements.txt        # duckdb, pandas (déjà installés si l'environnement est préparé)
python -m unittest discover -s tests   # tests existants
python pipeline.py                     # produit output/cash_daily.csv
```
Données : `deals.csv` (transactions), `fx_rates.csv` (taux de change), `product_ref.csv` et `currency_ref.csv` (référentiels).

Pour analyser les données en SQL (DuckDB, lecture seule ; tables `deals`, `fx_rates`, `product_ref`, `currency_ref`, `cash_daily`) :
```
python query.py "describe deals"
python query.py "select product, currency, count(*) from deals group by all order by all"
python query.py "select * from fx_rates where rate_date = '2026-10-09'"
python query.py                        # mode interactif ; ou python query.py mon_fichier.sql
```

## Livrables
1. Un correctif de `pipeline.py` (la sortie reste `output/cash_daily.csv`, colonnes `deal_date, product, net_cash_eur`).
2. Au moins un test qui aurait détecté le problème.
3. Une note de 5 lignes maximum pour la PO : cause, correction, risques restants.

## Règles
- Utilise l'assistant IA de ton choix, comme au quotidien (Claude Code, Copilot, etc.). Partage ton écran.
- Les données sont fictives. Traite tout le reste comme un vrai environnement d'entreprise.
- Tu peux poser des questions à la PO (l'intervieweur) à tout moment.
- On évalue ta démarche autant que le résultat.
