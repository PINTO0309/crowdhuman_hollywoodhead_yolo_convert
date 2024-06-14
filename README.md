# crowdhuman_hollywoodhead_yolo_convert
YOLOv7 training. Generates a head-only dataset in YOLO format. The labels included in the CrowdHuman dataset are Head and FullBody, but ignore FullBody.

## 1. Advance preparation
```bash
$ git clone https://github.com/PINTO0309/crowdhuman_hollywoodhead_yolo_convert.git
$ cd crowdhuman_hollywoodhead_yolo_convert
$ docker build -t crowdhuman_hollywoodhead_yolo_convert -f Dockerfile.prep .
```
## 2. CrowdHuman Single to YOLO(YOLOv7) format
### 2-1. Download CrowdHuman Datasets
```bash
$ docker run -it --rm \
-v `pwd`:/home/vscode \
crowdhuman_hollywoodhead_yolo_convert:latest

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
anchors = 8,9, 14,18, 21,29, 30,42, 42,57, 58,79, 79,113, 115,167, 159,303
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
### 2-5. Verify
```bash
$ python verify_txts.py 640x480
```
![image](https://user-images.githubusercontent.com/33194443/182999724-fcaef730-1b91-4afa-b721-c0e3ffc519af.png)
### 2-6. Exit Docker
```bash
$ exit
```

## 3. HollywoodHeads Single to YOLO(YOLOv7) format
### 3-1. Download HollywoodHeads Datasets
```bash
$ docker run -it --rm \
-v `pwd`:/home/vscode \
crowdhuman_hollywoodhead_yolo_convert:latest

$ cd 02_hollywoodheads2yolo
$ ./hollywoodheads_dataset_download.sh
```
### 3-2. Structure
```bash
$ tree
.
├── data
│   ├── gen_txts.py
│   ├── hollywoodheads.names
│   ├── hollywoodheads-template.data
│   ├── hollywoodheads-template.names
│   ├── prepare_data.sh
│   ├── raw
│   │   └── HollywoodHeads.zip
│   └── verify_txts.py
└── hollywoodheads_dataset_download.sh

2 directories, 8 files
```
### 3-3. Prepare Data
#### 3-3-1. Prepare Data e.g. 4:3
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x480

** Unzip dataset files
Archive:  HollywoodHeads.zip
** Processing Sets: test
** Processed Images: 6676
** Processing Sets: train
** Processed Images: 216693
** Processing .data
** Processed .data

** for yolov7-640x480,
resized bbox width/height clusters are:
(34.76, 51.48) (60.39, 90.79) (88.51, 129.47)
(108.60, 187.15) (154.80, 232.53) (159.70, 305.63)
(205.66, 388.56) (246.42, 284.98) (310.29, 409.41)
anchors = 34,51, 60,90, 88,129, 108,187, 154,232, 159,305, 205,388, 246,284, 310,409
** Done.
```
#### 3-3-2. Prepare Data e.g. 16:9
```bash
$ cd data
# {width}x{height}
$ ./prepare_data.sh 640x384
```
### 3-4. Structure
```bash
$ ls -l

total 17840
-rw-rw-r-- 1 vscode vscode     6838  8月  5 11:58 gen_txts.py
-rw-rw-r-- 1 vscode vscode     4057  8月  5 00:33 gen_txts_sample.py
drwxrwxr-x 2 vscode vscode 18219008  8月  5 12:03 hollywoodheads-640x480
-rw-rw-r-- 1 vscode vscode      161  8月  5 12:03 hollywoodheads-640x480.data
-rw-rw-r-- 1 vscode vscode        5  8月  4 20:20 hollywoodheads.names
-rw-rw-r-- 1 vscode vscode      179  8月  5 00:17 hollywoodheads-template.data
-rw-rw-r-- 1 vscode vscode        5  8月  5 00:16 hollywoodheads-template.names
-rwxrwxr-x 1 vscode vscode      880  8月  5 12:40 prepare_data.sh
drwxrwxr-x 3 vscode vscode     4096  8月  5 11:41 raw
-rw-rw-r-- 1 vscode vscode     1426  8月  5 12:50 verify_txts.py
```
### 3-5. Verify
```bash
$ python verify_txts.py 640x480
```
![image](https://user-images.githubusercontent.com/33194443/182999308-4be00185-9b00-4d89-81ee-11d58e571c9d.png)
### 3-6. Exit Docker
```bash
$ exit
```

## 4. (Optional) CrowdHuman and HollywoodHeads merge
### 4-1. image / txt marge
```bash
$ docker run -it --rm \
-v `pwd`:/home/vscode \
crowdhuman_hollywoodhead_yolo_convert:latest

# JPEG
$ find 02_hollywoodheads2yolo/data/hollywoodheads-640x480 \
-name "mov_*.jpeg" -print0 \
| xargs -0 -I {} cp {} 01_crowdhuman2yolo/data/crowdhuman-640x480

# TXT
$ find 02_hollywoodheads2yolo/data/hollywoodheads-640x480 \
-name "mov_*.txt" -print0 \
| xargs -0 -I {} cp {} 01_crowdhuman2yolo/data/crowdhuman-640x480
```
### 4-2. train.txt / test.txt marge
```bash
$ cat 02_hollywoodheads2yolo/data/hollywoodheads-640x480/train.txt >> \
01_crowdhuman2yolo/data/crowdhuman-640x480/train.txt

$ cat 02_hollywoodheads2yolo/data/hollywoodheads-640x480/test.txt >> \
01_crowdhuman2yolo/data/crowdhuman-640x480/test.txt

$ sed -i -e 's/hollywoodheads/crowdhuman/g' \
01_crowdhuman2yolo/data/crowdhuman-640x480/train.txt

$ sed -i -e 's/hollywoodheads/crowdhuman/g' \
01_crowdhuman2yolo/data/crowdhuman-640x480/test.txt
```
### 4-3. Calculation of anchor
```bash
$ python calc_anchor.py \
--image_txt_folder_path 01_crowdhuman2yolo/data/crowdhuman-640x480 \
--dim 640x480

** image files sorting...
** sorted_image_files count: 242808
** image files sort done
** txt files sorting...
** sorted_txt_files count: 242808
** txt files sort done
** anchor calculating...
100%|█████████████████████████████████████████| 242808/242808 [00:04<00:00, 51255.10it/s]
** anchor calculation done

** for yolov7-640x480,
resized bbox width/height clusters are:
(13.04, 17.13) (36.53, 51.66) (65.15, 96.20)
(94.95, 149.07) (132.95, 208.64) (157.31, 284.76)
(195.28, 379.18) (244.24, 282.09) (303.92, 407.06)

anchors = 13,17, 36,51, 65,96, 94,149, 132,208, 157,284, 195,379, 244,282, 303,407
```
### 4-4. Exit Docker
```bash
$ exit
```

## 5. Train on CrowdHuman Dataset
### 5-1. Preparation of the environment
```bash
$ cd ..
$ git clone https://github.com/WongKinYiu/yolov7.git
$ cd yolov7
$ git checkout b8956dd5a5bcbb81c92944545ca03390c22a695f

$ mv ../crowdhuman_hollywoodhead_yolo_convert/01_crowdhuman2yolo/data/crowdhuman-640x480 data/
$ cp ../crowdhuman_hollywoodhead_yolo_convert/.dockerignore .
$ cp ../crowdhuman_hollywoodhead_yolo_convert/Dockerfile.yolov7 .

$ cat << 'EOT' > data/crowdhuman.yaml
# path to train.txt or test.txt
train: ./data/crowdhuman-640x480/train.txt
val: ./data/crowdhuman-640x480/test.txt
# number of classes
nc: 1
# class names
names: ['head']
EOT

$ ls -l data/
coco.yaml
crowdhuman-640x480
crowdhuman.yaml
hyp.scratch.custom.yaml
hyp.scratch.p5.yaml
hyp.scratch.p6.yaml
hyp.scratch.tiny.yaml

# copy cfg
$ cp cfg/training/yolov7.yaml cfg/training/yolov7_crowdhuman_head.yaml
$ cp cfg/training/yolov7-tiny.yaml cfg/training/yolov7-tiny_crowdhuman_head.yaml

# change number of classes
$ sed -i -e 's/nc: 80/nc: 1/g' cfg/training/yolov7_crowdhuman_head.yaml
$ sed -i -e 's/nc: 80/nc: 1/g' cfg/training/yolov7-tiny_crowdhuman_head.yaml

# change anchors
$ sed -i -e \
's/\[12,16, 19,36, 40,28\]/\[13,17, 36,51, 65,96\]/g' \
cfg/training/yolov7_crowdhuman_head.yaml
$ sed -i -e \
's/\[36,75, 76,55, 72,146\]/\[94,149, 132,208, 157,284\]/g' \
cfg/training/yolov7_crowdhuman_head.yaml
$ sed -i -e \
's/\[142,110, 192,243, 459,401\]/\[195,379, 244,282, 303,407\]/g' \
cfg/training/yolov7_crowdhuman_head.yaml

$ sed -i -e \
's/\[10,13, 16,30, 33,23\]/\[13,17, 36,51, 65,96\]/g' \
cfg/training/yolov7-tiny_crowdhuman_head.yaml
$ sed -i -e \
's/\[30,61, 62,45, 59,119\]/\[94,149, 132,208, 157,284\]/g' \
cfg/training/yolov7-tiny_crowdhuman_head.yaml
$ sed -i -e \
's/\[116,90, 156,198, 373,326\]/\[195,379, 244,282, 303,407\]/g' \
cfg/training/yolov7-tiny_crowdhuman_head.yaml

$ docker build -t yolov7 -f Dockerfile.yolov7 .
```
### 5-2. Training YOLOv7
```bash
$ docker run --rm -it --gpus all \
-v `pwd`:/home/vscode \
--shm-size 64g \
--net host \
yolov7:latest

# Single GPU YOLOv7 training
# --name: save to project/name
# p5 (e.g. coco): 
#   anchors:
#   - [12,16, 19,36, 40,28]  # P3/8
#   - [36,75, 76,55, 72,146]  # P4/16
#   - [142,110, 192,243, 459,401]  # P5/32
# p6 (e.g. coco): 
#  anchors:
#  - [ 19,27,  44,40,  38,94 ]  # P3/8
#  - [ 96,68,  86,152,  180,137 ]  # P4/16
#  - [ 140,301,  303,264,  238,542 ]  # P5/32
#  - [ 436,615,  739,380,  925,792 ]  # P6/64
# --img-size: [train test] image sizes. e.g. 640 480 -> train:640, test:480
$ python train.py \
--workers 8 \
--device 0 \
--batch-size 8 \
--data data/crowdhuman.yaml \
--img-size 640 640 \
--cfg cfg/training/yolov7_crowdhuman_head.yaml \
--weights '' \
--name yolov7 \
--hyp data/hyp.scratch.p5.yaml

python train.py \
--workers 12 \
--device 0 \
--batch-size 62 \
--data data/crowdhuman.yaml \
--img-size 640 640 \
--cfg cfg/training/yolov7_crowdhuman_head.yaml \
--weights '' \
--name yolov7 \
--hyp data/hyp.scratch.p5.yaml

# Single GPU YOLOv7-tiny training
# --name: save to project/name
$ python train.py \
--workers 8 \
--device 0 \
--batch-size 40 \
--data data/crowdhuman.yaml \
--img-size 640 640 \
--cfg cfg/training/yolov7-tiny_crowdhuman_head.yaml \
--weights '' \
--name yolov7_tiny \
--hyp data/hyp.scratch.tiny.yaml

python train.py \
--workers 12 \
--device 0 \
--batch-size 300 \
--data data/crowdhuman.yaml \
--img-size 640 640 \
--cfg cfg/training/yolov7-tiny_crowdhuman_head.yaml \
--weights '' \
--name yolov7_tiny \
--hyp data/hyp.scratch.tiny.yaml
```
### 5-3. Tensorboard
Start a different terminal from the one in which you are running the training and execute the following commands.
```bash
$ cd yolov7
$ docker run --rm -it \
-v `pwd`:/home/vscode \
--shm-size 64g \
--net host \
yolov7:latest

$ tensorboard --logdir runs/train
```
Access `http://localhost:6006` from your browser.
![image](https://user-images.githubusercontent.com/33194443/182865555-c25939a0-5c64-464e-a3f3-1788e6b856bf.png)
![image](https://user-images.githubusercontent.com/33194443/182867133-eb21d3fd-e7aa-4235-9450-95d08339ab2d.png)

## 6. TXT format
- 273271,1a0d6000b9e1f5b7.txt
  - `classid` `center_x` `center_y` `w` `h`
  - `center_x`, `center_y`, `w`, and `h` are scale conversions.
  - `classid` = `0` = `Head`
  - `Head` ≠ `Face`
    ```
    0 0.971191 0.455485 0.057617 0.087440
    0 0.791504 0.392687 0.047852 0.089030
    0 0.656738 0.302862 0.045898 0.093800
    0 0.461914 0.294913 0.052734 0.087440
    0 0.588867 0.222576 0.050781 0.111288
    0 0.372559 0.252782 0.041992 0.095390
    0 0.249512 0.317170 0.063477 0.093800
    0 0.130371 0.193959 0.043945 0.085851
    0 0.235840 0.218601 0.057617 0.087440
    0 0.028320 0.310811 0.056641 0.100159
    0 0.364258 0.149444 0.042969 0.098569
    0 0.356445 0.031002 0.035156 0.062003
    0 0.484375 0.108903 0.039062 0.093800
    0 0.560547 0.032591 0.046875 0.065183
    0 0.708008 0.137520 0.050781 0.100159
    0 0.835938 0.216216 0.050781 0.079491
    0 0.938477 0.033386 0.041016 0.066773
    0 0.862305 0.020668 0.029297 0.041335
    0 0.829590 0.029412 0.036133 0.058824
    0 0.734375 0.024642 0.035156 0.049285
    0 0.684082 0.100954 0.038086 0.077901
    0 0.660645 0.054849 0.036133 0.071542
    0 0.541504 0.022258 0.030273 0.044515
    ```

## 7. Results
- YOLOv7
  ![image](https://user-images.githubusercontent.com/33194443/183258227-8a966dfa-0606-4403-b003-22da2ff10813.png)

- YOLOv7-tiny
  ![image](https://user-images.githubusercontent.com/33194443/183258218-a38fcbee-c9cf-453c-905d-8deac990a1fb.png)

## 8. Benchmark
- YOLOv7-tiny_Head with Post-Process, ONNX TensorRT, RTX3070
  ```bash
  $ sit4onnx \
  --input_onnx_file_path yolov7_tiny_head_0.752_post_480x640.onnx

  INFO: file: yolov7_tiny_head_0.752_post_480x640.onnx
  INFO: providers: ['TensorrtExecutionProvider', 'CPUExecutionProvider']
  INFO: input_name.1: input shape: [1, 3, 480, 640] dtype: float32
  INFO: test_loop_count: 10
  INFO: total elapsed time:  13.000011444091797 ms
  INFO: avg elapsed time per pred:  1.3000011444091797 ms
  INFO: output_name.1: score shape: [0, 1] dtype: float32
  INFO: output_name.2: batchno_classid_x1y1x2y2 shape: [0, 6] dtype: int64
  ```

- YOLOv7-tiny_Head with Post-Process Float16, ONNX CUDA, RTX3070
  ```bash
  $ sit4onnx \
  --input_onnx_file_path yolov7_tiny_head_0.752_post_480x640.onnx \
  --onnx_execution_provider cuda

  INFO: file: yolov7_tiny_head_0.752_post_480x640.onnx
  INFO: providers: ['CUDAExecutionProvider', 'CPUExecutionProvider']
  INFO: input_name.1: input shape: [1, 3, 480, 640] dtype: float32
  INFO: test_loop_count: 10
  INFO: total elapsed time:  35.124778747558594 ms
  INFO: avg elapsed time per pred:  3.5124778747558594 ms
  INFO: output_name.1: score shape: [0, 1] dtype: float32
  INFO: output_name.2: batchno_classid_x1y1x2y2 shape: [0, 6] dtype: int64
  ```

- YOLOv7-tiny_Head with Post-Process Float32, ONNX CPU, Corei9 Gen.10
  ```bash
  $ sit4onnx \
  --input_onnx_file_path yolov7_tiny_head_0.752_post_480x640.onnx \
  --onnx_execution_provider cpu
  
  INFO: file: yolov7_tiny_head_0.752_post_480x640.onnx
  INFO: providers: ['CPUExecutionProvider']
  INFO: input_name.1: input shape: [1, 3, 480, 640] dtype: float32
  INFO: test_loop_count: 10
  INFO: total elapsed time:  178.92169952392578 ms
  INFO: avg elapsed time per pred:  17.892169952392578 ms
  INFO: output_name.1: score shape: [0, 1] dtype: float32
  INFO: output_name.2: batchno_classid_x1y1x2y2 shape: [0, 6] dtype: int64
  ```

## 9. Citation
- CrowdHuman Dataset
    ```
    @article{shao2018crowdhuman,
        title={CrowdHuman: A Benchmark for Detecting Human in a Crowd},
        author={
            Shao,
            Shuai and Zhao,
            Zijian and Li,
            Boxun and Xiao,
            Tete and Yu,
            Gang and Zhang,
            Xiangyu and Sun,
            Jian
        },
        journal={arXiv preprint arXiv:1805.00123},
        year={2018}
    }
    ```

- Context-aware CNNs for person head detection
    ```
    @inproceedings{vu15heads,
        Author = {Vu, Tuan{-}Hung and Osokin, Anton and Laptev, Ivan},
        Title = {Context-aware {CNNs} for person head detection},
        Booktitle = {International Conference on Computer Vision ({ICCV})},
        Year = {2015}
    }
    ```
  - [aosokin](https://github.com/aosokin)
  - https://github.com/aosokin/cnn_head_detection


- Object Detection Toolkits
  - [kvzhao](https://github.com/kvzhao)
  - https://github.com/kvzhao/detection_toolkits

## 10. References
- YOLOv7
    ```
    @article{wang2022yolov7,
      title={
        {YOLOv7}: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors
      },
      author={Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark},
      journal={arXiv preprint arXiv:2207.02696},
      year={2022}
    }
    ```
  - [WongKinYiu](https://github.com/WongKinYiu)
  - https://github.com/WongKinYiu/yolov7

- PINTO_model_zoo

  https://github.com/PINTO0309/PINTO_model_zoo/tree/main/323_YOLOv7_Head
