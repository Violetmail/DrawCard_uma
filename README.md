# DrawCard_uma
基于` PYQT5`实现的[赛马娘抽卡模拟器] 

抽卡模拟连接数据库
# 预览
功能实现
- [x] 单抽+十连的结果图片显示
- [x] 十连保底出现SR
- [x] 重做界面，删除无用的登陆界面
- [x] 可以抽取马娘池，也可以抽取支援卡池子
- [x] 对抽卡结果的统计
- [x] 可以自主选择卡池
- [x] 选择不同卡池出现不同的标志性图片
- [x] 显示公告
- [x] 建立抽卡模拟器的数据库，建立表：卡池表，卡牌表，卡池&卡牌表，抽取结果表
- [x] 连接数据库
- [x] 输出抽卡日志文件draw_log.txt
![image](https://github.com/Violetmail/DrawCard_uma/assets/90465552/f03e8180-b68f-498d-8edb-5ad40c028970)

# 说明
抽卡逻辑为：
- 先得到本次抽卡卡的稀有度
- 在数据库中查询该稀有度的所有卡牌，随机返回一张
- 十连保底，但up的概率并未添加

# 快速开始
 - 安装pyqt5

 ```
 pip install pyqt5
 ```

 - 配置pyqt5 plugins的环境变量

    在环境变量中增加：

    `QT_QPA_PLATFORM_PLUGIN_PATH `

    样例路径（这里填你的PyQt的plugins文件夹位置：

    `C:\Program Files\Python38\Lib\site-packages\PyQt5\Qt\plugins`

- 运行`Start.py`文件


# 注意和解释
- 对于日志中的None，表示的是卡名称查询不到。这是因为卡牌数据库构建的不完备，数据太少，有的品质的卡没有具体写入，修改data文件夹中的数据可以完善。data文件夹就是数据库中构建的三个表，而第四个表--抽卡记录表在程序运行后会以txt格式输出到根目录。

- 如果乱码请自行修改txt文件的编码格式，默认utf-8
