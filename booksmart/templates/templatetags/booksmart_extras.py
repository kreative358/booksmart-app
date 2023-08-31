from django import template
register = template.Library()

@register.simple_tag()
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        # print('from extras: querystring', querystring)
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring)
        # print('from extras: filtered_querystring', filtered_querystring)
        encoded_querystrting = '&'.join(filtered_querystring)
        # print('from extras: encoded_querystrting', encoded_querystrting)
        url = '{}&{}'.format(url, encoded_querystrting)

    return url