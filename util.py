#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xiaoxiaowukong
# datetime:2020/6/25 上午10:17
# software: PyCharm
import math
from math import log
from math import tan
from math import pi
from math import e
from math import atan


def get_tile_num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    print(xtile, ytile)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)


def get_tile_bbox(z, x, y):
    right_top = num2deg(x + 1, y, z)
    left_bottom = num2deg(x, y + 1, z)
    return (left_bottom[0], right_top[1], right_top[0], left_bottom[1],)


def get_tile_bbox1(z, x, y):
    right_top = num2deg(x + 1, y, z)
    left_bottom = num2deg(x, y + 1, z)
    return (left_bottom[0], left_bottom[1], right_top[0], right_top[1])


def latlon2tile(lon, lat, z):
    x = int((lon / 180 + 1) * 2 ** z / 2)  # x座標
    y = int(((-log(tan((45 + lat / 2) * pi / 180)) + pi) * 2 ** z / (2 * pi)))  # y座標
    print [y, x]


def tile2latlon(x, y, z):
    lon0 = (x / 2.0 ** z) * 360 - 180  # 経度（東経）
    mapy = (y / 2.0 ** z) * 2 * pi - pi
    lat0 = 2 * atan(e ** (- mapy)) * 180 / pi - 90  # 緯度（北緯）

    # lon1 = (x / 2.0 ** z) * 360 + 180  # 経度（東経）
    # lat1 = 2 * atan(e ** (- mapy)) * 180 / pi - 85.051128  # 緯度（北緯）
    return [lon0, lat0]


def tile2latlon2(x, y, z):
    lon = (x / 2.0 ** z) * 360 + 180  # 経度（東経）
    mapy = (y / 2.0 ** z) * 2 * pi - pi
    lat = 2 * atan(e ** (- mapy)) * 180 / pi - 85.051128  # 緯度（北緯）
    return [lon, lat]
    ##############google###########


def create_png(o_name):
    from PIL import Image
    image = Image.open("./png/test.png")
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    pixels_out = []
    for row in pixels:
        for tup in row:
            pixels_out.append(255)
    image_out = Image.new(image.mode, image.size)
    image_out.putdata(pixels_out)
    image_out.save(o_name)


if __name__ == '__main__':
    create_png()
