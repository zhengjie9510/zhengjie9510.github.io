---
layout: article
title: ArcGIS API for Javascript之GP服务（矢量）
tags: ["ArcGIS API for JavaScript", "GP服务"]
key: ArcGIS API for Javascript之GP服务（矢量）
show_subscribe: false
license: false
---
WebGIS的开发经常会用到一些空间数据的处理与分析功能，而GP服务是实现这些功能的途径之一。下面以缓冲区分析的GP服务为例，详细介绍如何通过ArcGIS API for Javascript调用GP服务。GP服务的发布可参考[ArcGIS Server之发布GP服务-返回矢量数据](https://blog.csdn.net/lovecarpenter/article/details/52496876)  
<!--more-->
## 功能  
鼠标单击地图后在鼠标位置画圆点，并为圆点建立缓冲区。
## 工具  
* ArcGIS API for JavaScript 4.15  
* ArcGIS Server 10.2


## 调用GP服务
### GP服务的相关参数
![GP_Buffer](\assets\images\ArcGIS API for Javascript之GP服务（矢量）\GP服务参数.PNG)
### 主要代码
* 加载地图
```javascript
  require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/GraphicsLayer",
    "esri/Graphic",
    "esri/geometry/Point",
    "esri/tasks/Geoprocessor",
    "esri/tasks/support/LinearUnit",
    "esri/tasks/support/FeatureSet"
  ], function(
    Map,
    MapView,
    GraphicsLayer,
    Graphic,
    Point,
    Geoprocessor,
    LinearUnit,
    FeatureSet
  ) {
    var map = new Map({
      basemap:"streets",
    });

    var view = new MapView({
      container: "viewDiv",
      map: map,
      center: [115.80500, 38.02700],
      zoom: 4
    });
  });
```
* 添加GraphicsLayer图层，用于显示圆点和缓冲区
```javascript
    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);
```
* 设置圆点和缓冲区样式
```javascript
    // 圆点样式
    var markerSymbol = {
      type: "simple-marker", // autocasts as new SimpleMarkerSymbol()
      color: [255, 0, 0],
      outline: {
        // autocasts as new SimpleLineSymbol()
        color: [255, 255, 255],
        width: 2
      }
    };
    // 缓冲区样式
    var fillSymbol = {
      type: "simple-fill", // autocasts as new SimpleFillSymbol()
      color: [226, 119, 40, 0.75],
      outline: {
        // autocasts as new SimpleLineSymbol()
        color: [255, 255, 255],
        width: 1
      }
    };
```
* 添加GP（Buffer）服务
```javascript
    var gpUrl ="http://localhost:6080/arcgis/rest/services/Fuck/GPServer/MyBuffer";
        var gp = new Geoprocessor(gpUrl);
        gp.outSpatialReference = {
        // autocasts as new SpatialReference()
        wkid: 102100
    };
```
* 给View视图绑定单击事件，执行缓冲区分析
```javascript
    view.on("click", Buffer);
    function Buffer(event) {
      graphicsLayer.removeAll();

      var point = new Point({
        longitude: event.mapPoint.longitude,
        latitude: event.mapPoint.latitude
      });

      var inputGraphic = new Graphic({
        geometry: point,
        symbol: markerSymbol
      });

      graphicsLayer.add(inputGraphic);

      var inputGraphicContainer = [];
      inputGraphicContainer.push(inputGraphic);
      var featureSet = new FeatureSet();
      featureSet.features = inputGraphicContainer;

      var vsDistance = new LinearUnit();
      vsDistance.distance = 50;
      vsDistance.units = "Kilometers";

      var params = {
        Features: featureSet,
        Distance: vsDistance
      };

      gp.execute(params).then(drawResultData);
    }

    function drawResultData(result) {
      var resultFeatures = result.results[0].value.features;

      // Assign each resulting graphic a symbol
      var viewshedGraphics = resultFeatures.map(function(feature) {
        feature.symbol = fillSymbol;
        return feature;
      });

      // Add the resulting graphics to the graphics layer
      graphicsLayer.addMany(viewshedGraphics);
      view
        .goTo({
          target: viewshedGraphics,
        })
        .catch(function(error) {
          if (error.name != "AbortError") {
            console.error(error);
          }
        });
    }
```
## 最终效果
![Buffer_结果](\assets\images\ArcGIS API for Javascript之GP服务（矢量）\演示效果.gif)  
## 代码下载
点击[这里](https://github.com/zhengjie9510/ArcGIS-API-for-JavaScript)获取完整代码。  
如果对您有用的话，别忘了给点个赞哦^_^ ！
