from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from lxml import etree
webdriver_path = 'C:\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=webdriver_path)
url = "https://www.nuitblanchetaipei.info/artwork"
driver.implicitly_wait(5)  # 最長等待時間
driver.get(url)

act_name = []
artist = []
time_list = []
location = []

#手動定義總頁數
pages = 10
for page in range(1, pages+1):
    print('Now is: Page ', page)
    print('Working...')
    xdoc = etree.HTML(driver.page_source)
    
    act_namei = map(str.strip , xdoc.xpath("//tr[2]//div[@class='box-heading']/h2/span[@class='ch']/text()"))
    artisti = map(str.strip , xdoc.xpath("//tr[2]//div[@class='box-heading']/span[@class='artist']/text()"))
    time_listi = map(str.strip , xdoc.xpath("//tr[2]//div[@class='artwork_box box m-1 text-left']/dl[@class='details']/dd[1]/text()"))
    locationi = map(str.strip , xdoc.xpath("//tr[2]//div[@class='artwork_box box m-1 text-left']/dl[@class='details']/dd[2]/text()"))
    #selenium抓取xpath
    #act_namei = driver.find_element_by_xpath("//tr[2]//div[@class='box-heading']/h2/span[@class='ch']").text
    #artisti = driver.find_element_by_xpath("//tr[2]//div[@class='box-heading']/span[@class='artist']").text
    #descriptioni = driver.find_element_by_xpath("//tr[2]//div[@class='artwork_box box m-1 text-left']/a[@class='box-anchor']/p").text
    #time_listi = driver.find_element_by_xpath("//tr[2]//div[@class='artwork_box box m-1 text-left']/dl[@class='details']/dd[1]").text
    #locationi = driver.find_element_by_xpath("//tr[2]//div[@class='artwork_box box m-1 text-left']/dl[@class='details']/dd[2]").text
    
    [act_name.append(i) for i in act_namei ] 
    [artist.append(i) for i in artisti]  
    [time_list.append(i) for i in time_listi] 
    [location.append(i) for i in locationi] 
    print('Done!')
    #如果是最後一頁，就不繼續執行”點擊下一頁“
    if page == pages:
        break
    else:
        #button = driver.find_element_by_xpath("//tr[2]/td/div[@class='text-center']/ul[@class='pagination pagination-white']/li[3]/a[@class='btn-next']/@href").click()
        #ActionChains(driver).move_to_element(button).click(button).perform()
        next_url = driver.find_element_by_xpath("//tr[2]/td/div[@class='text-center']/ul[@class='pagination pagination-white']/li[3]/a[@class='btn-next']").get_attribute("href")
        driver.get(next_url)
    #開始下一個循環
    time.sleep(1)


driver.close()

data = list(zip(act_name,artist,time_list,location))
df = pd.DataFrame(data,columns=['act_name','artist','time_list','location'])
df.to_csv("nuitblanchetaipei.csv",index=False)

