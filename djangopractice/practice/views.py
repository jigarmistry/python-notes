import json
import time

from django.shortcuts import render,get_object_or_404 ,get_list_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from django.utils.text import unescape_entities
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from .models import Publisher, Author,Post,Project,API

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

class PublisherList(ListView):
    model = Publisher
    template_name = "practice/publisherlist.html"

class PostView(generic.ListView):
    template_name = 'practice/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'practice/blog_detail.html', {'post': post})

@csrf_exempt
def api_response(request, project_name , api_name):
    project = get_object_or_404(Project, name=project_name)
    api = get_object_or_404(API, project=project , path=api_name)
    data = api.response_body

    if api.content_type in ["application/json" , "text/json"]:
        data = json.dumps(strip_tags(mark_safe(data)))
        data = json.loads(data)
    elif api.content_type in ["application/xml" ,"text/xml"]:
        data = unescape_entities(strip_tags(mark_safe(data)))
    else:
        data = mark_safe(data)

    data = data.replace("&quot;","\"").replace("&nbsp;","")

    if request.method == api.method.upper():
        if api.response_delay not in ["0", ""] :
            time.sleep(int(api.response_delay))
        return HttpResponse(data, content_type=api.content_type, status=int(api.res_status))
    else:
        data = "Not Valid Method. Request method should be %s" % (api.method.upper())
        return HttpResponse(data)

def api_list(request, project_name):
    project_url = request.build_absolute_uri()
    project = get_object_or_404(Project, name=project_name)
    api = get_list_or_404(API.objects.order_by('path'), project=project)

    return render(request, 'practice/api_list.html', {'api_list': api,'project_name':project_name,'project_url':project_url})

def project_list(request):
    project_url = request.build_absolute_uri()
    project = Project.objects.all()
    return render(request, 'practice/project_list.html', {'project_list': project,'project_url':project_url})
