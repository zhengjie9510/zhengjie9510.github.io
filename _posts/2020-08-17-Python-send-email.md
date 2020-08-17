---
title: Pyhton 之发送电子邮件
tags: ["Python"]
key: Pyhton 之发送电子邮件
---
在进行大量的数据处理时人不会一直等在电脑前，但如果又想知道程序什么时候运行完成以及是否出错，则可以利用 Python smtplib 模块来发送电子邮件告知程序运行情况。
<!--more-->
```python
# -*- coding: utf-8 -*
'''
This code is used to send email

@author: Zheng Jie
@E-mail:1096318621@qq.com
'''
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

class Email(object):
    def __init__(self,account,password):
        self.account = account
        self.password = password

class Hotmail(Email):
    def __init__(self, account, password):
        super().__init__(account, password)

    def send(self,to_addrs,content,subject=None):
        msg=EmailMessage()
        # msg['From']=formataddr(['your name',self.account])
        msg['From']=self.account
        msg['To']=to_addrs
        msg['Subject']=subject
        msg.set_content(content)

        server=smtplib.SMTP(host='smtp-mail.outlook.com',port=587)
        try:
            server.ehlo()
            server.starttls()
            server.login(self.account,self.password)
            server.send_message(msg)
            print('Mail send successfully')
        except:
            print('Mail send failed')
        finally:
            server.quit()

if __name__ == "__main__":
    hotmail=Hotmail("hotmail account",'password')
    hotmail.send('to_addrs','your content','your subject')
```