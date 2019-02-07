#!env python
# -*- coding: utf-8 -*-
import requests
import re
import json
import os
import fire
from axel import axel

def get_video_data(page_uri):
	# 代理配置
	proxy = json.load(open('config.json'))['proxy'].strip()
	# 构造页面链接 page_uri
	page_uri = page_uri.strip()
	# 获取页面链接内容
	page_content = requests.get(page_uri, proxies=dict(http=proxy, https=proxy)).text	
	# 提取json字符串
	info_regexp = r'var flashvars_\d*? = (.*)?;'
	info_str = re.findall(info_regexp, page_content)[0]
	info_json = json.loads(info_str)
	# 获取视频标题
	title_regexp = r'<title>(.*)? - Pornhub.com</title>'
	title = re.findall(title_regexp, page_content)[0]
	# 提取最高画质视频链接
	video_array = info_json['mediaDefinitions']
	quality = 0
	for video_li in video_array:
		temp_quality = int(video_li['quality'])
		temp_video_uri = video_li['videoUrl']
		if temp_video_uri == '':
			continue
		if temp_quality > quality:
			quality = temp_quality
			video_uri = temp_video_uri
	return dict(video_uri=video_uri, quality=quality, title=title)


def download_video(video_data):
	# 获取线程数和下载文件夹
	num_connections = json.load(open('config.json'))['num_connections']
	# 设置下载目录,文件名
	output_dir = json.load(open('config.json'))['output_dir'].strip()
	if not output_dir:
		output_dir = os.path.join(os.getcwd(), 'ph-video')
		if not os.path.exists(output_dir):
			os.mkdir(output_dir)
	output_path = os.path.join(output_dir, video_data['title'])+'.mp4'
	if os.path.exists(output_path):
		os.remove(output_path)
	# 开始下载
	axel(video_data['video_uri'], output_path, num_connections)
	print('下载成功')
	return output_path

def move_video(output_path, title):
	dest_path = os.path.join('/pan/', title+'.mp4')
	os.system('mv "{}" "{}"'.format(output_path, dest_path))
	print('移动成功')


data = get_video_data(input('请输入视频页面链接：'))
op = download_video(data)
move_video(op, data['title'])