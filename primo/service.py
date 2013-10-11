from xml.etree import ElementTree
from suds.client import Client


class SearchService(object):

    def __init__(self, url):
        self.client = Client(url)

    def search_brief(self, request):
        print request
        response = self.client.service.searchBrief(request)
        xml_str = response.encode('ascii', 'ignore')
        print xml_str
        print ElementTree.ElementTree(ElementTree.fromstring(xml_str))
