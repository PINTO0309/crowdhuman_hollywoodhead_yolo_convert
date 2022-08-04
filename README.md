# crowdhuman_hollywoodhead_coco_convert
Generates a head-only dataset in COCO format. The labels included in the CrowdHuman dataset are Head and FullBody, but ignore FullBody.

## Advance preparation
```bash
$ pip install -U \
pip \
gdown \
tree \
numpy==1.23.1 \
scikit-learn==1.1.1 \
opencv-python==4.6.0 \
threadpoolctl==3.1.0 \
--user
$ git clone https://github.com/PINTO0309/crowdhuman_hollywoodhead_coco_convert.git
$ cd crowdhuman_hollywoodhead_coco_convert
```
## CrowdHuman to YOLO(COCO/YOLOv7) format
### Download CrowdHuman Datasets
```bash
$ cd 01_crowhuman2yolo
$ ./crowdhuman_dataset_download.sh
```
### Structure
```bash
$ tree
.
├── crowdhuman_dataset_download.sh
└── data
    ├── crowdhuman.names
    ├── crowdhuman-template.data
    ├── gen_txts.py
    ├── prepare_data.sh
    ├── raw
    │   ├── annotation_train.odgt
    │   ├── annotation_val.odgt
    │   ├── CrowdHuman_train01.zip
    │   ├── CrowdHuman_train02.zip
    │   ├── CrowdHuman_train03.zip
    │   └── CrowdHuman_val.zip
    └── verify_txts.py

2 directories, 12 files
```
### Prepare Data e.g. 4:3
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x480
```
### Prepare Data e.g. 16:9
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x384
```
