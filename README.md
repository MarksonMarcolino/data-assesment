# Ucademy Data Assessment

This project presents a complete data pipeline solution for Ucademy's technical assessment. It involves an ETL process using Python and MongoDB Atlas, exploratory data analysis (EDA), anomaly detection in lead conversion data, an interactive dashboard built with Streamlit, and a notebook for generating visual reports.

---

## Project Structure

```
.
├── data/                    # Raw input files (campaigns.json, leads.json, inscriptions.json)
├── output/                 # Processed files and exported visualizations
├── src/
│   ├── etl/
│   │   ├── prepare_dataset.py     # ETL logic: parsing, merging, anomaly detection
│   │   ├── upload_to_mongo.py     # Upload sanitized data to MongoDB
│   │   └── test_mongo_connection.py
│   ├── dashboard/
│   │   └── app.py                 # Streamlit dashboard
│   └── explore_dataset.ipynb     # EDA and automated report in Jupyter Notebook
├── .env                         # MongoDB credentials (not included in repo)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Features

* Clean and merge raw JSON datasets
* Parse European currency values
* Compute conversion delays
* Detect data anomalies (e.g., negative delays, missing inscriptions)
* Upload to MongoDB Atlas
* Explore insights using interactive filters and charts in a dashboard
* Generate automated reports with metrics, visualizations, and interpretations

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/MarksonMarcolino/ucademy-data-assessment.git
   cd ucademy-data-assessment
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory:

   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
   MONGO_DB=ucademy
   MONGO_COLLECTION=leads_enriched
   ```

5. **Run the ETL pipeline**

   ```bash
   python src/etl/prepare_dataset.py
   ```

6. **Launch the Streamlit dashboard**

   ```bash
   streamlit run src/dashboard/app.py
   ```

7. **Open the EDA notebook**

   ```bash
   jupyter notebook src/explore_dataset.ipynb
   ```

---

## Dashboard Features

* **Campaign Filter**: Select one or more campaigns
* **Date Range Filter**: Define lead creation date window
* **Valid Conversions Filter**: Toggle to view all or only valid conversions
* **Metrics Display**:

  * Total Leads
  * Valid Conversions
  * Invalid Conversions
* **Charts**:

  * Conversions by Campaign
  * Payment Distribution (Box Plot)
  * Anomaly Types by Campaign
  * Conversion Rate by Input Channel
  * Conversion Rate by Campaign
  * Funnel Chart of Conversion Evolution

---

## Proposed Automation

To automate daily ETL and dashboard updates:

* **Trigger**: Use `cron` or Apache Airflow to run `prepare_dataset.py`
* **Database**: MongoDB Atlas stores cleaned and enriched data
* **Frontend**: Streamlit automatically fetches updated data

---

## Deliverables

* Source code (well-documented and modular)
* Dashboard with interactive filters and charts
* MongoDB-based backend
* Automated Jupyter notebook report
* Proposal for pipeline automation

---

## License

This project is licensed for the purpose of the Ucademy technical assessment only.
