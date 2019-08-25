import requests
from bs4 import BeautifulSoup as bs
import  regex as re

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
base_url = 'https://spb.hh.ru/search/vacancy?only_with_salary=false&clusters=true&area=2&enable_snippets=falce&salary=&text=python'

def hh_parse(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':"vacancy-serp__vacancy"})
        divs_p = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy vacancy-serp__vacancy_premium'})
        def divs_find(divs, premium):
            for div in divs:
                title = div.find('a', attrs={'data-qa':"vacancy-serp__vacancy-title"}).text
                href = div.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"})['href']
                company = div.find('a', attrs={'data-qa': "vacancy-serp__vacancy-employer"}).text
                try:
                    salary = div.find('div', attrs={'data-qa': "vacancy-serp__vacancy-compensation"}).text
                except:
                    salary = 'Not'
                text1 = div.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text
                text2 = div.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_requirement"}).text
                content = '{} {}'.format(text1, text2)
                publick_date = div.find('span', attrs={'class': "vacancy-serp-item__publication-date"}).text
                try:
                    verif = div.find('span', attrs={'class': "bloko-icon bloko-icon_done bloko-icon_initial-action"}).text
                    verif = 'Yes verification'
                except:
                    verif = 'Not verification'
                premium = premium
                jobs.append({
                    'publick_date': publick_date,
                    'title': title,
                    'salary': salary,
                    'company': company,
                    'premium': premium,
                    'verif': verif,
                    'href': href,
                    'content': content
                })

        divs_find(divs, 'No')
        divs_find(divs_p, 'Yes')
        print(len(jobs))
    else:
        print('ERROR')

hh_parse(base_url, headers)

