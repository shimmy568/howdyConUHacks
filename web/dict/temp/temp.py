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
            out_dict[i].update(in_dict[i])


    with open('../out.json', 'w+') as f:
        # out_dict.update(json.loads(f.read()))
        # print(json.loads(f.read()))
        # print(out_dict)
        json.dump(out_dict, f)


# create_out('asian')
for i in ['china', 'asian', 'italian']:
    create_out(i)