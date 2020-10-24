---
title: ArcGIS API for Javascript之摄影地图
tags: ["ArcGIS API for JavaScript", "要素图层","图层渲染"]
key: ArcGIS API for Javascript之摄影地图
---
以前有想过将拍摄的照片根据其拍摄地点显示在地图上，刚好最近在学习ArcGIS API for Javascript，于是就考虑使用ArcGIS API for Javascript实现这样的功能。  
<!--more-->
## 目的
通过url访问照片，读取坐标创建要素图层，并以照片缩影为图标，在弹出窗口中展示大图。
## 工具  
* ArcGIS API for JavaScript 4.15  
* 可以通过url访问的带有地理信息的照片

## 主要步骤
### 加载底图
略
### 获取Promise列表
如果执行正常，返回的Promise中含有一个Graphic（带有照片的坐标和url）
```javascript
function exifToGraphic(url, id) {
    // 疑问：promiseUtils或者promise的用法？
    return promiseUtils.create(function(resolve, reject) {
        const image = document.createElement("img");
        image.src = url;
        image.onload = function() {
            image.load = image.onerror = null;
            EXIF.getData(image, function() {
                const latitude = EXIF.getTag(this, "GPSLatitude");
                const latitudeDirection = EXIF.getTag(this, "GPSLatitudeRef");
                const longitude = EXIF.getTag(this, "GPSLongitude");
                const longitudeDirection = EXIF.getTag(this, "GPSLongitudeRef");

                if (!latitude || !longitude) {
                    reject(
                        new Error(
                            "Photo doesn't contain GPS information: ",
                            this.src
                        )
                    );
                    return;
                }

                const location = new Point({
                    latitude: dmsDD(latitude, latitudeDirection),
                    longitude: dmsDD(longitude, longitudeDirection)
                });

                // 执行正常，返回照片的坐标和url
                resolve(
                    new Graphic({
                        geometry: location,
                        attributes: {
                            url: url,
                            OBJECTID: id
                        }
                    })
                );
            });
        };

        image.onerror = function() {
            image.load = image.onerror = null;
            reject(new Error("Error while loading the image"));
        };
    });
}
```
### 返回Promise中的坐标信息
过滤掉含无效值的Promise，并返回Promise中的value(Graphics)
```javascript
function getFeaturesFromPromises(eachAlwaysResponses) {
    return eachAlwaysResponses
        .filter(function(graphicPromise) {
            return graphicPromise.value;
    })
        .map(function(graphicPromise) {
            return graphicPromise.value;
    });
}
```
### 创建图层并渲染
根据上一步返回的Graphics建立FeatureLayer，以照片略缩进行渲染，并在popup中显示大图。
```javascript
function createLayer(graphics) {
    return new FeatureLayer({
        source: graphics,
        objectIdField: "OBJECTID",
        fields: [
            {
                name: "OBJECTID",
                type: "oid"
            },
            {
                name: "url",
                type: "string"
            }
        ],
        popupTemplate: {
            title: function(event) {
                return locatorTask
                .locationToAddress({
                    location: event.graphic.geometry
                })
                .then(function(response) {
                    return response.address;
                })
                .catch(function(error) {
                    return "The middle of nowhere";
                });
            },
            content: "<img src='{url}'>"
        },
        renderer: {
            type: "unique-value",
            field: "url",
            uniqueValueInfos: createMarkerSymbol(graphics)
        }
    });
}

function createMarkerSymbol(graphics) {
    var symbles = [];
    for (i = 0; i < graphics.length; i++) {
        symbles.push({
            value: graphics[i].attributes.url,
            symbol: {
                type: "picture-marker",
                url: graphics[i].attributes.url,
                width: "35px",
                height: "25px"
            },
        });
    };
    return symbles;
}
```
## 最终效果
![演示效果](\assets\images\ArcGIS-API-for-Javascript-photography-map\Demo.gif)
## 代码下载
[点击这里在线访问Demo](\demo\arcgis_api_for_javascript_photographic_map\index.html)  
[点击这里获取完整代码](https://github.com/zhengjie9510/ArcGIS-API-for-JavaScript)  
如果对您有用的话，别忘了给点个赞哦^_^ ！