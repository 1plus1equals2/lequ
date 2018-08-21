#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys
import json
import time
import commands
import requests
from urllib import quote
from hashlib import md5
import copy
import traceback
from aeswinpy import *

reload(sys)
sys.setdefaultencoding('utf-8')

API_URL="https://api.bestdjb.com/api/v1.0/song/list?appName=lequ&channel=appstore&os=ios&version=1.1.7&build=4&model=iPhone%206s"
KEY = "AnXPzkdY0y5y5Pxl"
IV = "0102030405060708"

def rep(str1):
	return str1.replace('\t', r'\t').replace('\n', r'\n').replace('\r', r'\r')

def GetMusicList():
	music_list = []
	headers = {
			"Host":"api.bestdjb.com",
			"Content-Type": "application/json",
			"Connection":"keep-alive",
			"Accept":"application/json",
			"User-Agent":"LeQu/1.1.7 iOS/12.0 (iPhone 6s)",
			"Accept-Language":"zh-Hans-CN;q=1",
			"Accept-Encoding":"br, gzip, deflate",
		}

	data = {
	    'lq':'78AQQmdcH5gIN\/SoNTbCfxYAjGspSxuAyc68htdRBqm3TqI7ZtDHnI25Uw9OfBo3I2EjvS\/1lwVCCywu9jqygmNB4ZwNP3n0Jmco2G2LLPJlfasD8xz8dQ1jDSz2EMZib9yFOcpexrM08BvR4NwZT1SZn9mYYlCGhgMy+Ju9edVDQpgDxEGmw47ZUbyXf3Xx5mzbtchjs9\/phmF6wZMLuE+aEzAasYKZDeLBC46duOikrO\/kePM+p1LfUe1X\/vvX5tJOOonRZzYUg5fezL2GhTOpCMLEHu2BWAl6l2guIqtzCuc2zWShY1d2p5E\/o7xwwrj231rwXBQDn3z9dEfLque5KmEJbxFbG1NXTqj8HP98mizLMHtaIuttNcvQzYcwhiEtjEiWBglc0nmHXka7e3mWSB7EEmBUPmSWLFleWC35KWWZPSjq8GyXJefGTfX3YekQ41Kg1lag0qP+VCPc1UHY7jKmBuGqES1sBfiwRmoD27YSDcE4nqTQkSGVQB51S1BkAUIn5MAZZF\/K6NKVqo1BKWf+Svu+cdGf9EnEWyxyqlTfBGAFV8jm3dsHbbYArfGytG1tqVuDemGbeLsBvkwqjBb7bDIpppcsT990NdU3NG7WdK9pC67hbOc5Fkz5HcEPLPi0BXhYcVQLEFpdbZ3LhdnsvD9WXtc6YVVqcelNFwlqzDC4w6yygdmSKaGWT3v+wkJo1QLggkFCn916FcKpXaOQo7YkInNYlwH1o9zszn4vz51TA8EyCOcdDlS\/tLur3Ww3qlva1Fsfmm3UCpXoLaq\/VTPA7MynSAIr6vn0MO3GeVxm1tYXc0RMHzcsnrlR+cnSef4mhaZEWlmnCGuhl9V39T15OCZbF6FMIep3fDPYy0VsAqNuDGO+tXdUjlb0c6hmOZjYtoEk+omLPr6EXLGcHGYJMXl582GtMna9RHfpXPACw5zqS4IPUUr4TfLcYcG4dIeVc6LYcb4xAshvfcmtHRZShKHd3MHyBcyDqdigrmXgOyMBdpmXyoTK9CwAR8caxRHF1Q9ZP5f1nfjGCVYHlwdeE7cKlCIQABW\/wrxTuQ4pnA+cBNfMLjcA+NmVMGQdVFip9pbflvfujXjztkG1Grm3jDN3hc88zmH9QwlPOsVauOZr0HbcG9I9Xg+TI0F9SK+g8cwlWrbU5g6W6FXYioEmsf1Ld4JiwrrHNWLzwjDZHt\/nCgkgpmbJlvl87UoJky1kCYHoLWONDp0kThwYg1\/tTid98NQxYho4c4aRYmsLYS0TeKszaq4\/Yzkuu2gbJWomp5wctTDx69JHCERBDw1JeMXOl9IPruGor+xXtXfBKS0ubBb2ESNQV3k8P1ho0RTBHqSZV0kILE15lfgCzDk9SxQrCDygvj1ucR8afqeyWsiD0k3gqd77PMvggFTsjBmu\/IIgSGtd4RZ38t53b4wr1KLHjuuVcnk='
		}
	try:
		response = requests.post(API_URL, data=json.dumps(data), headers=headers)
		if response.status_code != 200:
			return False,'req_code_error'
		out = json.loads(decrypt(KEY, IV, response.content))
		if out['code'] == 200:
			for info in out['data']['data']:
				t_info = {}
				t_info['uni_id'] = info['uni_id']
				t_info['name'] = rep(info['name'])
				t_info['author'] = rep(info['author'])
				t_info['music_url'] = info['music_url']
				t_info['bg_url'] = info['bg_url']
				t_info['lyrics_url'] = info['lyrics_url']
				t_info['cover_img'] = info['cover_img']
				t_info['translation_url'] = info['translation_url']
				music_list.append(t_info)
			sys.stdout.write('page: %s'  % (out['data']['pagination']['next_page_number']))
			sys.stdout.flush()
		else:
			sys.stderr.write('err_json_code: %s'  % (out['data']['pagination']['next_page_number']))
			sys.stdout.flush()
		return True,music_list
	except:
		return False,'req_conn_error'

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print '%s loop_times outfile' % (sys.argv[0])
		sys.exit(1)

	loop_times = int(sys.argv[1])
	outfile = sys.argv[2]
	
	counter = 0
	fp_out = open(outfile, 'w')
	while counter < loop_times:
		st,music_list = GetMusicList()
		if st == True:
			for info in music_list:
				fp_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (info['uni_id'], info['name'], info['author'], info['music_url'], info['bg_url'], info['lyrics_url'], info['cover_img'], info['translation_url']))
		else:
			sys.stderr.write('err:%s' % (music_list))
			sys.stderr.flush()
		counter += 1
		if counter % 100 == 0:
			time.sleep(0.5)
		
	fp_out.close()
		
