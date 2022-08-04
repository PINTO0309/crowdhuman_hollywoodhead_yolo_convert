import json
import tqdm
from os.path import join
from os import listdir
from argparse import ArgumentParser
import xml.etree.ElementTree as ET


'''
python hollywoodhead_to_coco.py \
--data_root . \
--output_path .
'''
agnostic_label_map = {
    1: 'head',
}

def read_a_xml(xml, boxes_wh):
    tree = ET.parse(xml)
    root = tree.getroot()
    fname = root.find("filename").text

    w = int(root.find("size/width").text)
    h = int(root.find("size/height").text)
    if fname not in boxes_wh.keys():
        boxes_wh[fname] = ((w,h),[])

    for obj in root.findall('object'):
        if obj.find('name') is None:
            continue
        name_class = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))

        # difficult = obj.find('difficult')
        # if difficult.text != '0':
        #     print(fname)

        #print(xmin,ymin,xmax,ymax)
        boxes_wh[fname][1].append(
            (
                xmin,
                ymin,
                xmax - xmin,
                ymax - ymin,
                name_class,
            )
        )


def read_xmls(subset_list, path, boxes_wh):
    for instancename in tqdm.tqdm(subset_list):
        read_a_xml(join(path,instancename+'.xml'), boxes_wh)
    return boxes_wh


def gen_coco_json(boxes_wh):
    json_dict = {
        'images': [],
        'annotations': [],
        'categories': [],
    }
    bb_id = 1
    for image_id, image_name in enumerate(tqdm.tqdm((boxes_wh.keys()))):
        w,h = boxes_wh[image_name][0]
        image_info = {
            'file_name': image_name,
            'height': h,
            'width': w,
            'id': image_id,
        }
        json_dict['images'].append(image_info)

        for i,v in enumerate(boxes_wh[image_name][1]):
            xmin,ymin,w,h,name_class = v
            annotation = {
                'id': bb_id,
                'image_id': image_id,
                'category_id': 1,
                'segmentation': [],
                'area': w * h,
                'bbox': [xmin, ymin, w, h],
                'iscrowd': 0,
                'ignore': 0,
            }
            json_dict['annotations'].append(annotation)
            bb_id = bb_id +1

    for label_id, label_name in agnostic_label_map.items():
        json_dict['categories'].append(
            {
                'supercategory': 'human',
                'id': label_id,
                'name': label_name,
            }
        )
    return json_dict


def main(args):
    root = args.data_root
    path = join(root, 'HollywoodHeads/Annotations')
    split_path = join(root, 'HollywoodHeads/Splits')
    split_dict = {
        'train.txt':[],
        'val.txt':[],
    }

    for p in listdir(split_path):
        if p in split_dict.keys():
            print('[*]Reading split file:', join(split_path, p))
            f = open(join(split_path, p), 'r')
            lines = f.read().splitlines()
            for line in tqdm.tqdm(lines):
                split_dict[p].append(line)

    for subset in split_dict.keys():
        boxes_wh = {}
        print('[*]Reading subset xmls:',subset)
        boxes_wh = read_xmls(split_dict[subset], path, boxes_wh)
        print('[*]Gen subset dict:', subset)
        # json_dict = gen_coco_json(boxes_wh)
        # with open(join(args.output_path, f'HollywoodHead_{subset.split(".")[0]}.json'), 'w') as json_fp:
        #     json_str = json.dumps(json_dict)
        #     json_fp.write(json_str)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-d',
        '--data_root',
        type=str,
        default='./',
        help='Path to the dataset root',
    )
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        default='./',
        help='Path to the output json file.',
    )
    args = parser.parse_args()
    main(args)
