import ipaddress
import re
import urllib
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import datetime
import time
from dateutil.parser import parse as date_parse
import sys
import ssl
import socket
from bs4 import BeautifulSoup
import datetime



class Extract:
    def __init__(self, url):
        self.url = url
        self.featureList = []


    def urlFormat(self):

        if not re.match(r"^https?", self.url):
            normalized_url = "http://" + self.url
        else:
            normalized_url = self.url

        return normalized_url


    def urlInfo(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            response = ""
            soup = -999

        domain = re.findall(r"://([^/]+)/?", url)[0]
        if re.match(r"^www.",domain):
    	       domain = domain.replace("www.","")

        try:
            whois_response = whois.whois(domain)
        except:
            whois_response = "none"

        return domain, response, soup, response, whois_response



    def url_having_ip(self, url):
        ippattern = '(?:http.*://)?(?P<ip>([0-9]+)(?:\.[0-9]+){3}).*'
        ipmatch = re.search(ippattern,url)
        if ipmatch is None:
            self.featureList.append(0)
        else:
            self.featureList.append(1)


    def url_length(self, url):
        length=len(url)
        if(length>54):
            self.featureList.append(1)
        else:
            self.featureList.append(0)


    def shortning_service(self, url):
        match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
        if match:
            self.featureList.append(1)
        else:
            self.featureList.append(0)


    def atCharacter(self, url):
        if re.findall("@", url):
            self.featureList.append(1)
        else:
            self.featureList.append(0)


    def doubleSlash(self, url):
        list=[x.start(0) for x in re.finditer('//', url)]
        if list[len(list)-1]> 6:
            self.featureList.append(1)
        else:
            self.featureList.append(0)


    def prefixSuffix(self, url):
        if re.findall(r"https?://[^\-]+-[^\-]+/", url):
            self.featureList.append(1)
        else:
            self.featureList.append(0)


    def subDomains(self, url):
        if len(re.findall("\.", url)) < 2:
            self.featureList.append(0)
        else:
            self.featureList.append(1)


    def httpsToken(self, url):
        if re.findall(r"^https://", url):
            #print("benign")
            self.featureList.append(0)
        else:
            self.featureList.append(1)
            #print("malicious")


    def favIcon(self, url, domain, soup):
        if soup == -999:
            #print("except")
            self.featureList.append(1)
        else:
            try:
                for head in soup.find_all('head'):
                    if head.link == None:
                        self.featureList.append(1)
                    for head.link in soup.find_all('link', href=True):
                        dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                        if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                            self.featureList.append(0)
                            raise StopIteration
                        else:
                            self.featureList.append(1)
                            raise StopIteration
            except StopIteration:
                pass


    def requestURL(self, url, domain, soup):
        i = 0
        success = 0
        if soup == -999:
            self.featureList.append(1)
        else:
            for img in soup.find_all('img', src= True):
               dots= [x.start(0) for x in re.finditer('\.', img['src'])]
               if url in img['src'] or domain in img['src'] or len(dots)==1:
                  success = success + 1
               i=i+1

            for audio in soup.find_all('audio', src= True):
               dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
               if url in audio['src'] or domain in audio['src'] or len(dots)==1:
                  success = success + 1
               i=i+1

            for embed in soup.find_all('embed', src= True):
               dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
               if url in embed['src'] or domain in embed['src'] or len(dots)==1:
                  success = success + 1
               i=i+1

            for iframe in soup.find_all('iframe', src= True):
               dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
               if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
                  success = success + 1
               i=i+1

            try:
               percentage = success/float(i) * 100
               if percentage < 61.0 :
                    self.featureList.append(0)
               else :
                    self.featureList.append(1)
            except:
                self.featureList.append(0)


    def anchorURL(self, url, domain, soup):
        percentage = 0
        i = 0
        unsafe=0
        if soup == -999:
            self.featureList.append(1)
        else:
            for a in soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                    unsafe = unsafe + 1
                i = i + 1

            try:
                percentage = unsafe / float(i) * 100
                if percentage < 97.0:
                    self.featureList.append(0)

                else:
                    self.featureList.append(1)
            except:
                self.featureList.append(0)


    def linksTags(self, url, domain, soup):
        i=0
        success =0
        if soup == -999:
            self.featureList.append(1)
        else:
            for link in soup.find_all('link', href= True):
               dots=[x.start(0) for x in re.finditer('\.',link['href'])]
               if url in link['href'] or domain in link['href'] or len(dots)==1:
                  success = success + 1
               i=i+1

            for script in soup.find_all('script', src= True):
               dots=[x.start(0) for x in re.finditer('\.',script['src'])]
               if url in script['src'] or domain in script['src'] or len(dots)==1 :
                  success = success + 1
               i=i+1
            try:
                percentage = success / float(i) * 100

                if percentage < 90.0 :
                    self.featureList.append(0)
                else :
                    self.featureList.append(1)

            except:
                self.featureList.append(0)



    def redirectURL(self, response):
        if response == "":
            self.featureList.append(1)
        else:
            if len(response.history) <= 1:
                self.featureList.append(0)
            else:
                self.featureList.append(1)


    def statusBar(self, response):
        if response == "" :
            self.featureList.append(1)
        else:
            if re.findall("<script>.+onmouseover.+</script>", response.text):
                self.featureList.append(1)
            else:
                self.featureList.append(0)


    def rightClick(self, response):
        if response == "":
            self.featureList.append(1)
        else:
            if re.findall(r"event.button ?== ?2", response.text):
                self.featureList.append(1)
            else:
                self.featureList.append(0)


    def popularWindow(self, response):
        if response == "":
            self.featureList.append(1)
        else:
            if re.findall(r"alert\(", response.text):
                self.featureList.append(1)
            else:
                self.featureList.append(0)


    def domainLife(self, response, whois_response):
        if response == "":
            self.featureList.append(1)
        else:
            try:
                creation_date = whois_response.get('creation_date')
                timing = datetime.datetime.now() - creation_date
                if timing.days/30 >= 12:
                    self.featureList.append(0)
                else:
                    self.featureList.append(1)
            except:
                self.featureList.append(0)


    def dnsRecord(self, domain, whois_response):
        try:
            expiration_date = whois_response.expiration_date
            dns = 1
            try:
                d = whois.whois(domain)
            except:
                dns=-1


            if dns == -1:
                self.featureList.append(1)
            else:
                try:
                    timing = expiration_date - datetime.datetime.now()
                    if timing.days/366 >= 1:
                        self.featureList.append(0)
                    else:
                        self.featureList.append(1)
                except:
                    self.featureList.append(0)

        except:
            self.featureList.append(1)


    def pageLinks(self, response):
        if response == "":
            self.featureList.append(1)
        else:
            number_of_links = len(re.findall(r"<a href=", response.text))
            if number_of_links <= 2:
                self.featureList.append(1)
            else:
                self.featureList.append(0)




    # this is the main function of work
    def inspectURL(self):
        url = self.urlFormat()
        domain, response, soup, response, whois_response= self.urlInfo(url)
        #url format
        self.url_having_ip(url)
        self.url_length(url)
        self.shortning_service(url)
        self.atCharacter(url)
        self.doubleSlash(url)
        self.prefixSuffix(url)
        self.subDomains(url)
        self.httpsToken(url)
        self.favIcon(url, domain, soup)

        #url objects
        self.requestURL(url, domain, soup)
        self.anchorURL(url, domain, soup)
        self.linksTags(url, domain, soup)

        #html and js
        self.redirectURL(response)
        self.statusBar(response)
        self.rightClick(response)
        self.popularWindow(response)

        #domain
        self.domainLife(response, whois_response)
        self.dnsRecord(domain, whois_response)
        self.pageLinks(response)

        return self.featureList
