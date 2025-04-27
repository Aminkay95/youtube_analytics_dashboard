
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, date_format, to_timestamp, concat_ws, when, lit
from datetime import date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Load environment variables
load_dotenv()

# Get API key from the environment file
google_api_key = os.getenv('API_KEY')

def get_spark():
    return SparkSession.builder\
        .appName("YoutubeAnalytics")\
        .config("spark.jars", "/mnt/c/Users/moham/Documents/LuxDE_projects/YouTube-Analytics-Dashboard-main (1)/YouTube-Analytics-Dashboard-main/jars/postgresql-42.6.0.jar") \
        .master("local[*]")\
        .getOrCreate()

def get_youtube():
    return build(
        'youtube',
        'v3',
        developerKey=google_api_key
    )


# Question 1: How has my channel grown over time?
def getSubscribers():
    spark = get_spark()  # Call get_spark() to get the Spark session
    youtube = get_youtube()  # Call get_youtube() to get the YouTube API client
    
    # Get data from YouTube channel
    request = youtube.channels().list(
        part='statistics',
        id='UCtxD0x6AuNNqdXO9Wp5GHew'
    )
    
    response = request.execute()
    subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
    date_at = date.today()
    subscriber_data = [(date_at, subscriber_count)]
    
    # Create a DataFrame
    df = spark.createDataFrame(subscriber_data, ["date", "subscribers"])

    return df


# Question 2: Which videos perform best by engagement (likes/comments/views)?
def get_videos(playlist_id="UUS-zdr8_cuUGNvOhLKUkjZQ"):
    youtube = get_youtube()
    spark = get_spark()

    next_page = None
    videos = []

    while True:
        # Get video IDs from the playlist
        request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
        )
        response = request.execute()

        video_ids = [item['contentDetails']['videoId'] for item in response['items']]

        # Get detailed video stats
        data_request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        )
        res = data_request.execute()

        for item in res['items']:
            try:
                title = item['snippet']['title']
                view_count = int(item['statistics'].get('viewCount', 0))
                like_count = int(item['statistics'].get('likeCount', 0))
                comment_count = int(item['statistics'].get('commentCount', 0))
                published_date = item['snippet']['publishedAt']

                engagement_rate = round((like_count + comment_count) / view_count, 2) if view_count > 0 else 0.0

                videos.append({
                    "title": title,
                    "published_date": published_date,
                    "view_count": view_count,
                    "likes": like_count,
                    "comments": comment_count,
                    "engagement_rate": engagement_rate
                })

            except Exception as e:
                print(f"Skipping a video due to error: {e}")
                continue

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    # Define schema
    schema = StructType([
        StructField("title", StringType(), True),
        StructField("published_date", StringType(), True),  # Still string (ISO8601 date)
        StructField("view_count", IntegerType(), True),
        StructField("likes", IntegerType(), True),
        StructField("comments", IntegerType(), True),
        StructField("engagement_rate", DoubleType(), True)
    ])

    # Create DataFrame with strict order
    df = spark.createDataFrame(videos, schema=schema)

    # Get top 5 videos by engagement rate
    best_df = df.orderBy(col("engagement_rate").desc()).limit(5)

    return videos, best_df


# Question 3: Best time to post based on engagement
def best_post_time(videos):
    spark = get_spark()

    # Convert videos into DataFrame
    df = spark.createDataFrame(videos)

    # Convert the published_date to TimestampType
    df = df.withColumn("published_date", to_timestamp(col('published_date')))

    # Extract hour and day
    df = df.withColumn("hour", hour(col('published_date')))
    df = df.withColumn("day", date_format(col('published_date'), "E"))

    # Calculate engagement
    df = df.withColumn("engagement", col('likes') + col('view_count') + col('comments'))

    # Group by day and hour and calculate avg engagement
    grouped = (
        df.groupBy("day", "hour")
        .avg("engagement")
        .withColumnRenamed("avg(engagement)", "avg_engagement")
    )

    # Format hour properly to AM/PM using lit() to ensure AM/PM is treated as a string literal
    grouped = grouped.withColumn(
        "hour_formatted",
        when(col("hour") == 0, lit("12 AM"))
        .when(col("hour") < 12, concat_ws("", col("hour").cast("string"), lit(" AM")))
        .when(col("hour") == 12, lit("12 PM"))
        .otherwise(concat_ws("", (col("hour") - 12).cast("string"), lit(" PM")))
    )

    # Combine day and hour_formatted into a single string
    grouped = grouped.withColumn(
        "day_hour",
        concat_ws(" ", col("day"), col("hour_formatted"))
    )

    # Select only day_hour and avg_engagement
    result = grouped.select("day_hour", "avg_engagement").orderBy(col("avg_engagement").desc())

    return result.limit(3)
