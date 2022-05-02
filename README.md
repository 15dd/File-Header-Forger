# File-Header-Forger
绕过aliyundrive(阿里云盘)的文件分享限制
## 用途
此工具针对使用aliyundrive时,受到文件分享类型限制进行伪造
## 原理
aliyundrive在分享文件时,会查看文件头(即文件类型),假如检测到压缩文件等受到限制的文件时会无法分享,在对受限制的文件进行伪造文件头后,即可突破限制,正常分享
目前(2022/5/2)经过多次测试,aliyundrive只对文件头进行了限制,没对扩展名做限制
## 缺点
使用麻烦,配置麻烦
## 参考内容:
- https://blog.csdn.net/qq_40657585/article/details/83097386
- https://blog.csdn.net/qq_36171645/article/details/88966127
- https://qa.1r1g.com/sf/ask/3714342551/?lastactivity
- https://www.cnblogs.com/schut/p/8410961.html
- https://blog.51cto.com/u_15052689/2562469
- https://blog.csdn.net/beijingyk/article/details/108581150
---
##### 2022/5/2 19:52 Edited by cyh128

