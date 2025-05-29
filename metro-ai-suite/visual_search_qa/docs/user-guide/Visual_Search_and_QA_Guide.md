# Get Started Guide

Get Started Guide for running visual search and QA application

**Updated based on dev branch `dev/searchQA`, Feb 2025 version** 

## Prerequisites
- Operating System: Ubuntu* 24.04.1 LTS (fresh installation) on target system
- Platform
  - Intel® Core™ Processors (13th gen) + Intel® Arc™ A770 Graphics

## Prepare docker images
Docker images list:
* `search_image_by_text_app`
* `ipex-llm-arc-server`
* `lvm-ipex-llm`    
* `visualqna-chat` 
* `visualqna-ui`
* `nginx`     

Note: Only `search_image_by_text_app`, `ipex-llm-arc-server`, `nginx` are necessary for visual search and QA application. The other ones are only needed for VQA standalone service (standalone VQA UI).

If you don't have the necessary docker images, you may build them manually by following [guide for search_image_by_text_app](./Get-Started-Guide.md) and [guide for the others](https://github.com/intel-innersource/applications.iot.video-edge-device.lvm-visualqna/blob/dev/visualserachQA/docker_compose/intel/xpu/searchQA-ipex-llm/README.md)

Here is a standard example for preparing the docker images manually:

``` bash
## clone the repo
git clone https://github.com/intel-innersource/applications.iot.video-edge-cloud.vlm-vss.git vlm
cd vlm

## checkout to the dev branch
git checkout --track origin/dev/searchQA 

## get the vqa submodule
git submodule init
git submodule update
git pull --recurse-submodules
git submodule update --init --recursive

## build image for search
cd docker
bash build_docker.sh
cd ..

## build image for vqa
cd vqa
cd docker_image_build/
git clone -b v1.0 https://github.com/opea-project/GenAIComps.git
docker compose -f build.yaml build --no-cache > ./docker_image_build.log

## go back to vlm source directory
cd ../..
```

If things go wrong, please refer to the original guides mentioned previously for more detailed steps

If successfully built, you should have these images

1. `opea/visualqna-ui:latest`
2. `opea/visualqna-chat:latest`
3. `opea/lvm-ipex-llm:latest`
4. `opea/ipex-llm-arc-server:latest`
5. `opea/nginx:latest`
6. `search_image_by_text_app:latest`

## Prepare models, local files, and build index for search service
Since the search service is currently packed in one single image, you need to do some offline preparation first. Please refer to [guide for search_image_by_text_app](./Get-Started-Guide.md) for details.

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

And remember to add your dataset to config.yml, in the dataset section
``` bash
datasets:
  your_dataset_name:
    path: "./dataset/your_dataset_name"
    video_frame_interval: "15"
```
`video_frame_interval` indicates the frame interval for extracting video frames. For example, 15 here means extracting 1 frame for every 15 frames.

## Deploy service
We use docker compose file to deploy the service, steps are listed below
```bash
## go to where the docker compose file is
cd docker_compose/intel/xpu/searchQA-ipex-llm/

# set Image Register and Tag
export REGISTRY="opea"
export TAG="latest"

# set other environment variables
source set_env.sh
```

Be careful for the `SEARCH_DB_PATH` variable (which would be printed in terminal for you to check). Make sure that this path is correctly pointing to where your local search database (models, files and index) is located. That is, your models, files, index should be at `$SEARCH_DB_PATH/models`, `$SEARCH_DB_PATH/dataset`, `$SEARCH_DB_PATH/data` respectively.

Once you have the environment ready, start the service
```bash
# If not existing, Create folder with regular user permission
mkdir -p $HOME/.cache/huggingface
docker compose -f compose.yaml up -d
```

> **Note**:  Please wait for a while since it takes some time to load models, especially for the first time deploying a new model. Resources will be downloaded from huggingface endpoint. 
> 
> Use `docker logs -f ipex-llm-arc-server` to check if everything is ready:
> ```bash
> 2024-10-23 07:53:47,639 - INFO - Time to load weights: 35.97s
> INFO:     Started server process [1]
> INFO:     Waiting for application startup.
> INFO:     Application startup complete.
> INFO:     Uvicorn running on http://0.0.0.0:8399 (Press CTRL+C to quit)
> 
> # everything is ready
> ```

For more operations such as changing models, changing ports, modifying config files, running api tests etc., please refer to the original guides.

## Play with web UI
To access the frontend, open the following URL in your browser: http://{host_ip}:5177. By default, the UI runs on port 5177 internally. If you would like to access to the standalone VQA service frontend, please use port number 5173: http://{host_ip}:5173
