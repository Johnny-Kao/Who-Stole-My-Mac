# 谁偷走我的MAC

## 功能概要

当电脑连接上陌生WIFI时，会定时调用前置摄像头拍照/截屏/记录当前连接WIFI/采集附近的WIFI资讯，采集后发送记录到指定的邮箱。

当连接上常用的WIFI时，会定时记录当前连接WIFI/采集附近的WIFI资讯，定时发送到指定邮箱。

## 系统要求

* Mac OS 10.11.X Above
* Python 3.7.x Above

## 依赖套件

* imagesnap - 截取前置摄像头照片
* whereami - 取得电脑当前GPS位置
* zip - 压缩档案（MAC内建）

## 使用方式

1. 复制专案到本地
`git clone https://github.com/Johnny-Kao/Who-Stole-My-Mac.git`

2. 确认依赖套件安装

	* imagesnap安装
	
	`brew install imagesnap`
	
	* whereami安装 - 放到任意资料夹，双击即可，首次运行需要授权
	* zip安装 - 确认是否安装
	
	`zip -help`

2. 设定**mac location check.py**参数

* Step 1.
	* 修改常用WIFI清单
	* 修改LOG路径名称
	* 设定执行频率
	* 设定发送邮件的服务器、账号、密码

* Step 2.
	* 设定whereami程序路径

* Step 3.
	* 设定发送邮件资讯 - send_mail(To Email, Title, Context, From Email, Attachment Path, Attachment File Name)

* Step 4. 添加定时执行
	* 检查Python3 绝对路径
	
	```
	which python3
	> /usr/local/bin/python3
	```
	* 新增定时排程
	
	```
	crontab -e
	> */15 * * * * /usr/local/bin/python3 PATH/mac_location_check.py.py >> /PATH/log.log 2>&1
	```
	[Crontab语法生成](https://crontab-generator.org)
	
## To DO List

* 自动安装
* 发送到服务器
* 隐藏程序运行
* GPS套件调用内部程序

## 后记

本脚本在编写上虽然使用了Python，但是大部分还是调用了Bash的语法执行，这样的写法大幅度的降低了Mac系统对于调用这些方式的安全限制，同时也降低了Python调用外部套件可能造成的错误，毕竟还是原生内建的最好。

