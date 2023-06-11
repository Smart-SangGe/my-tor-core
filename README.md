# xiaomian DNS

本项目是计算机网络的课程设计项目，该项目是一个私有DNS的简单实现。

## 项目原理

在server/xiaomiandns.py中实现了DNSserver和APIserver两个类。通过server/main.py启动实例化的server。配置文件在server/serverconf.yaml  
本项目选择sqlite作为数据库，存储节点信息等数据。

## 环境依赖
该项目依赖以下软件：  
python 3

## 安装步骤
```console
# 安装依赖
pip install -r requirements.txt

#初始化数据库
python3 database/initdb.py
```

## 使用说明
```python
python3 server/main.py
```
dns默认端口为53，域名api默认端口为81
需要添加数据可以通过post方法向API提交数据
usage: use POST method
           /add
           data: domian=xxxx&ip=xx.xx.xx.xx
           /delete
           data: domian=xxxx&ip=xx.xx.xx.xx
注意域名只能以xiaomian作为根域名

# 测试DNS功能：
```console
# Linux
sudo apt install dnsutils
dig @DNS_SERVER -p PORT DOMAIN 

# Windows
nslookup DOMAIN DNS_SERVER
```
# 测试API功能
```console
# Linux
# 添加解析
curl -d "domain=qqqwwweee.xiaomian&ip=123.12.23.34" -X POST http://10.20.117.208:81/add -i

# 删除解析
curl -d "domain=qqqwwweee.xiaomian&ip=123.12.23.34" -X POST http://10.20.117.208:81/delete -i

# Windows
Invoke-WebRequest工具一直收不到post的body，不知道问题出在哪里

## 未实现的功能
目前只能把解析记录作为a记录返回，还未实现添加其他解析记录。

## 许可证

GNU GENERAL PUBLIC LICENSE v3
