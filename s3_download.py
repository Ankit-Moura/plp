import os
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup

bucket_name = 'plp-data-bucket'
local_dir = './fast_downloaded_files'
os.makedirs(local_dir, exist_ok=True)

# Initialize S3 client
session = boto3.Session(profile_name="Development-241533129527")
s3 = session.client("s3")

# Helper function to download a single file
def download_file(obj):
    s3_key = obj['Key']
    
    # Skip folders
    if s3_key.endswith('/'):
        print(f"Skipping folder: {s3_key}")
        return

    local_file_path = os.path.join(local_dir, s3_key)
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    print(f"Downloading {s3_key}...")
    s3.download_file(bucket_name, s3_key, local_file_path)

# Gather all object keys using pagination
def list_all_objects():
    continuation_token = None
    all_objects = []

    while True:
        kwargs = {'Bucket': bucket_name}
        if continuation_token:
            kwargs['ContinuationToken'] = continuation_token

        response = s3.list_objects_v2(**kwargs)
        all_objects.extend(response.get('Contents', []))

        if response.get('IsTruncated'):
            continuation_token = response.get('NextContinuationToken')
        else:
            break

    return all_objects

# Main: Download files concurrently
all_objects = list_all_objects()
print(f"Found {len(all_objects)} objects. Starting download...")

max_workers = 16  # You can tweak this depending on your network/CPU
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(download_file, obj) for obj in all_objects]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error: {e}")

print("Download complete!")
