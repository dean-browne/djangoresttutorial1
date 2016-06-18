from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class JSONResponse(HttpResponse):
    """
    A http response that returns it's content in JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        # This calls the init method of the super class...
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
    """
    :param request: request (from urls.py)
    :return: List of all codes snippet or updates a snippet
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer = SnippetSerializer(data=data)
            serializer.save()
            return JSONResponse(serializer.data, status=201)

        return JSONResponse(serializer.error, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    :param request: request (from urls.py)
    :param pk: the primary key of the requested snippet
    :return: details of the requested snippet
    """
    try:
        snippet = Snippet.objects.get(pk=pk)

    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)

        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

