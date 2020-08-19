import pandas as pd
from pandas import DataFrame,Series
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#qs랭킹을 크롤링하여 univ_qs_ranking.csv를 만듦
def make_qs_ranking():
    #대학명을 url 검색에 적합한 형태로 변환하는 함수
    def make_proper_url(univ):
        univ = str(univ).lower()
        univ = univ.split(',')[0]
        univ = univ.split('(')[0]
        univ = univ.split(' - ')[0]
        univ = univ.split()
        delete_word = ['of', 'and', 'the', 'at', '&']
        for word in delete_word:
            if word in univ:
                univ.remove(word)
        univ = '-'.join(univ)
        return univ
    #data.xlsx 파일에서 대학명 불러오기 
    df=pd.read_excel('data.xlsx',sheet_name='Sheet1')
    univ_list = list(df['대학명'])
    univ_dict = dict()
    univ_dict = dict()
    for univ in univ_list:
        url = 'https://www.topuniversities.com/universities/' + make_proper_url(univ)
        html_source = requests.get(url) 
        plain_text = html_source.text 
        soup = BeautifulSoup(plain_text,'html.parser') 
        if soup.find('div','title_info'):
            logo = soup.find('div','field-profile-logo').find('img').get('src')
            info = soup.find_all('div','key pull-left')
            if info == []:
                univ_dict[univ] = ['1000+', logo]
                print('1000+')
            else:
                kind = info[0].find('div').find('label').text
                if kind == 'QS Global World Ranking':
                    rank = info[0].find('div','val')
                    univ_dict[univ] = [rank.text[1:].strip('='), logo]
                    print(rank.text[1:].strip('='))
                else:
                    univ_dict[univ] = ['1000+', logo]
                    print('1000+')
        else:
            univ_dict[univ] = ['정보 없음', 'https://www.topuniversities.com/sites/default/files/styles/logo_88x88/public/default_images/school-logo_def.png']
            print('정보 없음')
    
    #univ_dict로 DataFrame 만들어 univ_qs_ranking.csv 쓰기    
    df_univ = pd.DataFrame.from_dict(univ_dict, orient = 'index', columns=['ranking', 'logo'])
    df_univ.reset_index(inplace=True)
    df_univ.rename(columns={'index':'university'},inplace=True)
    df_univ.to_csv("univ_qs_ranking.csv", sep=',',index = False)

    
#univ를 입력하면 univ_qs_ranking.csv에서 해당 대학의 qs_ranking을 불러오는 함수 
def search_qs_ranking(univ):
    df_univ=pd.read_csv("univ_qs_ranking_revised.csv", index_col = 0, encoding='utf8', engine='python')
    return str(df_univ.loc[univ,'ranking'])

#univ를 입력하면 univ_qs_ranking.csv에서 해당 대학의 logo 을 불러오는 함수 
def search_logo(univ):
    df_univ=pd.read_csv("univ_qs_ranking_revised.csv", index_col = 0, encoding='utf8', engine='python')
    return str(df_univ.loc[univ,'logo'])



if __name__ == "__main__":
    print(search_qs_ranking('NEOMA Business School\n (Reims & Rouen)'))
    print(search_logo('Ulm University'))