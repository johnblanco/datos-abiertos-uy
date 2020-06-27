from os import system

import requests
from xml.etree import ElementTree


def get_current_csv_urls():
    response = requests.get('https://catalogodatos.gub.uy/dataset/'
                            'agesic-creacion-de-empresas-a-traves-de-empresa-en-el-dia.xml', verify=False)
    tree = ElementTree.fromstring(response.content)
    dataset = tree[0]

    distribution_tags = list(filter(lambda x: 'distribution' in x.tag, dataset))
    urls = []
    for d in distribution_tags:
        first_child = d[0]
        url_tag = list(filter(lambda x: 'accessURL' in x.tag, first_child))[0]
        url = list(url_tag.attrib.values())[0]
        urls.append(url)
    return urls


def download_csvs(urls):
    system('rm -rf csvs/empresa')
    system('mkdir csvs/empresa')
    for url in urls:
        system("wget {} --no-check-certificate".format(url))
    system("mv *.csv csvs/empresa")


if __name__ == '__main__':
    urls = get_current_csv_urls()
    download_csvs(urls)
