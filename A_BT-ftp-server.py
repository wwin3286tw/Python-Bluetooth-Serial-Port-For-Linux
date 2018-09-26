#!/usr/bin/python2
# -*- coding: UTF-8 -*-
'''
###Code Summary###
作者: Jack
電子信箱: wwin3286tw@yahoo.com.tw
手機：0970041387
日期: 2018-09-26
時間: 09:16:20 GMT+8
描述: BlueTooth classic Serial port ccFTP(Control & Communication& File Transfer Protocol) Server
讀我: 
1. 使用類似Android的R資源檔
2. 如果你遭遇到腳本的 ^M 錯誤，請使用 sed -i -e 's/\r$//' 腳本名稱.sh
3. 享受吧
版本更新資訊:
1. 程式碼已經重構
2. 命名改進
3. 增加除錯模式，開啟以顯示錯誤
4. 程式碼比以前乾淨數十倍。
5. 增加中文註解、翻譯英文註解
問題(issue)：
1. 可以考慮格式化命令與回應(formatting request command and respone data)
TODO:
1. 可以考慮新增LOG寫入到檔案功能
2. 考慮使用 命令後回應流程，移除人類可讀的描述資訊，進而簡化
   例如：一個命令對應一個回應
###Code Summary###
'''


import BlueServerLib as bsl #自己寫的外部程式庫，模組化並加速開發
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

debugMode=True #是否開啟除錯模式，不開啟將無法看到錯誤訊息
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick! #來自stackoverflow的答案 #https://stackoverflow.com/questions/2276200/changing-default-encoding-of-python
sys.setdefaultencoding('UTF8') #設定預設編碼，不再使用ASCII編碼，避免不必要的編碼錯誤
cam_path='/dev/video1' #設定攝影機位置 #TODO: 偵測正確的相機位置
ResourceFile="resource.json" #資源檔位置
R=bsl.GetResource(ResourceFile) #讀取資源檔
Default_FileName="sample.png" #預設試紙照片儲存檔名
cam0=bsl.camera(cam_path) #建立相機物件
#TransferMethod=1 #廢棄，請在Android端使用，xget 命令來啟動httpd伺服器，然後使用提供的網址進行下載
#使用過xget命令後，httpd伺服器將會一直在線上，除非使用killall命令
#啟動httpd前，務必確認該port無程式占用
#BT=0, WIFI=1
def WriteDefaultResource(): #可能廢棄，若遭遇到資源檔消失的問題，可使用此命令寫回
 resource='{"server_msg":{"error":{"server_encountered_error":"伺服器遭遇錯誤","address_or_port_in_use":"位置或連接口正在被使用中","cam_not_exist":"相機不存在","wifi_not_exist":"WiFi不存在","bt_not_exist":"藍芽不存在","ble_not_exist":"低功耗藍芽不存在","other_devices_fail":"其他裝置啟動失敗，無法啟動","other_devices_not_exist":"其他裝置不存在，無法啟動"},"info":{"restart_server":"伺服器正在重新啟動","user_disconnect":"使用者離線","server_restart_success":"伺服器成功重啟","user_interrupt":"伺服器收到使用者中斷","user_interrupt_and_going_offine":"伺服器收到使用者中斷，準備離線","operaction_done":"操作已經完成","operacting":"操作進行中","new_connection":"[新連線] 來自: {}","brocasting":"廣播並聆聽第{}頻道..."},"warning":{"server_encountered_fixable_error":"伺服器遭遇到可處理的錯誤","server_fixing_error":"伺服器正在嘗試修復錯誤"}},"file_msg":{"file_exist":"檔案存在","folder_exist":"資料夾存在","object_path_exist":"檔案路徑存在","file_not_exist":"檔案不存在","folder_not_exist":"資料夾不存在","object_path_not_exist":"檔案路徑不存在","resource_busy":"資源忙碌中，暫時不可用"},"msg_level":{"info":{"text":"訊息","color":"green"},"warning":{"text":"警告","color":"yellow"},"error":{"text":"錯誤","color":"red"},"debug":{"text":"除錯","color":"white"},"verbose":{"text":"詳細","color":"blue"},"dipshit":{"text":"幹話","color":"gary"}},"msg_direction":{"TX":"送出","RX":"收到"},"local_msg":{"permission_denied":"請以root權限執行本程式","connection_refused":"連線被拒，請使用sudo hciconfig檢查","path_not_found_error":"請檢查設定檔 /etc/systemd/system/dbus-org.bluez.service，是否設定正確","bt_not_available":"請檢查藍芽裝置是否啟動"}}'
 #TODO: 寫回檔案的指令
def doing1(conn,cmd): #只有一個命令(argc=1)的往這裡送 #conn為藍芽連線通道，若有需要，本程式將可支援多連線 #data為命令
 if (cmd=="get"): #取得預設檔名檔案，預設值為sample.png #鬆散的命令方法，不建議使用
  pass
  #bsl.server().SendText(conn,"DEFAULT,-") #廢棄
  #conn.send(bsl.ReadFile(Default_FileName))
  #bsl.server().SendText(conn,"DEFAULT,+")
 elif cmd=="close": #關閉藍芽連線，程式將結束
  flag=False #設定旗標，設定為false程式將不再等待，來自手機藍芽的命令
 #elif cmd=="filelen": #Deprecated, Use ls to get file info.
 # bsl.server().SendText(conn,bsl.getFileLen(Default_FileName))
 elif cmd=="ok": #echo 測試，藉由來回發送ok，測試藍芽連線是否正常
  bsl.server().SendText(conn,"ok") #送回ok給手機端
 elif cmd=="ls": #以json格式送回檔案清單
  bsl.server().SendText(conn,bsl.GetFileList()) #使用library取得檔案清單
 elif cmd=="shot": #拍照命令
  bsl.server().SendText(conn,R.server_msg.info.operacting) #拍照中請稍後
  cam0.take_photo(Default_FileName) #將拍攝檔案儲存為sample.png
  bsl.server().SendText(conn,R.server_msg.info.operaction_done) #拍攝完成
 elif cmd=="camchk": #檢查相機是否存在 #TODO: 檢查是否為特定廠牌的相機，或者就保持寫死video1路徑
  if cam0.exists(): #檢查相機是否存在
   bsl.server().SendText(conn,R.file_msg.object_path_exist) #相機物件"在"路徑上 #無法使用檔案的檢測方法
  else:
   bsl.server().SendText(conn,R.file_msg.object_path_not_exist) #相機物件"不在"路徑上 #無法使用檔案的檢測方法
 elif cmd=="reboot": #重開機，當機台遇到不想解決的問題時，可以使用此命令
  bsl.server().SendText(conn,'rebooting...') #重啟中
  os.system('reboot')
 elif cmd=="bye": #廢棄，為close命令的前身
  pass #填充用的空語句，保持縮排結構完整性
  #bsl.server().SendText(conn,'shuting down!')
 elif cmd=="xget": #這裡採用busybox的httpd applet，簡化設定
  bsl.service().stop_bhttpd_service() #不管有沒有，先送httpd終止命令
  bsl.server().SendText(conn,R.service.bhttpd.starting) #伺服器被啟動了
  bsl.service().start_bhttpd_service(80,".") #開始服務
  # TO DO: 確認服務是否真的被啟動成功
  bsl.server().SendText(conn,R.service.bhttpd.started) #伺服器已經被啟動
 elif cmd=="geturl": #獲取檔案位置
  bsl.server().SendText(conn,"http://{}/sample.png".format(bsl.common().GetIP())) #告知檔案位置。手機即可透過該位置下載檔案

def doing2(conn,data): #argc=2的命令丟這邊
 bsl.server().log(R.msg_level.info,data) #伺服器紀錄
 isfile=os.path.isfile(data.split(' ')[1]) #檢查檔案是否存在 #命令:data.split(' ')[0] #檔名:data.split(' ')[1]
 cmd=data.split()[0]
 if cmd=="get": #藍芽傳送命令，實際上可以傳送任何檔案，檔案接收必須在
  if(isfile): #檔案存在
   #title_start="{},{},{}".format(R.file_msg.file_exist,x,'+') #廢棄，作為檔案開頭，切換模式字串
   #title_end="{},{},{}".format(R.file_msg.file_exist,x,'-')  #廢棄，作為檔案結尾，切換模式字串
   bsl.server().SendText(conn,R.protocol.start_png_mode) #送出檔案開始字串
   bsl.server().SendData(conn,bsl.GetBase64Encode(bsl.ReadFile(data.split()[1]))) #送出檔案經過base64編碼的字串
   bsl.server().SendText(conn,R.protocol.end_png_mode) #送出檔案開始字串
  if (not(isfile)):#檔案不存在
   bsl.server().SendText(conn,R.file_msg.file_not_exist) #檔案不存在
 
def command_selector(conn,cmd): #命令選擇器，根據命令大小，丟給FUNCTION
 if (bsl.common().argc(cmd)==1):
  doing1(conn,cmd)
 elif(bsl.common().argc(cmd)==2):
  doing2(conn,cmd)

def main(restart): #主程式 (是否重啟)
 try: #避免錯誤，捕抓意外情況
  sock = lightblue.socket() #產生socket物件
  sock.bind(("", 1)) #綁定通道，若通道被占用，綁定通道將出錯
  sock.listen(1) #聆聽RFCOMM通道1
  lightblue.advertise("EchoService", sock, lightblue.RFCOMM) #開始廣播服務
  if (restart):#如果重啟旗標為真
   bsl.server().log(R.msg_level.info,R.server_msg.info.server_restart_success) #伺服器重啟成功
  bsl.server().log(R.msg_level.info,R.server_msg.info.brocasting.format(sock.getsockname()[1])) #告知手機綁定通道
  conn, addr = sock.accept() #新連線
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
 except Exception as exception: #捕抓到錯誤
  exceptionString=str(exception) #錯誤原因字串
  if (debugMode): #除錯模式?
   exc_type, exc_obj, exc_tb = sys.exc_info()
   fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
   print("{}, {}, {}, {}".format(exc_type, fname, exc_tb.tb_lineno,exceptionString))
  error_code=bsl.common().GetErrorCode(exceptionString)
  #print('error_code: {}'.format(error_code))
  if (error_code=='98'): #端口正在被使用中例外
   bsl.server().log(R.msg_level.error,R.server_msg.error.address_or_port_in_use)
   terminated = True
  elif (error_code=='104'):#使用者離線例外
   bsl.server().log(R.msg_level.info,R.server_msg.info.user_disconnect)
   bsl.server().log(R.msg_level.info,R.server_msg.warning.server_encountered_fixable_error)
   bsl.server().log(R.msg_level.info,R.server_msg.warning.server_fixing_error)
   conn.close()
   sock.close()
   bsl.server().log(R.msg_level.info,R.server_msg.info.restart_server)
   main(True)
  elif (error_code=='13'): #權限不足例外
   bsl.server().log(R.msg_level.error,R.local_msg.permission_denied)
   terminated = True
  elif (error_code=='111'): #連線被拒例外
   bsl.server().log(R.msg_level.error,R.local_msg.connection_refused)
  
if __name__ == '__main__': #避免程式被誤引入，當作library使用
 main(False)

