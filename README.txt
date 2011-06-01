此程序用来备份tweets，根据所提供的screen name，将此用户所有的 推 导出成一个完整的html文件。
使用过程只需提供screen name，不需要密码和任何其它信息。

支持平台：
  Windows/Linux/Mac + Python 2.6

可更改配置的地方：
1. 备份tweets缺省以顺序排列，即前最早的一条tweet在文件的最上面；若需要以倒序排列，即最新的更新排在最前面，请将第99行 oldestfirst 字段的值修改为 “no”
2. 第96行 pagesize 字段，指每次调用API获取消息的数量，缺省为200条，不建议修改，除非网络非常糟糕，可将此值适当改小。

另外：Twitter官方的限制，所有用户只能获取到最近的3200条推，早于3200条的推目前阶段无法备份；匿名用户每小时调用API次数限制为150次，请勿短时间内对大量用户做备份操作。

Project Home: http://pagebrin.com/projects/backup-tweets

