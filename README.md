# Smweb
This is a Operations management system

#架构
系统采用tornado + mysql + salt + bootstrap +jquery开发


#依赖
python >= 2.6
salt
tornado
torndb

#功能
1、自动上线
主要采用linux的rsync+salt来实现自动分发及服务重启。
2、资产管理
资产管理分为：
服务器信息展示
机柜展示
域名展示
网络设备展示
运维其它信息展示
3、监控功能
监控主要使用zabbix api来开发整合。
4、saltcmd
主要包括单机命令，服务管理，日志查看等功能。


#备注：
当前开发中。。。
