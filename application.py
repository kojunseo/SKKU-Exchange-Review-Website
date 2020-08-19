from flask import Flask, render_template, request, redirect, url_for, session
import search_engine, tmp_search_engine_by_KJS, registry_management, country_info, qs_ranking
import review_make
import pandas as pd

application = Flask(__name__)

application.secret_key = "sadfklj34dfsgjlk"

@application.route("/")
def basic():
    return redirect(url_for("home"))

@application.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("home"))

@application.errorhandler(500)
def technical_error(error):
    return "기술적 오류입니다. sta06167@g.skku.edu로 연락주시면 해결하겠습니다. 감사합니다."


@application.route("/home")
def home():
    if "username" in session:
        login = True
    else:
        login = False
    return render_template("hello_session.html", login = login)


@application.route("/login")
def login():
    if "username" not in session:
        return render_template("login.html")
    else:
        return redirect(url_for("home"))
    
@application.route("/mypage")
def mypage():
    if "username" not in session:
        return render_template("login.html")
    else:
        id_ = session["username"]
        id_, name, student_id, major, favorite, reviews = registry_management.search_info(id_)
        if reviews != None:
            for review in reviews:
                review[4] = int(review[4])
        return render_template("mypage.html", id_=id_, 
                               name = name,
                              student_number = student_id, major = major, favorite = favorite, 
                               my_reviews = reviews
                              )

@application.route("/register/<string:message>")
def register(message):
    if message == "None":
        message = None
    print(message)
    return render_template("registry.html", message=message)

@application.route("/register_done", methods = ["POST"])
def register_done():
    name = request.form['user_name']
    id_ = request.form['user_id']
    password = request.form["user_pw"]
    password2 = request.form["user_pw2"]
    if password2 != password:
        message = "비밀번호와 비밀번호 확인이 일치하지 않습니다."
        return redirect(url_for("register", message = message))  
    email = request.form["email"]
    student_number = request.form["student_number"]
    dept = request.form["college"]
    major = request.form["major"]
    campus = request.form["campus"]
    message = "회원가입에 성공했습니다"
    if len(str(student_number)) == 10:
        if not student_number.isdigit() or 1950 > int(str(student_number)[:4]) or int(str(student_number)[:4]) > 2100:
            message = "학번 양식에 맞지 않습니다"
            return redirect(url_for("register", message = message)) 
    else:
        message = "학번 양식에 맞지 않습니다"
        return redirect(url_for("register", message = message))
    message=  registry_management.sign_up(student_number,dept,major,campus,name,id_,password,email)
    
    if message == "회원가입에 성공했습니다":
        return redirect(url_for("home"))
    else:
        print("where")
        return redirect(url_for("register", message = message))        
    

@application.route("/login_done", methods = ["POST"])
def login_done():
    id_ = request.form['id']
    pass_ = request.form['password']
    # print(id_, pass_)
    if registry_management.login(id_, pass_):
        session["username"] = id_
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@application.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@application.route("/version")
def version():
    return render_template("dev_version.html")


@application.route("/developers")
def developers():
    return render_template("developer.html")


@application.route("/search_result")
def search():
    search_name = str(request.args.get("search"))
    
    if search_name == "토익":
        search_name = "toeic"
    elif search_name == "토플":
        search_name = "toefl"

    # print(search_name)
    search_in_univ,search_in_country,search_in_certification = tmp_search_engine_by_KJS.search_by_user(search_name)
    if search_in_univ == None:
        return render_template("search_result.html",
                           search=search_name) 
    else:
        make_list = list(zip(search_in_univ, search_in_country))
        return render_template("search_result_NO.html",
                               search=search_name, listed=make_list)


@application.route("/university/<string:university>")
def university(university):
    reviews = review_make.review_search(university)
    univ_info = tmp_search_engine_by_KJS.search_by_sys(university)
    # print(univ_info)
    country_infomation = country_info.search_country_info(list(univ_info["국가"])[0])
    qs_rank = qs_ranking.search_qs_ranking(university)
    ave_rate = 0
    if reviews != None:
        for i in reviews:
            i[4] = int(i[4])
            ave_rate += i[4]

        ave_rate = int(ave_rate / len(reviews))
    
    login = False
    if "username" not in session:
        login = True
        
    logo_img = qs_ranking.search_logo(university)
    print(logo_img)
    return render_template("university_info.html",
                           login = login,logo_img = logo_img,
                           name=university, star_rate=int(ave_rate),qs_rank = qs_rank,
                           country_infomation = country_infomation,
                           reviews=reviews, country = list(univ_info["국가"])[0],
                          count = list(univ_info["선발인원(교환학생)"])[0],certi = list(univ_info["어학자격기준"])[0],
                          at_least = list(univ_info["최소수료학기"])[0],
                           application = list(univ_info["Application Deadline:  "])[0],
                          nomination = list(univ_info["Nomination Deadline:"])[0],
                          money = list(univ_info["비용 관련 참고 사항"])[0],
                          cordi = list(univ_info["Please state the name of Inbound Exchange coordinator. (Contact Point)"])[0],
                          email = list(univ_info["Please state your E-mail for Exchange Nomination and Inquries."])[0],
                          department = list(univ_info["Please state which department you represent"])[0],
                          where = list(univ_info["Please state the Office of International Affairs' address. (To receive hard copies of documents)"])[0],
                          one_year = list(univ_info["1년 파견 가능 여부"])[0],
                          graduated = list(univ_info["대학원생 지원가능 여부"])[0],
                          apply_link = list(univ_info["온라인 Application link(없으면 email)"])[0],
                          in_real = list(univ_info["온라인 서류 접수 후 실물서류 제출 여부"])[0],
                          homepage = list(univ_info["홈페이지 제공여부"])[0],
                          ban = list(univ_info["수강 제한 영역 여부"])[0],
                          other_class = list(univ_info["전공 이외의 수업 수강 가능 여부"])[0],
                          consideration = list(univ_info["비고사항"])[0],)


@application.route("/add_favorite/<string:university>", methods=['POST'])
def add_favorite(university):
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        id_ = session["username"]
        registry_management.enter_favorite(id_, university)
        return redirect(url_for("university", university=university))


@application.route("/delete_favorite/<string:university>", methods=['POST'])
def delete_favorite(university):
    if "username" not in session:
        return render_template("login.html")
    else:
        id_ = session["username"]
        registry_management.delete_favorite(id_, university)
        return redirect(url_for("mypage"))



@application.route("/review_write/<string:university>'")
def review_write(university):
    if "username" in session:
        return render_template("write_review.html", name=university)
    else:
        return redirect(url_for("login"))


@application.route("/review_write_done/<string:university>'", methods=['POST'])
def review_write_done(university):
    if "username" not in session:
        return render_template("login.html")
    else:
        title = request.form['title']
        contents = request.form['contents']
        rating = int(request.form["rate"])
        id_ = session["username"]
        # print(id_,university, title, contents, rating)
        review_make.review_write(id_,university, title, contents, rating)

        return redirect(url_for("university", university=university))


@application.route("/delete_review/<string:serial>", methods=['POST'])
def delete_review(serial):
    if "username" not in session:
        return render_template("login.html")
    else:
        review_make.review_delete(serial)

        return redirect(url_for("mypage"))


if __name__ == "__main__":
    application.run(host='0.0.0.0')
