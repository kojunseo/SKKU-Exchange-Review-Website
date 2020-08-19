import pandas as pd
from pandas import DataFrame,Series

#사용자가 입력한 review를 reviews.csv파일에 쓰기
def review_write(id_, univ, title, contents, rating):
    df=pd.read_csv("reviews.csv", encoding='utf8', engine='python')
    serial_num = df.shape[0] + 1     #review의 고유번호

    #고유번호, id, 대학명, 리뷰제목, 본문, 별점(1~5사이의 정수) 순서로 csv파일에 기록
    new_review = pd.Series([serial_num, id_, univ, title, contents, rating], index = df.columns)
    df = df.append(new_review, ignore_index=True)
    df.to_csv("reviews.csv", sep=',', index = False)


    
#reviews.csv파일에서 해당 대학의 리뷰 반환
def review_search(university):
    df=pd.read_csv("reviews.csv", encoding='utf8', engine='python')
    condition = (df['university']==university)   
    condition_favor_df = df[condition]   #검색한 대학명과 같은 리뷰들의 데이터프레임
    searched_reviews = []                #검색한 대학명과 같은 리뷰들의 리스트
    #condition_favor_df에서 행별 정보를 searched_reviews에 추가
    def make_list(x):
        if x['rating'] != -1:  #리뷰가 삭제 되지 않은 경우
            searched_reviews.append([x['serial_num'], x['id'], x['title'], x['contents'], x['rating']])
    condition_favor_df.apply(make_list, axis=1)
    if len(searched_reviews) == 0:
        searched_reviews = None
    #return해줄 내용은 이중리스트로 [[고유번호1, 아이디1, 제목1, 본문1, 별점1], [고유번호2, 아이디2, 제목2, 본문2, 별점2]]
    return searched_reviews


#reviews.csv파일에서 해당 id의 리뷰 반환
def review_search_by_id(id_):
    df=pd.read_csv("reviews.csv", encoding='utf8', engine='python')
    condition = (df['id']==id_)   
    condition_favor_df = df[condition]   #검색한 대학명과 같은 리뷰들의 데이터프레임
    searched_reviews = []                #검색한 대학명과 같은 리뷰들의 리스트
    #condition_favor_df에서 행별 정보를 searched_reviews에 추가
    def make_list(x):
        if x['rating'] != -1:     #리뷰가 삭제 되지 않은 경우
            searched_reviews.append([x['serial_num'], x['university'], x['title'], x['contents'], x['rating']])
    condition_favor_df.apply(make_list, axis=1)
    if len(searched_reviews) == 0:
        searched_reviews = None
    #return해줄 내용은 이중리스트로 [[고유번호1, 대학명1, 제목1, 본문1, 별점1], [고유번호2, 대학명2, 제목2, 본문2, 별점2]]
    return searched_reviews


#serial_num을 통해 review 삭제해 reviews.csv에 저장
def review_delete(serial_num):
    print(serial_num)
    df = pd.read_csv("reviews.csv", encoding='utf8', engine='python')
    #리뷰 제목, 내용을 삭제하고, rating 을 -1로 변경 ->rating -1 은 삭제된 review를 의미
    df.loc[int(float(serial_num))-1, ['title', 'contents', 'rating']] = ['', '', -1]
    df.to_csv("reviews.csv", sep=',', index = False)


#serial_num을 통해 review 의 title, contents, raitng 을 수정해 reviews.csv에 저장
def review_modify(serial_num, title, contents, rating):
    df = pd.read_csv("reviews.csv", encoding='utf8', engine='python')
    #리뷰 제목, 내용, 별점 수정
    df.loc[int(serial_num)-1, ['title', 'contents', 'rating']] = [title, contents, rating]
    df.to_csv("reviews.csv", sep=',', index = False)


if __name__=="__main__":
    #review_write("hanil", "skku","good","만족스러운 학교생활", 5)
    #review_write("jenny", "korea","좋은 여행","한국문화 체험", 4)
    #review_modify(1,'best','만족스러운 학교생활, 캠퍼스 2개',5)
    #review_delete("6")
    print(review_search_by_id("hello"))
