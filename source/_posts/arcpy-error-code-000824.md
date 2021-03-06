---
title: Acrpy 之错误代码 000824
date: 2020-7-16 12:00:00
tags: ["Arcpy"]
categories: Python
---
今天在利用Arcpy处理数据时出现 000824 错误，通过查找资料了解到这是由于扩展模块工具默认不可用，需要加载扩展模块。  
<!--more-->

## 1、错误代码
![错误提示](/assets/image/acrpy-error-code-000824/error-code-000824.jpg)  
## 2、解决办法
通过CheckExtension函数引用模块。
```python
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("[扩展编码]")
```
扩展模块及对应的扩展编码如下：  

| 扩展模块 | 扩展编码
|-|:-:
| ArcGIS 3D Analyst | 3D
| ArcGIS Data Interoperability 10.5.1 for Desktop | DataInteroperability
| ArcGIS Data Reviewer for Desktop | Datareviewer
| ArcGIS for Aviation：Airports | Airports
| ArcGIS for Aviation：Charting | Aeronautical
| ArcGIS for Maritime:Bathymetry | Bathymetry
| ArcGIS for Maritime:Charting | Nautical
| ArcGIS Geostatistical Analyst | GeoStats
| ArcGIS Network Analyst | Network
| ArcGIS Spatial Analyst | Spatial
| ArcGIS Schematics | Schematics
| ArcGIS Tracking Analyst | racking
| ArcGIS Workflow Manager for Desktop | JTX
| ArcScan | ArcScan
| Business Analyst | Business
| Esri Defense Mapping | Defense
| Esri Production Mapping | Foundation
| Esri Roads and Highways | Highways
| StreetMap | StreetMap

## 3、参考链接
[Arcpy：Error 000824 The tool is not licensed 解决方式](https://blog.xiewei.link/index.php/archives/304/)  
如果对您有用的话，别忘了给点个赞哦^_^ ！