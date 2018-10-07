import requests as r
import math as m
import matplotlib.pyplot as mp

headers = {'User-Agent': 'MyLab/1.0'}
param = {
    'per_page': '50',
    'page': None,
    'text': None,
    'only_with_salary': 'true',
    'area': None

}
text = ['machine learning', 'NLP', 'Big Data', 'Data Science', 'Computer Vision']
pages = []
areas = r.get('https://api.hh.ru/areas/113', headers = headers).json()
for obl in areas['areas']:
    if obl['name'] == 'Москва':
        param['area'] = obl['id']
i=0

while len(pages) <= 1000:
    a = len(pages)
    param['page'] = i
    #print (i)
    for prof in text:
        param['text'] = prof
        # print (prof)
        # print (r.get('https://api.hh.ru/vacancies', headers = headers, params = param))
        response = r.get('https://api.hh.ru/vacancies', headers = headers, params = param).json()
        # print(response)
        pages += response['items']
        b = len(pages)
    if a == b:
         break
    i += 1

for sort in pages:   
    if sort['salary']['currency'] != 'RUR':
        pages.remove(sort)

print (len(pages))

vacs = []

for page in pages:
    name = page['name']
    salary = page['salary']
    new_vac = (name, salary)
    vacs.append(new_vac)

vacs_mid_sal = []

for vac in vacs:
    if vac[1]['from'] is not None and vac[1]['to'] is not None:
        salary = (vac[1]['from'] + vac[1]['to'])/2
    elif vac[1]['from'] is None:
        salary = vac[1]['to']
    else:
        salary = vac[1]['from']

    vac_mid_sal = (vac[0], salary)
    vacs_mid_sal.append(vac_mid_sal)

vacs_dict = {}

for name, salary in vacs_mid_sal:
    new_vec = []
    for badass_name, badass_salary in vacs_mid_sal:
        if name == badass_name:
            new_vec.append(badass_salary)
            vacs_mid_sal.remove((badass_name, badass_salary))
    new_vec.sort()
    n = len(new_vec)
    if n%2 == 1:
        middle = new_vec[n//2]
    else:
        middle = (new_vec[n//2] + new_vec[(n//2) - 1])/2
    vacs_dict[name] = middle

minimal = min(vacs_dict.values())
maximal = max(vacs_dict.values())

print (minimal, maximal)

borderlands = [80e3, 120e3, 150e3, 200e3, 300e3, m.inf]
fyrestone = [0] * (len(borderlands))

for val in vacs_dict.values():
    for i in range (len(borderlands)):
        if val <= borderlands[i]:
            fyrestone[i] += 1
            break

ind = range(len(borderlands))
mp.bar(ind, fyrestone, color = 'red')
mp.title('Распределение зарплат по диапазонам')

x_ticks = []
for i in ind:
    x_ticks.append(f'<={borderlands[i]}')

mp.xticks(ind, x_ticks)
mp.yticks(range(0, max(fyrestone) + 2, 2))
mp.xlabel('Размер зарплаты')
mp.ylabel('Количество вакансий')
mp.show()
print (fyrestone)

# for name, salary in vacs_dict.items():
    # print (name, salary)

# print (len(vacs_dict))
