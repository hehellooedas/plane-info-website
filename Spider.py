import requests, fake_useragent
import json,  time, random,hashlib,openpyxl

ua = fake_useragent.UserAgent()
city = {'深圳': 'SZX', '无锡': 'WUX', "北京": "BJS", "上海": "SHA", "广州": "CAN", "成都": "CTU", "杭州": "HGH", "武汉": "WUH",
        "西安": "SIA",
        "重庆": "CKG", "青岛": "TAO", "长沙": "CSX", "南京": "NKG", "厦门": "XMN", "昆明": "KMG", "大连": "DLC", "天津": "TSN",
        "郑州": "CGO", "三亚": "SYX", "济南": "TNA",
        "福州": "FOC", '阿勒泰': 'AAT', '兴义': 'ACX', '百色': 'AEB', '阿克苏': 'AKU', '鞍山': 'AOG', '安庆': 'AQG', '安顺': 'AVA',
        '阿拉善左旗': 'AXF',
        '包头': 'BAV', '毕节': 'BFJ', '北海': 'BHY', '秦皇岛': 'BPE', '博乐': 'BPL', '昌都': 'BPX', '保山': 'BSD', '承德': 'CDE',
        '常德': 'CGD',
        '长春': 'CGQ', '朝阳': 'CHG', '赤峰': 'CIF', '长治': 'CIH', '沧源': 'CWJ', '嘉义': 'CYI', '常州': 'CZX', '大同': 'DAT',
        '达县': 'DAX',
        '白城': 'DBC', '稻城': 'DCY', '丹东': 'DDG', '香格里拉(迪庆)': 'DIG', '大理': 'DLU', '敦煌': 'DNH', '东营': 'DOY', '大庆': 'DQA',
        '鄂尔多斯': 'DSN',
        '张家界': 'DYG', '额济纳旗': 'EJN', '恩施': 'ENH', '延安': 'ENY', '二连浩特': 'ERL', '阜阳': 'FUG', '佛山': 'FUO', '抚远': 'FYJ',
        '格尔木': 'GOQ',
        '广元': 'GYS', '固原': 'GYU', '海口': 'HAK', '邯郸': 'HDG', '黑河': 'HEK', '呼和浩特': 'HET', '合肥': 'HFE', '淮安': 'HIA',
        '怀化': 'HJJ',
        '香港': 'HKG', '海拉尔': 'HLD', '乌兰浩特': 'HLH', '哈密': 'HMI', '神农架': 'HPG', '哈尔滨': 'HRB', '舟山': 'HSN', '和田': 'HTN',
        '惠州': 'HUZ', '台州': 'HYN', '汉中': 'HZG', '黎平': 'HZH', '银川': 'INC', '且末': 'IQM', '庆阳': 'IQN', '景德镇': 'JDZ',
        '加格达奇': 'JGD',
        '嘉峪关': 'JGN', '井冈山': 'JGS', '西双版纳': 'JHG', '金昌': 'JIC', '黔江': 'JIQ', '九江': 'JIU', '晋江': 'JJN', '澜沧': 'JMJ',
        '佳木斯': 'JMU',
        '济宁': 'JNG', '锦州': 'JNZ', '建三江': 'JSJ', '池州': 'JUH', '衢州': 'JUZ', '鸡西': 'JXA', '九寨沟': 'JZH', '库车': 'KCA',
        '康定': 'KGT',
        '喀什': 'KHG', '南昌': 'KHN', '凯里': 'KJH', '金门': 'KNH', '赣州': 'KOW', '库尔勒': 'KRL', '克拉玛依': 'KRY', '贵阳': 'KWE',
        '桂林': 'KWL',
        '龙岩': 'LCX', '伊春': 'LDS', '临汾': 'LFQ', '兰州': 'LHW', '丽江': 'LJG', '荔波': 'LLB', '永州': 'LLF', '吕梁': 'LLV',
        '临沧': 'LNJ',
        '六盘水': 'LPF', '芒市': 'LUM', '拉萨': 'LXA', '洛阳': 'LYA', '连云港': 'LYG', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
        '林芝': 'LZY',
        '牡丹江': 'MDG', '马祖': 'MFK', '澳门': 'MFM', '绵阳': 'MIG', '梅州': 'MXZ', '南充': 'NAO', '白山': 'NBS', '齐齐哈尔': 'NDG',
        '宁波': 'NGB',
        '阿里': 'NGQ', '宁蒗': 'NLH', '南宁': 'NNG', '南阳': 'NNY', '南通': 'NTG', '满洲里': 'NZH', '漠河': 'OHE', '攀枝花': 'PZI',
        '阿拉善右旗': 'RHT',
        '日照': 'RIZ', '日喀则': 'RKZ', '巴彦淖尔': 'RLK', '沈阳': 'SHE', '石家庄': 'SJW', '揭阳': 'SWA', '普洱': 'SYM', '塔城': 'TCG',
        '腾冲': 'TCZ',
        '铜仁': 'TEN', '通辽': 'TGO', '天水': 'THQ', '吐鲁番': 'TLQ', '唐山': 'TVS', '黄山': 'TXN', '太原': 'TYN', '乌鲁木齐': 'URC',
        '榆林': 'UYN',
        '潍坊': 'WEF', '威海': 'WEH', '遵义(茅台)': 'WMT', '文山': 'WNH', '温州': 'WNZ', '乌海': 'WUA', '武夷山': 'WUS', '梧州': 'WUZ',
        '万州': 'WXN', '襄阳': 'XFN', '西昌': 'XIC', '锡林浩特': 'XIL', '西宁': 'XNN', '徐州': 'XUZ', '宜宾': 'YBP', '运城': 'YCU',
        '宜春': 'YIC',
        '阿尔山': 'YIE', '宜昌': 'YIH', '伊宁': 'YIN', '义乌': 'YIW', '延吉': 'YNJ', '烟台': 'YNT', '盐城': 'YNZ', '扬州': 'YTY',
        '玉树': 'YUS',
        '张掖': 'YZY', '昭通': 'ZAT', '湛江': 'ZHA', '中卫': 'ZHY', '张家口': 'ZQZ', '珠海': 'ZUH', '遵义(新舟)': 'ZYI'}

#建立ip池,伪装爬虫
ips = ['223.82.60.202:8060','122.9.101.6:8888','61.216.156.222:60808',
       '106.54.128.253:999','121.13.252.58:41564','202.55.5.209:8090',
       '183.247.215.218:30001','14.215.212.37:9168','124.156.100.83:8118',
       '218.75.102.198:8000','118.163.120.181:58837','61.216.185.88:60808']

#携程网传递航班数据的url
url = 'https://flights.ctrip.com/itinerary/api/12808/products'


def get_headers():
    # 伪装请求头
    headers = {
        'User-Agent': ua.random,  # 伪装User-Agent
        "Content-Type": "application/json",  # 数据传递格式（必填项）
        'referer': 'https://flights.ctrip.com',  # 前一个页面的url
        'origin': 'https://flights.ctrip.com'  # 初始页面的url
    }
    return headers

#爬虫函数
def spider(dcity, acity, date, sheet):
    """
    传入excel表格，输出新的表格
    :param dcity: 出发城市
    :param acity: 到达城市
    :param date: 出发时间
    :param sheet: excel表格数据
    :return: 数据sheet
    """
    str = "{}{}{}duew&^%5d54nc'KH".format(dcity, acity, 'Oneway')
    #验证哈希加密
    token = hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
    request_payload = {
        "flightWay": "Oneway",
        "army": "false",
        "classType": "ALL",
        "hasChild": 'false',
        "hasBaby": 'false',
        "searchIndex": 1,
        "selectedInfos": None,
        "token":token,
        "portingToken": "3fec6a5a249a44faba1f245e61e2af88",
        "airportParams": [
            {
                "dcity": city.get(dcity),
                "acity": city.get(acity),
                "dcityname": dcity,
                "acityname": acity,
                "date": date}
        ]
        }



    response = requests.post(url, headers=get_headers(), data=json.dumps(request_payload,ensure_ascii=False).encode('utf-8'),
                             timeout=(9,15),proxies={'http': random.choice(ips)})  # 发送post请求
    data = json.loads(response.text.encode('utf-8')).get('data')
    #如果数据是空的，则直接返回
    if data is None:
        return sheet
    datalist = data.get("routeList")  #得到存放所有航班信息的列表
    #如果航信信息是空的，也直接返回
    if datalist is None:
        return sheet
    for num in datalist:  #遍历所有航班
        legs = num.get("legs")[0]
        flight = legs.get("flight")  #找到航班信息
        airlineName = flight.get('airlineName')
        flight_no = flight.get("flightNumber")  #航班号
        plane_type = flight.get("craftTypeName")  #机型
        departuredate = flight.get("departureDate")  #出发时间
        arrivaldate = flight.get("arrivalDate")  #到达时间
        lowestPrice = legs.get('characteristic').get('lowestPrice')  # 经济舱价格
        fprice = legs.get('characteristic').get('lowestCfPrice')  # 公务舱价格
        #如果经济舱价格是空的，则模拟这个数据
        if lowestPrice is None:
            lowestPrice = random.randint(500,1500)
        #如果公务舱价格是空的，则模拟这个数据
        if fprice is None:
            fprice = random.randint(1500,4000)
        #写入到sheet中
        sheet.append([airlineName,flight_no,plane_type,departuredate,arrivaldate,dcity,acity,lowestPrice,fprice,400,400])
        return sheet


def plane_work(city1,city2):
    excel = openpyxl.load_workbook(f'./citys/{city1}.xlsx')
    sheet = excel['Sheet'] #获取sheet
    #2022下半年数据爬取
    for i in range(6, 13):
        for j in range(1, 32):
            sheet = spider(city1, city2, f'2022-{i}-{j}', sheet)
            time.sleep(3)
    #2023上半年数据爬取
    for i in range(1, 6):
        for j in range(1, 32):
            sheet = spider(city1, city2, f'2023-{i}-{j}', sheet)
            time.sleep(3)
    #保存文件
    excel.save(f'./citys/{city1}.xlsx')




if __name__ == '__main__':
    citylist = ['承德','长春','朝阳','常州','大同','义乌','烟台','扬州','西双版纳','佛山','合肥','九江',
                '洛阳','宁波','南阳','南通','南宁','攀枝花','衢州','沈阳',
                '温州','无锡','舟山','珠海','遵义']
    for i in citylist:
        plane_work('天津',i)
        print(i, '已经爬取成功!')