# crowdhuman_hollywoodhead_coco_convert

```bash
pip install gdown tree --user
git clone https://github.com/PINTO0309/crowdhuman_hollywoodhead_coco_convert.git
cd crowdhuman_hollywoodhead_coco_convert
```
## CrowdHuman to YOLO(COCO) format
### Download CrowdHuman Datasets
```bash
cd 01_crowhuman2yolo
./crowdhuman_dataset_download.sh
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
### Prepare Data
```bash
cd data
# {width}x{height}
./prepare_data.sh 640x640
```
