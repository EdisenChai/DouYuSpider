""" 
爬虫模块
 """
from urllib import request
import re

class Spider():
    """ 
    爬虫类 
    """
    url = 'https://www.panda.tv/cate/lol?pdt=1.24.s1.3.1loapcheq15'
    
    # 设置中间 匹配 所有 且非贪婪 加() 去掉外层 不需要的数据
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\w\W]*?)</span>'
    
    def __fetch_content(self):
        """ 抓取基本内容  __私有方法"""

        # 爬取网页的初始数据
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8') # 得到的数据进行转码

        return htmls

    def __analysis(self,htmls):
        """ 对初始数据进行处理 """

        #得到所有names的数据列表：infos
        root_htmls = re.findall(Spider.root_pattern,htmls)
        name_number_list = []

        for each_html in root_htmls:
            #得到name的一个列表 
            # ['\n                                                                        七堇年华小七                      ', '\n
            #                  ']
            name = re.findall(Spider.name_pattern, each_html)
            number = re.findall(Spider.number_pattern, each_html)
          
            # 添加进一个dict里,要注意字典的格式 key:value
            name_number_dict = {'name':name, 'number':number}

            #添加进；list 里
            name_number_list.append(name_number_dict)
        
        return name_number_list

    def __refine(self,name_number_list):
        """ 进一步处理数据 """
        
        # 将原始的name--number dict 的数据再处理一下：
        # {'name': ['\n                                                                        LOL丶摇摆哥                      ', '\n
        #                               '], 'number': ['7.3万']}
        l = lambda each_name_number: {'name':each_name_number['name'][0].strip(),
                                      'number':each_name_number['number'][0]}
        return map(l, name_number_list)

    def __sort(self,name_numbers):
        """ 排序 """
        name_numbers = sorted(name_numbers, key=self.__sort__seed, reverse = True)
        return name_numbers  

    def __sort__seed(self, name_number):
        """ 排序准备  """
        nu = re.findall('\d*',name_number['number'])
        number = float(nu[0])
        if '万' in name_number['number']:
            number = number * 10000

        return number 

    def __show(self,name_numbers):
        """ 展示数据 """

        #count = 1
        for rank in range(0,len(name_numbers)):
            print('Rank: '+str(rank+1)+'--'+
                   name_numbers[rank]['name']+'----'+
                   name_numbers[rank]['number'])

        # for name_number in name_numbers:
        #     print('Rank '+str(count) + '--'+ name_number['name']+'----'+name_number['number'])
        #     count += 1
        
    def go(self):
        """ 入口函数  """ 

        htmls = self.__fetch_content()
        name_number_list = self.__analysis(htmls)

        # 将refine返回的map对象强制转换为list
        name_numbers = list(self.__refine(name_number_list))
        name_numbers = self.__sort(name_numbers)
        self.__show(name_numbers)

spider = Spider()
spider.go()

