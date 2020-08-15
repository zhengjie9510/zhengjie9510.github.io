---
layout: article
title: ArcGIS API for JavaScript之迁徙图（Echarts）
tags: ["ArcGIS API for JavaScript", "Echarts","迁徙图"]
key: ArcGIS API for JavaScript之迁徙图（Echarts）
show_subscribe: false
license: false
---
ArcGIS API for JavaScript集成Echarts实现迁徙图效果的关键问题在于Echarts坐标系与ArcGIS坐标系不一致，需要进行Echarts坐标系与ArcGIS坐标系的转换。  
<!--more-->
## 功能  
ArcGIS API for JavaScript集成Echarts实现迁徙图  
## 工具  
* ArcGIS API for JavaScript 4.15  
* Echarts 4.70  

## 思路
调用 [esri/views/MapView](https://developers.arcgis.com/javascript/latest/api-reference/esri-views-MapView.html) 的 [toScreen()](https://developers.arcgis.com/javascript/latest/api-reference/esri-views-MapView.html#toScreen) 方法将地理坐标转为屏幕坐标，然后通过Echarts可视化。
## 最终效果
![Migration_Map](\assets\images\ArcGIS-API-for-JavaScript-migration-map-Echarts\Demo.gif)  
## 代码下载
[点击这里在线访问Demo](\demo\ArcGIS API for JavaScript Migration Map\index.html)  
点击[这里](https://github.com/zhengjie9510/ArcGIS-API-for-JavaScript)获取完整代码。  
如果对您有用的话，别忘了给点个赞哦^_^ ！
