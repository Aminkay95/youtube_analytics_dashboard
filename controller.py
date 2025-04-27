from main import getSubscribers, get_videos, best_post_time
from dotenv import load_dotenv
import os

jdbc_url = "jdbc:postgresql://localhost:5432/youtube_analytics"
load_dotenv()
properties = os.getenv('properties')

def loadData():
    # load data frame 
    subscriber_df = getSubscribers()
    videos_list, best_videos_df = get_videos()
    best_post_time_df = best_post_time(videos_list)

    # push the data frames in postgresql db
    # Write to PostgreSQL
    subscriber_df.write \
    .jdbc(url=jdbc_url, table="subscriber_data", mode='append', properties=properties)

    best_post_time_df.write \
    .jdbc(url=jdbc_url, table="best_post_time", mode='append', properties=properties)

    best_videos_df.write \
    .jdbc(url=jdbc_url, table="best_performing_videos", mode='append', properties=properties)


loadData()



