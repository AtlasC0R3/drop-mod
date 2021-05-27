class _SearchField:
    """A search field. Can be from a Wikipedia result field to a search result."""
    name = ""
    value = ""
    url = ""

    def __getitem__(self, item):
        return getattr(self, item)

    def from_dict(self, field: dict):
        self.name = field.get('name') if field.get('name') else field.get('title')
        self.value = field.get('desc') if field.get('desc') else field.get('value')
        self.url = field.get('url')
        return self


class Search:
    """The class for search results."""
    """
    {'title': 'Wikipedia',
     'description': 'Wikipedia is a free, multilingual online encyclopedia written ...',
     'url': 'https://en.wikipedia.org/wiki/Wikipedia', 'source': 'Wikipedia',
     'image': 'https://duckduckgo.com/i/a96348db.png',
     'fields': [{'name': 'Available in', 'value': 'languages'},
                {'name': 'Country of origin', 'value': 'United States'},
                {'name': 'Created by', 'value': 'Jimmy Wales, Larry Sanger'},
                {'name': 'Website', 'value': 'wikipedia.org'},
                {'name': 'Commercial', 'value': 'No'},
                {'name': 'Registration', 'value': 'Optional'}],
     'infobox': True}
    """
    title = ""
    description = ""
    url = ""
    source = ""
    engine = ""
    engine_icon = ""
    image = ""
    fields = []

    def __getitem__(self, item):
        # so that people using drop-mod with dictionaries will still be able to use it
        # hopefully without changing much. sort-of legacy support, I guess you can call it that?
        return getattr(self, item)

    def from_dict(self, search_result: dict):
        self.title = search_result['title']
        self.description = search_result['description']
        self.url = search_result['url']
        self.image = search_result['image']
        self.fields = [_SearchField().from_dict(x) for x in search_result['fields']]
        self.engine = search_result.get('engine')
        self.engine_icon = search_result.get('engine_icon')
        return self
