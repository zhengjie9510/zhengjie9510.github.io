---
layout: article
title: Python之遍历文件夹及其子文件夹中所有文件
tags: ["Python"]
key: Python之遍历文件夹及其子文件夹中所有文件
show_subscribe: false
license: false
---
使用os.walk()函数遍历文件夹及其子文件夹中的所有文件或文件夹。  
<!--more-->
直接进入正题
## 代码
### OsWalk类
```python
import os

class OsWalk(object):
    def __init__(self,folder_path=None):
        super().__init__()
        self._folder_path=folder_path
    
    # 文件夹及其子文件夹中的所有文件
    def file_list(self):
        file_list=[]
        for root,dirs,files in os.walk(self._folder_path):
            for name in files:
                file_list.append(os.path.join(root, name))
        return file_list
    
    # 文件夹及其子文件夹中的所有文件夹
    def folder_list(self):
        folder_list=[]
        for root,dirs,files in os.walk(self._folder_path):
            for name in dirs:
                folder_list.append(os.path.join(root, name))
        return folder_list
```
### 调用方法
```python
if __name__ == "__main__":
    folder_path=r'D:\Music\iTunes\iTunes Media\Apple Music'
    # 输出文件夹及其子文件夹中的所有文件
    for item in OsWalk(folder_path).file_list():
        print(item)
```
\Apple Music\Anson Seabra\Can You Feel the Love Tonight - Single\01 Can You Feel the Love Tonight.m4p  
\Apple Music\Beyond\Words & Music Final Live Gold\08 Sky (Introduced by Beyond) [Live].m4p  
\Apple Music\Coldplay\A Head Full of Dreams\04 Everglow.m4p  
\Apple Music\Compilations\25\19 Take Me To Your Heart.m4p  
\Apple Music\Compilations\25\24 Silent Times.m4p  
\Apple Music\Compilations\America, Vol. 10_ Country - The Folk Rev\2-19 Five Hundred Miles.m4p  
```python
if __name__ == "__main__":
    folder_path=r'D:\Music\iTunes\iTunes Media\Apple Music'
    # 输出文件夹及其子文件夹中的所有文件夹
    for item in OsWalk(folder_path).folder_list():
        print(item)
```
\Apple Music\Anson Seabra  
\Apple Music\Beyond  
\Apple Music\Coldplay  
\Apple Music\Compilations  
\Apple Music\Eason Chan  
\Apple Music\Fish Leong  
如果对您有用的话，别忘了给点个赞哦^_^ ！