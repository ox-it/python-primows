from xml.etree import ElementTree
from suds.client import Client


class SearchService(object):

    def __init__(self, url):
        self.client = Client(url)

    def search_brief(self, request):
        response = self.client.service.searchBrief(request)
        xml_str = response.encode('ascii', 'ignore')
        tree = ElementTree.ElementTree(ElementTree.fromstring(xml_str))
        print list(tree.iter())