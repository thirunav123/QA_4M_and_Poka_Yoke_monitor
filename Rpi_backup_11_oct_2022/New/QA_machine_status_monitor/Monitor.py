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
next_page_move_time=int(filedic.pop("next_page_move_time_in_miliseconds"))/1000
screen_refresh_time=int(filedic.pop("gui_screen_refresh_time_in_milliseconds"))
A=list(map(int,shiftA_start.strip().split(":")))
B=list(map(int,shiftB_start.strip().split(":")))
C=list(map(int,shiftC_start.strip().split(":")))

page_1_reset_flag=None
page_2_reset_flag=None
page_3_reset_flag=None

raw_button_name_list=[]
raw_button_state_list=[]
temp0_list=[]
temp1_list=[]

# STATE 
# 0 - Not Updated,
# 1 - No Change / Ok,
# 2 - Changed / Nok,
# 3 - Not Applicable.

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
temp0_list=[]
temp1_list=[]
for i in range(1,168):
    temp0_list.append(f'pb1_{i}')
    temp1_list.append(0)
raw_button_name_list.append(temp0_list)
raw_button_state_list.append(temp1_list)
temp0_list=[]
temp1_list=[]
for i in range(1,105):
    temp0_list.append(f'pb2_{i}')
    temp1_list.append(0)
raw_button_name_list.append(temp0_list)
raw_button_state_list.append(temp1_list)

previous_time=None
lock=threading.Lock()

class firstDialog(QDialog):

    def __init__(self):
        global previous_time
        super(firstDialog,self).__init__()     
        self.ui=loadUi("4M_Change.ui",self)#load the UI file 
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        for index_i,i in enumerate(raw_button_name_list[0]):
            for index_j,j in enumerate(i):
                raw_button_name_list[0][index_i][index_j]=self.ui.findChild(QtWidgets.QPushButton,j)
                raw_button_name_list[0][index_i][index_j].clicked.connect(self.status_change)
                raw_button_name_list[0][index_i][index_j].setStyleSheet('font: 87 25pt "Arial Black";background-color: blue;border-radius:30px;color: rgb(255, 255, 255);')
        self.screen_refresh()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.screen_refresh)
        self.check_timer.setInterval(screen_refresh_time)
        self.check_timer.start()
        print("First_d_init")

    def screen_refresh(self):
        global page_1_reset_flag
        date_today=int(time.strftime("%d"))
        for index_i,i in enumerate(raw_button_name_list[0]):
            for index_j,j in enumerate(i):
                if date_today<=index_j:
                    raw_button_state_list[0][index_i][index_j]=3
                    j.setStyleSheet('font: 87 25pt "Arial Black";background-color: rgb(174, 196, 255);border-radius:30px;color: rgb(255, 255, 255);') 
                    j.setEnabled(False)
        if page_1_reset_flag:
            for index_i,i in enumerate(raw_button_name_list[0]):
                for index_j,j in enumerate(i):
                    if raw_button_state_list[0][index_i][index_j]==3 or date_today==1:
                        j.setStyleSheet('font: 87 25pt "Arial Black";background-color: blue;border-radius:30px;color: rgb(255, 255, 255);')
                        j.setEnabled(True)
                        raw_button_state_list[0][index_i][index_j]=0
            page_1_reset_flag=False
            print("page_1 reset")
        count_NU=0
        count_NC=0
        count_C=0
        count_NA=0
        for i in range(len(raw_button_state_list[0])):
            count_NU=count_NU+raw_button_state_list[0][i].count(0)
            count_NC=count_NC+raw_button_state_list[0][i].count(1)
            count_C=count_C+raw_button_state_list[0][i].count(2)
            count_NA=count_NA+raw_button_state_list[0][i].count(3)
        self.label_NU.setText(str(count_NU))
        self.label_NC.setText(str(count_NC))
        self.label_C.setText(str(count_C))
        self.label_NA.setText(str(count_NA))
        time_now=datetime.datetime.now()
        shift=get_shift(datetime.time(time_now.hour,time_now.minute,time_now.second))
        self.label_date.setText(time.strftime('%d/%m/%Y ')+shift)
        self.label_time.setText(time.strftime('%H:%M:%S'))

    def status_change(self):
        global previous_time
        flag=False
        for index_i,i in enumerate(raw_button_name_list[0]):
            for index_j in range(len(i)):
                if raw_button_name_list[0][index_i][index_j]==self.sender():
                    if raw_button_state_list[0][index_i][index_j]==1:
                        raw_button_state_list[0][index_i][index_j]=2
                        self.sender().setStyleSheet('font: 87 25pt "Arial Black";background-color: red;border-radius:30px;color: rgb(255, 255, 255);')
                    elif raw_button_state_list[0][index_i][index_j]==2:
                        raw_button_state_list[0][index_i][index_j]=0
                        self.sender().setStyleSheet('font: 87 25pt "Arial Black";background-color: blue;border-radius:30px;color: rgb(255, 255, 255);')
                    else:
                        raw_button_state_list[0][index_i][index_j]=1
                        self.sender().setStyleSheet('font: 87 25pt "Arial Black";background-color: green;border-radius:30px;color: rgb(255, 255, 255);')
                    break
            if flag==True:
                break
        previous_time=time.time()
    
class secondDialog(QDialog):

    def __init__(self):
        global previous_time
        super(secondDialog,self).__init__()
        self.ui=loadUi("Poka_Yoke_page_1.ui",self) #loadui
        for index_i,i in enumerate(raw_button_name_list[1]):
            raw_button_name_list[1][index_i]=self.ui.findChild(QtWidgets.QPushButton,i)
            raw_button_name_list[1][index_i].clicked.connect(self.status_change)
            raw_button_name_list[1][index_i].setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
        self.screen_refresh()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.screen_refresh)
        self.check_timer.setInterval(screen_refresh_time)
        self.check_timer.start()
        print("Second_d_init")
    
    def screen_refresh(self):
        global page_2_reset_flag
        if page_2_reset_flag:
            for index_i,i in enumerate(raw_button_name_list[1]):
                i.setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                raw_button_state_list[1][index_i]=0
            page_2_reset_flag=False
            print("page_2 reset")
        self.label_NU.setText(str(raw_button_state_list[1].count(0)))
        self.label_ok.setText(str(raw_button_state_list[1].count(1)))
        self.label_nok.setText(str(raw_button_state_list[1].count(2)))
        time_now=datetime.datetime.now()
        shift=get_shift(datetime.time(time_now.hour,time_now.minute,time_now.second))
        self.label_date.setText(time.strftime('%d/%m/%Y ')+shift)
        self.label_time.setText(time.strftime('%H:%M:%S'))

    def status_change(self):
        global previous_time
        for index_i in range(len(raw_button_name_list[1])):
            if raw_button_name_list[1][index_i]==self.sender():
                if raw_button_state_list[1][index_i]==1:
                    raw_button_state_list[1][index_i]=2
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);')
                elif raw_button_state_list[1][index_i]==2:
                    raw_button_state_list[1][index_i]=0
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                else:
                    raw_button_state_list[1][index_i]=1
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                break
        previous_time=time.time()

class thirdDialog(QDialog):
    
    def __init__(self):
        super(thirdDialog,self).__init__()
        self.ui=loadUi("Poka_Yoke_page_2.ui",self) #loadui
        for index_i,i in enumerate(raw_button_name_list[2]):
            raw_button_name_list[2][index_i]=self.ui.findChild(QtWidgets.QPushButton,i)
            raw_button_name_list[2][index_i].clicked.connect(self.status_change)
            raw_button_name_list[2][index_i].setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
        self.screen_refresh()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.screen_refresh)
        self.check_timer.setInterval(screen_refresh_time)
        self.check_timer.start()
        print("Third_d_init")

    def screen_refresh(self):
        global page_3_reset_flag
        if page_3_reset_flag:
            for index_i,i in enumerate(raw_button_name_list[2]):
                i.setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                raw_button_state_list[2][index_i]=0
            page_3_reset_flag=False
            print("page_3 reset")
        self.label_NU.setText(str(raw_button_state_list[2].count(0)))
        self.label_ok.setText(str(raw_button_state_list[2].count(1)))
        self.label_nok.setText(str(raw_button_state_list[2].count(2)))
        time_now=datetime.datetime.now()
        shift=get_shift(datetime.time(time_now.hour,time_now.minute,time_now.second))
        self.label_date.setText(time.strftime('%d/%m/%Y ')+shift)
        self.label_time.setText(time.strftime('%H:%M:%S'))
        
    def status_change(self):
        global previous_time
        for index_i in range(len(raw_button_name_list[2])):
            if raw_button_name_list[2][index_i]==self.sender():
                if raw_button_state_list[2][index_i]==1:
                    raw_button_state_list[2][index_i]=2
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: red;border-radius:15px;color: rgb(255, 255, 255);')
                elif raw_button_state_list[2][index_i]==2:
                    raw_button_state_list[2][index_i]=0
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: blue;border-radius:15px;color: rgb(255, 255, 255);')
                else:
                    raw_button_state_list[2][index_i]=1
                    self.sender().setStyleSheet('font: 87 12pt "Arial Black";background-color: green;border-radius:15px;color: rgb(255, 255, 255);')
                break
        previous_time=time.time()

def get_shift(ct):
    startA=datetime.time(A[0],A[1],A[2])
    startB=datetime.time(B[0],B[1],B[2])
    startC=datetime.time(C[0],C[1],C[2])
    if startA<=ct<startB:
        return 'A'
    elif startB<=ct<startC:
        return 'B'
    else:
        return 'C'

def reset(s):
    global page_1_reset_flag,page_2_reset_flag,page_3_reset_flag
    temp_list=[]
    t=time.time()-30
    t=datetime.datetime.fromtimestamp(t)
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
    for i in raw_button_state_list[0]:
        for j in i:
            temp_list.append(j)
    for i in raw_button_state_list[1]:
        temp_list.append(i)             
    for i in raw_button_state_list[2]:
        temp_list.append(i)                     
    with open('report.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(temp_list)
    if s=="A":
        page_1_reset_flag=True
    page_2_reset_flag=True
    page_3_reset_flag=True

def schedule_thread():
    try:
        schedule.every().day.at(shiftA_start).do(reset,"A")
        schedule.every().day.at(shiftB_start).do(reset,"B")
        schedule.every().day.at(shiftC_start).do(reset,"C")
        while True:            
            schedule.run_pending()
            time.sleep(scheduler_delay)
    except Exception as e:
        print(e)

def next_page():
    global previous_time
    previous_time=time.time()
    while True:
        ct=time.time()
        if previous_time+next_page_move_time<ct:
            index_w=widget.currentIndex()
            if index_w<2:
                widget.setCurrentIndex(index_w+1)
                # print("next_page")
            else:
                widget.setCurrentIndex(0)
            lock.acquire()
            previous_time=ct
            lock.release()
        time.sleep(0.5)

app=QApplication(sys.argv)
firstwindow=firstDialog()
secondwindow=secondDialog()
thirdwindow=thirdDialog()
widget=QtWidgets.QStackedWidget()
widget.addWidget(firstwindow)
widget.addWidget(secondwindow)
widget.addWidget(thirdwindow)
schedule_th = threading.Thread(target=schedule_thread,daemon=True)
schedule_th.start()
print("MT: Schedule_thread thread started")
schedule_th = threading.Thread(target=next_page,daemon=True)
schedule_th.start()
print("MT: Next_page thread started")
widget.setWindowTitle("ZRAI_OSD")
widget.setWindowIcon(QIcon('gui_icon.ico'))
widget.show()
widget.showFullScreen()
sys.exit(app.exec())