# pornhub下载器
## 开发灵感
* 海外服务器下载速度较慢，使用体验很差（还是我天朝的东西好）
* 一直觉得这个网站中的人讲英语讲得非常native，学习一下

## 功能要点
* 支持视频播放页面视频下载
* 支持视频列表页面视频下载
* 支持多线程下载

## 目前不足
* 仅支持linux平台使用
* 下载进度不能实时展示
* ...

## 参考项目
https://github.com/blackmatch/pornhub-downloader
https://github.com/formateddd/pornhub

## 配置过程
* 下载此项目到你的主机中`git clone https://github.com/RyanSu98/pyph.git && cd pyph`
* 安装依赖`pip3 install -r requirements.txt`
* 安装多线程下载程序axel `sudo apt install axel`
* 若使用代理，仍需手动设置环境变量
```
export http_proxy=socks5h://127.0.0.1:1080
export https_proxy=socks5h://127.0.0.1:1080
```
* 程序配置
`cp config.json.example config.json`

num_connections 线程数 我在digitalocean上面开40个线程下载速度可以达到十几兆每秒，请以实际坏境为准

## 下载测试
* 视频播放页面下载 `python3 pyph.py "https://www.pornhub.com/view_video.php?viewkey=ph5c15d3fda4987"`
```bash
检测到【视频播放页面】链接，即将开始处理...
Twerking in  Masturbating       开始下载...   下载过程无进度提示，请耐心等待:)
Twerking in  Masturbating       下载成功

ubuntu@seoul:~/pyph$ ls ph-video/
'Twerking in  Masturbating.mp4'
```
* 视频列表页面下载 `python3 pyph.py "https://www.pornhub.com/video?o=ht&cc=us"`
```
ubuntu@seoul:~/pyph$ python3 pyph.py "https://www.pornhub.com/video?o=ht&cc=us"
检测到【视频列表页面】链接，即将开始处理...
Sister in Law Begs for Cock FULL SERIES 开始下载...   下载过程无进度提示，请耐心等待:)
Sister in Law Begs for Cock FULL SERIES 下载成功
Bratty Sis - Step Brother and Sister Share A Bed and Fuck S8:E1 开始下载...   下载过程无进度提示，请耐心等待:)
Bratty Sis - Step Brother and Sister Share A Bed and Fuck S8:E1 下载成功
The best Squirter ever  开始下载...   下载过程无进度提示，请耐心等待:)
```

## 开源协议
Do What The F*ck You Want To Public License 

## 写在最后
欢迎pr代码
