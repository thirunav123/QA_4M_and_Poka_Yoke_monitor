import sys,schedule,time,threading,datetime
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.QtGui import  QIcon
import csv
setting_file=open('GUI_settings.txt','r')
filedic={}
for line in setting_file:
    file_data=line.strip().split('===')
    a=file_data[0]
    b=file_data[1]
    filedic[a]=b
setting_file.close()

shiftA_start=filedic.pop('shiftA_start_time')
shiftB_start=filedic.pop('shiftB_start_time')
shiftC_start=filedic.pop('shiftC_start_time')
scheduler_delay=int(filedic.pop("scheduler_delay_in_milliseconds"))/1000
next_page_move_time=int(filedic.pop("next_page_move_time_in_miliseconds"))
screen_refresh_time=int(filedic.pop("gui_screen_refresh_time_in_milliseconds"))
A=list(map(int,shiftA_start.strip().split(":")))
B=list(map(int,shiftB_start.strip().split(":")))
C=list(map(int,shiftC_start.strip().split(":")))
# page_1_reset_flag=None
# page_2_reset_flag=None


raw_button_name_list=[]
raw_button_state_list=[]
temp0_list=[]
temp1_list=[]

# STATE 
# 0 - Not Upadated
# 1 - No Change / Ok
# 2 - Changed / Nok
# 3 - NA

for i in range(4):
    temp2_list=[]
    temp3_list=[]
    for j in range(1,32):
        temp2_list.append(f"pb_m{i+1}_{j}")
        temp3_list.append(0)
    temp0_list.append(temp2_list)
    temp1_list.append(temp3_list)
raw_button_name_list.append(temp0_list)
raw_button_state_list.append(temp1_list)
# raw_button_name_list=[]
temp0_list=[]
temp1_list=[]
for i in range(1,168):
    temp0_list.append(f'pb_{i}')
    temp1_list.append(0)
raw_button_name_list.append(temp0_list)
raw_button_state_list.append(temp1_list)
temp0_list=[]
temp1_list=[]
for i in range(1,105):
    temp0_list.append(f'pb_{i}')
    temp1_list.append(0)
raw_button_name_list.append(temp0_list)
raw_button_state_list.append(temp1_list)
# print(raw_button_name_list)

f_found_flag=False
s_found_flag=False
t_found_flag=False
f_added=False
s_added=False
# t_added=False

    
class firstDialog(QDialog):
    def __init__(self):
        global f_found_flag
        super(firstDialog,self).__init__()        
        self.ui=loadUi("4M_Change.ui",self)#load the UI file 
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        # self.button_name_list=[]
        # m=4
        # for i in range(m):
        #     self.temp_list=[]
        #     for j in range(1,32):
        #         self.temp_list.append(f"pb_m{i+1}_{j}")
        #     self.button_name_list.append(self.temp_list)
        # print(self.button_name_list)
        if not f_found_flag:
            for index_i,i in enumerate(raw_button_name_list[0]):
                for index_j,j in enumerate(i):
                    raw_button_name_list[0][index_i][index_j]=self.ui.findChild(QtWidgets.QPushButton,j)
                    # print(index_i,index_j)
            f_found_flag=True
        if f_found_flag:
            date_today=int(time.strftime("%d"))
            for index_i,i in enumerate(raw_button_name_list[0]):
                for index_j,j in enumerate(i):
                    if date_today<=index_j:
                        raw_button_state_list[0][index_i][index_j]=3                     
        for index_i,i in enumerate(raw_button_name_list[0]):
            for index_j,j in enumerate(i):
                state=raw_button_state_list[0][index_i][index_j]
                j.clicked.connect(self.status_change)
                if state==0:
                    j.setStyleSheet('font: 87 25pt "Arial Black";background-color: blue;border-radius:30px;color: rgb(255, 255, 255);')
                    j.setEnabled(True)
                elif state==1:
                    j.setStyleSheet('font: 87 25pt "Arial Black";background-color: green;border-radius:30px;color: rgb(255, 255, 255);')
                    j.setEnabled(True)
                elif state==2:
                    j.setStyleSheet('font: 87 25pt "Arial Black";background-color: red;border-radius:30px;color: rgb(255, 255, 255);')
                    j.setEnabled(True)
                else:
                    j.setStyleSheet('font: 87 25pt "Arial Black";background-color: rgb(174, 196, 255);border-radius:30px;color: rgb(255, 255, 255);') 
                    j.setEnabled(False)
        self.page_Timer = QTimer()
        self.page_Timer.timeout.connect(self.next_page)
        self.page_Timer.setInterval(next_page_move_time)
        self.page_Timer.start()
        print("First_d_init")

    def next_page(self):
        global f_added
        self.page_Timer.stop()
        secondpage=secondDialog()
        if not f_added:
            widget.addWidget(secondpage)
            f_added=True
        widget.setCurrentIndex(widget.currentIndex()+1)    
        print(f"f{widget.currentIndex()}")

    def status_change(self,):
        flag=False
        for index_i,i in enumerate(raw_button_name_list[0]):
            for index_j,j in enumerate(i):
                if raw_button_name_list[0][index_i][index_j]==self.sender():
                    if raw_button_state_list[0][index_i][index_j]==1:
                        raw_button_state_list[0][index_i][index_j]=2
                        self.sender().setStyleSheet('font: 87 25pt "Arial Black";background-color: red;border-radius:30px;color: rgb(255, 255, 255);')
                    else:
                        raw_button_state_list[0][index_i][index_j]=1
                        self.sender().setStyleSheet('font: 87 25pt "Arial Black";background-color: green;border-radius:30px;color: rgb(255, 255, 255);')
                    break
            if flag==True:
                break
        # print(raw_button_state_list[0][index_i][index_j],self.sender())
        self.page_Timer.start()            
    
    # def 
        # print(time.strftime('%d'))
            # if self.button_name_list[i][index_j]==None:
            #     print(index_j+1)
        # # buttonGroup_2=QtWidgets.QButtonGroup("buttonGroup_2")
        # self.page_Timer = QTimer()
        # self.page_Timer.timeout.connect(self.next_page)
        # conn_refresh_time=3000
        # self.page_Timer.setInterval(conn_refresh_time) 
        # # self.page_Timer.start()
        # self.page_Timer_1 = QTimer()
        # self.page_Timer_1.timeout.connect(self.status_change)
        # conn_refresh_time=3000
        # self.page_Timer_1.setInterval(conn_refresh_time) 
        # # self.page_Timer_1.start()
#         for i in self.button_name_list:
#             # pass
#             i.setStyleSheet(''' QPushButton:checked { background-color: red; border: none; }
# QPushButton{font: 87 25pt "Arial Black";background-color: green;border-radius:30px;color: rgb(255, 255, 255);
# }
# ''')
        #     i.setEnabled(False)
        #     # i.show()

    # def status_change(self,):
    #     self.sender().setStyleSheet(''' QPushButton:checked { background-color: green; border: none; }
    #                                     QPushButton{font: 87 10pt "Arial Black";
    #                                     background-color: red;
    #                                     border-radius:15px;
    #                                     color: rgb(255, 255, 255);}''')
    #     # print(self.sender().objectName())
    #     # print("status_change")

    # def reset_all_button_status(self):
    #     global page_1_reset_flag
    #     if reset_flag:
    #         for i in self.button_name_list:
    #             i.setStyleSheet(''' font: 87 10pt "Arial Black";
    #                                 background-color: blue;
    #                                 border-radius:15px;
    #                                 color: rgb(255, 255, 255);''')
    #         reset_flag=False
    #         print("reset_1")

    
    
class secondDialog(QDialog):

    def __init__(self):
        global s_found_flag
        super(secondDialog,self).__init__()
        self.ui=loadUi("Poka_Yoke_page_1.ui",self) #loadui
        if not s_found_flag:
            for index_i,i in enumerate(raw_button_name_list[1]):
                    raw_button_name_list[1][index_i]=self.ui.findChild(QtWidgets.QPushButton,i)
            s_found_flag=True
        for index_i,i in enumerate(raw_button_name_list[1]):
                state=raw_button_state_list[1][index_i]
                i.clicked.connect(self.status_change)
                if state==0:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                    # i.setEnabled(True)
                elif state==1:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                    # i.setEnabled(True)
                # elif state==2:
                #     i.setStyleSheet('font: 87 25pt "Arial Black";background-color: red;border-radius:30px;color: rgb(255, 255, 255);')
                #     i.setEnabled(True)
                else:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);') 
                    # i.setEnabled(False)
        self.page_Timer = QTimer()
        self.page_Timer.timeout.connect(self.next_page)
        self.page_Timer.setInterval(next_page_move_time)
        self.page_Timer.start()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.reset_all_button_status)
        self.check_timer.setInterval(1000)
        self.check_timer.start()
        print("Second_d_init")

    def next_page(self):
        global s_added
        self.page_Timer.stop()
        thirddpage=thirdDialog()
        if not s_added:
            widget.addWidget(thirddpage)
            s_added=True
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(f"s{widget.currentIndex()}")
    
    # def reset_all_button_status(self):
    #     global page_1_reset_flag
    #     if page_1_reset_flag:
    #         for i in self.button_name_list:
    #             i.setStyleSheet(''' font: 87 10pt "Arial Black";
    #                                 background-color: blue;
    #                                 border-radius:15px;
    #                                 color: rgb(255, 255, 255);''')
    #         page_1_reset_flag=False
        
    def status_change(self,):
        self.sender().setStyleSheet(''' QPushButton:checked { background-color: red; border: none; }
                                        QPushButton{font: 87 8pt "Arial Black";background-color: green;border-radius:15px;
                                        color: rgb(255, 255, 255);}''')
        for index_i,i in enumerate(raw_button_name_list[1]):
                if raw_button_name_list[1][index_i]==self.sender():
                    if raw_button_state_list[1][index_i]==1:
                        raw_button_state_list[1][index_i]=2
                        self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);')
                    else:
                        raw_button_state_list[1][index_i]=1
                        self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                    break
        # print(raw_button_state_list[1][index_i],self.sender())
        self.page_Timer.start() 

class thirdDialog(QDialog):
    def __init__(self):
        global t_found_flag
        super(thirdDialog,self).__init__()
        self.ui=loadUi("Poka_Yoke_page_2.ui",self) #loadui
        if not t_found_flag:
            for index_i,i in enumerate(raw_button_name_list[2]):
                    raw_button_name_list[2][index_i]=self.ui.findChild(QtWidgets.QPushButton,i)
            t_found_flag=True
        for index_i,i in enumerate(raw_button_name_list[2]):
                state=raw_button_state_list[2][index_i]
                # print(i)
                i.clicked.connect(self.status_change)
                if state==0:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                    # i.setEnabled(True)
                elif state==1:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                    # i.setEnabled(True)
                # elif state==2:
                #     i.setStyleSheet('font: 87 25pt "Arial Black";background-color: red;border-radius:30px;color: rgb(255, 255, 255);')
                #     i.setEnabled(True)
                else:
                    i.setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);') 
                    # i.setEnabled(False)
        self.page_Timer = QTimer()
        self.page_Timer.timeout.connect(self.next_page)
        self.page_Timer.setInterval(next_page_move_time)
        self.page_Timer.start()
        # self.check_timer = QTimer()
        # self.check_timer.timeout.connect(self.reset_all_button_status)
        # self.check_timer.setInterval(1000)
        # self.check_timer.start()
        print("Third_d_init")


    def next_page(self):
        # global t_added
        self.page_Timer.stop()
        firstpage=firstDialog()
        # if not t_added:
        #     widget.addWidget(firstpage)
        #     t_added=True
        widget.setCurrentIndex(0)
        print("Total count : ",widget.count())
        # print(f"t{widget.currentIndex()}")

    # def reset_all_button_status(self):
    #     global page_1_reset_flag
    #     if page_1_reset_flag:
    #         for i in self.button_name_list:
    #             i.setStyleSheet(''' font: 87 10pt "Arial Black";
    #                                 background-color: blue;
    #                                 border-radius:15px;
    #                                 color: rgb(255, 255, 255);''')
    #         page_1_reset_flag=False
        
    def status_change(self,):
        self.sender().setStyleSheet(''' QPushButton:checked { background-color: red; border: none; }
                                        QPushButton{font: 87 8pt "Arial Black";background-color: green;border-radius:15px;
                                        color: rgb(255, 255, 255);}''')
        for index_i,i in enumerate(raw_button_name_list[2]):
                if raw_button_name_list[2][index_i]==self.sender():
                    if raw_button_state_list[2][index_i]==1:
                        raw_button_state_list[2][index_i]=2
                        self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);')
                    else:
                        raw_button_state_list[2][index_i]=1
                        self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                    break
        # print(raw_button_state_list[2][index_i],self.sender())
        self.page_Timer.start() 

def get_shift(ct):
    startA=datetime.time(A[0],A[1],A[2])
    startB=datetime.time(B[0],B[1],B[2])
    startC=datetime.time(C[0],C[1],C[2])
    if startA<=ct<startB:
        return 'A'
    if startB<=ct<startC:
        return 'B'
    else:
        return 'C'
def reset():
    # global page_1_reset_flag,page_2_reset_flag
    with open('report.csv', 'a') as f:
            writer = csv.writer(f)
            temp_list=[]
            # time_eve=round(time.time())-prior_time
            t=datetime.datetime.now()
            current_time=datetime.time(t.hour,t.minute,t.second)
            if current_time<datetime.time(A[0],A[1],A[2]):
                dp=1
            else:
                dp=0
            date=t-datetime.timedelta(days=dp)
            date=date.strftime("%d-%m-%Y")
            shift=get_shift(current_time)
            temp_list.append(date)
            temp_list.append(shift)
            for index_i,i in enumerate(raw_button_state_list[0]):
                for j in enumerate(i):
                    if j==0:
                        temp_list.append("Not_Updated")
                    elif j==1:
                        temp_list.append("No_Change")
                    elif j==2:
                        temp_list.append("Changed")
                    else:
                        temp_list.append("NA")
            for index_i,i in enumerate(raw_button_state_list[1]):
                if i==0:
                    temp_list.append("Not_Updated")
                elif i==1:
                    temp_list.append("Ok")
                else:
                    temp_list.append("Nok")
                raw_button_state_list[1][index_i]=0
                
            for index_i,i in enumerate(raw_button_state_list[2]):
                if i==0:
                    temp_list.append("Not_Updated")
                elif i==1:
                    temp_list.append("Ok")
                else:
                    temp_list.append("Nok")
                raw_button_state_list[2][index_i]=0
                    
            writer.writerow(temp_list)
    # page_1_reset_flag=True
    # page_2_reset_flag=True
# print(raw_button_state_list)
# def state_change_date():
    # pass

def schedule_thread():
    try:
        schedule.every().day.at(shiftA_start).do(reset)
        schedule.every().day.at(shiftB_start).do(reset)
        schedule.every().day.at(shiftC_start).do(reset)
        while True:            
            schedule.run_pending()
            date_today=int(time.strftime("%d"))
            # if date_today<10:


            time.sleep(scheduler_delay)
    except Exception as e:
        print(e)

app=QApplication(sys.argv)
firstwindow=firstDialog()
# secondwindow=secondDialog()
# thirdwindow=thirdDialog()
schedule_th = threading.Thread(target=schedule_thread,daemon=True)
schedule_th.start()
print("MT: Schedule_thread thread started")
widget=QtWidgets.QStackedWidget()
widget.addWidget(firstwindow)
# widget.addWidget(secondwindow)
# widget.addWidget(thirdwindow)
# widget.showFullScreen()
widget.setWindowTitle("ZRAI_OSD")
widget.setWindowIcon(QIcon('gui_icon.ico'))


# widget.setFixedWidth(1280)
# widget.setFixedHeight(720)
widget.show()
sys.exit(app.exec())
# a=[]
# for i in range(1,200):
#     a.append(f"pb_{i}")
# print(a)
