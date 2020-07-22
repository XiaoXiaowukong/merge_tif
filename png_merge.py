#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xiaoxiaowukong
# datetime:2020/7/16 上午10:59
# software: PyCharm
import sys
import gdal
import os
import numpy as np
import osr
import util


class Pngmerge():
    def __init__(self):
        pass

    def read_png(self, png_path):
        driver = gdal.GetDriverByName('PNG')
        driver.Register()
        data_set = gdal.Open(png_path, gdal.GA_ReadOnly)
        x_size = data_set.RasterXSize
        y_size = data_set.RasterYSize
        bands = data_set.RasterCount
        if bands == 4:
            b = data_set.GetRasterBand(3).ReadAsArray(0, 0, x_size, y_size)
            b[b == 0] = 0
            b[b == 169] = 1
            b[b == 247] = 1
            b[b == 192] = 2
            b[b == 191] = 2
            b[b == 183] = 3
            b[b == 180] = 3
            b[b == 145] = 4
            b[b == 201] = 5
            b[b == 220] = 6
            all_data = b
        elif bands == 1:
            all_data = data_set.GetRasterBand(1).ReadAsArray(0, 0, x_size, y_size)
            all_data[all_data == 255] = 0
        del data_set
        return all_data

    def merge_png(self, png_root):
        self.find_size(png_root)
        def_x = 256
        def_y = 256
        self.empt_all_data = np.full(shape=(self.y_range.__len__() * def_y, self.x_range.__len__() * def_x),
                                     fill_value=0,
                                     dtype=np.uint8)
        for root, dirs, files in os.walk(png_root):
            for name in files:
                if os.path.splitext(name)[-1] == ".png":
                    item_data = self.read_png(os.path.join(root, name))
                    if np.max(item_data) > 6 or np.min(item_data) < 0:
                        print os.path.join(root, name)
                        print np.max(item_data)
                        print np.min(item_data)
                        self.check_png(os.path.join(root, name))
                        break
                    else:
                        [z, x, y] = os.path.splitext(name)[0].split("-")
                        for x_index, x_x in enumerate(self.x_range):
                            if int(x) == x_x:
                                break
                        for y_index, y_y in enumerate(self.y_range):
                            if int(y) == y_y:
                                break
                        self.empt_all_data[y_index * def_y:(y_index + 1) * def_y,
                        x_index * def_x:(x_index + 1) * def_x] = item_data

    def merge_to_tif(self, o_path):
        gtif_driver = gdal.GetDriverByName("GTiff")
        # 写入目标文件
        x, y = np.asarray(self.empt_all_data).shape
        print x, y
        out_ds = gtif_driver.Create(o_path, y, x, 1, gdal.GDT_UInt16)
        # 设置裁剪出来图的原点坐标
        dst_transform = (self.transform[0], (self.transform[1] - self.transform[0]) / y, 0.0, self.transform[2], 0.0,
                         (self.transform[3] - self.transform[2]) / x)
        print dst_transform
        out_ds.SetGeoTransform(dst_transform)
        srs = self.createSrs("4326")
        if (srs != None):
            # 设置SRS属性（投影信息）
            out_ds.SetProjection(srs)
        out_ds.GetRasterBand(1).WriteArray(self.empt_all_data[::-1])
        out_ds.GetRasterBand(1).SetNoDataValue(0)
        # 将缓存写入磁盘
        out_ds.FlushCache()
        del out_ds

    def createSrs(self, projstr):
        if (projstr == "4326"):
            srs4326 = osr.SpatialReference()
            srs4326.ImportFromEPSG(4326)
        proj = str(srs4326)
        return proj

    def find_transform(self):
        print self.x_range[0], self.y_range[0]
        print self.x_range[-1], self.y_range[-1]
        y0, x1 = util.tile2latlon(self.x_range[0], self.y_range[0], 17)
        y1, x0 = util.tile2latlon(self.x_range[-1] + 1, self.y_range[-1] + 1, 17)
        self.transform = [y0, y1, x0, x1]
        print(self.transform)

    def find_size(self, png_root):
        x_ranges = []
        y_ranges = []
        for root, dirs, files in os.walk(png_root):
            for name in files:
                if os.path.splitext(name)[-1] == ".png":
                    [z, x, y] = os.path.splitext(name)[0].split("-")
                    x_ranges.append(x)
                    y_ranges.append(y)
        print(max(x_ranges))
        print(min(x_ranges))
        print(max(y_ranges))
        print(min(y_ranges))
        self.x_range = np.arange(int(min(x_ranges)), int(max(x_ranges)) + 1)
        self.y_range = np.arange(int(min(y_ranges)), int(max(y_ranges)) + 1)
        print (self.x_range)
        print (self.y_range)

    def check_png(self, png_path):
        rgb_dic = {}
        driver = gdal.GetDriverByName('PNG')
        driver.Register()
        data_set = gdal.Open(png_path, gdal.GA_ReadOnly)
        x_size = data_set.RasterXSize
        y_size = data_set.RasterYSize
        bands = data_set.RasterCount
        if bands == 4:
            r = data_set.GetRasterBand(1).ReadAsArray(0, 0, x_size, y_size)
            g = data_set.GetRasterBand(2).ReadAsArray(0, 0, x_size, y_size)
            b = data_set.GetRasterBand(3).ReadAsArray(0, 0, x_size, y_size)

        for r_item, g_item, b_item in zip(r, g, b):
            for r_item_item, g_item_item, b_item_item in zip(r_item, g_item, b_item):
                key = "{}{}{}".format(r_item_item, g_item_item, b_item_item)
                rgb_dic[key] = 0
        print rgb_dic
        del data_set


if __name__ == '__main__':
    args = sys.argv[1:]
    i_path = args[0]
    o_path = "{}.tif".format(os.path.join(i_path,i_path.split("/")[-1]))
    pngmerge = Pngmerge()
    pngmerge.merge_png(i_path)
    pngmerge.find_transform()
    pngmerge.merge_to_tif(o_path)
