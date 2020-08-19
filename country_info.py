import pandas as pd
from pandas import DataFrame,Series
from urllib.request import urlopen
from bs4 import BeautifulSoup

#country_info.csv파일 만들기
def make_country_info():
    #data.xlsx에 있는 국가명 불러오기
    df=pd.read_excel('data.xlsx',sheet_name='Sheet1')
    nation_list = list(df['국가'].unique())   
    
    #외교부 해외 안전 여행 사이트에서 각 국가별 url을 알기 위한 국가 번호 크롤링
    url = "http://www.0404.go.kr/dev/country.mofa?idx=&hash=&chkvalue=no2&stext=&group_idx=&alert_level=0"
    a = urlopen(url)
    soup = BeautifulSoup(a.read(), 'html.parser')
    countries = soup.find('ul','country_list').find_all('li')
    country_dict = dict()
    for country in countries:
        name = country.find('a').text
        if name in nation_list:
            nation_list.remove(name)
            number = country.find('a').get('href').split("'")[1]
            country_dict[name] = [number]
    if nation_list != []:
        print("크롤링 실패 국가:", nation_lsit)
    
    #각 국가별 url에서 여행 안전경보 크롤링
    warning_types = {'beware':'여행유의','control':'여행자제','advice':'철수권고','prohibition':'여행금지','special_care':'특별여행주의보'}
    for key, value in country_dict.items():
        country_info_url = "http://www.0404.go.kr/dev/country_view.mofa?idx="+value[0]  #국가별 url
        b = urlopen(country_info_url)
        soup2 = BeautifulSoup(b.read(), 'html.parser')
        warning_page = soup2.find_all('div','tabs_country_cont')
        travel_warning = ''
        for warning in warning_page:
            if warning.find('div','cont').text.strip() != '':
                travel_warning += (warning_types[warning.get('id')]+ ' - ' +warning.find('div','cont').text.strip() + '!@#')
        value.append(travel_warning)
        country_dict[key] = value
        
    #country_dict를 dataframe으로 변경후 country_info.csv에 저장
    df_country = pd.DataFrame.from_dict(country_dict,orient = 'index', columns=['number','travel_warning'])
    df_country.reset_index(inplace=True)
    df_country.rename(columns={'index':'name'}, inplace=True)
    df_country.to_csv("country_info.csv", sep=',',index = False)
    
#country_info.csv파일에서 해당 country의 url과 travel_warning을 return     
def search_country_info(country):
    df_country=pd.read_csv("country_info.csv", index_col = 0, encoding='utf8', engine='python')
    url = "http://www.0404.go.kr/dev/country_view.mofa?idx=" + str(df_country.loc[country,'number'])
    #travel_warning은 list형태, 경보와 그에대한 설명을 원소로 가짐, 없을 경우 빈 리스트
    #ex)[철수권고 - 후베이성(우한시 포함), 특별여행주의보 - 적색경보 지정 지역을 제외한 전지역]
    travel_warning = df_country.loc[country,'travel_warning']
    travel_warning = travel_warning.split('!@#')
    travel_warning.pop(-1)
    return url, travel_warning

if __name__ =="__main__":
    print(search_country_info('중국'))
    print(search_country_info('네덜란드'))