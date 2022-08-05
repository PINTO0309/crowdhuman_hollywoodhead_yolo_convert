import os
import cv2
import glob
import tqdm
from natsort import natsorted
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-i',
        '--image_txt_folder_path',
        required=True,
        help='Path of the folder where the JPG and label TXT are stored.'
    )
    args = parser.parse_args()

    path = args.image_txt_folder_path
    image_files = glob.glob(f"{path}/*.jp*g")
    txt_files = glob.glob(f"{path}/*.txt")

    bbox_whs = []
    total_width = 0
    total_height = 0

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



if __name__ == '__main__':
    main()