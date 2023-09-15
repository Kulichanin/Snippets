from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index_page(request):

    if request.method == "GET":
        context = {'pagename': 'PythonBin'}
        return render(request, 'pages/index.html', context)
    
    if request.method == 'POST':
        try:
            snippet = Snippet.objects.get(id=request.POST['snippet_id'])
        except ObjectDoesNotExist:
            raise Http404
        context = {
            'pagename': 'Просмотр сниппета',
            'snippet': snippet,
            'type': 'view'
            }
        return render(request, 'pages/snippet_detail.html', context)
        


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def add_snippet_page(request):
    # Хотим получить чистую форму для заполнения
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    
    # Хотим создать новый Сниппет(данные от формы)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")
        return render(request,'pages/add_snippet.html', {'form': form})

def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        comments = Comment.objects.filter(snippet=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    context = {
        'pagename': 'Просмотр сниппета',
        'snippet': snippet,
        'comments': comments,
        'type': 'view'
        }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    # Перенаправление на ту страницу, с которой пришел
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    # Хотим получить страницу данных сниппета
    if request.method == "GET":
        context = {
            'pagename': 'Редактирование сниппета',
            'snippet': snippet,
            'type': 'edit'
        }
        return render(request, 'pages/snippet_detail.html', context)
    
    # Хотим создать новый Сниппет(данные от формы)
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.lang = data_form["lang"]
        snippet.code = data_form["code"]
        snippet.creation_date = data_form["creation_date"]
        snippet.public = data_form.get("public", False)
        snippet.save()
        return redirect("snippets-list")


@login_required
def comment_add(request,snippet_id):
    if request.method == "POST":
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)  
            comment.text = comment_form.data['text']
            comment.image = request.FILES['image']
            comment.save()
            return redirect(f'/snippet/{snippet_id}')
    comment_form = CommentForm()
    snippet = Snippet.objects.get(id=snippet_id)
    context = {
            'pagename': 'Просмотр снипета',
            'comment_form':comment_form,
            'snippet': snippet,
            'type': 'view'
        }
    return render(request, f'pages/snippet_detail.html', context)



def create_user(request):
    context = {"pagename": "Регистрация пользователя"}
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request, "pages/registration.html", context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context['form'] = form
        return render(request, "pages/registration.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ['wrong username or password']
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')

# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("snippets-list")
#         return render(request,'add_snippet.html', {'form': form})
