#! /usr/bin/env python

"""gen_txts.py

To generate YOLO txt files from the original CrowdHuman annotations.
Please also refer to README.md in this directory.

Inputs:
    * raw/annotation_train.odgt
    * raw/annotation_val.odgt
    * crowdhuman-{width}x{height}/[IDs].jpg

Outputs:
    * crowdhuman-{width}x{height}train.txt
    * crowdhuman-{width}x{height}/test.txt
    * crowdhuman-{width}x{height}/[IDs].txt (one annotation for each image in the training or test set)
"""

import os
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

# input image width/height of the yolov4 model, set by command-line argument
INPUT_WIDTH  = 0
INPUT_HEIGHT = 0

# Minimum width/height of objects for detection (don't learn from objects smaller than these)
MIN_W = 5
MIN_H = 5

# Do K-Means clustering in order to determine "anchor" sizes
DO_KMEANS = True
KMEANS_CLUSTERS = 9
BBOX_WHS = []  # keep track of bbox width/height with respect to 640x640


def txt_line(cls, bbox, img_w, img_h):
    """Generate 1 line in the txt file."""
    x, y, w, h = bbox
    x = max(int(x), 0)
    y = max(int(y), 0)
    w = min(int(w), img_w - x)
    h = min(int(h), img_h - y)
    w_rescaled = float(w) * INPUT_WIDTH  / img_w
    h_rescaled = float(h) * INPUT_HEIGHT / img_h
    if w_rescaled < MIN_W or h_rescaled < MIN_H:
        return ''
    else:
        if DO_KMEANS:
            global BBOX_WHS
            BBOX_WHS.append((w_rescaled, h_rescaled))
        cx = (x + w / 2.) / img_w
        cy = (y + h / 2.) / img_h
        nw = float(w) / img_w
        nh = float(h) / img_h
        return f'{int(cls)} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n'


def read_a_xml(xml, boxes_wh):
    tree = ET.parse(xml)
    root = tree.getroot()
    fname = root.find("filename").text

    w = int(root.find("size/width").text)
    h = int(root.find("size/height").text)
    if fname not in boxes_wh.keys():
        boxes_wh[fname] = {
            'image_size': [w, h],
            'boxes': [],
        }

    for obj in root.findall('object'):
        if obj.find('name') is None:
            continue
        bndbox = obj.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        boxes_wh[fname]['boxes'].append(
            [
                xmin, # x1
                ymin, # y1
                xmax - xmin, # w
                ymax - ymin, # h
            ]
        )

def read_xmls(annopath, split_list, boxes_wh):
    for instancename in split_list:
        read_a_xml(f'{annopath}/{instancename}.xml', boxes_wh)
    return boxes_wh


def process(set_, split_filename, annopath, output_dir=None):
    """Process either 'train' or 'test' set."""
    assert output_dir is not None
    output_dir.mkdir(exist_ok=True)
    jpgs = []
    split_list = []
    raw_anno_count = 0
    print(f'** Processing Sets: {set_}')

    f = open(split_filename, 'r')
    lines = f.read().splitlines()
    for line in lines:
        split_list.append(line)

    file_infos = {}
    file_infos = read_xmls(annopath, split_list, file_infos)
    """
    boxes_wh =
        {
            "image_filename": {"image_size": [image_width, image_height], "boxes": [[x1, y1, w, h], [x1, y1, w, h], ...]},
            "image_filename": {"image_size": [image_width, image_height], "boxes": [[x1, y1, w, h], [x1, y1, w, h], ...]},
            "image_filename": {"image_size": [image_width, image_height], "boxes": [[x1, y1, w, h], [x1, y1, w, h], ...]},
            :
        }
    """
    for image_filename, info in file_infos.items():
        image_filename_no_ext = os.path.splitext(os.path.basename(image_filename))[0]
        txt_path = f'{output_dir}/{image_filename_no_ext}.txt'
        line_count = 0
        with open(txt_path, 'w') as ftxt:
            for box_x1y1wh in info['boxes']:
                line = txt_line(0, box_x1y1wh, info['image_size'][0], info['image_size'][1])
                if line:
                    ftxt.write(line)
                    line_count += 1
        if line_count > 0:
            jpgs.append(f'data/{output_dir}/{image_filename_no_ext}.jpeg')
            raw_anno_count += 1
    print(f'** Processed Images: {raw_anno_count}')

    # write the 'data/hollywoodheads-{args.dim}/train.txt' or 'data/hollywoodheads-{args.dim}/test.txt'
    set_path = f'{output_dir}/{set_}.txt'
    with open(set_path, 'w') as fset:
        for jpg in jpgs:
            fset.write(f'{jpg}\n')


def rm_txts(output_dir):
    """Remove txt files in output_dir."""
    for txt in output_dir.glob('*.txt'):
        if txt.is_file():
            txt.unlink()


def main():
    global INPUT_WIDTH, INPUT_HEIGHT

    parser = ArgumentParser()
    parser.add_argument('dim', help='input width and height, e.g. 640x640')
    args = parser.parse_args()

    dim_split = args.dim.split('x')
    if len(dim_split) != 2:
        raise SystemExit(f'ERROR: bad spec of input dim ({args.dim})')
    INPUT_WIDTH, INPUT_HEIGHT = int(dim_split[0]), int(dim_split[1])
    if INPUT_WIDTH % 32 != 0 or INPUT_HEIGHT % 32 != 0:
        raise SystemExit(f'ERROR: bad spec of input dim ({args.dim})')

    output_dir = Path(f'hollywoodheads-{args.dim}')
    if not output_dir.is_dir():
        raise SystemExit(f'ERROR: {output_dir.as_posix()} does not exist.')

    rm_txts(output_dir)
    annopath = 'raw/HollywoodHeads/Annotations'
    process('test', 'raw/HollywoodHeads/Splits/val.txt', annopath, output_dir)
    process('train', 'raw/HollywoodHeads/Splits/train.txt', annopath, output_dir)

    print(f'** Processing .data')
    with open(f'hollywoodheads-{args.dim}.data', 'w') as f:
        f.write(f"""classes = 1
train   = data/hollywoodheads-{args.dim}/train.txt
valid   = data/hollywoodheads-{args.dim}/test.txt
names   = data/hollywoodheads.names
backup  = backup/\n""")
    print(f'** Processed .data')

    if DO_KMEANS:
        try:
            from sklearn.cluster import KMeans
        except ModuleNotFoundError:
            print('WARNING: no sklearn, skipping anchor clustering...')
        else:
            X = np.array(BBOX_WHS)
            kmeans = KMeans(n_clusters=KMEANS_CLUSTERS, random_state=0).fit(X)
            centers = kmeans.cluster_centers_
            centers = centers[centers[:, 0].argsort()]  # sort by bbox w
            print(f'\n** for yolov7-{int(INPUT_WIDTH)}x{int(INPUT_HEIGHT)}, ', end='')
            print('resized bbox width/height clusters are: ', end='')
            print(' '.join([f'({c[0]:.2f}, {c[1]:.2f})' for c in centers]))
            print('\nanchors = ', end='')
            print(',  '.join([f'{int(c[0])},{int(c[1])}' for c in centers]))


if __name__ == '__main__':
    main()
