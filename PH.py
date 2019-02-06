#!env python
import requests
import re
import json

def get_video_uri(viewkey_or_pageuri):
	# 构造页面链接 page_uri
	base_uri = "https://www.pornhub.com/view_video.php"
	if viewkey_or_pageuri[:38] == base_uri:
		page_uri = viewkey_or_pageuri
	else:
		page_uri = base_uri + '?viewkey=' + viewkey_or_pageuri

	# 获取页面链接内容
	try:
		page_content = requests.get(page_uri).text
		# page_content = open('./analyse/view_video.html', encoding='utf-8').read()
	except:
		print('There is some error during getting web page content')
	
	# 提取json字符串
	regexp = r'var flashvars_\d*? = (.*)?;'
	info_str = re.findall(regexp, page_content)[0]
	info_json = json.loads(info_str)

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
	return [video_uri, quality] 