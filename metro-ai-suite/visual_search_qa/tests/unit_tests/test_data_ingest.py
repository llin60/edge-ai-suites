# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import re
from streamlit.testing.v1 import AppTest

from ut_utils import copy_dataset

APP_TIMEOUT = 30

HOST_DATA_PATH = "/home/user/data/DAVIS/subset"
HOST_DATA_PATH_COPY = "/home/user/data/DAVIS/subset_copy"

at = AppTest.from_file("/home/user/visual_search_qa/src/app.py", default_timeout=APP_TIMEOUT)
at.run()

def test_data_ingestion():
    at.text_input(key="kfilePath").input(HOST_DATA_PATH)
    at.button(key="kupdate_db").click().run()
    # for the demo dataset case, total files should be 25
    insert_count = 0
    match = re.search(r"'insert_count': (\d+)", at.session_state.latest_log)
    if match:
        insert_count = int(match.group(1))
        assert insert_count > 0

        # re-ingest without clear should not change the insert count
        at.text_input(key="kfilePath").input(HOST_DATA_PATH)
        at.button(key="kupdate_db").click().run()
        match = re.search(r"'insert_count': (\d+)", at.session_state.latest_log)
        assert not match
    else:
        # clear db and re-ingest
        at.button(key="kclear_db").click().run()
        match = re.search(r"'delete_count': (\d+)", at.session_state.latest_log)
        delete_count = int(match.group(1))
        assert delete_count > 0

        at.button(key="kupdate_db").click().run()
        match = re.search(r"'insert_count': (\d+)", at.session_state.latest_log)
        if match:
            insert_count = int(match.group(1))
            assert insert_count > 0
        else:
            raise AssertionError("Data ingestion failed, no insert count found in logs.")
        
    # incremental ingestion with a copy of the dataset
    copy_dataset(HOST_DATA_PATH, HOST_DATA_PATH_COPY)
    at.text_input(key="kfilePath").input(HOST_DATA_PATH_COPY)
    at.button(key="kupdate_db").click().run()
    match = re.search(r"'insert_count': (\d+)", at.session_state.latest_log)
    if match:
        insert_count_copy = int(match.group(1))
        assert insert_count == insert_count_copy
    else:
        raise AssertionError("Data ingestion failed, no insert count found in logs.")
    
    at.button(key="kclear_db").click().run()
    match = re.search(r"'delete_count': (\d+)", at.session_state.latest_log)
    delete_count = int(match.group(1))
    assert delete_count == (insert_count+insert_count_copy)

    # put the original dataset back for other tests
    at.text_input(key="kfilePath").input(HOST_DATA_PATH)
    at.button(key="kupdate_db").click().run()