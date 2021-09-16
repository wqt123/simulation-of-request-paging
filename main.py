import time
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import random

class BLOCK:   #物理块类型
	pagenum = -1;#页号
	next_access_instruction = 0;#访问字段，其值表示多久未被访问LRU,已在块中存在时间FIFO

BlockNum =  4 #块数
pc = 0   #程序计数器，用来记录当前指令的序号
n  = 0   #缺页计数器，用来记录缺页的次数
temp = []#用来存储320条随机数
block = [BLOCK() for i in range(BlockNum)]; #定义一大小为4的物理块数组
page = []
for i in range(32):
    t = []
    page.append(t)

algorithm = 0 #选择算法
solution = 0#执行方法
order = 0 #执行顺序
press = 0 #点击次数	
is_reset = False #是否重置了
window = tk.Tk()
window.configure(background='white') 
window.title('请求调页存储管理模拟')
window.geometry('940x570')
window.resizable(0,0)


#----------------内存块展示-------------------------------------------
def round_rectangle(my_canvas,x1, y1, x2, y2, color, r = 25):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return my_canvas.create_polygon(points, fill = color, smooth=True)

block_canvas = []
for i in range(BlockNum):
    t = tk.Canvas(window,height = 265,width = 130)
    block_canvas.append(t)
num_text = []
rectangle_list = []
for i in range(BlockNum):
    t = []
    rectangle_list.append([])
for i in range(BlockNum):
    block_canvas[i].create_text(65,15,text = '内存块 '+str(i),font=('Times', 13))
    num_text.append(block_canvas[i].create_text(50,35, text = ' ',font=('Times', 16)))
    block_canvas[i].create_text(75,38, text = '页',font=('Times', 13))
    for j in range(10):            
        rectangle_list[i].append(round_rectangle(block_canvas[i],15,50+j*21, 115, 70+j*21,"lightblue",18))
        block_canvas[i].create_text(65, 60+j*21, text = str(j), font=('Times', 13))
    block_canvas[i].place(x = 320+155*i ,y = 20)

#----------------指令序列--------------------------------------------

tabel_frame = tk.Frame(window)
tabel_frame.place(x = 320 ,y = 320)

yscroll = tk.Scrollbar(tabel_frame, orient="vertical")

columns = ['指令地址', '缺页', '换入页', '换出页']
table = ttk.Treeview(
        master=tabel_frame,  # 父容器
        height=10,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        yscrollcommand=yscroll.set,  # y轴滚动条
        )
for column in columns:
    table.heading(column=column, text=column, anchor='center')  # 定义表头
    table.column(column=column, width=100, minwidth=100, anchor='center', )  # 定义列

yscroll.config(command=table.yview)
yscroll.pack(side='right', fill='y')
table.pack(expand=False)

#----------------缺页数据显示------------------------------------------

show_canvas = tk.Canvas(window,height = 225,width = 140)
show_canvas.create_text(70,20, text = '当前缺页数：',font=('Times', 15))
show_canvas.create_text(70,140, text = '当前缺页率：',font=('Times', 15))
lost_num_text = show_canvas.create_text(70,50, text = '',font=('Times', 15))
lost_ratio_text = show_canvas.create_text(70,170, text = '',font=('Times', 15))
show_canvas.place(x = 770 ,y = 320)

#----------------控制模块----------------------------------------------

control_frame = tk.Frame(window)
control_frame.place(x = 20,y = 20,height = 525,width = 260)
'''
 相关信息说明
'''
tk.Label(control_frame,text = '内存调度控制').place(x = 0,y = 0)

detail_canvas = tk.Canvas(control_frame,height = 190,width = 230)
detail_canvas.configure(background = 'white')
detail_canvas.create_text(125,20, text = '作业数目',font=('Times', 15))
detail_canvas.create_text(125,40, text = '1',font=('Times', 15))
detail_canvas.create_text(125,60, text = '作业分配的内存块数',font=('Times', 15))
detail_canvas.create_text(125,80, text = '4',font=('Times', 15))
detail_canvas.create_text(125,100, text = '每页存放的指令数',font=('Times', 15))
detail_canvas.create_text(125,120, text = '10',font=('Times', 15))
detail_canvas.create_text(125,140, text = '作业的指令数',font=('Times', 15))
detail_canvas.create_text(125,160, text = '320',font=('Times', 15))
detail_canvas.place(x = 10,y = 30)

'''
 页面置换算法选择按钮
'''
def choose_algorithm(i):
    global algorithm
    algorithm = i
algorithm_button = tk.Menubutton(control_frame,text = ' 页面置换算法(默认FIFO) ',width = 21,height = 2,relief = 'raised')
algorithm_button.place(x = 50, y = 240)   
algorithm_menu = tk.Menu(algorithm_button, tearoff=False,activeborderwidth = 16)
algorithm_menu.add_command(label = 'FIFO算法',command = lambda :choose_algorithm(1))
algorithm_menu.add_command(label = 'LRU算法',command = lambda :choose_algorithm(2))
algorithm_button.config(menu = algorithm_menu)

'''
 指令执行顺序选择按钮
'''
def choose_order(i):
    global order 
    order = i
order_button = tk.Menubutton(control_frame,text = ' 指令执行顺序(默认混合执行)',width = 21,height = 2,relief = 'raised')
order_button.place(x = 50, y = 300)   
order_menu = tk.Menu(order_button, tearoff=False,activeborderwidth = 16)
order_menu.add_command(label = '混合执行',command = lambda :choose_order(1))
order_menu.add_command(label = '顺序执行',command = lambda :choose_order(2))
order_menu.add_command(label = '随机执行',command = lambda :choose_order(3))
order_button.config(menu = order_menu)

'''
 指令执行选择按钮：单步、连续、重置
'''
canvas = tk.Canvas(control_frame,height = 140,width = 160)
round_rectangle(canvas,0, 0, 145,140, 'white',45)
canvas.place(x = 50,y = 365)
#检查页面是否在内存中
def findExist(curpage):
	for i in range(BlockNum):
		if block[i].pagenum == curpage:
			return i;#检测到内存中有该页面，返回block中的位置
	return -1
#查找空闲块
def findSpace():
	for i in range(BlockNum):
		if block[i].pagenum == -1:
			return i;#找到空闲的block，返回block中的位置
	return -1
#查找换页位置
def findReplace():
	pos = 0
	for i in range(BlockNum):
		if block[i].next_access_instruction > block[pos].next_access_instruction:
			pos = i;#找到应予置换页面，返回BLOCK中位置
	return pos
#顺序产生指令
def sequence():
	global temp
	for i in range(320):
		temp.append(i)
#混合产生指令:50%的指令是顺序执行的，25%是均匀分布在前地址部分，25％是均匀分布在后地址部分
def mix_order():
    global temp,pc
    flag = 0
    pc = random.randint(0, 319)
    for i in range(320):
        temp.append(pc)
        if flag % 2 == 0:
            pc = (pc + 1) % 320
        elif flag == 1:
            if pc <=1:
                continue
            pc = random.randint(0, pc - 1) + 1
        elif flag == 3:
            if pc +1 >= 319:
                continue
            pc = random.randint(pc + 1, 320 - 1) + 1
        flag += 1
        flag %= 4
#随机顺序产生指令
def random_order():
    global temp
    array = np.random.permutation(320)
    temp = array.tolist()
#更新渲染内存块
def show_page():
    global num_text
    for i in range(BlockNum):
        block_canvas[i].delete(num_text[i])
        if block[i].pagenum !=-1:
            num_text[i] = block_canvas[i].create_text(50,35, text = str(block[i].pagenum),font=('Times', 16))
        else:
            num_text[i] = block_canvas[i].create_text(50,35, text = '',font=('Times', 16))
        for j in range(10):
            if page[block[i].pagenum].count(j)!=0:
                block_canvas[i].delete(rectangle_list[i][j])
                rectangle_list[i][j] = round_rectangle(block_canvas[i],15,50+j*21, 115, 70+j*21,"yellow",18)
                block_canvas[i].create_text(65, 60+j*21, text = str(j), font=('Times', 13))
            else:
                block_canvas[i].delete(rectangle_list[i][j])
                rectangle_list[i][j] = round_rectangle(block_canvas[i],15,50+j*21, 115, 70+j*21,"lightblue",18)
                block_canvas[i].create_text(65, 60+j*21, text = str(j), font=('Times', 13))
        block_canvas[i].update()
#表格的插入
def insert(info):
    global table
    table.insert('', 'end', values=info)  # 添加数据到末尾
#表格的清空
def clear_table():
    global table
    x = table.get_children()
    for item in x:
        table.delete(item)
#LRU算法
def LRU(i):
    global pc,n,temp,block,page,lost_num_text,lost_ratio_text
    flag = False #是否缺页
    pc = temp[i]
    curpage = pc // 10
    page[curpage].append(pc%10)
    exist = findExist(curpage)
    if exist == -1:
        space = findSpace()
        if space != -1:
            block[space].pagenum = curpage
        else:
            n+=1
            flag = True
            position = findReplace()
            oldpage = block[position].pagenum
            block[position].pagenum = curpage
    else :
        block[exist].next_access_instruction = 0
    for j in range(BlockNum):              #每块中存在的页面未使用时长加1，下次寻找该值最大的块置换出去
        if j == exist:
            continue
        block[j].next_access_instruction += 1
    show_page()
    if flag:
        insert([str(pc),'是',str(curpage),str(oldpage)])
    else:
        insert([str(pc),'否','-','-'])
    flag = False
    show_canvas.delete(lost_num_text)
    show_canvas.delete(lost_ratio_text)
    lost_num_text = show_canvas.create_text(70,50, text = str(n),font=('Times', 15))
    lost_ratio_text = show_canvas.create_text(70,170, text = str(round((n / 320.0)*100,2)) + "%",font=('Times', 15))
    show_canvas.update()
#FIFO算法
def FIFO(i):
    global pc,n,block,page,lost_num_text,lost_ratio_text,temp
    flag = False#是否换页
    pc = temp[i]
    curpage = pc // 10
    page[curpage].append(pc%10)
    exist = findExist(curpage)
    if exist == -1:               #不在块内 
        space = findSpace()
        if space != -1:        #且没有空块 
            block[space].pagenum = curpage
        else:                  #需要置换  
            n+=1  
            flag = True
            position = findReplace()
            oldpage = block[position].pagenum
            block[position].pagenum = curpage
            block[position].next_access_instruction = 0
            
    for j in range(BlockNum): 
        block[j].next_access_instruction+=1  #每块存在时长加1 
    show_page()
    if flag:
        insert([str(pc),'是',str(curpage),str(oldpage)])
    else:
        insert([str(pc),'否','-','-'])
    flag = False
    show_canvas.delete(lost_num_text)
    show_canvas.delete(lost_ratio_text)
    lost_num_text = show_canvas.create_text(70,50, text = str(n),font=('Times', 15))
    lost_ratio_text = show_canvas.create_text(70,170, text = str(round((n / 320.0)*100,2)) + "%",font=('Times', 15))
    show_canvas.update()
#主要运行函数
def run(): 
    global algorithm,solution,press,pc,n,temp,block,page,lost_num_text,lost_ratio_text,order,is_reset

    if order == 1 or order == 0:
        mix_order()
    elif order == 2:
        sequence()
    elif order ==3:
        random_order()
    
    if algorithm == 0 or algorithm == 1:
        if solution == 1:
            FIFO(press)
        elif solution ==2:
            for i in range(320):
                try:
                    FIFO(i)
                except:
                    clear_table()
                    return 
                time.sleep(0.3)
    elif algorithm == 2:
        if solution == 1:
            LRU(press)
        elif solution ==2:
            for i in range(320):
                try:
                    LRU(i)
                except:
                    clear_table()
                    return
                time.sleep(0.3)
        
#单步执行
def one_step():
    global solution ,press
    if solution ==2:
        messagebox.showwarning('警告','连续运行期间无法进行单步执行') 
    solution = 1
    press +=1
    run()
one_step_button = tk.Button(control_frame,text = '单步执行',width = 15,height = 1,command = one_step)
one_step_button.place(x = 65, y = 380)

#连续执行
def continuous():
    global solution
    solution = 2
    run()
continuous_button = tk.Button(control_frame,text = '连续执行',width = 15,height = 1,command =continuous)
continuous_button.place(x = 65, y = 420)

#重置
def reset():
    global algorithm,press,pc,n,solution,temp,block,page,lost_num_text,lost_ratio_text,table,order
    algorithm = 0 #选择算法
    pc = 0   #程序计数器，用来记录当前指令的序号
    n  = 0   #缺页计数器，用来记录缺页的次数
    press = 0	
    order = 0
    solution = 0#执行方法
    temp = []#用来存储320条随机数
    block = [BLOCK() for i in range(BlockNum)]; #定义一大小为4的物理块数组
    page = []
    for i in range(32):
        t = []
        page.append(t)
    show_page()
    
    show_canvas.delete(lost_num_text)
    show_canvas.delete(lost_ratio_text)
    lost_num_text = show_canvas.create_text(70,50, text = '',font=('Times', 15))
    lost_ratio_text = show_canvas.create_text(70,170, text = '',font=('Times', 15))
    show_canvas.update()
    clear_table()
    
reset_button = tk.Button(control_frame,text = '重置',width = 15,height = 1,command = lambda:reset())
reset_button.place(x = 65, y = 460)

window.mainloop()
