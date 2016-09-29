from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
import re
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *


#BLOG ADMIN
@login_required
@staff_member_required
def publish_post (request, page):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		title = request.POST.get('title', '')
		body = request.POST.get('body', '')
		if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None
		if page == 'post':
			post = Post (title = title, post_image = headshot, post_body = body)
			post.save()
		elif page == 'gallery':
			post = Gallery (title = title, image = headshot, description = body)
			post.save()
		else:
			pass #error message
	return render_to_response ('blog/publish.html', {'page':page}, context_instance = RequestContext(request))
	


@login_required
@staff_member_required	
def edit_post (request, id= 0):
	if id == "0":
		post = Post.objects.all()
		return render_to_response ('blog/edit.html', {'post':post, 'page':'post'}, context_instance = RequestContext(request))
	else:
		post = Post.objects.get(id = id)
		return render_to_response ('blog/edit.html', {'post':post, 'page':'post', 'data':'data'}, context_instance = RequestContext(request))
		
	if request.method == 'POST':
		title = request.POST.get('title', '')
		body = request.POST.get('body', '')
		if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None
		post = Post.objects.get(id = id)
		post.title = title
		post.post_body = body
		post.post_image = headshot
		post.save()
		
		return render_to_response ('index.html', context_instance = RequestContext(request))
		
	
@login_required
@staff_member_required	
def edit_gallery (request, id = 0):
	if id == "0":
		post = Gallery.objects.all()
		return render_to_response ('blog/edit.html', {'post':post, 'page':'gallery'}, context_instance = RequestContext(request))
	else:
		post = Gallery.objects.get(id = id)
		return render_to_response ('blog/edit.html', {'post':post, 'page':'gallery', 'data':'data'}, context_instance = RequestContext(request))
		
	if request.method == 'POST':
		title = request.POST.get('title', '')
		body = request.POST.get('body', '')
		if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None
		post = Gallery.objects.get(id = id)
		post.title = title
		post.body = body
		post.description = headshot
		post.save()
		
		return render_to_response ('index.html', context_instance = RequestContext(request))
		



#BLOG DISPLAY

def load_post (request):
	try:
		post = Post.objects.filter (page = page)
		
		paginator = Paginator(products, 16) # 16 posts in each page
		pages = request.GET.get('page')
		try:
			posts = paginator.page(pages)
		except PageNotAnInteger:
			# If page is not an integer deliver the first page
			posts = paginator.page(1)
		except EmptyPage:
			# If page is out of range deliver last page of results
			posts = paginator.page(paginator.num_pages)
		return render_to_response ('product.html', {'page': pages, 'posts': posts, 'post': post}, context_instance = RequestContext(request))
	except:
		return render_to_response ('index.html', context_instance = RequestContext(request))
	
	
def post_detail (request, id, slug):
	post = Post.objects.get(id=id, slug=slug)
	return render_to_response('product.html', {'post': post}, context_instance = RequestContext(request))


	
def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
	
def search(request):
	
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		
		terms = normalize_query(query_string)
		result = []
		for term in terms:
			a = Post.objects.filter(name__icontains = term).distinct()
			for f in a:
				result.append(f)
		paginator = Paginator(result, 12)
		pages = request.GET.get('page')
		try:
			posts = paginator.page(pages)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
			
		return render_to_response('search.html', { 'search_query': query_string, 'result': result, 'page': pages, 'posts': posts, }, context_instance = RequestContext(request))
	return render_to_response('index.html', context_instance = RequestContext(request))