#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import os
import numpy as np
import argparse
import PIL

kImageWidth = 640
kImageHeight = 480
kColorWhite = [255, 255, 255]

# parse the command line
parser = argparse.ArgumentParser(description="A tool to adjust the images to fixed size using cropping, padding methods.", 
                           formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--source_dir", type=str, default="../shoes_dataset", help="path to source directory")
parser.add_argument("--target_dir", type=str, default="../shoes_dataset_new", help="path to target directory")

try:
    argv = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)


# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        img = param[0]
        param[1] = np.array([x, y])

def image_adjust(img, x, y, file_path):
    # print('height={}, width={}'.format(img.shape[0], img.shape[1]))
    
    # If image size is too small or too large --> resize
    if img.shape[0] <= kImageHeight/2 or img.shape[0] >= kImageHeight * 1.5:
        img = cv2.resize(img, (int(img.shape[1] * kImageHeight / img.shape[0]), kImageHeight))
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))
    if img.shape[1] <= kImageWidth/2 or img.shape[1] >= kImageWidth * 1.5:
        img = cv2.resize(img, (kImageWidth, int(img.shape[0] * kImageWidth / img.shape[1])))
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))
    # If image size is a little bit small --> padding
    if img.shape[0] < kImageHeight:
        pad_top = (kImageHeight - img.shape[0]) / 2
        pad_bottom = kImageHeight - img.shape[0] - pad_top
        img = cv2.copyMakeBorder(img, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=kColorWhite)
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))
    if img.shape[1] < kImageWidth:
        pad_left = (kImageWidth - img.shape[1]) / 2
        pad_right = kImageWidth - img.shape[1] - pad_left
        img = cv2.copyMakeBorder(img, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=kColorWhite)
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))

    # If image size is a little bit large --> cropping
    if img.shape[0] > kImageHeight:
        crop_bottom = int((img.shape[0] - kImageHeight) / 2)
        crop_top = crop_bottom + kImageHeight
        img = img[crop_bottom:crop_top, 0:img.shape[1]]
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))
    if img.shape[1] > kImageWidth:
        crop_left = int((img.shape[1] - kImageWidth) / 2)
        crop_right = crop_left + kImageWidth
        img = img[0:img.shape[0], crop_left:crop_right]
        # print('new h={}, new w={}'.format(img.shape[0], img.shape[1]))

    print('final h={}, final w={}'.format(img.shape[0], img.shape[1]))
    cv2.imwrite(file_path, img)


def processing_loop(images_list, source_dir, target_dir):
    for idx, filename in enumerate(images_list):
        img = cv2.imread(os.path.join(source_dir, filename))
        target_path = os.path.join(target_dir, filename)
        image_adjust(img=img, x=0, y=0, file_path=target_path)


def display_loop(images_list, source_dir, target_dir):
    img = cv2.imread(os.path.join(source_dir, images_list[0]))
    center_position = np.zeros(2, np.uint8)

    # Pass the [image, center_position] to mouse callback function
    params_list = [img, center_position]
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_callback, param=params_list)

    idx = 0
    while True:
        cv2.imshow('image', img)
        if params_list[1][0] != 0 and params_list[1][1] != 0:
            target_path = os.path.join(target_dir, images_list[idx])
            image_adjust(img=img, x=params_list[1][0], y=params_list[1][1], file_path=target_path)
            idx += 1
            if idx >= len(images_list): break
            img = cv2.imread(os.path.join(source_dir, images_list[idx]))
            
            params_list[1] = np.zeros(2, np.uint8)

        keyin = cv2.waitKey(1) & 0xFF 
        if keyin == ord('q') or keyin == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Check target directory
    target_dir = os.path.abspath(os.path.join(os.getcwd(), argv.target_dir))
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    # Check source directory
    source_dir = os.path.abspath(os.path.join(os.getcwd(), argv.source_dir))
    files_list = os.listdir(source_dir)
    images_list = []
    for filename in files_list:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            images_list.append(filename)

    processing_loop(images_list=images_list, source_dir=source_dir, target_dir=target_dir)

    # manually give x, y
    # images_list.sort()
    # images_list = images_list[:10]
    # display_loop(images_list=images_list, source_dir=source_dir, target_dir=target_dir)

