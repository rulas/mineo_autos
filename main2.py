#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lrvillan
#
# Created:     17/11/2012
# Copyright:   (c) lrvillan 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------



import urlparse
import urllib
import csv
import sys
import os


from google import search        # find at http://breakingcode.wordpress.com/2010/06/29/google-search-python/
from bs4 import BeautifulSoup   #find at http://www.crummy.com/software/BeautifulSoup/


NUM_URLS = 1000
SEARCH_CRITERIA = r'(autos carros automoviles) venta jalisco -chocados -autoestereos site:.mx -renta -partes -seguro -foro -blog -"seccion amarilla"'



def not_duplicate(urls):
    current_domains = []
    filtered_urls = []

    for url in urls:
        #print str(urlparse.urlparse(url).netloc).
        domain = get_domain(url)

        if domain not in current_domains:
            current_domains.append(domain)
            filtered_urls.append(url)

    return filtered_urls

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress)

def gather_data(urls):

    global fields

    gathered_data = []

    for url in urls:
        try:
            html_data = urllib.urlopen(url).read()
            soup = BeautifulSoup(html_data)
        except Exception:
            print "oops, somthing went wrong"
            continue

        for link in soup.find_all('a'):
            try:
                href = link['href']
                if 'http' in href:
                    gathered_data.append([url, str(href)])
            except:
                continue

    return gathered_data


def send_to_csv(data):
    global fields
    titles = ["fuente", "destino"]

    with open('cars_db_links.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel', )
        csvwriter.writerow(titles)

        for row in data:
            csvwriter.writerow(row)

def get_urls(force=False):
    prev_results_path = 'search_results.txt'
    urls =[]

    if force or not os.path.exists(prev_results_path):
        for url in search(SEARCH_CRITERIA, stop=NUM_URLS):
                urls.append(str(url))

        if force:
            try:
                urls = [url + "\n" for url in urls]
                open(prev_results_path, 'wb').writelines(urls)
            except IOError:
                print "oops, we could not save the results to file"
    else:
        try:
            urls = open(prev_results_path, 'rb').readlines()
            urls = [url.strip() for url in urls]
        except IOError:
            print "oops, no previous results yet"

    return urls


def get_domain(url):
    BASE_DOMAINS = ".com.mx .com .net .mx".split()

    host = urlparse.urlparse(url).hostname
    domain = ""

    for base in BASE_DOMAINS:
        if base in host:
            domain_index = host.index(base)
            domain = host[:domain_index]

            # check if subdomains exists
            if "." in domain:
                subdomain = domain.split(".")[-1]
            else:
                subdomain = domain

            domain = subdomain + base
            break

    return domain

def main():

    # get a list with first NUM_URLS
    urls = get_urls(force=False)

    # filter those that belongs to the same domain
    urls = not_duplicate(urls)

    # go to each web page and gather data
    data = gather_data(urls)

    # create a CSV file with data just gathered
    send_to_csv(data)

    #sys.exit(0)

    # DONE!
    print "DONE"




if __name__ == '__main__':
    main()


