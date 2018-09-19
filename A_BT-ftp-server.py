#!/usr/bin/python2
# -*- coding: UTF-8 -*-
'''
###Code Summary###
Author: Jack
E-Mail: wwin3286tw@yahoo.com.tw
Date: 2018-09-12
Time: 09:16:20 GMT+8
Description: BlueTooth classic Serial port ccFTP(Control & Communication& File Transfer Protocol) Server
ReadMe: 
1. Using Java like R Resource File.
2. #sed -i -e 's/\r$//' scriptname.sh #If you have DAMN ^M problem, try this shit.
3. Enjoy fucking salary.
Version Change info:
1. Code Refactoried.
2. Naming improved.
3. Add debug mode, Enable to show exception.
4. Code more clear than before. Although cannot see the older code.
###Code Summary###
'''


import BlueServerLib as bsl
import os
import sys
import base64
import time
import glob
import time
import json
import subprocess
import os.path
from datetime import datetime
import lightblue
import sys
debugMode=True
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

cam_path='/dev/video1'
ResourceFile="resource.json"
R=bsl.GetResource(ResourceFile)
Default_FileName="sample.png"
cam0=bsl.camera(cam_path)

def WriteDefaultResource():
 resource='{"server_msg":{"error":{"server_encountered_error":"伺服器遭遇錯誤","address_or_port_in_use":"位置或連接口正在被使用中","cam_not_exist":"相機不存在","wifi_not_exist":"WiFi不存在","bt_not_exist":"藍芽不存在","ble_not_exist":"低功耗藍芽不存在","other_devices_fail":"其他裝置啟動失敗，無法啟動","other_devices_not_exist":"其他裝置不存在，無法啟動"},"info":{"restart_server":"伺服器正在重新啟動","user_disconnect":"使用者離線","server_restart_success":"伺服器成功重啟","user_interrupt":"伺服器收到使用者中斷","user_interrupt_and_going_offine":"伺服器收到使用者中斷，準備離線","operaction_done":"操作已經完成","operacting":"操作進行中","new_connection":"[新連線] 來自: {}","brocasting":"廣播並聆聽第{}頻道..."},"warning":{"server_encountered_fixable_error":"伺服器遭遇到可處理的錯誤","server_fixing_error":"伺服器正在嘗試修復錯誤"}},"file_msg":{"file_exist":"檔案存在","folder_exist":"資料夾存在","object_path_exist":"檔案路徑存在","file_not_exist":"檔案不存在","folder_not_exist":"資料夾不存在","object_path_not_exist":"檔案路徑不存在","resource_busy":"資源忙碌中，暫時不可用"},"msg_level":{"info":{"text":"訊息","color":"green"},"warning":{"text":"警告","color":"yellow"},"error":{"text":"錯誤","color":"red"},"debug":{"text":"除錯","color":"white"},"verbose":{"text":"詳細","color":"blue"},"dipshit":{"text":"幹話","color":"gary"}},"msg_direction":{"TX":"送出","RX":"收到"},"local_msg":{"permission_denied":"請以root權限執行本程式","connection_refused":"連線被拒，請使用sudo hciconfig檢查","path_not_found_error":"請檢查設定檔 /etc/systemd/system/dbus-org.bluez.service，是否設定正確","bt_not_available":"請檢查藍芽裝置是否啟動"}}'


def doing1(conn,data):
 if (data=="get"):
  bsl.server().SendText(conn,"DEFAULT,-")
  conn.send(bsl.ReadFile(Default_FileName))
  bsl.server().SendText(conn,"DEFAULT,+")
 elif data=="close":
  flag=False
 #elif data=="filelen": #Deprecated, Use ls to get file info.
 # bsl.server().SendText(conn,bsl.getFileLen(Default_FileName))
 elif data=="ok":
  bsl.server().SendText(conn,"ok")
 elif data=="ls":
  bsl.server().SendText(conn,bsl.GetFileList())
 elif data=="shot":
  bsl.server().SendText(conn,R.server_msg.info.operacting)
  cam0.take_photo(Default_FileName)
  bsl.server().SendText(conn,R.server_msg.info.operaction_done)
 elif data=="camchk":
  if cam0.exists():
   bsl.server().SendText(conn,R.file_msg.object_path_exist)
  else:
   bsl.server().SendText(conn,R.file_msg.object_path_not_exist)
 elif data=="reboot":
  bsl.server().SendText(conn,'rebooting...')
  os.system('reboot')
 elif data=="bye":
  bsl.server().SendText(conn,'shuting down!')

def doing2(conn,data):
 bsl.server().log(R.msg_level.info,data)
 x=os.path.isfile(data.split(' ')[1])
 if data.split()[0]=="get":
 #if (data.split()[1]!=""):
  #print(x)
  if(x):
   title_start="{},{},{}".format(R.file_msg.file_exist,x,'+')
   title_end="{},{},{}".format(R.file_msg.file_exist,x,'-')
   bsl.server().SendText(conn,title_start)
   conn.send(bsl.ReadFile(data.split()[1]))
   bsl.server().SendText(conn,title_end)
  if (not(x)):
   bsl.server().SendText(conn,R.file_msg.file_not_exist)
def command_selector(conn,cmd):
 if (bsl.common().argc(cmd)==1):
  doing1(conn,cmd)
 elif(bsl.common().argc(cmd)==2):
  doing2(conn,cmd)

def main(restart):
 try:
  sock = lightblue.socket()
  sock.bind(("", 1))
  sock.listen(1)
  lightblue.advertise("EchoService", sock, lightblue.RFCOMM)
  if (restart):
   bsl.server().log(R.msg_level.info,R.server_msg.info.server_restart_success)
  bsl.server().log(R.msg_level.info,R.server_msg.info.brocasting.format(sock.getsockname()[1]))
  conn, addr = sock.accept()
  bsl.server().log(R.msg_level.info,R.server_msg.info.new_connection.format(addr[0]))
  flag=True
  while(flag):
   data = conn.recv(1024).rstrip()
   #print(data)
   bsl.server().log(R.msg_level.info,"{} {}".format(R.msg_direction.RX,data))
   command_selector(conn,data)
 except KeyboardInterrupt:
  print
  bsl.server().log(R.msg_level.info,R.server_msg.info.user_interrupt)
  exit();
 except Exception as exception:
  exceptionString=str(exception)
  if (debugMode):
   exc_type, exc_obj, exc_tb = sys.exc_info()
   fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
   print("{}, {}, {}, {}".format(exc_type, fname, exc_tb.tb_lineno,exceptionString))
  error_code=bsl.common().GetErrorCode(exceptionString)
  #print('error_code: {}'.format(error_code))
  if (error_code=='98'):
   bsl.server().log(R.msg_level.error,R.server_msg.error.address_or_port_in_use)
   terminated = True
  elif (error_code=='104'):
   bsl.server().log(R.msg_level.info,R.server_msg.info.user_disconnect)
   bsl.server().log(R.msg_level.info,R.server_msg.warning.server_encountered_fixable_error)
   bsl.server().log(R.msg_level.info,R.server_msg.warning.server_fixing_error)
   conn.close()
   sock.close()
   bsl.server().log(R.msg_level.info,R.server_msg.info.restart_server)
   main(True)
  elif (error_code=='13'):
   bsl.server().log(R.msg_level.error,R.local_msg.permission_denied)
   terminated = True
  elif (error_code=='111'):
   bsl.server().log(R.msg_level.error,R.local_msg.connection_refused)
  
if __name__ == '__main__':
 main(False)

