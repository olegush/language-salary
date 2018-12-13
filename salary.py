import argparse
import requests
import json
import time
import random
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_args_parser():
    parser = argparse.ArgumentParser(description='Average salary analysis')
    parser.add_argument(
        'region',
        help='region: Moscow, St-Petersburg',
        choices=['Moscow', 'St-Petersburg']
    )
    parser.add_argument(
        '--period',
        help='period: (from 1 to 30 days, 30 by default)',
        default=30
    )
    parser.add_argument(
        '--top',
        help='how many languages of rating to use (from 1 to 25, 5 by default)'
             'see https://github.com/benfred/github-analysis',
        default=5,
        type=int
    )
    return parser


def get_vacancies(url, headers, payload):
    response = requests.get(url, headers=headers, params=payload)
    return json.loads(response.text)


def get_lang_rankings(filepath):
    with open(filepath) as file:
        return json.loads(file.read())


def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] in 'RUR':
        if vacancy['salary']['from'] and vacancy['salary']['to']:
            return int(vacancy['salary']['from'] + vacancy['salary']['to'] / 2)
        elif not vacancy['salary']['to']:
            return int(vacancy['salary']['from'] * 1.2)
        else:
            return int(vacancy['salary']['to'] * 0.8)


def get_predict_rub_salary_sj(vacancy):
    if vacancy['currency'] in 'rub':
        if vacancy['payment_from'] and vacancy['payment_to']:
            return int(vacancy['payment_from'] + vacancy['payment_to'] / 2)
        elif not vacancy['payment_to']:
            return int(vacancy['payment_from'] * 1.2)
        elif not vacancy['payment_from']:
            return int(vacancy['payment_to'] * 0.8)


def get_salary_by_langs_hh(languages, top, region, period):
    hh_api_url = 'https://api.hh.ru/vacancies'
    headers = {}
    salary_by_langs = {}
    for language in languages[:top]:
        pages = 1
        page = 1
        salaries = []
        founded = 0
        while page <= pages:
            # HH.RU API parameters https://github.com/hhru/api/
            payload = {
                'specialization': '1.221',
                'area': region,
                'period': period,
                'text': language['lang'],
                'page': page
            }
            vacancies = get_vacancies(hh_api_url, headers, payload)
            salaries += [
                get_predict_rub_salary_hh(vacancy)
                for vacancy in vacancies['items']
                if get_predict_rub_salary_hh(vacancy)
            ]
            sec = random.random() * 3
            time.sleep(sec)
            page += 1
            pages = vacancies['pages']
            founded = vacancies['found']
        avg_salary = '{:,}'.format(int(sum(salaries) / len(salaries)))
        salary_by_langs[language['lang']] = dict(
            rank=language['rank'],
            vacancies_founded=founded,
            vacancies_processed=len(salaries),
            average_salary=avg_salary
        )
    return salary_by_langs


def get_salary_by_langs_sj(languages, top, region, period):
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    superjob_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    salary_by_langs = {}
    for language in languages[:top]:
        more = True
        page = 0
        salaries = []
        founded = 0
        while more:
            # SuperJob API parameters
            # https://api.superjob.ru/#search_vacanices
            payload = {
                't': region,
                'catalogues': '48',
                'count': '20',
                'page': page,
                'keyword': language['lang'],
                'period': period
            }
            vacancies = get_vacancies(superjob_api_url, headers, payload)
            salaries += [
                get_predict_rub_salary_sj(vacancy)
                for vacancy in vacancies['objects']
                if get_predict_rub_salary_sj(vacancy)
            ]
            sec = random.random() * 3
            time.sleep(sec)
            page += 1
            more = vacancies['more']
            founded = vacancies['total']
        if len(salaries):
            avg_salary = '{:,}'.format(int(sum(salaries) / len(salaries)))
        else:
            avg_salary = '-'
        salary_by_langs[language['lang']] = dict(
            rank=language['rank'],
            vacancies_founded=founded,
            vacancies_processed=len(salaries),
            average_salary=avg_salary
        )
    return salary_by_langs


def print_table(table_data, title):
    table_data_list = [[
        'Programming\nLanguage',
        'Language\nRank',
        'Vacancies\nfounded',
        'Vacancies\nProcessed',
        'Average\nSalary'
    ]]
    table_data_list += [
        [
            language[0],
            language[1]['rank'],
            language[1]['vacancies_founded'],
            language[1]['vacancies_processed'],
            language[1]['average_salary']
        ]
        for language in table_data.items()
    ]
    table = AsciiTable(table_data_list, title)
    table.justify_columns[1] = 'center'
    table.justify_columns[2] = 'center'
    table.justify_columns[3] = 'center'
    table.justify_columns[4] = 'center'
    print(table.table)


if __name__ == '__main__':
    arg_parser = get_args_parser()
    args = arg_parser.parse_args()
    top = args.top
    period = args.period
    regions = {
        'HeadHunter': {
            'Moscow': 1,
            'St-Petersburg': 2
        },
        'SuperJob': {
            'Moscow': 4,
            'St-Petersburg': 14
        }
    }
    region_hh_code = regions['HeadHunter'][args.region]
    region_sj_code = regions['SuperJob'][args.region]
    region_name = args.region
    lang_trends_json = 'rankings.json'
    lang_trends = get_lang_rankings(lang_trends_json)['languages']
    print(
        '\nHeadHunter\'s and SuperJob\'s average developers salary\n'
        'on trending programming languages.\n'
        'Ranking bases on research over 1.25 billion events from\n'
        'the public GitHub timeline (April 10 2018)\n'
        'For details visit https://github.com/benfred/github-analysis\n')
    print_table(
        get_salary_by_langs_hh(lang_trends, top, region_hh_code, period),
        'HeadHunter {}, {} days statistic'.format(region_name, period)
    )
    print()
    print_table(
        get_salary_by_langs_sj(lang_trends, top, region_sj_code, period),
        'SuperJob {}, {} days statistic'.format(region_name, period)
    )
