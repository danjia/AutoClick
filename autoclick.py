#-*- coding:utf-8 -*-
#========================================
# @brief 通过配置坐标实现鼠标自动
#        点击(类似按键精灵)
#========================================


from ctypes import *
import os
import pyHook
import pythoncom
import random
import sys
import time
import threading
import win32api
import win32con


# #中断标志位
# global g_interrupt
# g_interrupt = False

#是否自动关机
global g_isAutoShutdown
g_isAutoShutdown = False


#保存最近2个按下的按键
global g_last2PressKey
g_last2PressKey = ["", ""]



#========================
# @brief 鼠标移动
#========================
def mouseMove(x, y):
	windll.user32.SetCursorPos(x, y)

#========================
# @brief 鼠标点击(左键)
#========================
def mouseClick():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


#========================
# @brief 处理点击
#========================
def dealWithClick(x, y):
	print("click", x, y)
	mouseMove(x, y)
	mouseClick()

#=======================================
# @brief 自动点击
# @params costTime 自动点击的时常
#         clickPos 自动点击的位置坐标
#         isAutoShutdown 是否自动关机
#=======================================
def autoClick(costTime, clickPos):
	global g_interrupt
	global g_isAutoShutdown

	if g_isAutoShutdown:
		print("auto shutdown after:", costTime+5, "seconds...")
		os.system("shutdown -s -t "+str(costTime+5))
	curPos = win32api.GetCursorPos()
	cnt = 0
	sleepTime = 20
	total = costTime/sleepTime
	while True:
		#点击初始化的地方
		dealWithClick(curPos[0]+5, curPos[1]+5)

		#移动到某个点
		pos = clickPos[random.randint(0, 5)]
		dealWithClick(pos[0]+curPos[0], pos[1]+curPos[1])

		time.sleep(sleepTime)
		cnt = cnt +1
		if cnt >= total:
			break
	print("run finish!!!")
	


#============================
# @brief 键盘事件处理
#============================
def onKeyboardEvent(event):
	# print "MessageName:", event.MessageName
	# print "Message:", event.Message     
	# print "Time:", event.Time     
	# print "Window:", event.Window     
	# print "WindowName:", event.WindowName     
	# print "Ascii:", event.Ascii, chr(event.Ascii)     
	# print "Key:", event.Key     
	# print "KeyID:", event.KeyID     
	# print "ScanCode:", event.ScanCode     
	# print "Extended:", event.Extended     
	# print "Injected:", event.Injected     
	# print "Alt", event.Alt     
	# print "Transition", event.Transition
	#保存最新按得两个按键
	global g_last2PressKey
	g_last2PressKey[0] = g_last2PressKey[1]
	g_last2PressKey[1] = event.Key
	
	#如果是Ctrl + C
	if "Lcontrol" == g_last2PressKey[0] and\
		"C" == g_last2PressKey[1]:
		global g_isAutoShutdown
		if g_isAutoShutdown:
			print("cancle shutdown")
			os.system("shutdown -a")#取消关机任务
		os._exit(0)

	return True


#===============================
# @brief 全局监听键盘事件
#===============================
def hook():
	print("begin to hook the keyboard")
	hm = pyHook.HookManager()
	hm.KeyDown = onKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages()


if "__main__" == __name__:
    #=====================================
	#              参数设置
	#=====================================
	#自动关机
	g_isAutoShutdown = True
	#点击坐标
	clickPos = [\
		(454, 192), (704, 200), (946,200),\
		(464, 351), (704, 354), (946, 361)]
	#要运行多长时间
	costTime = 50
	# costTime = 50*60

	#=====================================
	#               开始
	#=====================================
	#全局监键盘事件
	waitForList = []
	tHook = threading.Thread(target=hook)
	waitForList.append(tHook)
	tHook.start()
	#自动点击
	tAutoClick = threading.Thread(target=autoClick, args=(costTime, clickPos))
	waitForList.append(tAutoClick)
	tAutoClick.start()
	#等待
	for t in waitForList:
		t.join()
	print("exit main")
