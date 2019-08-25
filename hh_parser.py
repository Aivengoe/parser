import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
base_url = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=python&page=0'

def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa':"pager-page"})
            count = int(pagination[-1].text)
            for i in range(count):
                url = "https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=python&page={}".format(i)
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
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
                    'p_date': publick_date,
                    'title': title,
                    'salary': salary,
                    'company': company,
                    'premium': premium,
                    'com_ver': verif,
                    'href': href,
                    'content': content
                })

        divs_find(divs, 'No')
        divs_find(divs_p, 'Yes')
        print(len(jobs))
    else:
        print('ERROR Done SC = ' + str(request.status_code))
    return (jobs)
def writer_files(jobs):
    with open('parsed_jobs_spb_python.csv', 'w', encoding="utf-8") as file:
        a_pen = csv.writer(file)
        for job in jobs:
            a_pen.writerow((job['p_date'], job['title'], job['salary'], job['company'], job['premium'], job['com_ver'], job['href'], job['content']))


jobs = hh_parse(base_url, headers)
writer_files(jobs)

