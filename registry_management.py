import csv
import hashing_algorithm
import review_make
import pandas as pd
#회원가입
def sign_up(student_number,dept,major,campus,name,id_,password,email,admin=False):
    f=open('member_information.csv', 'r', encoding='utf-8')
    rdr=csv.reader(f)
    member_information_list=list(rdr)
    
    #아무도 회원가입이 안 되어있는 경우(회원가입 여부, 아이디 중복 여부 확인 부분에서 인덱스 에러 방지 차원)
    if len(member_information_list)==0: 
        f=open('member_information.csv', 'w', encoding='utf-8', newline='')
        wr=csv.writer(f, delimiter=',')
        hashed_password=hashing_algorithm.hash_password(password)
        wr.writerow([student_number,dept,major,campus,name,id_,hashed_password,email,admin,""])
        print('회원가입 성공')
        f.close()
        return "회원가입에 성공했습니다"
        
    #회원가입 여부 확인    
    signed_up=False

    for line in member_information_list:
        if str(line[0])==str(student_number):
            signed_up=True
            break
 
    if signed_up==True: #이미 회원가입을 한 경우
        print('이미 가입된 회원입니다')
        f.close()
        return "이미 가입된 학번입니다"

    else: #처음 회원가입을 하는 경우
        #아이디 중복 확인
        existed_id=False
        for line in member_information_list:
            if line[5]==id_:
                existed_id=True
                break

        if existed_id==True: #이미 존재하는 아이디일 경우
            print("이미 존재하는 아이디입니다")
            f.close()
            return "이미 존재하는 아이디 입니다."
    
        else: #사용 가능한 아이디일 경우
            f.close()
            f=open('member_information.csv', 'a', encoding='utf-8', newline='')
            wr=csv.writer(f, delimiter=',')
            hashed_password=hashing_algorithm.hash_password(password)
            wr.writerow([student_number,dept,major,campus,name,id_,hashed_password,email,admin,""])
            f.close()
            print("회원가입 성공")
            return "회원가입에 성공했습니다"

#로그인
def login(id_, password):
    f=open('./member_information.csv','r',encoding='utf-8')
    rdr=csv.reader(f)
  
    for line in rdr:
        #만약 아이디가 데이터베이스에 존재하고, password도 그것에 일치한다면
        if line[5]==id_ and hashing_algorithm.verify_password(line[6],password):
            print('로그인 성공') #id라는 변수는 파이썬에서 예약어로 되어있기 때문에 id_로 사용하는 편이 나중에 문제가 발생하지 않도록 예방할 수 있습니다!
            f.close()
            return True
        
    #만약 아이디가 데이터베이스에 존재하지 않거나, password가 일치하지 않는다면
    print('로그인 실패')
    f.close()    
    return False

#회원정보 조회
def search_info(id_):
    f=open('./member_information.csv','r',encoding='utf-8')
    rdr=csv.reader(f)
    
    for line in rdr:
        if line[5]==id_:
            student_number=line[0]
            #dept=line[1]
            major=line[2]
            #campus=line[3]
            name=line[4]
            password=line[6]
            #email=line[7]
            if line[9] == "": #관심대학이 없을 경우
                favorite=None
            else:
                favorite=line[9].split('*')
    
    reviews=review_make.review_search_by_id(id_)
    f.close()
    print(id_, name, student_number, major, favorite, reviews)
    
    return id_, name, student_number, major, favorite, reviews

#관심대학 추가
def enter_favorite(id_, univ):
    #id_에 관심대학 추가하기
    readfile=open('./member_information.csv','r',encoding='utf-8')
    rdr=csv.reader(readfile)
    member_information_list=list(rdr)
    
    for line in member_information_list:
        if line[5]==id_:
            if line[9] == "":
                line[9] = univ
                
            else:
                line[9]=line[9]+'*'+univ
                break
                
    writefile=open('./member_information.csv','w',encoding='utf-8',newline='')
    wr=csv.writer(writefile)
    for line in member_information_list:
        wr.writerow(line)
    
    readfile.close()
    writefile.close()
    
    return None

#관심대학 삭제
def delete_favorite(id_,univ):
    readfile=open('./member_information.csv','r',encoding='utf-8')
    rdr=csv.reader(readfile)
    member_information_list=list(rdr)
    print(member_information_list)
    for line in member_information_list:
        if line[5]==id_:
            #관심대학이 있을 경우

            univ_list=line[9].split('*')
            idx = univ_list.index(univ)
            del univ_list[idx]
            line[9]='*'.join(univ_list)
            print(line[9])
            break

            
    writefile=open('./member_information.csv','w',encoding='utf-8',newline='')
    wr=csv.writer(writefile)
    for line in member_information_list:
        wr.writerow(line)
        
    readfile.close()
    writefile.close()
    return None
    
def change_personal(student_number,dept,major,campus,name,id_,password,email,admin, favorites):
    #에러나서 위에 코드 수정했으니, sign_up함수에 수정된 내용 참고해서 작성할 것(그렇지 않으면 에러 발생)
    #학번, 전공, 캠퍼스, 이메일 만 변경 가능함
    #비밀번호는 덮어쓰기로 해야해서 만약 만들어야 하면, 새로운 함수에 비밀번호 용을 만들어야 할듯 (우선은 정보 수정만 하자)
    #함수는 리턴할 필요 없음
    return None


if (__name__ == "__main__"):
    #sign_up(2019111111, '글로벌융합학부', '인공지능융합전공', '인사캠', '김제니', 'jenny', 'qwert', 'pjy707099@gmail.com',True)
    #sign_up(2019222222, '글로벌융합학부', '인공지능융합전공', '인사캠', '이한일', 'hanil', 'qwert', 'pjy707099@gmail.com')
    #sign_up(2019311195, '글로벌융합학부', '인공지능융합전공', '인사캠', '김지유', 'rlawldb0707', 'pjy707099', 'rlawldb0707@naver.com', True)
    #sign_up(2019111111, '글로벌융합학부', '인공지능융합전공', '인사캠', '라리사', 'lalisa', 'trewq', 'pjy707099@gmail.com') #이미 가입된 회원입니다
    #sign_up(2019000000, '글로벌융합학부', '인공지능융합전공', '인사캠', '이주민', 'hanil', 'qwert', 'pjy707099@gmail.com') #이미 존재하는 아이디입니다
    #login('jenny','qwert') #로그인 성공
    #login('hanil','trewq') #로그인 실패(틀린 비번)
    #login('americano','espresso') #로그인 실패(없는 계정)
    enter_favorite('jenny','utrecht university')
    enter_favorite('jenny','hongkong university')
    enter_favorite('jenny','oslo university')
    #enter_favorite('rlawldb0707','harvard')
    #enter_favorite('rlawldb0707','oxford')
    #search_info('jenny') #관심대학이 있는 경우
    #search_info('hanil') #관심대학이 없는 경우
    delete_favorite('jenny','hongkong university')