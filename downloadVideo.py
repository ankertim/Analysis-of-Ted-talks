import requests
from bs4 import BeautifulSoup
import re
import string

def videoDownload(url,location):
  try:
    page = requests.get(url)

    if(page.status_code != 200 ):
      print("page status code")
      print(page.status_code)
      print("沒抓到網頁")
      return 1
  except:
    print("沒抓到網頁")
    return 1
  pageData = BeautifulSoup(page.text, "html.parser")
  #print(pageData)
  a_tags = a_tags = pageData.find_all(attrs={"data-spec": "q"})
  d = ""

  try:
    for tag in a_tags:
      # 輸出超連結的文字
      ##print(tag.string)
      print()
      d = re.search("https://download.ted.com/products/\d+.mp4", tag.string)
      ##print(1)
      print(d.group(0))
      ##print(2)
      d = d.group(0)
    print("download....")
    download = requests.get(d)

    title= pageData.select("title",limit=1)
    name = ''
    for i in title:
      name=i.text
    print(name)
    name = name[name.find(':')+2:name.find(' |')]
    name = name.replace(":","")
    name = ''.join([i for i in name if i not in string.punctuation])
    #print(name)
    dlocation = location + name + '.mp4'
    open(dlocation, 'wb').write(download.content)
    print('download finish')
    return name
  except Exception as e:
    print("沒抓到影片")
    print(e)
    return 2

#  測試0   'https://www.ted.com/talks/angel_hsu_cities_are_driving_climate_change_here_s_how_they_can_fix_it/transcript?language=zh-tw'
#  測試1   'https://www.ted.com/talks/adie_de'
#  測試2   'https://www.ted.com/talks/canwen_xu_i_am_not_your_asian_stereotype?language=zh-tw'
# return  0正常執行  1沒抓到網頁  2沒抓到影片(可能是沒有開放下載)
if __name__ == '__main__':
  url = 'https://www.ted.com/talks/karen_scrivener_a_concrete_idea_to_reduce_carbon_emissions?language=zh-tw'
  result = videoDownload(url, location="database/video/")
  print(result)