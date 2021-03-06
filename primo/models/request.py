from lxml import etree

# namespaces
DEFAULT_NS_URI = "http://www.exlibris.com/primo/xsd/wsRequest"
DEFAULT_NS = "{%s}" % DEFAULT_NS_URI
UIC_NS_URI = "http://www.exlibris.com/primo/xsd/primoview/uicomponents"
UIC_NS = "{%s}" % UIC_NS_URI
PRIMO_NS_URI = "http://www.exlibris.com/primo/xsd/search/request"
PRIMO_NS = "{%s}" % PRIMO_NS_URI

REQUEST_NSMAP = {None: DEFAULT_NS_URI, 'uic': UIC_NS_URI}
PRIMO_NSMAP = {None: PRIMO_NS_URI}


class BaseRequest(object):

    def __init__(self, method_name, institution, group, on_campus, ip):
        """Base request
        :param method_name: name of the method to be used
        :param institution: code of the institution (PRIMO)
        :param group: code of the group (PRIMO)
        :param on_campus: true/false (PRIMO)
        :param ip: string representing IP address (PRIMO)
        """
        self.request_root = etree.Element(method_name, nsmap=REQUEST_NSMAP)
        self.request_root.append(self._add_element('institution', institution))
        self.request_root.append(self._add_element('group', group))
        self.request_root.append(self._add_element('onCampus', on_campus))
        self.request_root.append(self._add_element('ip', ip))

    @staticmethod
    def _add_element(name, value):
        e = etree.Element(name)
        e.text = value
        return e

    @staticmethod
    def _int_to_str(value):
        return str(value)


class SearchBriefRequest(BaseRequest):

    def __init__(self, institution, group, on_campus, ip, query_terms_bool_operator="AND", start_index=1, bulk_size=10):
        """
        Search brief
        (params institution, group, on_campus, ip as per BaseRequest)
        :param query_terms_bool_operator: operator AND/OR to be used between QueryTerms
        :param start_index: first item to retrieve
        :param bulk_size: number of items to retrieve
        """
        super(SearchBriefRequest, self).__init__('searchRequest', institution, group, on_campus, ip)
        self.start_index = start_index
        self.bulk_size = bulk_size
        self.psr = etree.Element('PrimoSearchRequest', nsmap=PRIMO_NSMAP)
        self.query_terms = etree.Element('QueryTerms')
        self.query_terms.append(self._add_element('BoolOpeator', query_terms_bool_operator))

    def _append_psr_parameters(self):
        """PrimoSearchRequest parameters to be appended
        *after* the <QueryTerms> (doesn't seem to work otherwise...??)
        """
        self.psr.append(self._add_element('StartIndex', self._int_to_str(self.start_index)))
        self.psr.append(self._add_element('BulkSize', self._int_to_str(self.bulk_size)))
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
        location = etree.Element(UIC_NS + "Location", type="local", value="")
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
        self._append_psr_parameters()
        self.request_root.append(self.psr)
        return etree.tostring(self.request_root)
