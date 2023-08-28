import sys
import random
import os
#PyQt5中使用的基本控件
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5.QtGui import QPixmap

#导入designer界面
from Ui_抽卡系统 import*
import conn2sql
class MyMainForm(QMainWindow, Ui_Form): 
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #提供标题
        self.setWindowTitle("抽卡模拟器")
        #添加信号和槽。      
        self.change_cardpool.clicked.connect(self.change_pool)
        self.change_cardpool_2.clicked.connect(self.change_pool_2)
        self.getone.clicked.connect(self.one)
        self.getten.clicked.connect(self.ten)
        self.getone_2.clicked.connect(self.one_2)
        self.getten_2.clicked.connect(self.ten_2)
        self.askbutton.clicked.connect(self.ask)

        # 加载并显示默认图片
        image_path = "res/2.5th Anniversary卡池.png" #默认出现的图片
        self.load_image(image_path)
        image_path = "res/2.5th Anniversary支援卡池.png" #默认出现的图片
        self.load_image_2(image_path)

        #连接数据库
        db_name = "card_database.db"
        #未创建数据库则创建
        if os.path.exists(db_name):
             pass
        else:
             conn2sql.create_database_from_sql("data/draw_card.sql",db_name)
             conn2sql.insert_cardpool("data/cardpool.txt",db_name)
             conn2sql.insert_card("data/card.txt",db_name)
             conn2sql.insert_pool_card("data/pool&card.txt",db_name)

#################### 加载图片，参数设置一个图片的路径


    #马池图
    def load_image(self,image_path): 
        pixmap = QPixmap(image_path) #变为Qpixmap对象
        # 调整 QLabel 大小以适应图片
        self.view_pool.setPixmap(pixmap)
        self.view_pool.setScaledContents(True)
    #支援卡池图
    def load_image_2(self,image_path):
        pixmap_2 = QPixmap(image_path) #变为Qpixmap对象
        # 调整 QLabel 大小以适应图片
        self.view_pool_2.setPixmap(pixmap_2)
        self.view_pool_2.setScaledContents(True)    

    #定义改变卡池的函数
    def change_pool(self):
        cardpool_name=self.cardpool_Box.currentText() #读取卡池信息  
        self.label_cardpool.setText(cardpool_name)
        image_path = "res/"+cardpool_name+".png" 
        self.load_image(image_path)

    def change_pool_2(self):
        cardpool_name=self.cardpool_Box_2.currentText() #读取卡池信息  
        self.label_cardpool_2.setText(cardpool_name)  
        image_path = "res/"+cardpool_name+".png" 
        self.load_image_2(image_path)  

####################### 马池
    def one(self):
         #清空十连的显示结果
        self.labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5,
                       self.label_6, self.label_7, self.label_8, self.label_9, self.label_10] #将标签存放为标签数组
        for label in self.labels:
            label.clear()
        #获取控件数据
        getnum=int(self.value_getnum.text())
        ssrnum=int(self.value_ssrnum.text())
        srnum=int(self.value_srnum.text())
        rnum=int(self.value_rnum.text())
        poolname=self.cardpool_Box.currentText()
        db_name = "card_database.db"


         # 定义不同星级卡的概率
        star_probabilities = {
            "R": 0.79,
            "SR": 0.18,
            "SSR": 0.03
        }
        # 根据概率随机抽取星级
        star = random.choices(list(star_probabilities.keys()), weights=list(star_probabilities.values()), k=1)[0]
        #得到抽卡结果
        cardname=conn2sql.get_cardname(pool_name=poolname,star=star,db_name=db_name)
        conn2sql.insert_draw_log(db_name,poolname,cardname) #存入抽卡记录的数据库
        #显示抽卡结果
        image_path = "res/"+star+".png"  # 替换为你的图片路径
        pixmap = QPixmap(image_path) #变为Qpixmap对象
        # 调整 QLabel 大小以适应图片
        self.label_11.setPixmap(pixmap)
        self.label_11.setScaledContents(True)

        #更新统计数据
        getnum=getnum+1
        self.value_getnum.setText(str(getnum))
        if (star=="R"):
            rnum=rnum+1
            self.value_rnum.setText(str(rnum))
        elif(star=="SR"):
            srnum=srnum+1
            self.value_srnum.setText(str(srnum))
        elif(star=="SSR"):
            ssrnum=ssrnum+1
            self.value_ssrnum.setText(str(ssrnum))
        
        self.value_Pssr.setText(str(round(ssrnum*100/(getnum),2))+"%")

        #输出日志文件
        table_name="draw_log"
        txt_file="draw_log.txt"
        conn2sql.export_table_to_txt(table_name,db_name,txt_file) #抽卡记录表导出为txt

    def ten(self):
        #单抽结果置为空
        self.label_11.clear()
        #获取控件数据
        getnum=int(self.value_getnum.text())
        ssrnum=int(self.value_ssrnum.text())
        srnum=int(self.value_srnum.text())
        rnum=int(self.value_rnum.text())
        poolname=self.cardpool_Box.currentText()
        db_name = "card_database.db"

         # 定义不同星级卡的概率
        star_probabilities = {
            "R": 0.79,
            "SR": 0.18,
            "SSR": 0.03
        }
         # 确保至少出现一张SR卡,具体实现为没有SR卡就循环重抽
        while True:
            cards_star = []
            for _ in range(10):
                rand_num = random.random()  # 生成0到1之间的随机数
                card_type = None
                # 根据随机数和概率判断抽到的卡牌类型
                if rand_num < star_probabilities['SSR']:
                    card_type = 'SSR'
                elif rand_num < star_probabilities['SSR'] + star_probabilities['SR']:
                    card_type = 'SR'
                else:
                    card_type = 'R'
                
                cards_star.append(card_type)
            
            if 'SR' in cards_star:
                #得到抽卡结果
                for i in range(10):
                    cardname=conn2sql.get_cardname(pool_name=poolname,star=cards_star[i],db_name=db_name)
                    conn2sql.insert_draw_log(db_name,poolname,cardname) #存入抽卡记录的数据库
                break 
            
             
        #将十张卡内容展现出来，并计算抽卡结果的计数
        self.labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5,
                       self.label_6, self.label_7, self.label_8, self.label_9, self.label_10] #将标签存放为标签数组
        for label in self.labels:
            i=self.labels.index(label)
            image_path = "res/"+str(cards_star[i])+".png"  # 替换为你的图片路径
            pixmap = QPixmap(image_path) #变为Qpixmap对象
            # 调整 QLabel 大小以适应图片
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            #同时更新计数器
            if (cards_star[i]=="R"):
                rnum=rnum+1               
            elif(cards_star[i]=="SR"):
                srnum=srnum+1      
            elif(cards_star[i]=="SSR"):
                ssrnum=ssrnum+1

        #更新统计数据
        getnum=getnum+10
        self.value_getnum.setText(str(getnum))
        self.value_rnum.setText(str(rnum))
        self.value_srnum.setText(str(srnum))
        self.value_ssrnum.setText(str(ssrnum))
        self.value_Pssr.setText(str(round(ssrnum*100/(getnum),2))+"%")

        #输出日志文件
        table_name="draw_log"
        txt_file="draw_log.txt"
        conn2sql.export_table_to_txt(table_name,db_name,txt_file) #抽卡记录表导出为txt

################# 支援卡池（上两个函数的复制，就是改变了标签名字，xxx->xxx_2）
    def one_2(self):
         #清空十连的显示结果
        self.labels = [self.label_12, self.label_13, self.label_14, self.label_15,
                       self.label_16, self.label_17, self.label_18, self.label_19, self.label_20, self.label_21] #将标签存放为标签数组
        for label in self.labels:
            label.clear()
        #获取控件数据
        getnum=int(self.value_getnum_3.text())
        ssrnum=int(self.value_ssrnum_3.text())
        srnum=int(self.value_srnum_2.text())
        rnum=int(self.value_rnum_3.text())
        poolname=self.cardpool_Box_2.currentText()
        db_name = "card_database.db"
         # 定义不同星级卡的概率
        star_probabilities = {
            "R": 0.79,
            "SR": 0.18,
            "SSR": 0.03
        }
        # 根据概率随机抽取星级
        star = random.choices(list(star_probabilities.keys()), weights=list(star_probabilities.values()), k=1)[0]
        #得到抽卡结果
        cardname=conn2sql.get_cardname(pool_name=poolname,star=star,db_name=db_name)
        conn2sql.insert_draw_log(db_name,poolname,cardname) #存入抽卡记录的数据库

        #显示抽卡结果
        image_path = "res/"+star+".png"  # 替换为你的图片路径
        pixmap = QPixmap(image_path) #变为Qpixmap对象
        # 调整 QLabel 大小以适应图片
        self.label_22.setPixmap(pixmap)
        self.label_22.setScaledContents(True)

        #更新统计数据
        getnum=getnum+1
        self.value_getnum_3.setText(str(getnum))
        if (star=="R"):
            rnum=rnum+1
            self.value_rnum_3.setText(str(rnum))
        elif(star=="SR"):
            srnum=srnum+1
            self.value_srnum_2.setText(str(srnum))
        elif(star=="SSR"):
            ssrnum=ssrnum+1
            self.value_ssrnum_3.setText(str(ssrnum))
        
        self.value_Pssr_3.setText(str(round(ssrnum*100/(getnum),2))+"%")  

        #输出日志文件
        table_name="draw_log"
        txt_file="draw_log.txt"
        conn2sql.export_table_to_txt(table_name,db_name,txt_file) #抽卡记录表导出为txt       


    def ten_2(self):
        #单抽结果置为空
        self.label_22.clear()
        #获取控件数据
        getnum=int(self.value_getnum_3.text())
        ssrnum=int(self.value_ssrnum_3.text())
        srnum=int(self.value_srnum_2.text())
        rnum=int(self.value_rnum_3.text())
        poolname=self.cardpool_Box_2.currentText()
        db_name = "card_database.db"

         # 定义不同星级卡的概率
        star_probabilities = {
            "R": 0.79,
            "SR": 0.18,
            "SSR": 0.03
        }
         # 确保至少出现一张SR卡,具体实现为没有SR卡就循环重抽
        while True:
            cards_star = []
            for _ in range(10):
                rand_num = random.random()  # 生成0到1之间的随机数
                card_type = None
                # 根据随机数和概率判断抽到的卡牌类型
                if rand_num < star_probabilities['SSR']:
                    card_type = 'SSR'
                elif rand_num < star_probabilities['SSR'] + star_probabilities['SR']:
                    card_type = 'SR'
                else:
                    card_type = 'R'
                
                cards_star.append(card_type)
            
            if 'SR' in cards_star:
                #得到抽卡结果
                for i in range(10):
                    cardname=conn2sql.get_cardname(pool_name=poolname,star=cards_star[i],db_name=db_name)
                    conn2sql.insert_draw_log(db_name,poolname,cardname) #存入抽卡记录的数据库
                break

        #将十张卡内容展现出来，并计算抽卡结果的计数
        self.labels = [self.label_12, self.label_13, self.label_14, self.label_15,
                       self.label_16, self.label_17, self.label_18, self.label_19, self.label_20, self.label_21] #将标签存放为标签数组
        for label in self.labels:
            i=self.labels.index(label)
            image_path = "res/"+cards_star[i]+".png"  # 替换为你的图片路径
            pixmap = QPixmap(image_path) #变为Qpixmap对象
            # 调整 QLabel 大小以适应图片
            self.labels[i].setPixmap(pixmap)
            self.labels[i].setScaledContents(True)
            #同时更新计数器
            if (cards_star[i]=="R"):
                rnum=rnum+1               
            elif(cards_star[i]=="SR"):
                srnum=srnum+1      
            elif(cards_star[i]=="SSR"):
                ssrnum=ssrnum+1

        #更新统计数据
        getnum=getnum+10
        self.value_getnum_3.setText(str(getnum))
        self.value_rnum_3.setText(str(rnum))
        self.value_srnum_2.setText(str(srnum))
        self.value_ssrnum_3.setText(str(ssrnum))
        self.value_Pssr_3.setText(str(round(ssrnum*100/(getnum),2))+"%")
        
        #输出日志文件
        table_name="draw_log"
        txt_file="draw_log.txt"
        conn2sql.export_table_to_txt(table_name,db_name,txt_file) #抽卡记录表导出为txt

####################################
     #定义公告函数
    def ask(self):         
        text=open("data/公告.txt").read()           
        QMessageBox.about(self, "公告内容", text )   
    


if __name__ == "__main__":
    #固定语句。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
    