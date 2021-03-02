# -*- coding: utf-8 -*-
# @Time    : 2021/03/02 06:30
# @Author  : womade
# @Email   : admin@ssss.fun
import smtplib,traceback,os,requests,urllib
from email.mime.text import MIMEText

#返回要推送的通知内容
#对markdown的适配要更好
def readFile(filepath):
    content = ''
    for line in open(filepath):
        content += line + '\n\n'
    return content

#邮件推送
def sendEmail(email):
    try:
        #要发送邮件内容
        content = readFile('./log.txt')
        #接收方邮箱
        receivers = email
        #邮件主题
        subject = 'UnicomTask每日报表'
        param1 = '?subject=' + subject + '&b1=' + content
        param2 = '?subject=' + subject + '&a1=' + content
        res1 = requests.get('https://api.ssss.fun/push/post.php' + param1)
        res1.encoding = 'utf-8'
        res1 = res1.json()
        if res1['Code'] == '1':
            print(res1['msg'])
        else:
            #备用推送
            requests.get('https://email.berfen.com/api' + param2)
            print('email push BER')
            #这里不知道为什么，在很多情况下返回的不是 json，
            # 但在测试过程中成功率极高,因此直接输出
    except Exception as e:
        print('邮件推送异常，原因为: ' + str(e))
        print(traceback.format_exc())

#钉钉群自定义机器人推送
def sendDing(webhook):
    try:
        #要发送邮件内容
        content = readFile('./log.txt')
        data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': 'UnicomTask每日报表',
                'text': content
            }
        }
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        res = requests.post(webhook,headers=headers,json=data)
        res.encoding = 'utf-8'
        res = res.json()
        print('dinngTalk push : ' + res['errmsg'])
    except Exception as e:
        print('钉钉机器人推送异常，原因为: ' + str(e))
        print(traceback.format_exc())

#发送Tg通知
def sendTg(token,chat_id):
    try:
        #发送内容
        content = readFile('./log.txt')
        data = {
            'UnicomTask每日报表':content
        }
        content = urllib.parse.urlencode(data)
        #TG_BOT的token
        #token = os.environ.get('TG_TOKEN')
        #用户的ID
        #chat_id = os.environ.get('TG_USERID')
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={content}'
        session = requests.Session()
        resp = session.post(url)
        print(resp)
    except Exception as e:
        print('Tg通知推送异常，原因为: ' + str(e))
        print(traceback.format_exc())