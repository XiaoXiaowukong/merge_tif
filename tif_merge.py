#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xiaoxiaowukong
# datetime:2020/6/29 下午2:42
# software: PyCharm
import glob
import os
import subprocess
import sys

import math
import numpy as np


def merge_tiles(input_pattern, output_path):
    merge_command = ['gdal_merge.py', '-o', output_path]
    for name in glob.glob(input_pattern):
        merge_command.append(name)
    subprocess.call(merge_command)


# 将tif转为shp
def transform_to_shp():
    shp_command = ['gdal_polygonize.py', '/Volumes/pionner2/日本数据/new_merge/1/0_merged.tif', '-nomask', '0', '-f',
                   'ESRI SHAPEFILE', "./123.shp"]
    subprocess.call(shp_command)


def tif_range(tif_path):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for tif_index, tif_file in enumerate(os.listdir(tif_path)):
        if os.path.splitext(tif_file)[-1] != ".tif":
            continue
        [z, x, y] = os.path.splitext(tif_file)[0].split("-")
        if min_x == 0:
            min_x = int(x)
        if max_x == 0:
            max_x = int(x)
        if min_y == 0:
            min_y = int(y)
        if max_y == 0:
            max_y = int(y)
        if int(x) > max_x:
            max_x = int(x)
        elif int(x) < min_x:
            min_x = int(x)
        if int(y) > max_y:
            max_y = int(y)
        elif int(y) < min_y:
            min_y = int(y)

    return min_x, max_x, min_y, max_y


# 第一遍可以这么弄
def merge_tiles_size(tif_path, output_path, max_size):
    min_x, max_x, min_y, max_y = tif_range(tif_path)
    print min_x, max_x, min_y, max_y
    # 开始分区以X轴为标准

    x_split = range(min_x, max_x + max_size, max_size)
    y_split = range(min_y, max_y + max_size, max_size)
    print (x_split)
    print (y_split)
    group_xy = []
    for x_split_s_index, x_split_s in enumerate(x_split):
        for y_split_s_index, y_split_s in enumerate(y_split):
            if x_split_s_index + 1 == x_split.__len__() or y_split_s_index + 1 == y_split.__len__():
                pass
            else:
                group_xy.append([x_split_s, x_split[x_split_s_index + 1], y_split_s, y_split[y_split_s_index + 1]])
    # print group_xy
    for group_xy_item_index, group_xy_item in enumerate(group_xy):
        merge_command = ['gdal_merge.py', '-o',
                         os.path.join(output_path, "{}_merged.tif".format(group_xy_item_index))]
        print(group_xy_item)
        merge_tifs = []
        for tif_i, tif_f in enumerate(os.listdir(tif_path)):
            if not os.path.splitext(tif_f)[-1] == ".tif":
                continue
            [z, x, y] = os.path.splitext(tif_f)[0].split("-")
            if int(x) >= group_xy_item[0] and int(x) < group_xy_item[1] and int(y) >= group_xy_item[2] and int(y) < \
                    group_xy_item[3]:
                merge_tifs.append(os.path.join(tif_path, tif_f))
        if merge_tifs.__len__() == 0:
            print("range no file")
            continue
        merge_command.extend(merge_tifs)
        try:
            subprocess.call(merge_command)
        except Exception as e:
            print (e.message)

            # merge_count = merge_tif.__len__() / max_size
            # for split_index in range(merge_count + 1):
            #     item_merge_tif = merge_tif[split_index * max_size:(split_index + 1) * max_size]
            #     merge_command = ['gdal_merge.py', '-o',
            #                      os.path.join(output_path, "{}_merged.tif".format(split_index))]
            #     if item_merge_tif.__len__() == 0:
            #         continue
            #     merge_command.extend(item_merge_tif)
            #     try:
            #         subprocess.call(merge_command)
            #     except Exception as e:
            #         print (e.message)


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
    merge_tiles_size(tif_root, merge_dir, int(max_size))
    # transform_to_shp()

    # all_count = file_count(tif_root)
    # level_dir = 0
    # while (all_count > 1):
    #     print(level_dir)
    #     merge_level_dir = os.path.join(merge_dir, str(level_dir))
    #     if not os.path.exists(merge_level_dir):
    #         os.mkdir(merge_level_dir)
    #     merge_tiles_size(tif_root, merge_level_dir, int(max_size))
    #     tif_root = merge_level_dir
    #     all_count = file_count(merge_level_dir)
    #     level_dir += 1
