#!/anaconda3/bin/python3
# coding: utf-8

import requests
import os
import subprocess
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Step 1. Setting up all the param below

## 常用WIFI清单 - 添加常用WIFI清单，当连接下列WIFI时，不会定时拍照、截屏
safe_wifi_list = ['XXXX', 'XXXX', 'XXXX']

## 固定参数
exe_time = time.gmtime() ### 不可删除，用于检查程序运行时间
unsafe_min_time = 15 ### 当分钟被15整除的时候，执行
safe_min_time = 60 ### 当分钟被60整除的时候，执行
safe_hr_time = 2 ### 当24时制的消失被2整除的时候，执行

## Log路径/名称
log_name = time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.log' ### YYYY/MM/DD_HHMMSS.log
log_path = '~/Documents/GPS_Record/' ### 存储截屏、视频拍照、当前链接WIFI

## 邮件服务器/登入账号/登录密码或API_Secret
smtp_srv = "smtp.qq.com"
_user = "XXXXXXX@qq.com"
_pwd = "XXXXXXXX"

def send_mail(to_addr, title, content, from_addr, att_path = "", att_name = ""):
    ### 初始宣告
    msg = MIMEMultipart()

    ### 发信人、收件人、主题、内文
    ### 发件人可以随意乱填写
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = title
    msg.attach(MIMEText(content))

    ### 判定是否有附件路径和附件名称
    if att_name != "" and att_path != "":
        part = MIMEApplication(open(att_path + att_name ,'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename = att_name)
        msg.attach(part)

    try:
        srv = smtplib.SMTP(smtp_srv, timeout = 30) ### 连接smtp邮件服务器,端口默认是25
        srv.login(_user, _pwd) ### 登录
        srv.sendmail(_user, to_addr, msg.as_string()) ### 发信
        print("发送成功")

    except Exception as e:
        print("发送失败")
    
    finally:
        srv.close()

def get_ssid():
    cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | sed -e "s/^  *SSID: //p" -e d'
    ### return example 'SSID_NAME\n'
    res = os.popen(cmd).read()
    if res == '':
        res = 'NOT CONNECTED'
        return res
    else:
        return res[:-1:]

def scan_wifi():
    cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s'
    res = os.popen(cmd).read()
    return res

def get_gps():
    # Step 2. Add the path
    cmd = "XXXXXXXXXX/whereami" ### The path of the whereami_executable_file
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output = str(output)
    lat = output[output.rfind("Latitude:")+ len("Latitude: "):output.rfind("Latitude:")+ len("Latitude: ")+9]
    log = output[output.rfind("Longitude:")+ len("Longitude: "):output.rfind("Longitude:")+ len("Longitude: ")+9]
    return lat, log

def cmd_exe(cmd):
    os.system(cmd)

def take_sceenshot(execute_time):
    cmd = 'screencapture -x ' + log_path + str(execute_time[0:-4:]) + ".jpg"
    cmd_exe(cmd)

def take_webcameshot(execute_time):
    # Step 3. Install imagesnap using command in terminal - 'brew install imagesnap'
    cmd = 'imagesnap -w 1 ' + log_path + str(execute_time[0:-4:]) + ".png"
    cmd_exe(cmd)

def zip_file(execute_time):
    cmd = 'zip -q' + log_path + str(execute_time[0:-4:]) + ".zip " + log_path + str(execute_time[0:-4:]) + ".*"
    cmd_exe(cmd)

if __name__ == '__main__':
    if get_ssid() not in safe_wifi_list: ### 判断是否使用安全WIFI
        if exe_time[4] % unsafe_min_time != 0: ### 分钟被15整除（00，15，30，45，60）时候，执行：LOG/拍照/截屏/发送记录
            t3 = "===== Wifi List =====\n" + scan_wifi()
            t1 = "SSID: " + str(get_ssid()) + "\n"
            t2 = "GPS: " + str(get_gps()) + "\n"
            tmp_text = t1 + t2 + t3
            cmd = "echo " + "\"" +tmp_text + "\"" + " >> " + log_path + log_name 
            cmd_exe(cmd)

            ## Extra Safe Check
            take_sceenshot(log_name) ### 截屏
            take_webcameshot(log_name) ### 视频牌照
            zip_file(log_name) ### 压缩记录
            # Step 4. Setup your email address
            send_mail("TO_YOUR_ADD", "【GPS】" + str(log_name[0:-4:]) , tmp_text, "FROM_YOUR_ADDRESS", 'FILE_PATH', str(log_name[0:-4:]) + ".zip") ### Send Email with attachment

    else:
        if exe_time[4] % safe_min_time != 0: ### 分钟被60整除（00，60）时候，执行：LOG
            t3 = "===== Wifi List =====\n" + scan_wifi()
            t1 = "SSID: " + str(get_ssid()) + "\n"
            t2 = "GPS: " + str(get_gps()) + "\n"
            tmp_text = t1 + t2 + t3
            cmd = "echo " + "\"" +tmp_text + "\"" + " >> " + log_path + log_name 
            cmd_exe(cmd)

            if (exe_time[3] + 8) % safe_hr_time != 0: ### 消失被2整除（0，2，4，6，8，10，12，14，16，18，20，22，24）时候，执行：发送LOG
                
                send_mail("TO_YOUR_ADD", "【GPS】" + str(log_name[0:-4:]) , tmp_text, "FROM_YOUR_ADDRESS") ### Send Email with attachment


    cmd_exe('rm -rf ' + log_path + "*.zip") ### 清除临时生成的压缩包
