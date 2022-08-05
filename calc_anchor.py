#! /usr/bin/env python

import cv2
import glob
import tqdm
import numpy as np
from natsort import natsorted
from sklearn.cluster import KMeans
from argparse import ArgumentParser


KMEANS_CLUSTERS = 9


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-i',
        '--image_txt_folder_path',
        type=str,
        required=True,
        help='Path of the folder where the JPG and label TXT are stored.',
    )
    parser.add_argument(
        '-d',
        '--dim',
        type=str,
        required=True,
        help='input width and height, e.g. 640x480',
    )

    args = parser.parse_args()

    path = args.image_txt_folder_path
    dim_split = args.dim.split('x')
    if len(dim_split) != 2:
        raise SystemExit(f'ERROR: bad spec of input dim ({args.dim})')
    input_width, input_height = int(dim_split[0]), int(dim_split[1])
    if input_width % 32 != 0 or input_height % 32 != 0:
        raise SystemExit(f'ERROR: bad spec of input dim ({args.dim})')

    image_files = glob.glob(f"{path}/*.jp*g")
    txt_files = glob.glob(f"{path}/*.txt")

    bbox_whs = []
    for (image_file, txt_file) in tqdm(zip(natsorted(image_files), natsorted(txt_files))):
        image = cv2.imread(image_file)
        w, h = image.shape[1], image.shape[0]
        with open(txt_file, 'r') as txtf:
            lines = txtf.read().splitlines()
            for line in lines:
                lw_scale = line.split()[3]
                lh_scale = line.split()[4]
                w_rescaled = lw_scale * w
                h_rescaled = lh_scale * h
                bbox_whs.append((w_rescaled, h_rescaled))

    x = np.array(bbox_whs)
    kmeans = KMeans(n_clusters=KMEANS_CLUSTERS, random_state=0).fit(x)
    centers = kmeans.cluster_centers_
    centers = centers[centers[:, 0].argsort()]  # sort by bbox w
    print(f'\n** for yolov7-{int(input_width)}x{int(input_height)}, ', end='')
    print('resized bbox width/height clusters are: ', end='')
    print(' '.join([f'({c[0]:.2f}, {c[1]:.2f})' for c in centers]))
    print('\nanchors = ', end='')
    print(',  '.join([f'{int(c[0])},{int(c[1])}' for c in centers]))


if __name__ == '__main__':
    main()