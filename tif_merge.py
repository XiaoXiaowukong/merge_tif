#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xiaoxiaowukong
# datetime:2020/6/29 下午2:42
# software: PyCharm
import glob
import os
import subprocess
import sys


def merge_tiles(input_pattern, output_path):
    merge_command = ['gdal_merge.py', '-o', output_path]
    for name in glob.glob(input_pattern):
        merge_command.append(name)
    subprocess.call(merge_command)


def merge_tiles_size(tif_path, output_path, max_size):
    merge_tif = []
    for tif_index, tif_file in enumerate(os.listdir(tif_path)):
        if os.path.splitext(tif_file)[-1] != ".tif":
            continue
        merge_tif.append(os.path.join(tif_path, tif_file))
    merge_count = merge_tif.__len__() / max_size
    for split_index in range(merge_count + 1):
        item_merge_tif = merge_tif[split_index * max_size:(split_index + 1) * max_size]
        merge_command = ['gdal_merge.py', '-o',
                         os.path.join(output_path, "{}_merged.tif".format(split_index))]
        if item_merge_tif.__len__() == 0:
            continue
        merge_command.extend(item_merge_tif)
        try:
            subprocess.call(merge_command)
        except Exception as e:
            print (e.message)


def file_count(tif_root):
    file_count = 0
    for file_item in os.listdir(tif_root):
        if os.path.isfile(os.path.join(tif_root, file_item)):
            file_count += 1
    return file_count


if __name__ == '__main__':
    args = sys.argv[1:]
    tif_root = args[0]
    merge_dir = args[1]
    max_size = args[2]
    if not os.path.exists(tif_root) or not os.path.exists(merge_dir):
        print("dir is not exist")
        exit(1)

    all_count = file_count(tif_root)
    level_dir = 0
    while (all_count > 1):
        print(level_dir)
        merge_level_dir = os.path.join(merge_dir, str(level_dir))
        if not os.path.exists(merge_level_dir):
            os.mkdir(merge_level_dir)
        merge_tiles_size(tif_root, merge_level_dir, int(max_size))
        tif_root = merge_level_dir
        all_count = file_count(merge_level_dir)
        level_dir += 1
