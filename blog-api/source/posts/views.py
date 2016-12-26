# from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from urllib.parse import quote

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post


def post_create(request):

    # Evita que um usuário anônimo e que não é da equipe, acesse a
    # página para criar um post
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    # Evita que um usuário anônimo crie um post
    if not request.user.is_authenticated():
        raise Http404

    # 'None' faz com que, ao carregar a página, não seja exibido
    # quais campos são obrigatórios. Do contrário, essas mensagens
    # seriam exibidas antes de qualquer ação do usuário
    # request.POST para dados do formulário
    # request.FILES para arquivos de mídia
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        # O argumento 'extra_tags' inclui a string que ele recebe na
        # 'class' da tag correspondente. Pode ser usado pra usar uma
        # CSS específica para a mensagem. Use a opção 'inspecionar' do
        # navegador para ver 'some-tag' exibida na 'class' da mensagem
        # Ver também 'messages_display.html', é pra onde vão essas tags
        # messages.success(request, 'Successfuly Created',
        # extra_tags='some-tag')

        # Redireciona para a página do post.
        # .get_absolute_url() é um método da classe 'Post' em 'models.py'
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': 'Form',
        'form': form,
        'tag_create': 'active',
    }
    return render(request, 'post_form.html', context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    # 'quote' converte string em 'url-encoded text', um formato
    # que pode ser enviado pela internet
    # share_string será enviado pela barra de endereço no links das
    # redes socias
    share_string = quote(instance.content)


    ####################################################
    #

    """
    Instances of ContentType represent and store information about
    the models installed in your project, and new instances of
    ContentType are automatically created whenever new models are installed.

    Relations between your models and ContentType can also be used to enable
    “generic” relationships between an instance of one of your models and
    instances of any model you have installed.

    """

    # Fazendo a relação entre o conteúdo do model 'Post' do app 'posts' e o
    # conteudo do model Comment do app comments

    # 'content_type' recebe uma instancia de ContentType que representa
    # a model Post
    # content_type = ContentType.objects.get_for_model(Post)

    # id da instância
    # obj_id = instance.id

    # Filtra os comentários relacionados com a instância atual de Post
    # comments = Comment.objects.filter(content_type=content_type,
    #                                   object_id=obj_id)

    # comments = Comment.objects.filter(post=instance)
    # comments = Comment.objects.filter(user=user.request.user)

    #
    ############################################################

    # comments = Comment.objects.filter_by_instance(instance)

    # comments = instance.comments.order_by('-timestamp')

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None

        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        """
        A convenience method for looking up an object with the given kwargs
        (may be empty if your model has defaults for all fields), creating
        one if necessary.

        Returns a tuple of (object, created), where object is the retrieved
        or created object and created is a boolean specifying whether a new
        object was created.

        https://docs.djangoproject.com/en/1.10/ref/models/querysets/#get-or-create
        """
        new_comment, created = Comment.objects.get_or_create(
                                    user=request.user,
                                    content_type=content_type,
                                    object_id=obj_id,
                                    content=content_data,
                                    parent=parent_obj,
                                )

        return HttpResponseRedirect(new_comment.content_object.
                                    get_absolute_url())

    comments = instance.comments

    context = {
        'instance': instance,
        'title': instance.title,
        'share_string': share_string,
        'comments': comments,
        'form': form,
    }

    return render(request, "post_detail.html", context)


def post_list(request):

    # Instanciando 'queryset' como um objeto 'Post' e usando o método
    # object.all(), herdado por 'Post' de 'models', para retornar todas
    # as entradas no banco de dados.
    # queryset_list = Post.objects.all()

    # .order_by(-timestamp) faz com que o post sejam retornados do
    # mais novo para o mais antigo, ou seja, na ordem inversa do 'timestamp'
    # indicado pelo sinal de menos na frente
    # queryset_list = Post.objects.order_by("-timestamp")
    #
    # Porém essa ordenação foi passada em 'models.py'
    #
    # timezone.now() foi declarado como default para o campo publish
    # em 'models.py', no momento em que foi usado 'makemigrations'
    # queryset_list = Post.objects.filter(draft=False).\
    #        filter(publish__lte=timezone.now())

    # o método padrão do django '.active()' foi sobrescrito. Ver 'models.py'
    queryset_list = Post.objects.active()

    today = timezone.now().date()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    # Páginador - Documentação do Django
    paginator = Paginator(queryset_list, 2)  # Exibe 2 post por página

    # Altera o que será exibido na barra de endereço. Ver 'post_list.html'.
    page_request_var = 'pagina'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # Se page não é um inteiro, retorna a primeira página
        queryset = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do número real de páginas existentes,
        # retorna a última página
        queryset = paginator.page(paginator.num_pages)

    context = {
        'title': 'List',
        'object_list': queryset,
        'tag_home': 'active',
        'page_request_var': page_request_var,
        'today': today,
    }
    return render(request, "post_list.html", context)


# O argumento 'instance=instance' em PostForm() adiciona os dados
# para a edição. O resto da função é basicamente igual a função 'create'
def post_update(request, slug=None):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        # Outro exemplo de um possível uso do argumento 'extra_tags'
        # messages.success(request,
        #                  "<a href='#'>Item</a> Saved",
        #                  extra_tags='html_safe')

        # Retorna para a página do post após confirmar a edição
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'post_form.html', context)


def post_delete(request, slug=None):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    # messages.success(request, 'Successfuly Deleted')
    return redirect('posts:list')
