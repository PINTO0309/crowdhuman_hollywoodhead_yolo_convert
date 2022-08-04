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


import json
from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import cv2


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


def image_shape(ID, image_dir):
    assert image_dir is not None
    jpg_path = image_dir / (f'{ID}.jpg')
    img = cv2.imread(jpg_path.as_posix())
    return img.shape


def txt_line(cls, bbox, img_w, img_h):
    """Generate 1 line in the txt file."""
    assert INPUT_WIDTH > 0 and INPUT_HEIGHT > 0
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


def process(set_='test', annotation_filename='raw/annotation_val.odgt', output_dir=None):
    """Process either 'train' or 'test' set."""
    assert output_dir is not None
    output_dir.mkdir(exist_ok=True)
    jpgs = []
    raw_anno_count = 0
    print(f'** Processing Sets: {set_}')
    with open(annotation_filename, 'r') as fanno:
        for raw_anno in fanno.readlines():
            anno = json.loads(raw_anno)
            ID = anno['ID']  # e.g. '273271,c9db000d5146c15'
            # print('Processing ID: %s' % ID)
            img_h, img_w, img_c = image_shape(ID, output_dir)
            assert img_c == 3  # should be a BGR image
            txt_path = output_dir / (f'{ID}.txt')
            # write a txt for each image
            line_count = 0
            with open(txt_path.as_posix(), 'w') as ftxt:
                for obj in anno['gtboxes']:
                    if obj['tag'] == 'mask':
                        continue  # ignore non-human
                    assert obj['tag'] == 'person'
                    if 'hbox' in obj.keys():  # head
                        line = txt_line(0, obj['hbox'], img_w, img_h)
                        if line:
                            ftxt.write(line)
                            line_count += 1
                    if 'fbox' in obj.keys():  # full body
                        # line = txt_line(1, obj['fbox'], img_w, img_h)
                        # if line:
                        #     ftxt.write(line)
                        pass # ignore non-head
            if line_count > 0:
                jpgs.append(f'data/{output_dir}/{ID}.jpg')
                raw_anno_count += 1
    print(f'** Processed Images: {raw_anno_count}')
    # write the 'data/crowdhuman/train.txt' or 'data/crowdhuman/test.txt'
    set_path = output_dir / (f'{set_}.txt')
    with open(set_path.as_posix(), 'w') as fset:
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

    output_dir = Path(f'crowdhuman-{args.dim}')
    if not output_dir.is_dir():
        raise SystemExit(f'ERROR: {output_dir.as_posix()} does not exist.')

    rm_txts(output_dir)
    process('test', 'raw/annotation_val.odgt', output_dir)
    process('train', 'raw/annotation_train.odgt', output_dir)

    print(f'** Processing .data')
    with open(f'crowdhuman-{args.dim}.data', 'w') as f:
        f.write(f"""classes = 1
train   = data/crowdhuman-{args.dim}/train.txt
valid   = data/crowdhuman-{args.dim}/test.txt
names   = data/crowdhuman.names
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
            print('\n** for yolov7-%dx%d, ' % (INPUT_WIDTH, INPUT_HEIGHT), end='')
            print('resized bbox width/height clusters are: ', end='')
            print(' '.join([f'({c[0]:.2f}, {c[1]:.2f})' for c in centers]))
            print('\nanchors = ', end='')
            print(',  '.join([f'{int(c[0])},{int(c[1])}' for c in centers]))


if __name__ == '__main__':
    main()
