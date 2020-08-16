---
title: MapGIS 转 ArcGIS ShapeFile 攻略
tags: ["MapGIS"]
key: MapGIS 转 ArcGIS ShapeFile 攻略
---
在处理空间数据时，经常会需要将 MapGIS 格式数据转为 ArcGIS 格式，而在这个过程中可能会遇到属性丢失或者空间坐标系设置的问题。一番百度之后找到了一种个人认为比较好的转换方法，在此记录一下，以便日后查看使用。
<!--more-->
## 1、.WL .WP .WT 转为 .mif 格式
打开MapGIS图形处理->文件转换，导入需要转换的数据文件。
![](\assets\images\MapGIS-to-ArcGIS\to_mif.jpg)
## 2、导入.mif 格式数据
![](\assets\images\MapGIS-to-ArcGIS\load_mif.jpg)
## 3、.mif 转出为 .shp 格式
![](\assets\images\MapGIS-to-ArcGIS\to_shp.jpg)
## 4、定义 .shp 格式文件空间坐标系
在 MapGIS 中查看原始数据的坐标信息，**需要注意原始数据的比例尺和单位**。  
![](\assets\images\MapGIS-to-ArcGIS\coordinate-information.jpg)  
从图中可以看出原始数据的比例尺为 **1:100000**，坐标单位为**毫米**，也就是一个坐标单位代表实际 **100 m**，而ArcGIS中一个坐标单位代表实地 **1 m**。所以，若要转换到 ArcGIS 的正常坐标，需要将目标投影参数的比例尺设为 **100**，这样转换出来的结果才能作为ArcGIS文件正确使用。  
![](\assets\images\MapGIS-to-ArcGIS\define-coordinate.jpg)  
经过上述步骤之后，坐标单位为 **100 m**，后续如果需要转为 1m，可以使用 ArcToolbox 工具箱中的 Project 工具。

如果对您有用的话，别忘了给点个赞哦^_^ ！