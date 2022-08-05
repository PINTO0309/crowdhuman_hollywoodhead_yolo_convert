#! /usr/bin/env python

import os
import cv2
import glob
from tqdm import tqdm
import numpy as np
from natsort import natsorted
from sklearn.cluster import KMeans
from argparse import ArgumentParser


KMEANS_CLUSTERS = 9
MAX_TARGET = 1000000

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

    print('** image files sorting...')
    sorted_image_files = natsorted(image_files)
    print(f'** sorted_image_files count: {len(sorted_image_files)}')
    print('** image files sort done')
    if f"{path}/train.txt" in txt_files:
        txt_files.remove(f"{path}/train.txt")
    if f"{path}/val.txt" in txt_files:
        txt_files.remove(f"{path}/val.txt")
    if f"{path}/test.txt" in txt_files:
        txt_files.remove(f"{path}/test.txt")
    sorted_txt_files = natsorted(txt_files)

    print('** txt files sorting...')
    print(f'** sorted_txt_files count: {len(sorted_txt_files)}')
    print('** txt files sort done')
    """
    sorted_image_files count: 244110
    sorted_txt_files count: 242808
    """

    image_files_to_be_removed = []
    if len(sorted_txt_files) < len(sorted_image_files):
        print('** image files cleaning...')
        sorted_txt_files_no_ext = [os.path.splitext(os.path.basename(txt))[0] for txt in sorted_txt_files]
        sorted_image_files_no_ext = [os.path.splitext(os.path.basename(img))[0] for img in sorted_image_files]
        image_files_to_be_removed = [img for img in sorted_image_files_no_ext if img not in sorted_txt_files_no_ext]
        for remove_file in image_files_to_be_removed:
            target_files = glob.glob(f"{path}/{remove_file}.jp*g")
            for f in target_files:
                os.remove(f)
        print('** image files cleaning done')

        print('** files re-sorting...')
        image_files = glob.glob(f"{path}/*.jp*g")
        sorted_image_files = natsorted(image_files)
        txt_files = glob.glob(f"{path}/*.txt")
        sorted_txt_files = natsorted(txt_files)
        print('** files re-sort done')
        print(f'** re-sorted_image_files count: {len(sorted_image_files)}')
        print(f'** re-sorted_txt_files count: {len(sorted_txt_files)}')

    print('** anchor calculating...')
    bbox_whs = []
    processed_count = 0
    for txt_file in tqdm(sorted_txt_files):
        with open(txt_file, 'r') as txtf:
            lines = txtf.read().splitlines()
            for line in lines:
                lw_scale = float(line.split()[3])
                lh_scale = float(line.split()[4])
                w_rescaled = lw_scale * input_width
                h_rescaled = lh_scale * input_height
                bbox_whs.append((w_rescaled, h_rescaled))

        processed_count += 1
        if processed_count >= MAX_TARGET:
            break

    x = np.array(bbox_whs)
    kmeans = KMeans(n_clusters=KMEANS_CLUSTERS, random_state=0).fit(x)
    centers = kmeans.cluster_centers_
    centers = centers[centers[:, 0].argsort()]  # sort by bbox w
    print('** anchor calculation done')
    print(f'\n** for yolov7-{int(input_width)}x{int(input_height)}, ', end='')
    print('resized bbox width/height clusters are: ', end='')
    print(' '.join([f'({c[0]:.2f}, {c[1]:.2f})' for c in centers]))
    print('\nanchors = ', end='')
    print(',  '.join([f'{int(c[0])},{int(c[1])}' for c in centers]))


if __name__ == '__main__':
    main()