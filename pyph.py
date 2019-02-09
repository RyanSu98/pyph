#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : RyanSu
# @Filename : pyph.py
# @Mailto   : i@suruifu.com
# @Website  : https://www.suruifu.com/
import os
import re
import sys
import json
import requests
from axel import axel
from bs4 import BeautifulSoup


def pyph(pasted_uri):
	"""
	判断粘贴链接(pasted_uri)类型，分别执行操作
		* 视频播放页面(video_uri)
		* 视频列表页面(list_uri)
	"""
	pasted_uri = pasted_uri.strip()
	if 'view_video.php?viewkey' in pasted_uri:
		print('检测到【视频播放页面】链接，即将开始处理...')
		download_video(pasted_uri)
	else:
		print('检测到【视频列表页面】链接，即将开始处理...')
		download_list(pasted_uri)


def download_video(video_uri):
	""" 下载视频播放页面对应的视频 """
	# 1. 获取视频播放页面网页内容
	video_page_content = get_page_content(video_uri).text
	# 2. 提取视频标题 video_title
	video_title_regexp = r'<title>(.*)? - Pornhub.com</title>'
	video_title = re.findall(video_title_regexp, video_page_content)[0].strip()
	# 3. 提取视频直链 video_direct_uri
	#	3.1 提取存储视频信息的json字符串
	video_info_regexp = r'var flashvars_\d*? = (.*)?;'
	video_info_string = re.findall(video_info_regexp, video_page_content)[0]
	video_info_json = json.loads(video_info_string)
	#	3.2 获取最高画质视频链接
	video_info_array = video_info_json['mediaDefinitions']
	video_quality = 0
	for video_info in video_info_array:
		temp_video_quality = int(video_info['quality'])
		temp_video_direct_uri = video_info['videoUrl']
		if temp_video_direct_uri == '':
			continue
		if temp_video_quality > video_quality:
			video_quality = temp_video_quality
			video_direct_uri = temp_video_direct_uri
	# 4. 下载视频
	axel_download(video_title, video_direct_uri)


def download_list(list_uri):
	""" 下载视频列表页面对应的视频 """
	# 1. 获取网页内容，构造bs对象
	list_page_content = get_page_content(list_uri).content
	list_page_bs = BeautifulSoup(list_page_content, 'html.parser')
	# 2. 获取视频列表
	if len(bs_page.findAll(class_='noVideosNotice')) == 1:
		print('未发现视频链接')
		exit()
	video_uri_array = []
	for video_li_tag in bs_page.findAll(id='videoCategory')[0].findAll('li'):
		video_uri_array.append(video_li_tag.a['href'])
	# 3. 依次下载视频
	for video_uri in video_uri_array:
		download_video(video_uri)


def get_page_content(uri):
	""" 获取网页内容 """
	# 1. 获取代理配置信息
	proxy = json.load(open('config.json'))['proxy'].strip()
	# 2. 重试三次获取网页内容
	for i in [1,2,3]:
		try:
			return requests.get(uri, proxies=dict(http=proxy, https=proxy))
		except:
			continue
		break
	print('获取网页内容失败')
	exit()


def axel_download(file_name, file_uri):
	""" 使用多线程下载程序axel下载文件 """
	print("{}\t开始下载...   下载过程无进度提示，请耐心等待:)".format(file_name))
	# 1. 获取下载配置信息 线程数目 下载文件夹
	config =  json.load(open('config.json'))
	num_connections = config['num_connections']
	output_dir = config['output_dir'].strip()
	# 2. 下载文件夹的前期准备（未配置则是默认文件夹，不存在则创建文件夹）
	if not output_dir:
		output_dir = os.path.join(os.getcwd(), 'ph-video')
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	# 3. 清理之前的下载缓存（例如下载失败之后的不完整文件，如果不清理使用axel下载会报错）
	output_path = os.path.join(output_dir, file_name)+'.mp4'
	if os.path.exists(output_path):
		os.remove(output_path)
	# 4. 下载视频
	axel(file_uri, output_path, num_connections)
	print('{}\t下载成功'.format(file_name))


if __name__ == "__main__":
	pyph(sys.argv[1])