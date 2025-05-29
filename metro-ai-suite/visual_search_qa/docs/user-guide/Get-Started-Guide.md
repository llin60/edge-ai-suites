# Get Started Guide

Get Started Guide for running on NEP RA base platform and step-by-step instructions for users.

## Prerequisites
- Operating System: Ubuntu* 24.04.1 LTS (fresh installation) on target system
- Platform
  - Intel® Core™ Processors (13th gen) + Intel® Arc™ A770 Graphics

## Get started

### Download and install
1. Select options to download the Intel® Metro AI Suite Image Search by Text package. 
    ![Configure and Download](./_images/esc_download_page.png)
    <center>Figure 1: Download Page </center>

2. Click **Download**. In the next screen, accept the license agreement and copy the Product Key.

3. Transfer the downloaded package to the target Ubuntu* system and unzip:

    ```bash
    unzip MetroAISuite-LVM-Search.zip
    ```

4. Go to the `MetroAISuite-LVM-Search/` directory:
   
    ```bash
    cd MetroAISuite-LVM-Search
    ```

5. Prepare a Python virtual environment
    ```bash
    sudo apt-get install python3.12-venv
    python3 -m venv venv
    source venv/bin/activate
    ```

    (Optional) If needed, configure your network proxy

    ```
    export http_proxy=<Your-Proxy>
    export https_proxy=<Your-Proxy>
    ```

6. Change the permission of the executable `edgesoftware` file:
    ```bash
    chmod 755 edgesoftware
    ```

7. Install the package:
   
    ```bash
    ./edgesoftware install
    ```

8. When prompted, enter the Product Key. You can enter the Product Key mentioned in the email from Intel confirming your download (or the Product Key you copied in Step 2).

9. When prompted for the Remote Device Management feature, type no
    ![Prompt to Enable RDM](./_images/remote-device-management-setting.png)
    <center>Figure 2: Enable RDM</center>

10. When prompted for the BECOME password, enter your Linux* account password.
    ![Prompt for BECOME Password](./_images/installation-linux-credentials.png)  
    <center>Figure 3: Enter BECOME password</center>

11. When prompted to reboot the machine, press Enter. Ensure to save your work before rebooting.

12. After rebooting, resume the installation:
    ```bash
    cd MetroAISuite-LVM-Search
    ./edgesoftware install
    ```

13. When the installation is complete, you will see the message `Installation of package complete` and the installation status for each module.
    ![Installation success](./_images/esc_success.png)  
    <center>Figure 4: Installation Complete Message</center>

14. After the installation is done, you can find the directory structure like below where `LVM_Demo_Searchimagebytext_Source_Code` contains the source code.
    ``` bash
    Metro_AI_Suite_Image_Search_by_Text_1.0/
    ├── <some-hash>.zip
    ├── <some-hash>.zip
    ├── <some-hash>.zip
    ├── bmra_base
    ├── esb_common
    └── LVM_Demo_Searchimagebytext_Source_Code
    ```

15. When you check the docker image with `docker images`, there should be an image named `metro-1.0/search_image_by_text_app `.

16. Now that you have both the docker image and source code, let's move on to get started with docker image and source code.


## Get started with docker image and source code
1. Make sure you are at the source code directory `Metro_AI_Suite_Image_Search_by_Text_1.0/LVM_Demo_Searchimagebytext_Source_Code/`

2. Ensure you have the docker image named `search_image_by_text_app`. For image installed by the ESC package, there will a prefix `metro-1.0/`, remove it by renaming the image so that the scripts used in later steps could work

    ``` bash
    docker tag metro-1.0/search_image_by_text_app:latest search_image_by_text_app:latest
    ```

3. If you do not have the image but do have the source code, you can build it with source code by the following steps. 

    ``` bash
    ## at the source code directory
    cd docker
    bash build_docker.sh
    ```
    In this case, there would be no name prefix for the docker image built.

> Note that from the command above and so on, the `source code directory` would be referred to `LVM_Demo_Searchimagebytext_Source_Code/`

### Prepare directories on the host

Since we will be using a container to run the application, it is better to explicitly define volumes for the container to write data. Prepare the following directories under the source code directory on host before running the container.

``` bash
mkdir example
mkdir dataset
mkdir models
mkdir data
```

### Download demo dataset on host machine
If you would like to try this application out with a sample dataset, please read this section. If you prefer to running it with your own data, please skip and follow the next section.

1. Since the demo dataset is a large zip file, it is recommended to download it to the host machine instead of downloading it in the docker container. So first on your host machine, go to `example` folder and download the dataset `DAVIS-2017-trainval-480p.zip` from [DAVIS official website](https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip)

    ``` bash
    ## at the source code directory
    cd example
    wget https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip

    ## after the download is finished, unzip it in the same directory, generate example/DAVIS/
    unzip DAVIS-2017-trainval-480p.zip
    ```

2. You can download and unzip it in the docker container as well. 


### Prepare your own dataset on host machine
If you would like to run with your own dataset, please put your data (images and videos) under `dataset` in this structure:
``` bash
cp your_images dataset/your_dataset_name/image/
cp your_videos dataset/your_dataset_name/video/

## dataset should look like this after it's done
tree dataset
dataset
└── your_dataset_name
    ├── image
    │   ├── xxxx.jpg
    │   ├── xxxx.jpg
    │   ├── xxxx.jpg
    │   ├── ...
    └── video
        ├── xxxx.mp4
        ├── xxxx.mp4
        ├── xxxx.mp4
        └── ...
```


### Run a docker container
1. Start a docker container with this script at the source code directory
    ``` bash
    bash run_docker_container.sh
    ```
2. The container ID will be printed out by this script. In the following sections, the container ID created will be referred to as `<Container ID>`

3. You can also check the container ID with:
    ```bash
    $ docker ps -a
    CONTAINER ID   IMAGE
    <CONTAINER_ID>  search_image_by_text_app
    ```

4. After you have the container ID, enter the container with
    ``` bash
    docker exec -it <Container ID> bash
    ```

### Data preparation (inside container)
1. For the demo DAVIS dataset, we provide a script `prepare_demo_dataset.py` to process it. Simply run
    ``` bash
    cd script
    python prepare_demo_dataset.py
    ```
    > Please note that running `python script/prepare_demo_dataset.py` is NOT equivalent due to some directory relationship issue. It is a must to change directory first.

2. After running script, `dataset` should look like:
    ``` bash
    dataset
    └── DAVIS
        ├── image
        │   ├── bike-packing_00000.jpg
        │   ├── bike-packing_00020.jpg
        │   ├── ...
        └── video
            ├── bear.mp4
            ├── blackswan.mp4
            └── ...
    ```

### Model preparation (inside container)
> For PRC users, first setup mirror of huggingface.co.
>
> ```bash
> export HF_ENDPOINT=https://hf-mirror.com
> ```

1. Go back to `/home/lvm-search/app` if you are still in the `/home/lvm-search/app/script/` directory

2. Convert BLIP2 model.
    ```bash
    python convert_blip2.py
    ```

3. Download weights of CLIP model.
    ```bash
    huggingface-cli download laion/CLIP-ViT-H-14-laion2B-s32B-b79K open_clip_pytorch_model.bin --local-dir ./

    # make sure the weights file is correct.
    md5sum open_clip_pytorch_model.bin 
    2aa6c46521b165a0daeb8cdc6668c7d3  open_clip_pytorch_model.bin
    ```

3. Convert CLIP model
    ```bash
    python convert_clip.py
    ```

4. Convert translator model

    ``` bash
    optimum-cli export openvino --model "Helsinki-NLP/opus-mt-zh-en" ./models/ov_opus_zh_en
    ```

5. Now `./models` looks like:
    ```bash
    models
    ├── blip2
    │   ├── bert_tokenizer.bin
    │   ├── bert_tokenizer.xml
    │   ├── img_features_extractor.bin
    │   ├── img_features_extractor.xml
    │   ├── text_features_extractor.bin
    │   └── text_features_extractor.xml
    ├── clip
    │   ├── vit_h_14_text.bin
    │   ├── vit_h_14_text.xml
    │   ├── vit_h_14_visual.bin
    │   └── vit_h_14_visual.xml
    └── ov_opus_zh_en
        ├── config.json
        ├── generation_config.json
        ├── openvino_decoder_model.bin
        ├── openvino_decoder_model.xml
        ├── openvino_decoder_with_past_model.bin
        ├── openvino_decoder_with_past_model.xml
        ├── openvino_encoder_model.bin
        ├── openvino_encoder_model.xml
        ├── source.spm
        ├── special_tokens_map.json
        ├── target.spm
        ├── tokenizer_config.json
        └── vocab.json

    3 directories, 23 files
    ```

### Create embeddings and build index (inside container)
1. Now the dataset and models are ready, we can create embeddings and build index for searching. The searching is based on the similarity between image features and text features. For videos, we extract frames by certain interval first, then we use the extracted frames for searching and reflect the search result back to the original video.

2. Check `config.yml` for parameters, `video_frame_interval` indicates the interval of taking one frame every x frames for videos. 
For example, `video_frame_interval: 15` means taking 1 frame at every 15 frames for all the videos in the dataset. The extracted frames would be used for searching and as video play back timestamp. The smaller the interval is, the less possible to miss searching target, and the longer time it takes to build index.
    ``` yaml
    models:
      CLIP/H14:
        image_encoder: "models/clip/vit_h_14_visual.xml"
        text_encoder: "models/clip/vit_h_14_text.xml"
      BLIP2/G14:
        image_encoder: "models/blip2/img_features_extractor.xml"
        text_encoder: "models/blip2/text_features_extractor.xml"
        tokenizer: "models/blip2/bert_tokenizer.xml"
    translator: "models/ov_opus_zh_en"
    datasets:
      DAVIS:
        path: "./dataset/DAVIS"
        video_frame_interval: "15"
    index_dir: "./data"
    device: "GPU.1"
    result_per_row: "5"
    max_queries: "20"
    excessive_search_multiplier: "2"
    overlap_filter_thresh_sec: "5"
    verbose: "False"
    ```

3. Run this script to build index:
    ``` bash
    python build_index.py
    ```

4. Notice that in `config.yml` we use `./data` as the `index_dir`. After building is done, the index directory should look like:
    ``` bash
    data
    ├── all_file_list.pkl
    ├── blip2_g14_all.pkl
    └── clip_h14_all.pkl
    ```

5. Also as mentioned earlier the videos in dataset will be extracted into frames, so there will be a new directory for each dataset which stores the extracted frames. `dataset` now looks like:
    ``` bash
    dataset
    └── DAVIS
        ├── image
        │   ├── bike-packing_00000.jpg
        │   ├── bike-packing_00020.jpg
        │   ├── ...
        ├── snapshot
        │   ├── bear_0.jpg
        │   ├── bear_15.jpg
        │   ├── ...
        └── video
            ├── bear.mp4
            ├── blackswan.mp4
            └── ...
    ```

### Run the app (inside container)
1. Run following command:
    ``` bash
    streamlit run app.py --server.port 17580
    ```
2. You will get some URLs to access the web application.

### Parameters in `config.yml`
- `models`: name and path to the models
- `translator`: path to the translation model
- `datasets`: name and path to the datasets. Each dataset needs to be specified with `video_frame_interval` indicating the interval for video frame extraction
- `index_dir`: where the index data is stored after `build_index.py`. Note that the default location `data` applies as the mount volume described in the previous section of this guide. If a different location is needed, modifications should be done accordingly
- `device`: which device to run the application on
- `result_per_row`: how many search results would be shown per row for queries. For example, for a query that returns 10 results, setting this parameter to 5 will lead to a display of results of 2 rows and 5 results per row
- `max_queries`: max number of query results
- `excessive_search_multiplier`: a multiplier for excessive search. If this parameter is larger than 1, the actual number of search results will be an integer of `excessive_search_multiplier * output_number`. The excessive number of results can be used for an overlapping filtering process and finally the number of `output_number` results will be shown.
- `overlap_filter_thresh_sec`: a threshold value in seconds for the overlapping filter. The filter applies to searched video results, where any two video frames in the results that are from the same video file and within the threshold interval will be filtered, and the one result with a higher search score would be kept. This filter helps when there are too many video frame results from the same video. Setting this parameter to `0` equals to turning off the overlapping filter.
- `verbose`: setting for log level, `True` indicates `Debug` level of logs, and `False` is for `Info` level.

## Get started on bare metal environment with source code
If you have the source code and would like to run this application on a bare metal environment instead of a docker environment, you can start by installing a local python environment.

### Setup python virtual environment (bare metal)

1. Check the Python version on your machine 
    ``` bash
    python --version
    ```

    If it is 3.12, it could be problematic. Install a version of 3.11 by the following command

    ``` bash
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.11 python3.11-venv
    ```

2. Generate a virtual environment and active it. Ignore the error if any.
    ``` bash
    python3.11 -m venv .env
    source .env/bin/activate
    ```

    If step 1 is skipped and Python 3.11 is not installed manually, try the following command instead
    ``` bash
    python3 -m venv .env
    source .env/bin/activate
    ```

3. Update `pip` to latest version. Then install `pytorch` of CPU version to save time.
    ```bash
    pip install -U pip
    pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cpu
    ```

4. Then install other requirements.
    ```bash
    pip install -r requirements.txt
    ```

5. Install `pytest` package manually if the unit tests are expected to run.
    ```bash
    pip install pytest
    ```

6. The `salesforce-lavis` package requires an older version of `transformers`, which will cause failure when converting BLIP2 model. So manually update `transformers` and ignore the error.
    ```bash
    pip install -U transformers==4.40.2
    ```

7. Check whether the GPU device is detectable to OpenVINO by running this command
    ```bash
    python -c "from openvino import Core; print(Core().available_devices)"
    ```

    A device list containing `GPU` should be printed out.

    If the GPU device is not seen, here are two possible solutions:

    - Manually install the base platform dependency

      Recall the directory structure of the installed ESC package
        ``` bash
        Metro_AI_Suite_Image_Search_by_Text_1.0/
        ├── <some-hash>.zip
        ├── <some-hash>.zip
        ├── <some-hash>.zip
        ├── bmra_base
        ├── esb_common
        └── LVM_Demo_Searchimagebytext_Source_Code
        ```

        Go to the `bmra_base` directory, manually run the set up script:
        ``` bash
        cd bmra_base
        bash setup.sh
        ```
    - Alternatively, you may try to install Intel GPU drivers referring to the [offical guide](https://dgpu-docs.intel.com/driver/client/overview.html)
        

### Prepare dataset, prepare models, build index and run the app (bare metal)
Once you have the python environment activated locally, the steps of preparation, building index and running the app are mostly the same with those inside the container. Just run those commands on bare metal instead of inside container.


## Customized development

### Add models

1. Currently, the application supports only pre-trained CLIP and BLIP2 models. To add another model, please refer to `convert_clip.py` and `convert_blip2.py` and convert your model into OpenVINO models, then add the model info into `models` section in `config.yml`.
    ``` yaml
    models:
      model_name:
        image_encoder: "/path/to/img_features_extractor.xml"
        text_encoder: "/path/to/text_features_extractor.xml"
    ```

2. Then go to `build_index.py` and `app.py` and check if anything needs to be modified according to the model structure.

### Add datasets

1. In `config.yml`, modify `datasets` section to add datasets. You should specify the path to the dataset and the video frame interval respectively.

2. The `dataset name` will be used in both `build_index.py` and `app.py`.

3. Remember to place the images and videos in the dataset into separate directories (refer to section `Prepare your own dataset on host machine (optional)` for details)
    ``` yaml
    datasets:
      <dataset name>:
        path: <dataset path>
        video_frame_interval: <frame interval>
    ```

## Release Notes
Current Version: 1.0
- Initialized the image search by text reference implementation
- Added CLIP model
- Added BLIP2 model
- Added Faiss for vector searching


## Known Issues
- The default value of parameter `result_per_row` in the configuration file `config.yml` is 5. However, if it is set to a small number such as 1 or 2, the result images on the UI can be displayed with stretched and abnormal aspect ratio. Users should avoid setting the parameter to small values if deformed display results are not acceptable.
