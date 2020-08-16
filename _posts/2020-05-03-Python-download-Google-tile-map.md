---
title: Python之谷歌瓦片地图影像批量下载
tags: ["Python", "Google Map"]
key: Python之谷歌瓦片地图影像批量下载
---
最近在写毕业论文，想用谷歌影像作为底图来展示研究区，然后Google了很多脚本，结果发现输出的影像都不带空间坐标系，所以就想自己写个小工具，通过输入空间范围就可以实现Google地图的下载，并输出为**TIFF**格式，含**WGS 84**空间坐标系。
<!--more-->
## 拟解决问题
下载谷歌影像，并输出为带空间坐标系的TIFF格式
## 简单说明
通过多线程、多进程的方式实现快速下载  
下面只给出主要的思路及代码  
您也可以点击[这里](https://github.com/zhengjie9510/Google-Map-Downloader)获取完整的代码   
如果对您有用的话，别忘了给点个赞哦^_^ ！
## 主要思路及代码
### 计算给定空间范围内的瓦片行列号，并返回URL
```python
MAP_URLS = {
    "Google": "http://mts0.googleapis.com/vt?lyrs={style}&x={x}&y={y}&z={z}",
    "Google China": "http://mt2.google.cn/vt/lyrs={style}&hl=zh-CN&gl=CN&src=app&x={x}&y={y}&z={z}"}    

def get_url(source, x, y, z, style):#
    if source == 'Google China':
        url = MAP_URLS["Google China"].format(x=x, y=y, z=z, style=style)
    elif source == 'Google':
        url = MAP_URLS["Google"].format(x=x, y=y, z=z, style=style)
    else:
        raise Exception("Unknown Map Source ! ")
    return url
    
def get_urls(x1, y1, x2, y2, z, source='google', style='s'):
    pos1x, pos1y = wgs_to_tile(x1, y1, z)
    pos2x, pos2y = wgs_to_tile(x2, y2, z)
    lenx = pos2x - pos1x + 1
    leny = pos2y - pos1y + 1
    print("Total tiles number：{x} X {y}".format(x=lenx, y=leny))
    urls = [get_url(source, i, j, z, style) for j in range(pos1y, pos1y + leny) for i in range(pos1x, pos1x + lenx)]
    return urls
```
### 根据上一步得到的URL下载瓦片
```python
def download_tiles(urls,multi=10):
    def makeupdate(s):
        def up():
            global COUNT
            COUNT+=1
            print("\rDownLoading...[{0}/{1}]".format(COUNT,s),end='')
        return up

    url_len=len(urls)
    datas=[None] * url_len
    if multi <1 or multi >20 or not isinstance(multi,int):
        raise Exception("multi of Downloader shuold be int and between 1 to 20.")
    tasks=[Downloader(i,multi,urls,datas,makeupdate(url_len)) for i in range(multi)]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
    return datas
```
### 合并瓦片为一张影像
```python
def merge_tiles(datas,x1, y1, x2, y2, z):
    pos1x, pos1y = wgs_to_tile(x1, y1, z)
    pos2x, pos2y = wgs_to_tile(x2, y2, z)
    lenx = pos2x - pos1x + 1
    leny = pos2y - pos1y + 1
    outpic = pil.new('RGBA', (lenx * 256, leny * 256))
    for i, data in enumerate(datas):
        picio = io.BytesIO(data)
        small_pic = pil.open(picio)

        y, x = i // lenx, i % lenx
        outpic.paste(small_pic, (x * 256, y * 256))
    print('\nTiles merge completed')
    return outpic
```
### 计算所下载瓦片的实际空间范围（我们需要的是瓦片边缘的经纬度信息）
```python
def getExtent(x1, y1, x2, y2, z,source="Google China"):
    pos1x, pos1y = wgs_to_tile(x1, y1, z)
    pos2x, pos2y = wgs_to_tile(x2, y2, z)
    Xframe=pixls_to_mercator({"LT":(pos1x,pos1y),"RT":(pos2x,pos1y),"LB":(pos1x,pos2y),"RB":(pos2x,pos2y),"z":z})
    for i in ["LT","LB","RT","RB"]:
        Xframe[i]=mercator_to_wgs(*Xframe[i])
    if source=="Google":
        pass
    elif source=="Google China":
            for i in ["LT","LB","RT","RB"]:
                Xframe[i]=gcj_to_wgs(*Xframe[i])
    else:
        raise Exception("Invalid argument: source.") 
    return Xframe
```
### 最后将结果输出为TIFF格式
```python
def saveTiff(r,g,b,gt,filePath):
    fname_out   = filePath
    driver      = gdal.GetDriverByName('GTiff')
    # Create a 3-band dataset
    dset_output = driver.Create(fname_out, r.shape[1], r.shape[0], 3, gdal.GDT_UInt16)
    dset_output.SetGeoTransform(gt)
    try:
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        dset_output.SetSpatialRef(proj)
    except:
        print("Error: Coordinate system setting failed")
    dset_output.GetRasterBand(1).WriteArray(r)
    dset_output.GetRasterBand(2).WriteArray(g)
    dset_output.GetRasterBand(3).WriteArray(b)
    dset_output.FlushCache()
    dset_output = None
    print("Image Saved")
```
完成！