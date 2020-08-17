---
title: Pyhton 之多线程并行计算
tags: ["Python"]
key: Pyhton 之多线程并行计算
---
Python 中多线程是假的多线程，受 GIL 影响，一次只能运行一个线程，因此只适用于 IO 密集型，不适合 CPU 密集型。

<!--more-->
# 1、Python 中多线程的实现方式
```python
import threading
import time
```
## 1.1、by passing a callable object to the constructor
```python
def do_job(data):
    for i in range(len(data)):
        data[i]=data[i]**2
    time.sleep(2)
    print(data)

if __name__ == '__main__':
    datas=[[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    start_time=time.time()
    print('Start multi-threaded operation')
    threads=[]
    for i in range(4):
        t=threading.Thread(target=do_job,args=[datas[i]])
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end_time=time.time()
    print('End multi-threaded operation')
    print('多线程用时{0}'.format(end_time-start_time))
    print()
    datas=[[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    print('开始普通运算')
    start_time=time.time()
    for data in datas:
        do_job(data)
    end_time=time.time()
    print('结束普通运算')
    print('普通运算用时{0}'.format(end_time-start_time))
```
输出：  
Start multi-threaded operation  
[1, 1, 1]  
[9, 9, 9]  
[4, 4, 4]  
[16, 16, 16]  
End multi-threaded operation  
多线程用时2.0247037410736084  

开始普通运算  
[1, 1, 1]  
[4, 4, 4]  
[9, 9, 9]  
[16, 16, 16]  
结束普通运算  
普通运算用时8.038983821868896  
## 1.2、by overriding the run() method in a subclass
```python
class do_job_class(threading.Thread):
    def __init__(self,data):
        threading.Thread.__init__(self) 
        self.data=data
    def run(self):
        for i in range(len(self.data)):
            self.data[i]=self.data[i]**2
        time.sleep(2)
        print(self.data)
        
if __name__ == '__main__':
    datas=[[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    start_time=time.time()
    print('Start multi-threaded operation')
    jobs=[]
    for i in range(4):
        jobs.append(do_job_class(datas[i]))
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    end_time=time.time()
    print('End multi-threaded operation')
    print('多线程用时{0}'.format(end_time-start_time))
    print()
    
    datas=[[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    print('开始普通运算')
    start_time=time.time()
    for data in datas:
        do_job(data)
    end_time=time.time()
    print('结束普通运算')
    print('普通运算用时{0}'.format(end_time-start_time))
```
输出：  
Start multi-threaded operation  
[16, 16, 16]  
[4, 4, 4]  
[1, 1, 1]  
[9, 9, 9]  
End multi-threaded operation  
多线程用时2.02193546295166  

开始普通运算  
[1, 1, 1]  
[4, 4, 4]  
[9, 9, 9]  
[16, 16, 16]  
结束普通运算  
普通运算用时8.030825138092041  
# 2、多任务分配，并行运算
## 2.1、通过求余数的方法将任务分配到各线程
```python
class do_job_class(threading.Thread):
    def __init__(self,index,count,datas,results):
        threading.Thread.__init__(self)
        self.index=index
        self.count=count
        self.datas=datas
    def run(self):
        for i, data in enumerate(self.datas):
            if i%self.count!=self.index:       # 通过求余数的方法分配任务到各线程
                continue
            for j in range(len(data)):
                data[j]=data[j]**2
            print(data)
            results[i]=data
            time.sleep(2)

if __name__ == '__main__':
    datas=[[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5]]
    start_time=time.time()
    print('Start multi-threaded operation')
    results=[None]*len(datas)
    thread_number=5 # 线程数量
    jobs=[do_job_class(i,thread_number,datas,results) for i in range(thread_number)]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    end_time=time.time()
    print('End multi-threaded operation')
    print('多线程用时{0}'.format(end_time-start_time))
```
输出：  
Start multi-threaded operation  
[1, 1, 1]  
[4, 4, 4]  
[9, 9, 9]  
[16, 16, 16]  
[25, 25, 25]  
End multi-threaded operation  
多线程用时2.0182318687438965  
# 3、多线程返回值
## 3.1、通过引用类型获取返回值
```python
def do_job(data):
    for i in range(len(data)):
        data[i]=data[i]**2
    time.sleep(2)
    print(data)
    print('after id: {0}'.format(id(data)))

if __name__ == '__main__':
    datas=[[2,2,2]]
    threads=[]
    for i in range(len(datas)):
        print(datas[i])
        print('before id: {0}'.format(id(datas[i])))
        t=threading.Thread(target=do_job,args=[datas[i]])
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
```
输出：  
[2, 2, 2]  
before id: 2665418657224  
[4, 4, 4]  
after id: 2665418657224  
**可以发现数据内存地址是一样的，也就是说修改的多线程外的值**
