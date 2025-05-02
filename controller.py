from main import getSubscribers, get_videos, best_post_time
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()

jdbc_url = "jdbc:postgresql://localhost:5432/amin_youtube"
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# JDBC connection properties for Spark
properties = {
    "user": db_user,
    "password": db_password,
    "driver": "org.postgresql.Driver"
}

# Function to clear a table using psycopg2
def clear_table(table_name):
    conn = psycopg2.connect(
        dbname="amin_youtube",
        user=db_user,
        password=db_password,
        host="localhost",
        port=5432
    )
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name}")
    conn.commit()
    cur.close()
    conn.close()

def loadData():
    # Load DataFrames
    subscriber_df = getSubscribers()
    videos_list, best_videos_df = get_videos()
    best_post_time_df = best_post_time(videos_list)

    
    subscriber_df.write \
        .jdbc(url=jdbc_url, table="subscriber_data", mode='append', properties=properties)

    
    clear_table("best_post_time")
    best_post_time_df.write \
        .jdbc(url=jdbc_url, table="best_post_time", mode='append', properties=properties)

    
    clear_table("best_performing_videos")
    best_videos_df.write \
        .jdbc(url=jdbc_url, table="best_performing_videos", mode='append', properties=properties)


loadData()
