# -*- coding: utf-8 -*-
#生信1501 邓泽旺 2015317200114
#这是一个游戏程序，游戏名字叫做连连看，玩家的目标是在限定时间内把矩阵内
#的图案全部消除。每次只能消除两个相同的图案，但是连接两个图案的路径线段不
#能超过三段，不能走曲线
import numpy as np
from time import time
def insure_input(k,ij):
	try:
	    x=input("请输入第"+str(k)+"个点的"+ij+"坐标:")
	except:
		return insure_input(k,ij)
	else:return x
#确保输入安全，防止出现字符输入或无输入
def lianliankan():
    def show_picture(picture):
        print "     1 2 3 4 5 6 7 8 9 10"
        for i in range(12):
            if i in range(1,11):
                print '%2s'%(i),' '.join(picture[i])
            else:print '  ',' '.join(picture[i])
    #显示当前图像
    def is_viable(picture,Ai,Aj,Bi,Bj):
        if Ai==Bi:
            if Aj-Bj==1 or Bj-Aj==1:return True
            x=1
            if Aj<Bj:r=range(Aj+1,Bj)
            else:r=range(Bj+1,Aj)
            for j in r:
                if picture[Ai][j]==' ':pass
                else:
                    x=0
                    break
            if x:return True
            else:return False
        if Aj==Bj:
            x=1
            if Ai-Bi==1 or Bi-Ai==1:return True
            if Ai<Bi:r=range(Ai+1,Bi)
            else:r=range(Bi+1,Ai)
            for i in r:
                if picture[i][Aj]==' ':pass
                else:
                    x=0
                    break
            if x:return True
            else:return False
    #检测线段两点之间是否可行，若有阻碍，返回False
    def mark_route(picture,Ai,Aj,Bi,Bj):
        if Ai==Bi:
            if Aj<Bj:r=range(Aj,Bj+1)
            else:r=range(Bj,Aj+1)
            for j in r:picture[Ai][j]='*'
        if Aj==Bj:
            if Ai<Bi:r=range(Ai,Bi+1)
            else:r=range(Bi,Ai+1)
            for i in r:picture[i][Aj]='*'
    #对线路进行标记‘*’
    def renew_picture(picture,Ai,Aj,Bi,Bj):
        if Ai==Bi:
            if Aj<Bj:r=range(Aj,Bj+1)
            else:r=range(Bj,Aj+1)
            for j in r:picture[Ai][j]=' '
        if Aj==Bj:
            if Ai<Bi:r=range(Ai,Bi+1)
            else:r=range(Bi,Ai+1)
            for i in r:picture[i][Aj]=' '
    #更新标记后的图像
    def row_search(picture,Ai,Aj,Bi,Bj,r):
        x=0
        for i in r:
            if picture[i][Aj]==' ' and picture[i][Bj]==' 'and\
            is_viable(picture,Ai,Aj,i,Aj)and\
            is_viable(picture,Bi,Bj,i,Bj)and\
            is_viable(picture,i,Aj,i,Bj):
                mark_route(picture,Ai,Aj,i,Aj) 
                mark_route(picture,Bi,Bj,i,Bj)
                mark_route(picture,i,Aj,i,Bj)
                picture[i][Aj]=picture[i][Bj]='*'
                show_picture(picture)
                renew_picture(picture,Ai,Aj,i,Aj)
                renew_picture(picture,Bi,Bj,i,Bj)
                renew_picture(picture,i,Aj,i,Bj)
                x=1
                break
        if x:return True
        else:return False
    #按行来进行扫描搜索路径
    def column_search(picture,Ai,Aj,Bi,Bj,r):
        x=0
        for j in r:
            if picture[Ai][j]==' ' and picture[Bi][j]==' 'and\
            is_viable(picture,Ai,Aj,Ai,j)and\
            is_viable(picture,Bi,Bj,Bi,j)and\
            is_viable(picture,Ai,j,Bi,j):
                mark_route(picture,Ai,Aj,Ai,j) 
                mark_route(picture,Bi,Bj,Bi,j)
                mark_route(picture,Ai,j,Bi,j)
                picture[Ai][j]=picture[Bi][j]='*'
                show_picture(picture)
                renew_picture(picture,Ai,Aj,Ai,j)
                renew_picture(picture,Bi,Bj,Bi,j)
                renew_picture(picture,Ai,j,Bi,j)
                x=1
                break
        if x:return True
        else:return False
    #按列来进行扫描搜索路径
    def find_route(picture,Ai,Aj,Bi,Bj):
        if Ai in range(1,11) and Aj in range(1,11) \
        and Bi in range(1,11) and Bj in range(1,11):pass
        else:
            print "坐标值超出范围了！"
            return False
        if picture[Ai][Aj]==' ' or picture[Bi][Bj]==' ':
            print "你输入的点有空点！"
            return False
        if picture[Ai][Aj]!=picture[Bi][Bj]:
            print "这两个点图案不相同！"
            return False
        if Ai==Bi and Aj==Bj:
            print "这两个点是同一个点！"
            return False
        if Ai==Bi:pattern=1
        if Aj==Bj:pattern=2
        if Ai!=Bi and Aj!=Bj:pattern=3
        #根据输入坐标相对位置（横线、竖线、对角）分为三种模式查找路径
        #优先找出最短路径，一旦找出其中一种则返回True，若所有路径搜索
        #方法都找不到，说明两点不能连通，则返回False
        if pattern==1:
            if is_viable(picture,Ai,Aj,Bi,Bj):
                mark_route(picture,Ai,Aj,Bi,Bj)
                show_picture(picture)
                renew_picture(picture,Ai,Aj,Bi,Bj)
                return True
            r=range(Ai)
            r.reverse()
            if row_search(picture,Ai,Aj,Bi,Bj,r):return True
            if row_search(picture,Ai,Aj,Bi,Bj,range(Ai+1,12)):return True
            print "两点不能连通！"
            return False
        if pattern==2:
            if is_viable(picture,Ai,Aj,Bi,Bj):
                mark_route(picture,Ai,Aj,Bi,Bj)
                show_picture(picture)
                renew_picture(picture,Ai,Aj,Bi,Bj)
                return True
            r=range(Aj)
            r.reverse()
            if column_search(picture,Ai,Aj,Bi,Bj,r):return True
            if column_search(picture,Ai,Aj,Bi,Bj,range(Aj+1,12)):return True
            print "两点不能连通！"
            return False
        if pattern==3:
            if is_viable(picture,Ai,Aj,Ai,Bj) and\
            is_viable(picture,Bi,Bj,Ai,Bj)and\
            picture[Ai][Bj]==' ':
                mark_route(picture,Ai,Aj,Ai,Bj)
                mark_route(picture,Bi,Bj,Ai,Bj)
                show_picture(picture)
                renew_picture(picture,Ai,Aj,Ai,Bj)
                renew_picture(picture,Bi,Bj,Ai,Bj)
                return True
            if is_viable(picture,Ai,Aj,Bi,Aj) and\
            is_viable(picture,Bi,Bj,Bi,Aj) and\
            picture[Bi][Aj]==' ':
                mark_route(picture,Ai,Aj,Bi,Aj)
                mark_route(picture,Bi,Bj,Bi,Aj)
                show_picture(picture)
                renew_picture(picture,Ai,Aj,Bi,Aj)
                renew_picture(picture,Bi,Bj,Bi,Aj)
                return True
            if Aj<Bj:
                r=range(Aj+1,Bj)
                rr=range(Bj+1,12)
                rl=range(Aj)
                rl.reverse()
            else:
                r=range(Bj+1,Aj)
                rr=range(Aj+1,12)
                rl=range(Bj)
                rl.reverse()
            if column_search(picture,Ai,Aj,Bi,Bj,r):return True
            if Ai<Bi:
                r=range(Ai+1,Bi)
                rd=range(Bi,12)
                ru=range(Ai)
                ru.reverse()
            else:
                r=range(Bi+1,Ai)
                rd=range(Ai,12)
                ru=range(Bi)
                ru.reverse()
            if row_search(picture,Ai,Aj,Bi,Bj,r):return True
            if column_search(picture,Ai,Aj,Bi,Bj,rl):return True
            if column_search(picture,Ai,Aj,Bi,Bj,rr):return True
            if row_search(picture,Ai,Aj,Bi,Bj,ru):return True
            if row_search(picture,Ai,Aj,Bi,Bj,rd):return True
            print "两点不能连通！"
            return False
    matrix=np.random.randint(0,9,size=(12,12))
    #生成10*10的每个元素为0-8的随机矩阵，外围有一圈是用来存放路径的
    count=np.zeros(9)
    for i in range (1,11):
        for j in range (1,11):count[matrix[i][j]]+=1
    #统计每种元素的个数
    adjust=[]
    for i in range(9):
        if count[i]%2!=0:adjust.append(i)
    n=len(adjust)
    #记录元素个数为奇数的那些元素，由于10*10=100为偶数，奇数元素的个数也为偶数
    k=0
    while(k<n/2):
        for i in range(1,11):
            x=0
            for j in range(1,11):
                if matrix[i][j]==adjust[k]:
                    matrix[i][j]=adjust[n-k-1]
                    x=1
                    break
            if x:break
        k+=1
    #将这些元素分成两部分，将前一部分元素中每一个第一次出现的转换成后一部分对应
    #位置的元素，从而保证每种元素的个数都是偶数，不会出现有元素无法配对的情况
    symbol=['A','B','C','D','E','F','G','H','I']
    picture=[]
    for i in range(12):
        picture.append([])
        for j in range(12):
            if i in [0,11] or j in [0,11]:picture[i].append(' ')
            else:picture[i].append(symbol[matrix[i][j]])
    show_picture(picture)
    #将对应元素转换成字母图形
    left_number=100
    t1=time()
    limit_time=420
    while(left_number):
        t2=time()
        left_time=int(limit_time-(t2-t1))
        if left_time<=0:
            print "你已超时,游戏失败！"
            break
        else:
            print "你还剩",left_time,"s/",limit_time,"s"
        #每一次操作都检验是否超时，第一次检验提示剩余时间
        Ai=insure_input(1,"行")
        t2=time()
        left_time=int(limit_time-(t2-t1))
        if left_time<=0:
            print "你已超时,游戏失败！"
            break
        Aj=insure_input(1,"列")
        t2=time()
        left_time=int(limit_time-(t2-t1))
        if left_time<=0:
            print "你已超时,游戏失败！"
            break
        Bi=insure_input(2,"行")
        t2=time()
        left_time=int(limit_time-(t2-t1))
        if left_time<=0:
            print "你已超时,游戏失败！"
            break
        Bj=insure_input(2,"列")
        t2=time()
        left_time=int(limit_time-(t2-t1))
        if left_time<=0:
            print "你已超时,游戏失败！"
            break
        if find_route(picture,Ai,Aj,Bi,Bj):
            print "消除成功，请继续！"
            left_number=left_number-2
        else:print "请重新输入坐标值！"
    if left_number==0:
        print "恭喜你挑战成功"
    opt=raw_input("是否再来一局？y/n：")
    if opt=='y':lianliankan()
lianliankan()

        

