# JDXiaoLongXiaSeleniumSpider


备注：
* 本项目演示了使用Selenium + Chrome 抓取京东全国小龙虾店铺相关数据信息
* 演示了Flask_SQLALCHEMY工具将数据保存到本地MySQL数据库中

## 安装

### 安装Python3.7.2以上版本

### 安装MySQL数据库
安装好之后开启MySQL数据库

###安装三方依赖库

```
pip3 install -r requirements.txt
```

## 配置 AdministrativeRegionCodeSpider
### 打开 models.py 配置mysql数据库连接
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://数据库用户名:数据库连接密码@数据库所在宿主机ip:3306/数据库名称'
e.g.
 SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qcl123@127.0.0.1:3306/xiao_long_xia'
 
```
### 手动创建数据库
```
mysql -u数据库用户名 -p数据库连接密码

mysql> create database xiao_long_xia default charset="utf8";

```
### 创建迁移仓库
#### 这个命令会创建migrations文件夹，所有迁移文件都放在里面。
```
cd spiders
python models.py db init
```
### 创建迁移脚本
#### 创建自动迁移脚本
```
cd spiders
python models.py db migrate -m 'initial migration'
```

### 更新数据库
```
cd spiders
python models.py db upgrade
```

## 启动程序
```
cd JDXiaoLongXiaSeleniumSpider
python start.py