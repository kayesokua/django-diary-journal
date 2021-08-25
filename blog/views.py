from functools import total_ordering
from django.db.models.aggregates import Sum
from django.views import generic
from .models import Comment, EditableFields, PostViews, Post, SociaLinks
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from django.db.models import Count
import datetime
from django.db.models import Q

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(status=1).count()
        context['total_comments'] = Comment.objects.filter(active=True).count()
        context['tag_count'] = Tag.objects.all().annotate(num_times=Count('taggit_taggeditem_items')).order_by("-num_times")
        context['social_links'] =  SociaLinks.objects.all()
        context['liked_posts'] = Post.objects.filter(status=1).order_by("-total_likes")[:3]
        context['total_likes_count'] = Post.objects.filter(total_likes__gte=1).aggregate(Sum('total_likes'))['total_likes__sum']
        context['total_views_count'] = PostViews.objects.all().count()
        context['total_word_count'] = Post.objects.filter(status=1,content__isnull=False).values_list('content')
        
        return context


def tag_detail(request, tag):
    template_name = 'category.html'
    posts = Post.objects.filter(tags__slug=tag)
    tag_count = Tag.objects.all().annotate(num_times=Count('taggit_taggeditem_items')).order_by("-num_times")
    liked_posts = Post.objects.filter(status=1).order_by("-total_likes")[:3]
    social_links = SociaLinks.objects.all()
    total_likes_count = Post.objects.filter(total_likes__gte=1).aggregate(Sum('total_likes'))['total_likes__sum']
    total_views_count = PostViews.objects.all().count()
    total_word_count = Post.objects.filter(status=1,content__isnull=False).values_list('content')

    return render(
        request,
        template_name,
        {
            "posts": posts,
            "tag": tag,
            "tag_count": tag_count,
            "liked_posts": liked_posts,
            "social_links": social_links,
            "total_likes_count": total_likes_count,
            "total_views_count":total_views_count,
            "total_word_count": total_word_count
            
            }
        )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    total_posts =  Post.objects.filter(status=1).count()
    total_comments = post.comments.filter(active=True).count()
    tag_count = Tag.objects.all().annotate(num_times=Count('taggit_taggeditem_items')).order_by("-num_times")
    views_count = PostViews.objects.all().filter(post=post).count()
    liked_posts = Post.objects.filter(status=1).order_by("-total_likes")[:3]
    social_links = SociaLinks.objects.all()
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    total_likes_count = Post.objects.filter(total_likes__gte=1).aggregate(Sum('total_likes'))['total_likes__sum']
    total_views_count = PostViews.objects.all().count()
    total_views = PostViews.objects.filter(post=post).count()
    total_word_count = Post.objects.filter(status=1,content__isnull=False).values_list('content')

    #If Session Key won't generate 
    if not request.session.session_key:
        request.session.save()
        session = request.session.session_key

    #Saving sessions    
    if not PostViews.objects.filter(post=post,session=request.session.session_key):
        view = PostViews(post=post, ip=request.META['REMOTE_ADDR'], created=datetime.datetime.now(), session=request.session.session_key)
        view.save()
    else:
        print("session count is " + str(views_count))
    
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "total_comments":total_comments,
            "total_posts": total_posts,
            "tag_count":tag_count,
            "liked_posts":liked_posts,
            "social_links":social_links,
            "total_likes_count":total_likes_count,
            "views_count": views_count,
            "total_views_count":total_views_count,
            "total_views":total_views,
            "total_word_count":total_word_count
            },
    )

def like_post(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.total_likes += 1
        post.save()
    return redirect(request.META["HTTP_REFERER"])

def unlike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.total_likes -= 1
        post.save()
    return redirect(request.META["HTTP_REFERER"])

def about_me(request):

    #Editable Fields
    about_intro = EditableFields.objects.filter(field_id__contains="about_intro")
    about_feature = EditableFields.objects.filter(field_id__contains="about_feature")
    feature_1 = EditableFields.objects.filter(field_id__contains="feature_1")
    feature_2 = EditableFields.objects.filter(field_id__contains="feature_2")
    feature_3 = EditableFields.objects.filter(field_id__contains="feature_3")
    feature_box1 = EditableFields.objects.filter(field_id__contains="feature_box1")
    feature_box2 = EditableFields.objects.filter(field_id__contains="feature_box2")
    social_links = SociaLinks.objects.all()
    total_posts =  Post.objects.filter(status=1).count()
    total_likes_count = Post.objects.filter(total_likes__gte=1).aggregate(Sum('total_likes'))['total_likes__sum']
    total_views_count = PostViews.objects.all().count()
    total_word_count = Post.objects.filter(status=1,content__isnull=False).values_list('content')

    return render(request,'about.html',{
        'social_links':social_links,
        'about_intro':about_intro,
        'about_feature':about_feature,
        'feature_1':feature_1,
        'feature_2':feature_2,
        'feature_3':feature_3,
        'feature_box1':feature_box1,
        'feature_box2':feature_box2,
        'total_posts':total_posts,
        "total_likes_count":total_likes_count,
        "total_views_count":total_views_count,
        "total_word_count": total_word_count

    })

def post_search(request):
    social_links = SociaLinks.objects.all()
    total_posts =  Post.objects.filter(status=1).count()
    total_likes_count = Post.objects.filter(total_likes__gte=1).aggregate(Sum('total_likes'))['total_likes__sum']
    total_views_count = PostViews.objects.all().count()
    tag_count = Tag.objects.all().annotate(num_times=Count('taggit_taggeditem_items')).order_by("-num_times")
    liked_posts = Post.objects.filter(status=1).order_by("-total_likes")[:3]
    total_word_count = Post.objects.filter(status=1,content__isnull=False).values_list('content')


    query=request.GET['query']
    print(len(query)<51)

    if len(query)>51:
        posts=Post.objects.none()
    else:        
        posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-created_on')

    if posts.count()==0:
        print("No search results found. Please refine your query.")
    
    return render(request, 'search.html', 
        {
            'posts': posts,
            'query': query,
            'total_posts':total_posts,
            'total_likes_count':total_likes_count,
            'total_views_count':total_views_count,
            'tag_count':tag_count,
            'liked_posts':liked_posts,
            'social_links':social_links,
            "total_word_count":total_word_count
            
            })
