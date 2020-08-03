#!/usr/bin/env python3
try:
    import os, time, argparse, webbrowser
    from shodan import Shodan
    from colorama import Fore
    from random import choice

except ImportError:
    print(Fore.RED + 'Use pip install -r requirements.txt')
    CloseProgram()

global api
api = '' #Insert your API KEY here

def CloseProgram():
    print(Fore.RED + '[SYSTEM EXIT]')
    exit()

def Options():
    parser = argparse.ArgumentParser(description='Discover the world with Shodan')
    parser.add_argument('-t','--target',help="Shodan query, only with ('')")
    parser.add_argument('-o','--output', help='File name for save')
    parser.add_argument('-w','--html',help='Save devices with html format', action='store_true')
    parser.add_argument('-r','--random',help='Add a random query option [COUNTRY,DEVICE,MIX]', type=str)
    parser.add_argument('-n','--number', help='The page number to access [DEFAULT 1]', default=1, type=int)

    args = parser.parse_args()
    return args.target, args.output, args.html, args.random, args.number

def ReplaceString(random,target): 
    if not random:
        target.strip('')

def Finder(target,output,html,random,number):
    motor = Shodan(api)
    query = SelectOption(random,target,motor,number)
    try:

        print('Total found: {}\n'.format(query['total']))
        time.sleep(1)

        for host in query['matches']:
            time.sleep(0.3)
            print('IP: {} \nPort: {} \nOrg: {} \nAsn: {} \nOperating System: {}'.format(host.get('ip_str','None'), host.get('port','None'), host.get('org','None'), host.get('asn','None'), host.get('os','None')))
            for x in host['location']:
                print(x + ': ' + str(host['location'][x]))
            print('\n')
            SaveFile(host,output,html)

    except KeyboardInterrupt:
        CloseProgram()

def ReportHtml(html,output): #In case of adding the html argument, check if file exists and add the extension
    if html:
        if os.path.isfile(output):
            os.rename(output,output + '.html')
            option = input(Fore.CYAN + 'Open html report in browser ? (YES/NO) ')
            if option == 'YES' or option == 'yes':
                url = os.getcwd()
                location = 'file://' + url + '/' + output + '.html'
                webbrowser.open_new_tab(location)
            else:
                pass

def GetRandomCountry(): #Select a random country code from codes.txt file
    if os.path.isfile('codes.txt'):

        codelist = open('codes.txt','r')
        codelist = codelist.read().split('\n')
        country = choice(codelist)
        country = 'country:' + country
        print('Random ' + country)
        return country 

    else:
        print(Fore.RED + 'File with country codes not found!')
        CloseProgram()

def GetRandomDevice(): #Select a random Shodan query from devices.txt file
    if os.path.isfile('devices.txt'):

        devicelist = open('devices.txt','r')
        devicelist = devicelist.read().split('\n')
        selected = choice(devicelist)
        print('Random device: ' + selected)
        return selected

    else:
        print(Fore.RED + 'File with device list in path not found!')
        CloseProgram()

def SelectOption(random,target,motor,number): #Send a query to shodan depending on its optional arguments
    if random == 'DEVICE' and not target:

        selected = GetRandomDevice()
        query = motor.search(selected, page=number)
        return query

    elif random == 'COUNTRY' and target:

        country = GetRandomCountry()
        query = motor.search('{} {}'.format(target,country), page=number)
        return query

    elif not random and target:

        query = motor.search(target, page=number)
        return query

    elif not target and random == 'MIX':

        selected = GetRandomDevice()
        country = GetRandomCountry()
        query = motor.search('{} {}'.format(selected,country), page=number)
        return query
    
    elif random == 'COUNTRY' and not target:

        country = GetRandomCountry()
        query = motor.search(country)
        return query

    else:
        print(Fore.RED + 'Invalid options, remember: target argument is not compatible with --random DEVICE and MIX')
        CloseProgram()

def SaveFile(host,output,html):
    file = open(output,'a')
    if html:
        file.write('<p><a href="http://{}:{}">{}:{}</a></p>\n'.format(host['ip_str'],host['port'],host['ip_str'],host['port']))
    else:
        file.write('{}:{}\n'.format(host['ip_str'],host['port']))
        
def ShowBanner():
    os.system('clear')
    os.system('cat logo.txt')  
    print(Fore.GREEN + 'Created with love by intrackeable \n')
    
def main():
    ShowBanner()

    target, output, html, random, number = Options() #Return argparse arguments

    if output:

        print(Fore.GREEN + 'Searching, please wait...\n')
        ReplaceString(random,target)
        Finder(target,output,html,random,number)
        ReportHtml(html,output)

    elif not output:

        print(Fore.RED + 'File name not found!')
        CloseProgram()

if __name__ == '__main__': #Main program
        main()