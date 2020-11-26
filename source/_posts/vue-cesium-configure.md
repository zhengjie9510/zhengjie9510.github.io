---
title: Vue 集成 Cesium
date: 2020-11-26 23:00:00
tags: ["Vue","Cesium"]
categories: Javascript
---
好记性不如烂笔头，对于一个刚接触 Vue、Cesium 的菜鸟来说，Vue + Cesium 集成之路可以说是历经艰辛，因此特意记录一下 Vue + Cesium 的配置过程，以便日后查看。
<!--more-->
## 1、Vue Cli 3.0+
### 1.1、安装
```
# 全局安装vue-cli 3.x版本
npm install -g @vue/cli

# 创建 vue-cesium 项目
vue create vue-cesium

# 创建好一个 vue-cesium 项目后，在项目了安装插件
vue add vue-cli-plugin-cesium
```
### 1.2、使用
开发时如下，直接在模块中使用 Cesium 对象即可
```javascript
<template>
  <div class="map-box">
    <div id="cesiumContainer"></div>
  </div>
</template>

<script>
// 文件 node_modules\vue-cli-plugin-cesium\index.js 中已经引入 Cesium，因此无需再次 import
// 也可注释之后通过 require 引用
// var Cesium = require('cesium/Cesium');//To require all of CesiumJS
// 也可以通过 import 引用
// import {Viewer} from 'cesium/Cesium';//这里有坑，不能 import Cesium
export default {
  name: "",
  mounted() {
    // eslint-disable-next-line no-undef
    var viewer = new Cesium.Viewer("cesiumContainer");

    // eslint-disable-next-line no-console
    console.log(viewer);
  },
};
</script> 
<style scoped>
.map-box {
  width: 100%;
  height: 100%;
}
#cesiumContainer {
  width: 100%;
  height: 100%;
}
</style>
```
## 2、Vue Cli 2.X
### 2.1、安装

如果对您有用的话，别忘了给点个赞哦^_^ ！