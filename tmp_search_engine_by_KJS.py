import pandas as pd

dataset = pd.read_excel("data.xlsx", header= 0)

def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "k" if k_count>1 else "e"

def search_by_user(key):
    univ_list = []
    for i in dataset["대학명"]:
        if not str(i).isdigit():
            if key.lower() in i.lower():
                univ_list.append(i)
    university_names = dataset[dataset["대학명"].isin(univ_list)]
    
    certi_list = []
    for i in dataset["어학자격기준"]:
        if not str(i).isdigit():
            if key.lower() in i.lower():
                certi_list.append(i)
    certi_names = dataset[dataset["어학자격기준"].isin(set(certi_list))]
    
    country_list = []
    for i in dataset["국가"]:
        if not str(i).isdigit():
            if key.lower() in i.lower():
                country_list.append(i)
    country_names = dataset[dataset["국가"].isin(country_list)]

    result = pd.concat([university_names, certi_names, country_names]).drop_duplicates()
    if len(result) != 0:
        return list(result["대학명"]), list(result["국가"]), list(result["어학자격기준"])
    else:
        return None, None, None
    
    
def search_by_sys(key):
    info = dataset[dataset["대학명"] == key]
    
    return info

        
if __name__ == "__main__":
    search_by_user("네덜란드")