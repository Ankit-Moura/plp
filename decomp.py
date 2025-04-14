import pandas as pd
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def deComp(input_path, output_path):
    try:
        print(f"Converting: {input_path}")
        df = pd.read_parquet(input_path)

        json_data = df.to_json(orient='records', lines=True)
        data = json.loads(f"[{json_data.strip().replace('\n', ',')}]")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f" Saved to {output_path}")
    except Exception as e:
        print(f" Error converting {input_path}: {e}")

def batch_convert_parquet_to_json(input_dir, output_dir, max_workers=8):
    os.makedirs(output_dir, exist_ok=True)

    parquet_files = [
        (os.path.join(input_dir, filename), os.path.join(output_dir, os.path.splitext(filename)[0] + ".json"))
        for filename in os.listdir(input_dir) if filename.endswith(".parquet")
    ]

    print(f"Found {len(parquet_files)} Parquet files. Starting conversion with {max_workers} threads...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(deComp, input_path, output_path) for input_path, output_path in parquet_files]
        for future in as_completed(futures):
            future.result()

    print("All Parquet files have been converted to JSON.")

if __name__ == "__main__":
    batch_convert_parquet_to_json("fast_downloaded_files/tmp_data", "fast_converted_files/tmp", max_workers=8)
    batch_convert_parquet_to_json("fast_downloaded_files/data", "fast_converted_files/data", max_workers=8)


