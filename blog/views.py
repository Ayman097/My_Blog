from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag

# Create your views here.

# Retrive All Posts

def post_list(request, tag_slug=None):
    posts_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])


    # Pagination with 3 posts per page
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)

    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})

# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

# Post Details

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                               status=Post.Status.PUBLISHED,
                               slug=post,
                               publish__year=year,
                               publish__month=month,
                               publish__day=day
                    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    '''
     retrieving list of IDs for the tags of the current post.
     The "values_list()" QuerySet returns tuples with the values for the given fields.
     flat=True ==> to get single values such as [1, 2, 3, ...] instead of one-tuples such as [(1,), (2,), (3,) ...]
    '''
    post_tags_ids = post.tags.values_list('id', flat=True)
    # get all posts that contain any of these tags, excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    .exclude(id=post.id)
    # similar to Gruop by Tag
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
    .order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'form':form,
                                                     'similar_posts':similar_posts})



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data # If your form data does not validate, cleaned_data will contain only the valid fields.
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, 
                    message, 
                    'engaymanfarag1997@gmail.com', 
                    [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent}
                )



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                                                {'post': post,
                                                'form': form,
                                                'comment': comment}
    )


