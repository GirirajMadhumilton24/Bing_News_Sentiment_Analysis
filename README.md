# Bing News Sentiment Analysis with Microsoft Fabric

## Project Overview

This project builds an end-to-end news ingestion, transformation, sentiment analysis, and reporting pipeline using **Microsoft Fabric** services. It integrates Bing News data via the Bing Search API (or similar sources), transforms and analyzes the data, and delivers actionable insights through Power BI dashboards and real-time alerts.

The solution leverages **Lakehouse (Delta Lake)**, **Synapse Data Science**, **Power BI with Fabric schematic models**, **Fabric Pipelines**, and **Data Activator** to provide a scalable, automated, and governed analytics platform.

---

## Architecture and Workflow

### 1. Data Ingestion

- Configure Bing Search API (or equivalent) in Azure.
- Use Fabric Data Factory pipelines to pull the latest news JSON data via REST API.
- Store the raw JSON files in a Fabric Lakehouse (Delta Lake).
- Schedule pipeline runs for automated periodic ingestion.

### 2. Data Transformation

- Use Synapse Spark Notebooks to parse and clean raw JSON data.
- Extract key fields (title, description, category, url, image, provider, datePublished).
- Filter and handle inconsistent data.
- Convert date formats and save clean data as Delta tables in the Lakehouse.

### 3. Incremental Data Load (Type 1 SCD)

- Implement incremental loads via PySpark `MERGE` statements on Delta tables.
- Update existing records by matching on unique URL identifiers.
- Insert new records if no match exists.
- Manage schema and handle exceptions dynamically.

### 4. Sentiment Analysis

- Run Synapse Data Science notebooks using pre-trained models (`AnalyzeText` API) for sentiment classification on news descriptions.
- Append sentiment labels (positive, negative, neutral) to the data.
- Save sentiment-enriched data back to Delta Lake with incremental merge.

### 5. Power BI Reporting

- Create Fabric schematic datasets connecting to Lakehouse Delta tables.
- Build interactive dashboards with filters, slicers, and custom sentiment metrics.
- Format URLs as clickable links.
- Provide daily refreshed visuals for sentiment distributions and recent news.

### 6. Pipeline Orchestration

- Build and automate the entire workflow in Fabric Pipelines.
- Use parameters to customize search queries (e.g., topics or regions).
- Include error handling and data schema fixes.
- Schedule pipeline runs for regular updates.

### 7. Alerts and Monitoring

- Utilize Data Activator to define alert conditions based on sentiment thresholds.
- Send alerts via Microsoft Teams or Email.
- Test alerts and monitor via Fabric workspace tools.

---

## Key Microsoft Fabric Components Used

- **Lakehouse (Delta Lake):** For scalable, ACID-compliant data storage and incremental merges.
- **Synapse Data Science:** For applying pre-trained machine learning models on Spark data.
- **Power BI with Fabric Schematic Models:** For secure, governed, and performant analytics reporting.
- **Data Factory Pipelines:** For orchestrating data ingestion, transformation, and analysis workflows.
- **Data Activator:** For real-time alerts and notifications on business-critical metrics.

---

## How to Get Started

1. **Set up your Azure environment:**
   - Create resource group and API resources.
   - Acquire Bing API keys and endpoints.

2. **Create Microsoft Fabric workspace:**
   - Build Lakehouse for raw and processed data.
   - Configure Data Factory pipelines for data ingestion.
   - Develop Synapse notebooks for transformation and sentiment analysis.

3. **Configure Power BI:**
   - Create schematic datasets connecting to Lakehouse tables.
   - Design dashboards with sentiment insights.

4. **Build and schedule Fabric Pipelines:**
   - Orchestrate the entire process from ingestion to reporting.
   - Parameterize and schedule for daily runs.

5. **Set up Data Activator alerts:**
   - Define alert rules on Power BI dataset metrics.
   - Configure notification channels (Teams, email).

6. **Monitor and maintain:**
   - Track pipeline executions and alerts in Fabric workspace.
   - Tune and expand sentiment models and dashboards as needed.

---

## Summary

This project demonstrates a robust, scalable solution for real-time news sentiment analytics by combining:

- Efficient data ingestion and incremental Delta Lake merges.
- Pre-trained sentiment models executed in Synapse Data Science.
- Secure, dynamic Power BI reporting using Fabric schematic models.
- Automated pipelines for seamless end-to-end workflow.
- Real-time alerting with Data Activator for proactive insights.

---
