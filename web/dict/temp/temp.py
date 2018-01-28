from bs4 import BeautifulSoup
from urllib import request

def get_glossary():
    # for i in 'abcdefghijklmnopqrstuvwxyz':
    for i in 'a':

        url = "https://theodora.com/food/index.html"
        # url = 'https://theodora.com/food/culinary_dictionary_food_glossary_%s.html'%(i)

        page = request.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        # print(soup.find_all('table').text)
        data = ""
        for j in soup.find_all('tr')[8:]:
            # print('AHHHHHHH', j.text.replace("i", ""))
            if ':' in j.text:
                data += "%s\n"%str(j.text).replace("\t", "").replace("[", "").replace("]", "").strip()

            # data.append(i.text)

        with open('./letters/'+i, 'w+') as f:
            f.write(data)

# get_glossary()




def create_out(file_name):
    with open(file_name) as f:
        # print(f.read())
        a = f.read().split('\n')
    b = []
    for i in range(len(a)):
        if a[i]:
            b.append(a[i])


    out_dict = {}

    # print(b)
    for i in b:
        
        c = i.split(':')
        if len(c[0]) == 1:
            continue
        # print(c)
        if len(c[0].split(' ')) > 3:
            continue
        try:
            if not out_dict.get(str(len(c[0].split(' ')))):
                out_dict[str(len(c[0].split(' ')))] = {}
            out_dict[str(len(c[0].split(' ')))] [c[0].strip().lower()] = c[1].strip().lower()
        except:
            print('error', c)
            pass    

    print(out_dict['2'])



    import json

    with open('../out.json', 'r') as f:
        in_dict = json.load(f)
        # out_dict.update(json.load(f))
        print('IN DICT', in_dict)
        for i in out_dict.keys():
            if out_dict.get(i) and in_dict.get(i):
                out_dict[i].update(in_dict[i])


    with open('../out.json', 'w+') as f:
        # out_dict.update(json.loads(f.read()))
        # print(json.loads(f.read()))
        # print(out_dict)
        json.dump(out_dict, f)


def add_to_register_from_dir(fdir):
    import os
    for fi in os.listdir(fdir):
        create_out(fdir+fi)


add_to_register_from_dir('./letters/')

# create_out('asian')
# for i in ['china', 'asian', 'italian']:
#     create_out(i)