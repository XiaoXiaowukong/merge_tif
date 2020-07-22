#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xiaoxiaowukong
# datetime:2020/7/3 下午1:22
# software: PyCharm

import sys
import os
import gdal
import color_config
import numpy as np
import subprocess


class TifBandMerge():
    def __init__(self):
        pass

    def getSingleBandData(self, i_path):
        all = {}
        for c_tif in os.listdir(i_path):
            if c_tif != "34_merged.tif":
                continue
            print(c_tif)
            driver = gdal.GetDriverByName("GTiff")
            driver.Register()
            data_set = gdal.Open(os.path.join(i_path, c_tif), gdal.GA_ReadOnly)
            x_size = data_set.RasterXSize
            y_size = data_set.RasterYSize
            bands = data_set.RasterCount
            print("x_size", x_size)
            print("y_size", y_size)
            print("bands", bands)
            if bands == 4:
                r = data_set.GetRasterBand(1).ReadAsArray(0, 0, x_size, y_size)
                g = data_set.GetRasterBand(2).ReadAsArray(0, 0, x_size, y_size)
                b = data_set.GetRasterBand(3).ReadAsArray(0, 0, x_size, y_size)
                all_data = []
                for r_item, g_item, b_item in zip(r, g, b):
                    item_data = []
                    for r_item_item, g_item_item, b_item_item in zip(r_item, g_item, b_item):
                        key = "{}{}{}".format(r_item_item, g_item_item, b_item_item)
                        all[key] = 0
                        try:
                            item_data.append(color_config.color_level[key])
                        except Exception as e:
                            print(e.message)
                            # all_data.append(item_data)
                            # all_data = np.asarray(all_data, dtype=np.uint8)
                            # wirte_geotiff(all_data, os.path.join(o_path, name).replace(".png", "_test.tif"), bounds)
            elif bands == 1:
                item_data = data_set.GetRasterBand(1).ReadAsArray(0, 0, x_size, y_size)
                print(item_data)
                item_data = np.asarray(item_data, dtype="float")
                item_data[item_data == 255] = np.nan
                print(np.nanmax(item_data))
                print(np.nanmin(item_data))
                print(item_data)
            break
        print (all)

    def merge_single(self, i_path):
        merge_command = ['gdal_merge.py', '-o',
                         os.path.join(i_path, "merged.tif")]
        print i_path
        for c_tif in os.listdir(i_path):
            # if c_tif == "34_merged.tif":
            #     continue
            merge_command.append(os.path.join(i_path, c_tif))
        print(merge_command)
        subprocess.call(merge_command)


if __name__ == '__main__':
    args = sys.argv[1:]
    i_path = args[0]
    tif_band_merge = TifBandMerge()
    # tif_band_merge.getSingleBandData(i_path)
    tif_band_merge.merge_single(i_path)
