import urllib

#@get #placeholder for flask decorator
def parse_encoded_message_components(request):
    message_components = urllib.parse.parse_qs(request)
    