#!/usr/bin/python2
# -*- coding: UTF-8 -*-
'''
###Code Summary###
Author: Jack
E-Mail: wwin3286tw@yahoo.com.tw
Date: 2018-09-12
Time: 09:16:20 GMT+8
Description: BlueTooth classic Serial port C&C&FTP(Control & Communication& Fuck Trust Pig) Server support library
ReadMe: 
1. Using Java like R Resource File.
2. #sed -i -e 's/\r$//' scriptname.sh #If you have DAMN ^M problem, try this shit.
3. Enjoy your fucking salary.
###Code Summary###
'''


##Most frequently access method, so I do not use fucking class.
from datetime import datetime
import io
import sys
import os
import json
import glob
import re
import subprocess
from datetime import datetime

LocalhostName="Server_Localhost"
def ReadFile(filename):
 bin= open(filename,"rb").read()
 return bin
def ReadAllText(filename):
 all_text=""
 with io.open(filename, mode='r', encoding='utf-8') as f:
  all_text=f.read()
 return all_text
def LoadResource(ResourceFile):
 return ReadAllText(ResourceFile)
def GetResource(ResourceFile):
 from collections import namedtuple
 return json.loads(LoadResource(ResourceFile),object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def GetFileLen(filename):
  return str(os.path.getsize(filename))
def ListFilesWithExt(ext):
 return glob.glob("*." + ext )
def GetFileList():
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

class device:
 #sudo udevadm info --query=all /dev/video1 | grep 'VENDOR_ID\|MODEL_ID\|SERIAL_SHORT'
 def usb_info(self):
  device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
  df = subprocess.check_output("lsusb")
  devices = []
  for i in df.split('\n'):
   if i:
    info = device_re.match(i)
    if info:
     dinfo = info.groupdict()
     dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
     devices.append(dinfo)
  return devices
class camera:
 #這裡務必宣告成物件在使用相機 #支援多相機操營養
 def __init__(self,camPath):
  self.CamPath=camPath
 def take_photo(self,Filename):
  os.system("sudo fswebcam -d {0} -r 800x600 --no-title --no-timestamp --no-subtitle --no-shadow --no-banner {1} --png 9".format(self.CamPath,Filename));
 def exists(self):
  return os.path.exists(self.CamPath);
class server:
 def log(self,level,info):
  now=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
  print("{} [{}] - [{}] {}".format(now,LocalhostName,level,info))
  sys.stdout.flush()
 def SendText(self,conn,val):
  import lightblue
  self.log(R.msg_direction.TX,val)
  conn.send(val+'\n')
class common:
 def argc(self,arg_array):
  return len(arg_array.split(' '))
 def GetErrorCode(self,s):
  if s.endswith(")") and s.startswith("("):
   s = s[:-1]
   s = s[1:]
   error_code=s.split(',')[0]
  else:
   error_code=s
  return error_code
ResourceFile="resource.json"
R=GetResource(ResourceFile)
#server().log(R.msg_level.info,R.file_msg.folder_exist)
#cam0=camera('/dev/video0')
#print(cam0.exists())