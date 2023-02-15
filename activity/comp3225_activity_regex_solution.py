# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2022
#
# Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Mercedes Arguello Casteleiro
# Created Date : 2023/02/10
# Project : Teaching
# Restriction: Content for internal use at University of Southampton only
#
######################################################################

### *** *** *** *** *** *** *** *** ***
### Fraudulent E-mail Corpus
### 6 MB with 4,075 fraudulent e-mails
### https://www.kaggle.com/datasets/rtatman/fraudulent-email-corpus
### *** *** *** *** *** *** *** *** ***
# ______________________________________________________
### Part 1
# ______________________________________________________
### Let's have some text from the Fraudulent E-mail Corpus

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

### let's do a quick check
print('_______________') 
print (email_txt)
print ('_______________')

# ______________________________________________________
### Let's start with some simple tasks
### (a) Let's search for email subjects

x = re.findall(r'Subject:.*', email_txt)
print(x)

# ______________________________________________________
### Another simple task
### (b) Let's search for strings that start with '<' and end with '>'

x = re.findall(r'<(.+?)>', email_txt)
print(x)

# ______________________________________________________
### Another simple task
### (c) Let's find multiple alternatives for returning the first string that starts with '<' and ends with '>'

x = re.findall(r'<(.+?)>', email_txt)[0]
print(x)
x = re.findall(r'<(.*?)>', email_txt)[0]
print(x)
x = re.findall(r'<(.*)>', email_txt)[0]
print(x)

x = re.search('<([^<>]*)>', email_txt)
print(x.group(1))

# ______________________________________________________
### Part 2
# ______________________________________________________
### Let's find some common Python Regex Patterns
### Let's concentrate on the lines with 'From:'

email2_txt = """ 
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
... ... ...
... ... ...
From r  Thu Oct 31 17:27:16 2002
Return-Path: <obong_715@epatra.com>
X-Sieve: cmu-sieve 2.0
Return-Path: <obong_715@epatra.com>
Message-Id: <200210312227.g9VMQvDj017948@bluewhale.cs.CU>
From: "PRINCE OBONG ELEME" <obong_715@epatra.com>
Reply-To: obong_715@epatra.com
To: webmaster@aclweb.org
Date: Thu, 31 Oct 2002 22:17:55 +0100
Subject: GOOD DAY TO YOU
X-Mailer: Microsoft Outlook Express 5.00.2919.6900DM
MIME-Version: 1.0
Content-Type: text/plain; charset="us-ascii"
Content-Transfer-Encoding: 8bit
X-MIME-Autoconverted: from quoted-printable to 8bit by sideshowmel.si.UM id g9VMRBW20642
Status: RO
"""

### let's do a quick check
print('_______________') 
print (email2_txt)
print ('_______________')

# ______________________________________________________
### (d) Let's split the text into lines using the re module

line = re.split("\n", email2_txt)

### let's do a quick check
print('...' + line[2] + '...') 
### ...Return-Path: <bensul2004nng@spinfinder.com>...

# ______________________________________________________
### (e) Let's find the lines with 'From:'

for line in re.findall("From:.", email2_txt):
    print(line)

### we know the lines, we do not know the content!

for line in re.findall("From:.*", email2_txt):
    print(line)

### we know the lines, and we also know the content!

# ______________________________________________________
### (f) Let's find the lines with 'From:' skipping the email

ptn = re.findall("From:.*", email2_txt)
for line in ptn:
    print(re.findall('\".*\"', line))

### Using the backslash other special characters are avoided, such as < left angle bracket

# ______________________________________________________
### (g) Let's find the lines with 'From:' and keeping Only the email address

ptn = re.findall("From:.*", email2_txt)
for line in ptn:
    print(re.findall("\w\S*@", line))
    print(re.findall("\w\S*@.*\w", line))

### w matches alphanumeric characters
### S matches non-whitespace characters
### "\w\S*@" versus "\w\S*@.*\w"
### "@.*" gets the ending of the email address

# ______________________________________________________
### Part 3
# ______________________________________________________
### (h) Let's find time stamps

ts_regex = re.compile(r'\d\d:\d\d:\d\d')

### let's do a quick check

ts_ds = ts_regex.search('From r  Thu Oct 31 17:27:16 2002')
print(f'found: {ts_ds.group()}')

ts_regex = re.compile(r'\d\d:\d\d:\d\d')
lines = re.split("\n", email2_txt)
for line in lines:
  ts_m = ts_regex.search(line)
  if ts_m:
    print('Time Stamp found: ', ts_m.group() + ' in <line>' + line + '</line>')

# ______________________________________________________
### (i) Let's find time stamps with the year appearing After the time stamp

lines = re.split("\n", email2_txt)
ts_regex = re.compile(r'(?<=\d\d:\d\d:\d\d[ ])\d{4}')
for line in lines:
  ts_m = ts_regex.search(line)
  if ts_m:
    print('Time Stamp found: ', ts_m.group() + ' in <line>' + line + '</line>')

### we used positive lookbehind (?<=text)

# ______________________________________________________
### (j) Let's find time stamps with the year Not appearing Before the time stamp

lines = re.split("\n", email2_txt)
ts_regex = re.compile(r'(?<!\d{4}[ ])\d\d:\d\d:\d\d')
for line in lines:
  ts_m = ts_regex.search(line)
  if ts_m:
    print('Time Stamp found: ', ts_m.group() + ' in <line>' + line + '</line>')

### we used Negative lookbehind (?<!text)

# ______________________________________________________
### (k) Let's find time stamps with the Year appearing Before the time stamp

lines = re.split("\n", email2_txt)
ts_regex = re.compile(r'(?<=\d{4}[ ])\d\d:\d\d:\d\d')
for line in lines:
  ts_m = ts_regex.search(line)
  if ts_m:
    print('Time Stamp found: ', ts_m.group() + ' in <line>' + line + '</line>')

### we used positive lookbehind (?<=text)