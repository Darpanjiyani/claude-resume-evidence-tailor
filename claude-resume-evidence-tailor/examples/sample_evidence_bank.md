# Evidence Bank — Jordan Lee (fictional sample)

Everything in this file is made up to show the format. Lines in `[square brackets]` are deliberately left unconfirmed so you can see how the skill treats them: it never puts them on the resume and lists them under "Confirm Before Sending" instead.

---

## Project Library

### 1. Inventory Analytics with dbt
- **Status:** Completed
- **Origin:** Self-designed
- **Team / my part:** Solo. Built the whole project.
- **Best for roles:** Analytics Engineer, Data Engineer
- **Domain:** Retail / E-commerce
- **Tools and tech:** dbt, Snowflake, SQL, GitHub Actions
- **Methods and concepts:** Staging, intermediate and mart layers; star schema; dbt tests (unique, not_null, relationships); CI that runs tests on every pull request
- **Data and scale:** 3 source tables, ~1.2M inventory snapshot rows; 14 dbt models; 31 tests
- **Results and metrics:** Daily stockout report for 40 stores; failing tests block a merge
- **Link:** https://github.com/example/inventory-dbt
- **Ready-to-use bullets (one line each):**
  - Modeled 1.2M inventory snapshot rows into a 14-model dbt star schema on Snowflake for a 40-store stockout report
  - Added 31 dbt tests and a GitHub Actions check that runs them on every pull request

### 2. Delivery Time Forecast
- **Status:** Completed
- **Origin:** Course project, Machine Learning, State University
- **Team / my part:** Built the whole project. Co-authors listed (the report names 2 authors).
- **Best for roles:** Data Scientist, Data Analyst
- **Domain:** Transportation / Mobility
- **Tools and tech:** Python, pandas, scikit-learn, Prophet
- **Methods and concepts:** Time-series forecasting, feature engineering, baseline comparison
- **Data and scale:** 18 months of delivery records, ~250K rows
- **Results and metrics:** MAPE 11% vs 19% for a naive baseline
- **Link:** https://github.com/example/delivery-forecast
- **Ready-to-use bullets (one line each):**
  - Forecast weekly delivery times with Prophet on 250K records, cutting MAPE from 19% (naive baseline) to 11%
  - Engineered holiday and weather features in pandas and compared Prophet with a scikit-learn gradient boosting model

### 3. Warehouse Sensor Pipeline
- **Status:** Planned
- **Origin:** Self-designed
- **Team / my part:** Solo
- **Best for roles:** Data Engineer
- **Domain:** Transportation / Mobility
- **Tools and tech:** [Kafka, Airflow, Snowflake — not built yet]
- **Methods and concepts:** [streaming ingestion]
- **Data and scale:** [—]
- **Results and metrics:** [—]
- **Link:** [—]
- **Ready-to-use bullets (one line each):**
  - [not built yet; Planned projects only appear as Gap Triage suggestions]

### 4. Student Club Membership Dashboard
- **Status:** Completed
- **Origin:** [Course project (which course?)]
- **Team / my part:** [Team of 4; my part: ?]
- **Best for roles:** Data Analyst, BI Analyst
- **Domain:** Tech / General
- **Tools and tech:** Tableau, Excel
- **Methods and concepts:** Dashboard design, survey data cleaning
- **Data and scale:** [number of survey responses]
- **Results and metrics:** [—]
- **Link:** [—]
- **Ready-to-use bullets (one line each):**
  - [Contributed to a 4-person team that ...]

---

## Skills learned through self-study (Skills section only)

- **Apache Airflow** — self-study repo with 6 practice DAGs (TaskFlow API, schedules, retries) on Docker Compose. Practice data only. Can explain in an interview? Y

---

## Metrics not on the resume
- [Hours saved per week by the site-manager KPI dashboard: __]

## Domain exposure
- Transportation / Logistics: shipment data, warehouse KPIs (Acme Logistics)
- Retail: weekly store sales reporting (Bluebird Retail internship)

## Stakeholders worked with
- Site managers, finance analysts, merchandising team

## Education
- BS in Statistics, State University (May 2024)
- Relevant courses: Machine Learning, Database Systems, Regression Analysis
