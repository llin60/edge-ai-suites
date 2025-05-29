# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import json
from datetime import datetime

def generate_fake_meta(file_dir):
    if not os.path.isdir(file_dir):
        raise ValueError(f"The provided path '{file_dir}' is not a valid directory.")
    
    fake_labels = []
    timestamp = int(datetime.now().timestamp())

    cnt = 0

    meta_dir = os.path.join(file_dir, "meta")
    os.makedirs(meta_dir, exist_ok=True)

    for file_name in sorted(os.listdir(file_dir)):
        file_path = os.path.join(file_dir, file_name)

        # Skip directories, only process files
        if os.path.isfile(file_path):
            # Generate the JSON file name
            base_name, _ = os.path.splitext(file_name)
            json_file_path = os.path.join(meta_dir, f"{base_name}.json")
            fake_label = f"camera_{cnt}"
            fake_timestamp = timestamp - cnt * 100
            fake_meta = {
                "camera": fake_label,  
                "timestamp": fake_timestamp  
            }

            print(fake_meta)
            cnt += 1

            # Write the JSON content to the file
            with open(json_file_path, "w") as json_file:
                json.dump(fake_meta, json_file, indent=4)

            print(f"Generated metadata file: {json_file_path}")

def remove_fake_meta_files(file_dir):
    meta_dir = os.path.join(file_dir, "meta")
    if os.path.exists(meta_dir):
        for file_name in os.listdir(meta_dir):
            file_path = os.path.join(meta_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed metadata file: {file_path}")
        os.rmdir(meta_dir)
        print(f"Removed directory: {meta_dir}")