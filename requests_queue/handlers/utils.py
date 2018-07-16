from json import loads


def parse_body(request):
    return loads(request.body.decode("utf-8"))
