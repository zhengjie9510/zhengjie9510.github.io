---
title: Pyhton 之读取照片拍摄经纬度
tags: ["Python"]
key: Pyhton 之读取照片拍摄经纬度
---
Python 读取照片的经纬度和时间信息需要 ExifRead 模块。
<!--more-->
```python
# -*- coding: utf-8 -*
import exifread

def readPhotoInfo(photo):
    '''
    photo : the file path of the photo
    return the taken date, Lat and Lon
    '''
    # Open image file for reading (binary mode)
    f = open(photo,'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        #拍摄时间
        DateTaken=tags["EXIF DateTimeOriginal"].printable
        #纬度
        LatRef=tags["GPS GPSLatitudeRef"].printable
        Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
        if LatRef != "N":
            Lat=Lat*(-1)
        #经度
        LonRef=tags["GPS GPSLongitudeRef"].printable
        Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
        if LonRef!="E":
            Lon=Lon*(-1)
        f.close()
    except:
        return "Error : Make sure the photo contains EXIF information such as latitude and longitude."
    else:
        return DateTaken,Lat,Lon
```