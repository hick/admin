# -*- coding: UTF-8 -*-
import re
import sys
import json

import importlib

from django.http import HttpResponse
from chip.models import Chip
from django.template import RequestContext, loader

from django.shortcuts import render

### 工具函数，去掉默认转换出来的链接和图片中的换行符
def trip_link_break(txt):
    match_list = re.findall("[\(\[].*[\n\r]+.*[\]\)]", txt)
    for seg in match_list:
        new_seg = seg.replace("\n", "")
        new_seg = new_seg.replace("\r", "")
        txt = txt.replace(seg, new_seg)
    return txt



def index(request):
    ### 这就是控制器的, 我晕
    latest_chip_list = Chip.objects.order_by('-pub_time')[:100]
    # latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_chip_list': latest_chip_list}
    return render(request, 'chip/index.html', context)


def detail(request, chip_id):
    return HttpResponse("You're looking at chip %s." % chip_id)

def results(request, chip_id):
    return HttpResponse("You're looking at the results of chip %s." % chip_id)

def fetch(request, fetch_url):
    """参数 fetch_url 规则定义  url@selector"""
    import urllib2, sys
    import urllib
    import re
    import json
    from bs4 import BeautifulSoup
    import sqlite3
    import time
    import html2text

    # 追加 spider 包相关控制
    sys.path.insert(0, 'E:\\MyDocument\\KuaiPan\\source\\utls\\spide')
    import utl # 下载 url 等


    ######################################################### 解析参数 
    # 参数分隔符 @ ， 如果 url 中有出现 # 会被替换成 & ，所以下面有还原
    param_arr = fetch_url.split('@')
    # 来源名为第二个参数
    origin_name = ''
    if len(param_arr) > 1:
        origin_name  = param_arr[1]
    # 选择器为第三个参数
    css_selector = ''
    if len(param_arr) > 2:
        css_selector = param_arr[2]
        css_selector = css_selector.replace('&', '#')

    # 真实要取的 url
    url = param_arr[0]
    proto, rest = urllib.splittype(url)  
    host, rest = urllib.splithost(rest) 

    ### 一些特殊处理， 比如 oschina 的翻译文章直接取打印版
    if origin_name == 'oschina' and url.find('/translate/') > 0 :
        url += '?print'
        get_content = utl.down({'id': 'translate', 'name': 'oschina', 'url': url}).decode('utf-8')
        markdown_text = html2text.html2text(get_content, 'http://' + host)
        ret_str = json.dumps({'detail': markdown_text})
        return HttpResponse("%s" % ret_str)


        #http://www.oschina.net/translate/serving-python-web-applications?print
        #http://www.oschina.net/translate/serving-python-web-applications

    # hickdebug
    # ret_str = url
    # return HttpResponse("%s" % ret_str)

    ### 获得数据源
    post = {} 
    data = urllib.urlencode(post) 
    # http 头
    user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1' 
    send_headers = { 
      'User-Agent' : user_agent,
      "Accept": "image/gif, image/jpeg, application/xaml+xml,  */*",
      "Host": host
    } 
    # 请求对象
    req = urllib2.Request(url, headers=send_headers) 
     # 请求数据
    response = urllib2.urlopen(req) 
    the_page = response.read() 
    # 替换掉 > 后的空格引起 xa0 编码问题
    reg = re.compile(r'''> +''')
    the_page = reg.subn('>', the_page)[0]
    # 保存数据到文件
    content_file = file('content.htm', 'w')
    ret = content_file.write(the_page)

    ### 得到主要的正文部分
    cfile = file('content.htm', 'r')
    content = cfile.read()
    soup = BeautifulSoup(content)
    # 尝试获取的 css selector 列表
    try_list = ('div.NewsContent', 'div.TextContent', 'div.BlogContent', 
        'table.vwtb td',   # lupaworld 的比较奇葩, 因为也有 div.content ，所以要提前些
        'div.BlogEntity',
        'div#articleShow',
        'div.entry',    ### 伯乐在线： http://blog.jobbole.com/ 的
        'td.t_f',    ### linux.cn
        'div.bort',    ### donews 的
        'div.artic_text',    ###  www.freebuf.com
        'div#article-content',    ###  http://www.itworld.com/
        'div.story',    ###  http://www.phpdeveloper.org/
        'div.content',    ###  http://www.ttlsa.com/  这种越常见的越往后放， 容易干扰
        )
    # 记录匹配的 selector, 后边还可以做进一步细化处理
    matched_selector = ''
    for selector in try_list:
        selected_item = soup.select(selector)
        if len(selected_item) > 0:
            matched_selector = selector
            break


    ### hickdebug
    # ret_str = len(css_selector)
    # return HttpResponse("%s" % css_selector)

    ### 如果传递了选择器，则按照选择器操作
    if len(param_arr) > 1 and len(css_selector) > 3:
        selected_item = soup.select(css_selector)
    
    ### 下面走按照模块名，也就是 spide 下有定义的方式
    if len(selected_item) < 1:
        ### 以上是为兼容自定义方式，最规范的是走这里，去模块的 article 取得数据
        mod = importlib.import_module(origin_name)
        article = mod.article(content, {'name': origin_name, 'url': url})
        if len(article['detail']) < 3:
            ret_str = "no content match"
        else:
            ret_str = json.dumps(article)
    ### 这里为直接传递或者默认选择器的方式
    else:
        body_content = str(selected_item[0]).decode('utf8')
        tmp_str = html2text.html2text(body_content, 'http://' + host)
        detail_str = trip_link_break(tmp_str)
        article = {'detail': detail_str}
        ret_str = json.dumps(article)

    return HttpResponse("%s" % ret_str)