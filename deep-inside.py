#!/usr/bin/env python3
#github.com/intrackeable

import argparse
import random
import pyfiglet
import os
import shodan
import time
from colorama import Fore, Style
from datetime import datetime

global shodan_api_key
shodan_api_key = ''

global red, green, reset

red = Fore.RED 
green = Fore.GREEN
reset = Style.RESET_ALL

def display_banner():
    os.system('clear')
    draw = pyfiglet.figlet_format('DeepInside',font='slant')
    print(red + draw + reset)
    print(green + 'Explore IoT devices by using Shodan search engine.')

def get_random_country():
    codes = ['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'XK', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RS', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'CS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'XT', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']
    country = random.choice(codes)
    return country

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-R', help='Add a random country code', dest='random_code', action='store_true')
    parser.add_argument('-P', help='The page number to access [DEFAULT 1]', dest='page_number', type=int, default=1)
    parser.add_argument('-L', help='Limit of results yo want to obtain [DEFAULT 100]', dest='results', type=int, default=100)
    parser.add_argument('-S', help='Display and save data with [IP:PORT] format', dest='simple', action='store_true')
    flags = parser.parse_args()
    return flags.random_code, flags.page_number, flags.results, flags.simple

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S") + '.txt'
    return current_time

def save_in_file(data,current_time):
    with open (current_time, 'a') as file:
        file.write(data)

def shodan_search(page_number,results,simple,target):
    current_time = get_time()
    api = shodan.Shodan(shodan_api_key)
    query = api.search(target, page=page_number, limit=results)
    print('TOTAL FOUND: {}\n'.format(query['total']))
    try:
        for device in query['matches']:
            time.sleep(0.2)
            if simple:
                collected_data = '{}:{}\n'.format(device.get('ip_str','None'),device.get('port','None'))
            else:
                collected_data = 'http://{}:{} Org: {} Product: {} OS: {} Country: {}\n'.format(device.get('ip_str','None'),device.get('port','None'),device.get('org','None'),device.get('product','None'),device.get('os','None'),device['location']['country_name'] or 'None')
            save_in_file(collected_data,current_time)
            print(collected_data)
    except KeyboardInterrupt:
        print(red + 'CTRL+C DETECTED!')
        exit()

def main():
    display_banner()
    random_code,page_number,results,simple = options()
    print(green + 'PLEASE USE [-h] TO SEE ALL OPTIONS')
    target = input(green + 'ENTER A VALID QUERY: ')
    try:
        if random_code:
            target = '{} Country:{}'.format(target,get_random_country())
            print(target)
        shodan_search(page_number,results,simple,target)
    except shodan.APIError as error:
        print(red + 'Insufficient query credits, please upgrade your API plan or wait for the monthly limit to reset.')
    finally:
        print('CLOSING PROGRAM')
    
if __name__ == '__main__':
    main()

