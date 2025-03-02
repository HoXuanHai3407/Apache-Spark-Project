from pyspark.sql import SparkSession
import pickle
import os
from utils.video_utils import merge_videos

spark = SparkSession.builder \
    .appName('ParallelObjectTracking') \
    .master('spark://10.254.216.44:7077') \
    .getOrCreate()

with open('batches.pkl', 'rb') as f:
    batches = pickle.load(f)

frames_rdd = spark.sparkContext.parallelize(enumerate(batches))

def process_batch(batch):
    batch_id, frames = batch
    os.system(f'python3 worker/process_batch.py {batch_id}')
    return f'video/output/output_chunk_{batch_id}.mp4'

video_chunks = frames_rdd.map(process_batch).collect()

merge_videos(video_chunks, 'video/final_output.mp4')
spark.stop()
