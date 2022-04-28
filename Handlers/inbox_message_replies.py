import urllib

#@get #placeholder for flask or fastapi framework
def parse_encoded_message_components(request):
    message_components = urllib.parse.parse_qs(request)
    