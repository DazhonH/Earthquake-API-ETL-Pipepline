import requests
import pandas as pd
from datetime import date, timedelta, datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

@dag(
    start_date=datetime(2025, 3, 24),
    schedule='@once',
    catchup=False,
    tags=['etl']
)
def earthquake_etl():

    @task()
    def extract():
        start_date = date.today() - timedelta(7)
        end_date = date.today() - timedelta(1)

        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("API fetch successful")
            return data
        else:
            raise Exception("Error fetching JSON data")

    @task()
    def transform(data):
        data_raw = pd.json_normalize(data['features'])

        # Dropping unwanted columns
        data_cleaned = data_raw.drop(columns=['properties.detail', 'properties.url', 'properties.tz',
                                              'properties.felt', 'properties.nst', 'properties.gap',
                                              'properties.dmin', 'geometry.type', 'properties.cdi',
                                              'properties.mmi', 'properties.alert', 'properties.status',
                                              'properties.net', 'properties.code', 'properties.ids',
                                              'properties.sources', 'properties.tsunami', 'properties.types',
                                              'properties.rms', 'properties.type', 'type'])

        # Convert timestamp to datetime
        data_cleaned['properties.time'] = pd.to_datetime(data_cleaned['properties.time'] / 1000, unit='s')
        data_cleaned['properties.updated'] = pd.to_datetime(data_cleaned['properties.updated'] / 1000, unit='s')

        # Convert datetime to string (ISO format)
        data_cleaned['properties.time'] = data_cleaned['properties.time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data_cleaned['properties.updated'] = data_cleaned['properties.updated'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Extract coordinates
        data_cleaned[['longitude', 'latitude', 'elevation']] = pd.DataFrame(
            data_cleaned['geometry.coordinates'].to_list(), index=data_cleaned.index)
        data_cleaned = data_cleaned.drop(columns=['geometry.coordinates'])

        # Rename columns
        data_cleaned = data_cleaned.rename(columns={'properties.mag': 'mag',
                                                    'properties.place': 'place',
                                                    'properties.time': 'time',
                                                    'properties.updated': 'updated',
                                                    'properties.sig': 'sig',
                                                    'properties.magType': 'magType',
                                                    'properties.title': 'title'})

        # Define significance class
        def sig_class(sig):
            if sig < 100:
                return 'Low'
            elif 100 <= sig < 500:
                return 'Moderate'
            else:
                return 'High'

        # Apply classification
        data_cleaned['sig_class'] = data_cleaned['sig'].apply(sig_class)

        # Reordering Columns
        data_cleaned = data_cleaned[['id', 'longitude', 'latitude', 'elevation',
                                     'title', 'place', 'sig', 'mag', 'magType', 'time', 'sig_class']]

        # Extract state/province
        data_cleaned['state_province'] = data_cleaned['place'].str.split(',').str[-1].str.strip()

        return data_cleaned.to_dict(orient='records')  
    
    @task() 
    def load_data(transformed_data):
        postgres_conn = "my_postgres_id"
        pg_hook = PostgresHook(postgres_conn_id=postgres_conn)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create Earthquake Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS earthquake (
            id VARCHAR(50) PRIMARY KEY,
            longitude FLOAT,
            latitude FLOAT,
            elevation FLOAT,
            title VARCHAR(255),
            place VARCHAR(255),
            sig INT,
            mag FLOAT,
            magType VARCHAR(10),
            time TIMESTAMP,
            sig_class VARCHAR(10),
            state_province VARCHAR(255)
        );
        """)

        # Inserting transformed data into table
        insert_query = """
        INSERT INTO earthquake (id, longitude, latitude, elevation, title, place, sig, mag, magType, time, sig_class, state_province)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """

        for row in transformed_data:
            cursor.execute(insert_query, (
                row['id'], row['longitude'], row['latitude'], row['elevation'], 
                row['title'], row['place'], row['sig'], row['mag'], row['magType'], 
                str(row['time']), row['sig_class'], row['state_province']
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print("Data loaded successfully into PostgreSQL")

    # DAG execution order
    raw_data = extract()
    transformed_data = transform(raw_data)
    load_data(transformed_data)

# Instantiate the DAG
earthquake_etl()


