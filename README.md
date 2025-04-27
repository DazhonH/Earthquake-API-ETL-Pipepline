# ETL Pipeline with Airflow, Docker, and PostgreSQL

# Project Overview

This project is an end-to-end ETL pipeline that extracts earthquake data from the USGS Earthquake API, processes it using Apache Airflow with Astronomer CLI, stores it in a PostgreSQL database, and finally visualizes it in Tableau. Everything runs in a local Docker environment, with PGAdmin 4.


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

- IDE - VSCode

# Local Environment Setup

To set up airflow, I've installed Docker and Astronomer CLI. Astronomer simplifies the management and setup of Apache Airflow.

[Astro Installation](https://www.astronomer.io/docs/astro/cli/install-cli/)

 I'm using Docker with Astro CLI and Apache Airflow to build and run data pipelines in a local environment that closely mirrors production. This setup makes it easy to test, scale, and manage workflows efficiently.

To begin the project I create the following directory in my terminal:

``` bash

mkdir earthquake_etl

cd earthquake_etl

```

After the directory is created, I input the following command into my terminal

``` bash

astro dev init

```

This sets up my local environment in VSCode for developing airflow workflows.
<br><br>
<img width="255" alt="Vscode Airflow Env" src="https://github.com/user-attachments/assets/1d8be271-f5cf-428d-a54b-c42b6c37752e" />

To start the astro project I input the following command into the terminal.
```bash

astro dev start

```

This command builds the project and spins up 4 Docker containers, each for a different Airflow component:

- Postgres: Airflow's metadata database

- Webserver: The Airflow component responsible for rendering the Airflow UI

- Scheduler: The Airflow component responsible for monitoring and triggering tasks

- Triggerer: The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met.

<br><br>
<img width="1037" alt="Docker Containers" src="https://github.com/user-attachments/assets/ee07cf58-7f48-4369-9882-296a1b979092" />

After a successful setup, I received the credentials to Postgres and Airflow's UI.

<br><br>
<img width="634" alt="Astro credentials" src="https://github.com/user-attachments/assets/ea185320-4fd0-475c-95b8-f177f33b1a99" />

In the local environment under dags, I created a DAG file ETL.py to write my code.

Below is the code to extract the data from the api, transform the data, and then loaded into my local Postgres.

[ETL Pipeline Code](https://github.com/DazhonH/Earthquake-API-ETL-Pipepline/blob/6e7ee48dff2b89056c2c76d0627afe740dad2567/Code/DAG%20-%20ETL.py)

After initializing my dag, it appeared in Airflow's UI.

Before running the dag, I connected to Postgres via admin - connections.

I pressed play to run the dag and it was successful.
<br><br>

<img width="1431" alt="ETL Airflow Success" src="https://github.com/user-attachments/assets/d7ccb007-9bd6-4822-a9cc-5872386740fb" />

<br><br>

<img width="1440" alt="ETl Airflow 2" src="https://github.com/user-attachments/assets/8ac1e709-a3cb-4f3f-8e6d-0ef42e7e8691" />

Once the data was loaded into my local Postgres, I derived a couple of insights.


 1. Finding earthquakes with high sig_class.

```sql
   SELECT DISTINCT ON (state_province)
       state_province,
	   place,
	   sig_class
FROM earthquake
WHERE sig_class = 'High'
GROUP BY place,
         state_province,
		 sig_class
ORDER BY state_province,
        sig_class DESC
LIMIT 5;
```
<img width="583" alt="1 SQL" src="https://github.com/user-attachments/assets/48ec5c5b-9f19-4044-91f4-6459f4ef5779" />
<br><br>


2. Top 5 states/provinces by count of earthquakes.

```sql
SELECT state_province,
	   Count(*) AS quake_count
FROM earthquake
GROUP BY state_province
ORDER BY quake_count DESC
LIMIT 5;
```
<img width="333" alt="2 SQL" src="https://github.com/user-attachments/assets/6f0eb1ab-b713-46e8-b235-d19489d20d83" />
<br><br>
 
3. Number of earthquakes by elevation.

```sql
SELECT CASE 
            WHEN elevation < 0 THEN 'Below Sea Level'
            WHEN elevation BETWEEN 0 AND 500 THEN '0-500m'
            WHEN elevation BETWEEN 501 AND 1000 THEN '501-1000m'
            ELSE 'Above 1000m'
       END AS elevation_range,
       COUNT(*) AS quake_count
FROM earthquake
GROUP BY elevation_range
ORDER BY quake_count DESC;
```
<img width="338" alt="3 SQL" src="https://github.com/user-attachments/assets/4b793a60-2015-40ea-8904-8debc44ad68d" />
<br><br>


4. Top 5 strongest earthquakes by magnitude.

```sql
SELECT state_province, 
       ROUND(AVG(mag)::NUMERIC, 2) AS avg_magnitude
FROM earthquake
GROUP BY state_province
ORDER BY avg_magnitude DESC
LIMIT 5;
```
<img width="375" alt="4 SQL" src="https://github.com/user-attachments/assets/6f6556c1-ee7b-49f6-ad0e-c4cf04161f42" />
<br><br>

Lastly, the data was ingested into Tableau for visualization. (Scroll to the top)
<img width="1437" alt=" Tableau Screenshot" src="https://github.com/user-attachments/assets/2e63593f-ffbf-4aa0-bb7e-b110847faab4" />
<br><br>

Tableau public was used because I do not have Tableau Desktop downloaded. With Tableau Public, I;m only able to upload CSV files and not connect to any sources.

# Problems

1. When creating my airflow environment, port 5432 was in use on a Postgres server. In airflow using Astronomer, Postgres is automatically mapped to 5432. This caused the failure for the environment set-up. However, port 5433 was free. To change the sql mapping, i wrote this into the terminal:

```bash

astro config set postgres.port 5433

```
