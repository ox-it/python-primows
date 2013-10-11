from lxml import etree

DEFAULT_NS = "http://www.exlibris.com/primo/xsd/wsRequest"
NS = "{%s}" % DEFAULT_NS
UIC_NS = "http://www.exlibris.com/primo/xsd/primoview/uicomponents"
UIC = "{%s}" % UIC_NS
PRIMO_NS = "http://www.exlibris.com/primo/xsd/search/request"
PRIMO = "{%s}" % PRIMO_NS

NSMAP = {None : DEFAULT_NS, 'uic': UIC_NS}
PRIMONSMAP = { None: PRIMO_NS }


class BaseRequest(object):

    def __init__(self, institution, group, on_campus, ip):
        pass


class SearchBriefRequest(object):

    def __init__(self, institution, group, on_campus, ip, query_terms_bool_operator="AND"):
        self.request_root = etree.Element('searchRequest', nsmap=NSMAP)

        self.request_root.append(self._add_element('institution', institution))
        self.request_root.append(self._add_element('group', group))
        self.request_root.append(self._add_element('onCampus', on_campus))
        self.request_root.append(self._add_element('ip', ip))

        self.psr = etree.Element('PrimoSearchRequest', nsmap=PRIMONSMAP)

        self.query_terms = etree.Element('QueryTerms')
        self.query_terms.append(self._add_element('BoolOpeator', query_terms_bool_operator))

    def append_psr_parameters(self):
        self.psr.append(self._add_element('StartIndex', "1"))
        self.psr.append(self._add_element('BulkSize', "20"))
        self.psr.append(self._add_element('DidUMeanEnabled', "false"))
        self.psr.append(self._add_element('HighlightingEnabled', "false"))

        languages = etree.Element('Languages')
        languages.append(self._add_element('Language', 'eng'))
        self.psr.append(languages)

        sort_by_list = etree.Element('SortByList')
        sort_by_list.append(self._add_element('SortField', 'popularity'))
        self.psr.append(sort_by_list)

        self.psr.append(self._add_element('DisplayFields', "creator"))

        locations = etree.Element('Locations')
        location = etree.Element(UIC + "Location", type="local", value="")
        locations.append(location)
        self.psr.append(locations)

    def add_query_term(self, value, index_field="any", precision_operator="contains"):
        """Add a query term to the search request
        :param value:
        :param index_field:
        :param precision_operator:
        """
        qt = etree.Element('QueryTerm')
        qt.append(self._add_element('IndexField', index_field))
        qt.append(self._add_element('PrecisionOperator', precision_operator))
        qt.append(self._add_element('Value', value))
        self.query_terms.append(qt)

    def get_request_as_string(self):
        self.psr.append(self.query_terms)
        self.append_psr_parameters()
        self.request_root.append(self.psr)
        return etree.tostring(self.request_root, pretty_print=True)

    @staticmethod
    def _add_element(name, value):
        e = etree.Element(name)
        e.text = value
        return e

