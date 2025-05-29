# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import time
from streamlit.testing.v1 import AppTest

APP_TIMEOUT = 30

HOST_DATA_PATH = "/home/user/data/DAVIS/subset"

at = AppTest.from_file("/home/user/visual_search_qa/src/app.py", default_timeout=APP_TIMEOUT)
at.run()

def test_search_result_qa():
    at.text_input(key="kfilePath").input(HOST_DATA_PATH)
    at.button(key="kupdate_db").click().run()
    at.text_input(key="ktext").input("rollercoaster")
    at.button(key="kSearch").click().run()
    # select the first video result
    at.checkbox(key="0v").check().run()
    prompt = "describe this video in 50 words"
    at.chat_input[0].set_value(prompt).run()
    assert at.chat_message[0].markdown[0].value == prompt
    assert at.chat_message[0].avatar == "user"
    # time.sleep(5)  # Allow some time for the model to respond
    assert "rollercoaster" in at.session_state.latest_log or "roller coaster" in at.session_state.latest_log
    
    # select the first image result
    at.checkbox(key="0i").check().run()
    prompt = "describe this image in 50 words"
    at.chat_input[0].set_value(prompt).run()
    # time.sleep(5)  # Allow some time for the model to respond
    assert "horse" in at.session_state.latest_log