from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import PostForm, UserForm
from .models import Post

def post_create(request):
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(obj.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "posts/post_form.html", context)


def post_detail(request, id=None):
    obj = get_object_or_404(Post, id=id)
    context = {
        "title": obj.title,
        "obj": obj,
    }
    return render(request, "posts/post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()



    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)


    context = {
        "object_list": queryset,
        "title": "Posts"
    }
    return render(request, "posts/post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,request.FILES,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "posts/post_form.html", context)




def post_delete(request, id=None):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    messages.success(request, "Successfully deleted")
    return redirect("post_list")


class UserFormView(View):
    form_class = UserForm
    template = 'posts/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template ,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid:
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password=form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username='username', password='password')

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('post_list')


        return render(request,self.template, {'form':form})


