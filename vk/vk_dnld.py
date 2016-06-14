import vk
import time
import json
import csv
import os

def rem ():
    try:
        os.remove('vk.csv')
    except OSError:
        pass

def get_city(api):
    city = api.database.getCities(country_id ='1', q = 'Когалым')[0]
    city_id = city['cid']
    return(city_id)

def get_users(api, city_id):
    user_list = api.users.search(city = city_id, count = '100')
    return user_list

def get_info(api, id_list):
    info_list = []
    for i in id_list:
        try:
            info_list.append(
                (api.users.get(user_ids = i, fields = 'sex,bdate,education,home_town,ocupation,relation,personal'),
                api.wall.get(owner_id = i, filter = 'owner')))
        except:
            time.sleep(.5)
    return info_list

def org_data():
    with open('test.json', 'r', encoding = 'utf-8') as js:
        data = json.loads(js.read())
    csv_info_conv(data)
    write_posts(data)


def csv_info_conv(data):
    first_row = ['User ID', 'First Name', 'Last Name', 'Sex', 'City', 'Birthday',
    'Home Town', 'Relation', 'University', 'Graduation', 'Religion', 'Languages']
    lang = []
    first = False
    for x in data:
        meta = x[0][0]
        uid = meta['uid']
        f_name = meta['first_name'] 
        l_name = meta['last_name']
        sex = meta['sex']
        city = 'Когалым'
        try:
            bdate = meta['bdate']
        except KeyError:
            bdate = 'N/A'
        try:
            home_town = meta['home_town']
        except KeyError:
            home_town = 'N/A'
        try:
            relation = meta['relation']
            if relation == 1:
                relation = 'single'
            elif relation == 2:
                relation = 'in a relationship'
            elif relation == 3:
                relation = 'engaged'
            elif relation == 4:
                relation = 'married'
            elif relation == 5:
                relation = "it's complicated"
            elif relation == 6:
                relation = 'actively searching'
            else:
                relation = 'in love'
        except KeyError:
            relation = 'N/A'
        try:
            unversity = meta['university_name']
        except KeyError:
            unversity = 'N/A'
        try:
            graduation = meta['graduation']
        except KeyError:
            graduation = 'N/A'
        if 'personal' in meta.keys():
            personal = meta['personal']
            if type(personal) is dict:
                try:
                    political = personal['political']
                    if political == 1:
                        political = 'single'
                    elif political == 2:
                        political = 'in a politicalship'
                    elif political == 3:
                        political = 'engaged'
                    elif political == 4:
                        political = 'married'
                    elif political == 5:
                        political = "it's complicated"
                    elif political == 6:
                        political = 'actively searching'
                    elif political == 7:
                        political = 'in love'
                    elif political == 8:
                        political = 'Apathetic'
                    elif political == 9:
                        political = 'Libertian'
                except KeyError:
                    political = 'N/A'
                try:
                    religion = personal['religion']
                except KeyError:
                    religion = 'N/A'
                try:
                    for x in personal['langs']:
                        lang.append(x)
                    langs = lang[0:len(langs) - 1]
                except KeyError:
                    langs = 'N/A'
            else:
                political = 'N/A'
                religion = 'N/A'
                langs = 'N/A'
        else:
            political = 'N/A'
            religion = 'N/A'
            langs = 'N/A'
        info_row = [uid, f_name, l_name, sex, city, bdate, home_town,
        relation, unversity, graduation, religion, langs]
        with open('vk.csv', 'a', encoding = 'utf-8') as csv_f:
            csv_file = csv.writer(csv_f, delimiter = ';', quotechar = '|',
                quoting = csv.QUOTE_MINIMAL)
            if first == False:
                csv_file.writerow(first_row)
                first = True
            csv_file.writerow(info_row)

def write_posts(data):
    for x in data:
        meta = x[0][0]
        posts = x[1]
        if not os.path.exists('UserPosts'):
            os.makedirs('UserPosts')
        us_dir = 'UserPosts/{0}'.format(meta['uid'])
        if not os.path.exists(us_dir):
            os.makedirs(us_dir)
        i = 1
        for post in posts:
            if type(post) is not int: 
                text = post['text']
                likes = post['likes']['count']
                try:
                    if 'photo' in post['attachment'].keys():
                        typ = 'photo'
                        src = post['attachment']['photo']['src_big']
                    elif 'audio' in post['attachment'].keys():
                        typ = 'audio'
                        src = post['attachment']['audio']['url']
                    elif 'video' in post['attachment'].keys():
                        typ = 'video'
                        src = post['attachment']['video']['image']
                    elif 'link' in post['attachment'].keys():
                        typ = 'link'
                        src = post['attachment']['link']['url']
                    elif 'doc' in post['attachment'].keys():
                        typ = 'doc'
                        src = post['attachment']['doc']['url']
                    else:
                        typ = 'N/A'
                        src = 'N/A'
                except KeyError:
                    typ = 'N/A'
                    src = 'N/A'
                formated = 'src@{0}\ntype@{1}\nlikes@{2}\n\n\n\t{3}'.format(src, typ, likes, text)
                with open('{0}/{1}.txt'.format(us_dir, i), 'w', encoding = 'utf-8') as doc:
                    doc.write(formated)
                i += 1

# id_list = []
# session = vk.AuthSession(app_id = '5439491', user_login = 'jlyell@wisc.edu', user_password = 'Pickle9247.')
# api = vk.API(session)
# city_id = get_city(api)
# user_list = get_users(api, city_id)
# for x in user_list:
#     if type(x) is int:
#         pass
#     else:
#         id_list.append(x['uid'])
# info_list = get_info(api, id_list)
# with open('test.json', 'w') as li:
#     li.write(json.dumps(info_list))
org_data()