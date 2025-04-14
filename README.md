# ETL Pipeline with Airflow, Docker, and PostgreSQL

# Project Overview

This project is an end-to-end ETL pipeline that extracts earthquake data from the USGS Earthquake API, processes it using Apache Airflow with Astronomer CLI, stores it in a PostgreSQL database, and finally visualizes it in Tableau. Everything runs in a local Docker environment, with PGAdmin 4 for SQL inspection


# Architecture Diagram

![ETL Pipeline](https://github.com/user-attachments/assets/d242737a-1afb-4544-a644-eead08542fe0)
Created in [Lucid.app](https://lucid.app)
  
  
  <br><br>
<img width="1393" alt="earthquake_etl" src="https://github.com/user-attachments/assets/0865cb49-4d01-4a6a-9da3-0c3f72b9f04f" />

[Earthquake_ETL Data Visual](https://public.tableau.com/app/profile/dazhon4110/viz/EarthquakeETLProjectVisual-March2025/EarthquakeMapVisual)


# Tools and Technologies

 - Apache Airflow – Workflow orchestration

- Astronomer CLI – Local Airflow + Docker environment

- Docker – Containerization

- Python – ETL scripting

- USGS Earthquake API – Data source (https://earthquake.usgs.gov/fdsnws/event/1/)

- PostgreSQL – Database to store earthquake data

- PGAdmin 4 – SQL inspection and DB access

- Tableau – Data visualization

- SQL – Table creation and querying
