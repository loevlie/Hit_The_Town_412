from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Post
from django.views import generic
# from .serializers import PostSerializer
# Create your views here.
# def index(request):
#     return render(request, 'Blog/index.html')

# class PostList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


    
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'index.html'
#     paginate_by = 3


def post_detail(request, slug):
    template_name = 'Blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    #user_profile = User.objects.get(username=request.user.username)
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            #new_comment.author = user_profile
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def AddPostView(request):
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        #model = Post.objects.get(author=user.request.user)
        post_form = BlogPostForm(data=request.POST)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'making'})
        else:
            print(post_form.errors)
            return HttpResponse('Something did not work the slug may already exist!')
    else:
        form = BlogPostForm(instance=request.user)
    return render(request,'Portfolio/add_post.html',{'form':form})


class index(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'Blog/index.html'
    paginate_by = 3



def UpdatePostView(request,slug):
    blog_post = get_object_or_404(Post,slug=slug)
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        post_form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'updating'})
        else:
            print(post_form.errors)
    else:
        if str(request.user.username) == str(blog_post.author):
            form = UpdateBlogPostForm(instance=request.user,initial = {"title":blog_post.title,"slug":blog_post.slug,"snippet":blog_post.snippet,"content":blog_post.content,"status":blog_post.status})
            return render(request,'Portfolio/update_post.html',{'form':form})
        else:
            return HttpResponse("<h1>Only the user who created the post may edit it</h1>")