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



