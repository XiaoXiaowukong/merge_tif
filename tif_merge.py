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
    merge_command = None
    for tif_index, tif_file in enumerate(os.listdir(tif_path)):
        if tif_index == 0:
            merge_command = ['gdal_merge.py', '-o',
                             output_path.replace("merged.tif", "{}_merged.tif".format(tif_index / max_size))]
        else:
            if tif_index % max_size == 0:
                process(merge_command)
                merge_command = ['gdal_merge.py', '-o',
                                 output_path.replace("merged.tif", "{}_merged.tif".format(tif_index / max_size))]
            else:
                merge_command.append(os.path.join(tif_path, tif_file))
    if merge_command is not None:
        process(merge_command)


def process(command):
    try:
        subprocess.call(command)
    except Exception as e:
        print (e.message)


if __name__ == '__main__':
    args = sys.argv[1:]
    png_root = args[0]
    output_dir = args[1]
    max_size = args[2]
    print (png_root)
    print (output_dir)
    print (max_size)
    merge_tiles_size(png_root, output_dir + '/merged.tif', max_size)
