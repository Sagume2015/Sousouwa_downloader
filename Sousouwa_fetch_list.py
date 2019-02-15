#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
import sys
from time import sleep


def removeSpaceEntity(s):
    pattern = re.compile('(&#160;|&ensp;|&emsp;)')
    return pattern.sub('', s)

def convertEntity(s):
	pattern = re.compile('(&#([0-9a-fA-F]{4});)')
	return pattern.sub(lambda x: unichr(int(x.group(2), 16)), s)

def brRemove(s):
	brRemover = re.compile(r'<br.*?>')
	return brRemover.sub('\r\n', s)

def divRemove(s):
	divRemover = re.compile(r'(<div.*?>|</div>)')
	return divRemover.sub('', s)

def tagRemove(s):
	tagRemover = re.compile(r'(<.*?>|</.*?>)')
	return tagRemover.sub('', s)

def spaceRemove(s):
	spaceRemover = re.compile(r'( |　|	|\n)')
	return spaceRemover.sub('', s)

def unescape(s):
	s = removeSpaceEntity(s)
	s = convertEntity(s)
	s = brRemove(s)
	s = tagRemove(s)
	return s

def main():
	with open('URL_list.txt', 'r') as f:
		page_id_list = f.read().splitlines()
	
	for page_id in page_id_list:
		res = requests.get(page_id)
		soup = BeautifulSoup(res.text,'lxml')	
		title = soup.find('title')
		body = soup.find('div', id='contentBody')
		aft = soup.find('div', id='afterwordBody')
		title = unescape(str(title))
		body = unescape(str(body))
		aft = unescape(str(aft))	
		bou = "\r\n"*8 + '-'*30 + '\r\n'*2	
		body = body + bou + aft
		filename = './sousouwa_ss/' + title.replace("\t", "", 4).replace("\t", "　").replace(":", "") + '.txt'
		sleep(1)
		if os.path.exists("./sousouwa_ss") == False:
			os.mkdir('./sousouwa_ss')
		with open(filename, 'w') as f: # 書き込みモードで開く
			f.write(body) # 引数の文字列をファイルに書き込む
	
	
if __name__ == '__main__':
	main()
