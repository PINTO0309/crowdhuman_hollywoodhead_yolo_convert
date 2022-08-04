# crowdhuman_hollywoodhead_coco_convert
Generates a head-only dataset in COCO format. The labels included in the CrowdHuman dataset are Head and FullBody, but ignore FullBody.

## 1. Advance preparation
```bash
$ git clone https://github.com/PINTO0309/crowdhuman_hollywoodhead_coco_convert.git
$ cd crowdhuman_hollywoodhead_coco_convert
$ docker build -t crowdhuman_hollywoodhead_coco_convert .

$ docker run -it --rm \
-v `pwd`:/home/vscode \
crowdhuman_hollywoodhead_coco_convert:latest
```
## 2. CrowdHuman Single to YOLO(COCO/YOLOv7) format
### 2-1. Download CrowdHuman Datasets
```bash
$ cd 01_crowdhuman2yolo
$ ./crowdhuman_dataset_download.sh
```
### 2-2. Structure
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
### 2-3. Prepare Data
#### 2-3-1. Prepare Data e.g. 4:3
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x480

** Unzip dataset files
Archive:  CrowdHuman_train01.zip
Archive:  CrowdHuman_train02.zip
Archive:  CrowdHuman_train03.zip
Archive:  CrowdHuman_val.zip
** Create the crowdhuman-640x480/ subdirectory
** Generate yolo txt files
** Processing Sets: test
** Processed Images: 4361
** Processing Sets: train
** Processed Images: 14962
** Processing .data
** Processed .data

** for yolov7-640x480,
resized bbox width/height clusters are:
(8.03, 9.75) (14.27, 18.82) (21.57, 29.40) (30.31, 42.13) (42.60, 57.28)
(58.03, 79.86) (79.73, 113.81) (115.23, 167.94) (159.88, 303.94)
anchors = 8,9,  14,18,  21,29,  30,42,  42,57,  58,79,  79,113,  115,167,  159,303
** Done.
```
#### 2-3-2. Prepare Data e.g. 16:9
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x384
```
### 2-4. Structure
```bash
$ ls -l

total 2040
drwxr-xr-x 2 vscode vscode 2048000 Aug  4 11:27 crowdhuman-640x480
-rw-r--r-- 1 vscode vscode     149 Aug  4 11:27 crowdhuman-640x480.data
-rw-rw-r-- 1 vscode vscode     167 Aug  4 08:24 crowdhuman-template.data
-rw-rw-r-- 1 vscode vscode      12 Aug  4 11:20 crowdhuman-template.names
-rw-rw-r-- 1 vscode vscode       5 Aug  4 11:20 crowdhuman.names
-rw-rw-r-- 1 vscode vscode    5937 Aug  4 10:17 gen_txts.py
-rwxrwxr-x 1 vscode vscode     909 Aug  4 10:03 prepare_data.sh
drwxrwxr-x 3 vscode vscode    4096 Aug  4 09:34 raw
-rw-rw-r-- 1 vscode vscode    1426 Aug  4 08:24 verify_txts.py
```
