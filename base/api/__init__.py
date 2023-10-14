from django.http import JsonResponse

def getroutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return JsonResponse(routes, safe=False)