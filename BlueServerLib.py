#!/usr/bin/python2
# -*- coding: UTF-8 -*-
'''
###Code Summary###
Author: Jack
E-Mail: wwin3286tw@yahoo.com.tw
Tested Date: 2018-09-14 11:39:15 GMT+8
Description: BlueTooth classic Serial port ccFTP(Control & Communication& Fuck Trust Pig) Server support library
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

##最常用的方法，為了減少複雜性，不使用class
##Most frequently access method, so I do not use fucking class.
from datetime import datetime
import io
import sys
import os
import json
import glob
import re
import base64
import socket
import subprocess
from datetime import datetime
from termcolor import colored
LocalhostName="Server_Localhost"
def ReadFile(filename): #讀取檔案(檔名) #I:檔名, O:二進位資料
 bin= open(filename,"rb").read()
 return bin
def GetBase64Encode(bin): #將二進位資料轉成Base64字串 #I: 二進位資料, O:Base64編碼後字串
 return base64.b64encode(bin)

def GetBase64Decode(bin): #將Base64字串資料轉成二進位 #I:Base64編碼後字串, O:二進位資料
 return base64.b64decode(bin)

def ReadAllText(filename): #讀取檔案所有資料  #I:檔案名稱, 字串資料
 all_text=""
 with io.open(filename, mode='r', encoding='utf-8') as f:
  all_text=f.read()
 return all_text
def LoadResource(ResourceFile): #讀取資源檔 #I:資源檔名稱, O:資源檔全部內容，JSON字串
 return ReadAllText(ResourceFile) #調用讀取全部文字function
def GetResource(ResourceFile): #將JSON轉成好用的物件格式，可以使用"."點存取資源檔(feed Google dog: JSON to Python object)
 from collections import namedtuple
 return json.loads(LoadResource(ResourceFile),object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
 

def GetFileLen(filename): #取得檔案大小
  return str(os.path.getsize(filename))
def ListFilesWithExt(ext): #取得經過副檔名 篩選後的檔案清單
 return glob.glob("*." + ext )
def GetFileList(): #取得檔案清單
 list="[";files=ListFilesWithExt('png');fileCount=len(files);count=0;
 for file in files: 
  count+=1;
  if (count<=fileCount-1):
   list+= json.dumps({'name':file,'size':GetFileLen(file)},separators=(',',':')) + ","
  else:
   list+= json.dumps({'name':file,'size':GetFileLen(file)},separators=(',',':'))
 list+="]"
 return list
##Most frequently use
class service: #服務
 def start_bhttpd_service(self,port,dir): #啟動busybox_httpd服務
  os.system("sudo busybox httpd -p {0} -h {1}".format(port,dir)) #
 def stop_bhttpd_service(self): #停止busybox_httpd服務
  os.system("sudo killall busybox") #把busybox殺掉就可以停止服務
class device: #外部裝置(外設)
 #sudo udevadm info --query=all /dev/video1 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'
 def usb_info(self): #尚未使用，但未廢棄，可以返回USB資訊清單，供確認是否使用正確的USB相機 #參考：https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python
  device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I) #神奇又萬用的正規表達式
  df = subprocess.check_output("lsusb") #這裡都是狗吐給我的，所以不解釋囉~
  devices = []
  for i in df.split('\n'):
   if i:
    info = device_re.match(i)
    if info:
     dinfo = info.groupdict()
     dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
     devices.append(dinfo)
  return devices
class camera: #相機物件
 #這裡務必宣告成物件在使用相機 #支援多相機操營養
 def __init__(self,camPath): #初始化相機物件
  self.CamPath=camPath
 def take_photo(self,Filename): #拍一張照片 #TODO: 如果需要設定更多選項，可以變動下面的指令參數，請餵狗：fswebcam
  os.system("sudo fswebcam -d {0} -r 800x600 --no-title --no-timestamp --no-subtitle --no-shadow --no-banner {1} --png 9".format(self.CamPath,Filename));
 def exists(self): #確認相機是否存在
  return os.path.exists(self.CamPath);
class server: #伺服器
 def log(self,level,info): #伺服器紀錄器，主要會顯示在機台上
  now=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
  print("{} [{}] - [{}] {}".format(now,LocalhostName,colored(level.text,level.color),info)) #紀錄會依層級給予不同的顏色 [資訊]、[警告]、[錯誤]
  sys.stdout.flush()#立刻顯示，不拖延，python有個懶惰的特性，print資料不會是即時，需要用命令讓他立刻顯示
 def SendText(self,conn,val): 
  import lightblue
  self.log(R.msg_level.info,"{} {}".format(R.msg_direction.TX,val))
  conn.send(val+'\n')
 def SendData(self,conn,val):
  import lightblue
  #self.log(R.msg_level.info,"{} {}".format(R.msg_direction.TX,val))
  conn.send(val+'\n')
class common:
 def argc(self,arg_array): #計算命令的長度，有幾個空格分開
  return len(arg_array.split(' '))
 def GetErrorCode(self,s):
  if s.endswith(")") and s.startswith("("):
   s = s[:-1]
   s = s[1:]
   error_code=s.split(',')[0]
  else:
   error_code=s
  return error_code
 def GetIP(self): #獲得機台IP位置
  return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
  #參考：https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
ResourceFile="resource.json"
R=GetResource(ResourceFile)
##圖書館遊樂場(Library Playground)##
#可以在這裡除錯，隨你玩。
#print(R.services.bhttpd.starting)
#server().log(R.msg_level.info,R.file_msg.folder_exist)
#cam0=camera('/dev/video0')
#print(cam0.exists())