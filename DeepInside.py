#!/usr/bin/env python3
#Author: Intrackeable
#Github: https://github.com/intrackeable
try:
    import os, time, argparse, webbrowser, pyfiglet
    from shodan import Shodan
    from colorama import Fore, Style
    from random import choice

except ImportError:
    print('Use pip install -r requirements.txt')
    CloseProgram()

#COLORS
class colors:
    red = Fore.RED + Style.BRIGHT
    green = Fore.LIGHTGREEN_EX
    cyan = Fore.CYAN + Style.BRIGHT
    reset = Style.RESET_ALL

c = colors()

global api
api = '' #Insert your API KEY here

def CloseProgram():
    print(c.red + '[SYSTEM EXIT]')
    exit()

def Options():
    parser = argparse.ArgumentParser(description='Discover the world with Shodan')
    parser.add_argument('-t','--target', help="Shodan query, only with ('')")
    parser.add_argument('-o','--output', help='File name for save')
    parser.add_argument('-w','--html', help='Save devices with html format', action='store_true')
    parser.add_argument('-r','--random', help='Add a random query option [COUNTRY,DEVICE,MIX]', type=str)
    parser.add_argument('-p','--page', dest='number', help='The page number to access [DEFAULT 1]', default=1, type=int)
    parser.add_argument('-l','--limit', dest='results', help='Limit of results you want to obtain [DEFAULT 100]', default=100, type=int)

    args = parser.parse_args()
    return args.target, args.output, args.html, args.random, args.number, args.results

def ReplaceString(random,target): 
    if not random:
        target.strip('')

def Finder(target,output,html,random,number,results):
    try:
        motor = Shodan(api)
        query = SelectOption(random,target,motor,number,results)

        print('TOTAL FOUND: {}\n'.format(query['total']))
        time.sleep(1)

        for host in query['matches']:

            time.sleep(0.3)

            ip = host.get('ip_str','None')
            port = host.get('port','None')
            org = host.get('org','None')
            product = host.get('product','None')
            os = host.get('os','None')
            country = host['location']['country_name'] or 'None'
            city = host['location']['city'] or 'None'

            print('IP: {} \nPort: {} \nOrg: {}\nProduct: {} \nOperating System: {} \nCountry: {} \nCity: {}'.format(ip,port,org,product,os,country,city))
            print('\n')

            SaveFile(ip,port,org,product,os,country,city,output,html)

    except KeyboardInterrupt:
        CloseProgram()
    
    except Shodan.APIError as error:
        print(c.red + 'ERROR: {}'.format(error))

def ReportHtml(html,output): #In case of adding the html argument, check if file exists and add the extension
    if html:
        if os.path.exists(output):
            os.rename(output,output + '.html')
            option = input(c.cyan + 'Open HTML report in browser ? (YES/NO) ')
            if option.upper() == 'YES':
                url = os.getcwd()
                location = 'file://' + url + '/' + output + '.html'
                webbrowser.open_new_tab(location)
    else:
        if not output.endswith('.txt'):
            os.rename(output,output + '.txt')

def GetRandomCountry(): #Select a random country code from codes.txt file
    if os.path.exists('codes.txt'):

        codelist = open('codes.txt','r')
        codelist = codelist.read().split('\n')
        country = choice(codelist)
        print('Random Country: ' + country)
        country = 'country:' + country
        return country 

    else:
        print(c.red + 'File with country codes not found!')
        CloseProgram()

def GetRandomDevice(): #Select a random Shodan query from devices.txt file
    if os.path.exists('devices.txt'):

        devicelist = open('devices.txt','r')
        devicelist = devicelist.read().split('\n')
        selected = choice(devicelist)
        print('Random Device: ' + selected)
        return selected

    else:
        print(c.red + 'File with device list in path not found!')
        CloseProgram()

def SelectOption(random,target,motor,number,results): #Send a query to shodan depending on its optional arguments
    if random == 'DEVICE' and not target:

        selected = GetRandomDevice()
        query = motor.search(selected, page=number, limit=results)
        return query

    elif random == 'COUNTRY' and target:

        country = GetRandomCountry()
        query = motor.search('{} {}'.format(target,country), page=number, limit=results)
        return query

    elif not random and target:

        query = motor.search(target, page=number, limit=results)
        return query

    elif not target and random == 'MIX':

        selected = GetRandomDevice()
        country = GetRandomCountry()
        query = motor.search('{} {}'.format(selected,country), page=number, limit=results)
        return query
    
    elif random == 'COUNTRY' and not target:

        country = GetRandomCountry()
        query = motor.search(country, page=number, limit=results)
        return query

    else:
        print(c.red + 'Invalid options, remember: target argument is not compatible with --random DEVICE and MIX')
        CloseProgram()

def SaveFile(ip,port,org,product,os,country,city,output,html):
    file = open(output,'a')
    if html:
        file.write('{} {} {} {} {}'.format(org,product,os,country,city))
        file.write('<p><a href="http://{}:{}">{}:{}</a></p>\n'.format(ip,port,ip,port))
        file.close()
    else:
        file.write('{}:{}\n'.format(ip,port))
        file.close()
        
def ShowBanner():
    os.system('clear')
    logo = pyfiglet.figlet_format('DeepInside', font='slant')
    print(c.red + logo)
    print(c.reset)
    print(c.green + 'Created with love by Intrackeable \n')
    
def main():
    ShowBanner()

    target, output, html, random, number, results = Options() #Return argparse arguments

    if output:

        print(c.green + 'Searching, please wait...\n')
        ReplaceString(random,target)
        Finder(target,output,html,random,number,results)
        ReportHtml(html,output)

    elif not output:

        print(c.red + 'File name not found!')
        CloseProgram()

if __name__ == '__main__': #Main program
        main()
