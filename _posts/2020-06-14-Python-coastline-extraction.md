---
layout: article
title: Python之海岸线提取
tags: ["Python","海岸线"]
key: Python之海岸线提取
show_subscribe: false
license: false
---
海岸线提取是找工作时遇到的一道测试题，因为时间有限，所以代码简单粗暴。具体要求是设计一种算法从给定影像中检测海岸线，并将结果另存为矢量GeoJSON文件。
<!--more-->
## 思路
这里使用归一化水体指数（NDWI）来区分水体和陆地，然后通过边缘检测提取海岸线。
## 步骤
### 加载必要模块
```python
import gdal
from gdalconst import *
import matplotlib.pyplot as plt
import cv2
import numpy as np
import ogr
import os
```
### 读取影像数据
```python
# 色光波段
green_ds=gdal.Open(r'D:\Documents\sentinel-2\B03.tif',GA_ReadOnly)
green_band=green_ds.GetRasterBand(1)
green=green_band.ReadAsArray()
# 读取原影像信息，用于保存结果
gt = green_ds.GetGeoTransform()
proj = green_ds.GetProjectionRef()
# 近红外波段
nir_ds=gdal.Open(r'D:\Documents\sentinel-2\B08.tif',GA_ReadOnly)
nir_band=nir_ds.GetRasterBand(1)
nir=nir_band.ReadAsArray()
```
### 区分陆地和水体
```python
# 计算NDWI，二值化，区分陆地和水面信息
# 还可以对影像进行处理，如空间滤波去除噪声等。
ndwi=np.uint8((green-nir)/(green+nir))
ndwi = cv2.medianBlur(ndwi,9)
ndwi=cv2.threshold(ndwi,10,255,0)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(30,30))
ndwi = cv2.dilate(ndwi,kernel)

plt.figure(figsize=(10, 10))
plt.imshow(ndwi)
plt.show()
```
二值化结果展示：  
![二值化结果](\assets\images\Python-coastline-extraction\water-and-land.png)
### 边缘检测
```python
# find contours
image, contours, hierarchy=cv2.findContours(ndwi,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
```
### 保存为GeoJSON格式
```python
# save the coastline as GeoJSON
driver = ogr.GetDriverByName('GeoJSON')
# create a new data source and layer
if os.path.exists(r'D:\Documents\sentinel-2\coastline.geojson'):
    driver.DeleteDataSource(r'D:\Documents\sentinel-2\coastline.geojson')
ds = driver.CreateDataSource(r'D:\Documents\sentinel-2\coastline.geojson')
if ds is None:
    print('Could not create file')
layer = ds.CreateLayer('coastline.geojson', geom_type=ogr.wkbLineString)

for item in contours:
    line = ogr.Geometry(ogr.wkbLineString)
    for points in item:
        line.AddPoint(points[0][0]*10+gt[0]+5,gt[3]-points[0][1]*10-5)
    # get the FeatureDefn for the output layer
    featureDefn = layer.GetLayerDefn()
    # create a new feature
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(line)
    # add the feature to the output layer
    layer.CreateFeature(feature)
# destroy the geometry and feature and close the data source
line.Destroy()
feature.Destroy()
ds.Destroy()
```
### 保存为shapefile格式
```python
# save the coastline as shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
# create a new data source and layer
if os.path.exists(r'D:\Documents\sentinel-2\coastline.shp'):
    driver.DeleteDataSource(r'D:\Documents\sentinel-2\coastline.shp')
ds = driver.CreateDataSource(r'D:\Documents\sentinel-2\coastline.shp')
if ds is None:
    print('Could not create file')
layer = ds.CreateLayer('coastline', geom_type=ogr.wkbLineString)
# add an id field to the output
fieldDefn = ogr.FieldDefn('id', ogr.OFTInteger)
layer.CreateField(fieldDefn)
i=0
for item in contours:
    line = ogr.Geometry(ogr.wkbLineString)
    for points in item:
        line.AddPoint(points[0][0]*10+gt[0]+5,gt[3]-points[0][1]*10-5)
    # get the FeatureDefn for the output layer
    featureDefn = layer.GetLayerDefn()
    # create a new feature
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(line)
    feature.SetField('id', i)
    # add the feature to the output layer
    layer.CreateFeature(feature)

# destroy the geometry and feature and close the data source
line.Destroy()
feature.Destroy()
ds.Destroy()
```
## 结果展示  
![海岸线](\assets\images\Python-coastline-extraction\coastline.jpg)  
如果对您有用的话，别忘了给点个赞哦^_^ ！