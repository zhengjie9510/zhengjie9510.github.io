---
layout: article
title: Acrpy之设为空函数
tags: ["Python","Arcpy"]
key: Acrpy之设为空函数
show_subscribe: false
license: false
---
利用栅格计算器中的SetNull函数将满足条件(值大于100)的像元值设为NoData.
<!--more-->
```python
# -*- coding: utf-8 -*-
import arcpy
from arcpy import env
from arcpy.sa import *
# 如果出现错误代码000824，需要加入下一行代码
# https://zhengjie9510.github.io/2020/07/16/Acrpy%E4%B9%8B%E9%94%99%E8%AF%AF%E4%BB%A3%E7%A0%81000824.html
arcpy.CheckOutExtension("Spatial")
env.workspace = r"D:\Downloads\TEST"
rasters = arcpy.ListRasters("*", "tif")
for item in rasters:
    # Set local variables
    inRaster = item
    inFalseRaster = item
    whereClause = "VALUE > 100"

    # Execute SetNull
    outSetNull = SetNull(inRaster, inFalseRaster, whereClause)
    print item
    outSetNull.save('D:\\Downloads\\OUT\\'+item) # 最好使用双斜线，否则容易出错
```
如果对您有用的话，别忘了给点个赞哦^_^ ！