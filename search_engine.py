import pandas as pd

#국가, 대학명, 어학자격증
def search_by_user(key):
    #유저 검색, 있는 행을 모두 뽑아내야함
    df=pd.read_excel('./data.xlsx',sheet_name='Sheet1')
    
    #해당하는 검색값이 각 열에 없는 경우 None을 리턴하기 위해 각 변수에 None 저장
    uni=None
    nation=None
    certification=None
    
    new_key=key.replace(" ","").lower() #key를 소문자로만 이루어진 띄어쓰기가 없는 문자열로 만들어서 new_key에 저장
    
    #대학명 데이터프레임 만들기
    df['검색을 위한 대학명']=df['대학명'].str.replace(" ", "").str.lower() #new_key와 비교할'검색을 위한 대학명'열 만들기
    if not df[df['검색을 위한 대학명'].str.contains(new_key, na=False)].empty: #해당하는 검색값이 '검색을 위한 대학명'열 있는 경우
        uni=df[df['검색을 위한 대학명'].str.contains(new_key, na=False)].drop('검색을 위한 대학명',axis=1)
        
    #국가 데이터프레임 만들기
    if not df[df['국가'].str.contains(key, na=False)].empty: #해당하는 검색값이 '국가'열에 있는 경우
        nation=df[df['국가'].str.contains(key, na=False)]
        
    #어학자격기준 데이터프레임 만들기
    df['검색을 위한 어학자격기준']=df['어학자격기준'].str.replace(" ", "").str.lower() #new_key와 비교할 '검색을 위한 어학자격기준'열 만들기
    if not df[df['검색을 위한 어학자격기준'].str.contains(key, na=False)].empty: #해당하는 검색값이 '검색을 위한 어학자격기준'열에 있는 경우
        certification=df[df['검색을 위한 어학자격기준'].str.contains(key, na=False)].drop('검색을 위한 어학자격기준', axis=1)
    
    if uni==None and nation==None and certification==None:
        return None, None, None
    else:
        #데이터프레임 합치기
        frames=[uni,nation,certification] 
        result=pd.concat(frames,keys=['uni','nation','certification']).drop_duplicates() #합친 후, 중복된 행 제거하기

        #데이터프레임을 리스트로 변환하기
        uni_list=result['대학명'].tolist()
        nation_list=result['국가'].tolist()
    certification_list=result['어학자격기준'].tolist()
    print(uni_list)
    if len(uni_list) == 0:
        return None, None, None
    return (uni_list, nation_list, certification_list)
    

def search_by_sys(key):
    df=pd.read_excel('./data.xlsx',sheet_name='Sheet1')
    
    if not df[df['대학명']==key].empty:
        return df[df['대학명']==key]