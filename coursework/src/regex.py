import re

email_txt = """ 
From r  Thu Oct 31 08:11:39 2002
Return-Path: <bensul2004nng@spinfinder.com>
X-Sieve: cmu-sieve 2.0
Return-Path: <bensul2004nng@spinfinder.com>
Message-Id: <200210311310.g9VDANt24674@bloodwork.mr.itd.UM>
From: "Mr. Ben Suleman" <bensul2004nng@spinfinder.com>
Date: Thu, 31 Oct 2002 05:10:00
To: R@M
Subject: URGENT ASSISTANCE /RELATIONSHIP (P)
MIME-Version: 1.0
Content-Type: text/plain;charset="iso-8859-1"
Content-Transfer-Encoding: 7bit
Status: O
"""

pattern = r".xt"
x = re.findall(pattern, email_txt)
# x is *xt 以xt结尾的字符串 且.只是任意一个字符
print(x)


pattern = r"^.z"
x = re.findall(pattern, email_txt)
# x is *xt 以xt结尾的字符串 且.只是任意一个字符
print(x)