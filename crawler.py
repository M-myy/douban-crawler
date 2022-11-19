import requests
import bs4
import re
import time

start_url = "https://www.douban.com/group/topic/79870081/"

# request_header http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

def load_page_url(page_url):
    response = requests.get(page_url,headers = headers)
    response_all_page = bs4.BeautifulSoup(response.text,"lxml")  #提取这个到页面
    response_paginator = response_all_page.find("div",attrs={'class':'paginator'})

    all_page_url = set()
    all_page_url.add(page_url)
    for response_paginator_href in response_paginator.find_all("a"):
        all_page_url.add(response_paginator_href.attrs.get('href'))

    return all_page_url

def download_email_addr(url_set,file_path):
    file_eamil = open(file_path,'a')

    for tmp_url in url_set:
        print(f'''正在保存分页:{tmp_url}...''')
        response = requests.get(tmp_url,headers = headers)
        response_all_page = bs4.BeautifulSoup(response.text,"lxml")
        response_reply_doc = response_all_page.find_all("div",attrs={'class':'reply-doc'})

        for response_ele in response_reply_doc:
            response_reply_content = response_ele.find("p",attrs={'class':"reply-content"}) 
            reply_email_addr = re.search("\w+@\w+.\w+",response_reply_content.text,flags=re.A)  #正则匹配邮箱
            #reply_email_addr = re.search("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",response_reply_content.text,flags=re.A)
            if reply_email_addr:  #如果匹配到邮箱则保存
                #print(reply_email_addr.group())
                file_eamil.write(reply_email_addr.group() + '\n')
#    time.sleep(2)  #防止请求过快被封IP

    file_eamil.close()
    print('保存完成!')

download_email_addr(load_page_url(start_url),'email.db')
