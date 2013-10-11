Python Primo Web Services
=========================

Python wrapper around the Primo SOAP Web Services.

First focus is on the search methods. This is a very early prototype.

Usage example
-------------

    from primo.service import SearchService
    from primo.models.request import SearchBriefRequest

    url = "<path of your WSDL>"

    service = SearchService(url)

    req = SearchBriefRequest("org", "group", "on campus", "ip")
    req.add_query_term("Salvador")
    req.add_query_term("Dali")

    # outputs the search results for now
    service.search_brief(req.get_request_as_string())
