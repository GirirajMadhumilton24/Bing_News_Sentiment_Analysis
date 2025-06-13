# News Sentiment Analysis Project with Microsoft Fabric

## Overview

This project implements an end-to-end news ingestion, transformation, sentiment analysis, and reporting pipeline using **Microsoft Fabric** services. It leverages the **Lakehouse**, **Synapse Data Science**, **Power BI**, and **Data Activator** within Fabric to create a scalable, automated solution for real-time news sentiment insights.

---

## Architecture and Components

### 1. Incremental Data Load (Type 1 Slowly Changing Dimension)

- We utilize a **Type 1** data warehouse approach for incremental data loading.
- New data is merged into existing Delta tables in the **Lakehouse** using a SQL `MERGE` operation:
  - If a record with the same identifier (URL) exists and differs, it is updated.
  - If no matching record exists, the new record is inserted.
- This logic is embedded inside a `try-except` block in PySpark within Fabric to handle table creation and merging dynamically.
- The incremental load is implemented using **Delta Lake** tables in Fabric's Lakehouse.

---

### 2. Sentiment Analysis with Synapse Data Science

- Sentiment analysis is performed on the news **description** column using a **pre-trained model** available in the **Synapse data science tool** in Fabric.
- We create a notebook named **`news_sentiment_analysis`**, and load data directly from the Lakehouse Delta table (`tbl_latest_news`).
- The analysis uses the `AnalyzeText` service from the **Synapse ML** library, specifying `SentimentAnalysis` as the analysis kind.
- The sentiment results are extracted from JSON responses and appended as a new column.
- The resulting data is saved back to the Lakehouse as a Delta table (`tbl_sentiment_analysis`) using the same Type 1 merge logic.

---

### 3. Power BI Reporting with Fabric Schematic Models

- We build interactive dashboards in **Power BI** connected via **Fabric schematic models** for:
  - Secure data access governance.
  - Selective loading of tables rather than the entire Lakehouse dataset.
- The schematic model is named (e.g., `bing-news-dashboard-dataset`) and includes the sentiment analysis table.
- URLs are formatted as clickable web URLs in Power BI by adjusting the data type in the model.
- Filters and slicers (e.g., by year) and "Top N" filters are configured for recent news display.
- Custom measures are created in Power BI to calculate positive, neutral, and negative sentiment percentages dynamically.
- Visuals such as cards display the percentage sentiment metrics updated daily.

---

### 4. Pipeline Orchestration in Fabric

- Pipelines automate the entire workflow:
  - Data ingestion from API to Lakehouse.
  - Data transformation and cleaning.
  - Sentiment analysis notebook execution.
- Pipelines are parameterized to allow dynamic search terms (e.g., `latest news`, `football`, `movies`).
- Schedules enable automated daily runs at specified times.
- Pipelines include error handling and schema management (e.g., date formatting fixes for `datePublished`).

---

### 5. Alerts with Data Activator

- **Data Activator** in Fabric is used to create real-time alerts on sentiment changes in Power BI dashboards.
- Alerts trigger on specific conditions (e.g., positive sentiment exceeds 6%).
- Notifications can be delivered to Outlook, Teams, or email.
- Test alerts validate the setup before live monitoring.
- Activators are managed and monitored within the Fabric workspace.

---

## Key Fabric Features Utilized

- **Lakehouse** (Delta Lake) for scalable data storage and incremental merges.
- **Synapse Data Science** for applying pre-trained models on Lakehouse data without extensive model training overhead.
- **Power BI** integrated with Fabric schematic models for advanced reporting, data security, and governance.
- **Pipeline Orchestration** within Fabric for automated, parameter-driven data workflows.
- **Data Activator** for setting up automated, actionable alerts linked to Power BI reports.

---

## Summary

This project demonstrates a comprehensive data engineering and data science pipeline leveraging Microsoft Fabric’s end-to-end capabilities:

- Efficient **incremental loading** and **data management** using Delta Lake in Fabric Lakehouse.
- Use of **pre-trained sentiment analysis models** via Synapse Data Science notebooks.
- Dynamic, governed **reporting dashboards** using Power BI schematic models.
- Robust **orchestration and automation** of data workflows with Fabric Pipelines.
- Real-time **business alerts** powered by Data Activator.

Together, these components deliver a seamless, scalable solution for extracting actionable insights from news data with sentiment analysis and real-time monitoring.

---

## How to Use

1. Clone the repository.
2. Deploy the pipeline and notebooks in your Microsoft Fabric workspace.
3. Configure Power BI reports with schematic models for dashboarding.
4. Set up Data Activator alerts as needed.
5. Schedule pipelines to run automatically with desired parameters.
6. Monitor pipeline runs and alerts via the Fabric monitoring tools.

---
