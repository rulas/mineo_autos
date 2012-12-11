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


from google import search           # find at http://breakingcode.wordpress.com/2010/06/29/google-search-python/
import BeautifulSoup                 #find at http://www.crummy.com/software/BeautifulSoup/
import urlparse
import urllib
import csv
import sys


NUM_URLS = 500
SEARCH_CRITERIA = r'(autos carros automoviles) venta jalisco -chocados -autoestereos site:.mx -renta -partes -seguro -foro -blog -"seccion amarilla"'
BASE_DOMAINS = ".com.mx .com .net .mx".split()

fields = {
    "imagen"        : "imagen".split(),
    "modelo"        : "modelo mod".split(),
    "año"           : "año".split(),
    "marca"         : "marca".split(),
    "precio"        : "precio".split(),
    "colores"       : "colores".split(),
    "descuento"     : "descuento promocion desc".split(),
    "bateria"       : "bateria pila".split(),
    "origen"        : "ciudad".split(),
    "kilometraje"   : "kilometraje km k.m.".split(),
    "descripcion"     : "descipcion".split(),
    "forma de pago" : ["forma de pago", "metodo de pago", "credito", "contado"],
    "vendedor"      : "vendedor anunciante".split(),
    "telefono"      : "telefono tel celular cel".split(), #agregar un regex para numero telefonico
    "contacto"      : "contacto".split(),      # buscar un correo electronica
    "enlaces"       : "href".split()
}

TITLES = fields.keys()

def not_duplicate(urls):
    current_domains = []
    filtered_urls = []

    for url in urls:
        #print str(urlparse.urlparse(url).netloc).
        host = urlparse.urlparse(url).hostname

        domain = ""

        # figure out the domain
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

        if domain not in current_domains:
            current_domains.append(domain)
            filtered_urls.append(url)


    #print filtered_urls

    return filtered_urls

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress)

def gather_data(urls):

    global fields

    gathered_data = []
    total = len(urls)

    for number, url in enumerate(urls):
        data = urllib.urlopen(url).read()

        #data = bs4.BeautifulSoup(data).body.get_text(strip=True).lower()

        data = data.lower()
        # TODO: we would improve the search below if we convert from unicode to ascii such as
        # we convert chars like ? to u only for a simple search. Not for now

        #print data
        #print bs4.BeautifulSoup(data).prettify()
        found_fields = []

        for field, words in fields.iteritems():
            for word in words:
                if word in data:
                    found_fields.append(field)
                    break

        gathered_data.append([url, found_fields])

        update_progress(number/total)

    return gathered_data

def format_row(row_data):
    pass

def send_to_csv(data):
    global fields
    titles = TITLES
    titles.insert(0, "url")
    print titles

    with open('cars_db.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel', )
        csvwriter.writerow(titles)

        for row in data:
            url, found_fields = row
            print row

            csv_row = []
            csv_row.append(url)

            for title in titles[1:]:
                if title in found_fields:
                    csv_row.append('YES')
                else:
                    csv_row.append('NO')

            csvwriter.writerow(csv_row)

#def get_search_results(query):
#    import urllib2
#    import simplejson
#
#    # The request also includes the userip parameter which provides the end
#    # user's IP address. Doing so will help distinguish this legitimate
#    # server-side traffic from traffic which doesn't come from an end-user.
#    url = ('https://ajax.googleapis.com/ajax/services/search/web'
#           '?v=1.0&q=Paris%20Hilton&userip=USERS-IP-ADDRESS')
#
#    request = urllib2.Request(
#        url, None, {'Referer': /* Enter the URL of your site here */})
#    response = urllib2.urlopen(request)
#
#    # Process the JSON string.
#    results = simplejson.load(response)

def main():

    # get a list with first NUM_URLS
    urls = []

    # now have some fun with the results...

    for url in search(SEARCH_CRITERIA, stop=NUM_URLS):
        urls.append(str(url))

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


