from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from comments.models import Comment
from markdown_deux import markdown

from .utils import get_read_time


# Sobrescrevendo o método 'active' para exibir os posts com alguns filtros
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).\
                filter(publish__lte=timezone.now())


def upload_location(instance, filename):

    ##  # filebase, extension = filename.split(".")
    ##  # return "%s/%s.%s" %(instance.id, instance.id, extension)
    ##  
    ##  PostModel = instance.__class__
    ##  new_id = PostModel.objects.order_by("id").last().id + 1
    ##
    ##  """
    ##  instance.__class__ gets the model Post. We must use this method because
    ##  the model is defined below. Then create a queryset ordered by
    ##  the "id"s of each object, then we get the last object in the queryset
    ##  with `.last()` which will give us the most recently created
    ##  Model instance we add 1 to it, so we get what should be the same id
    ##  as the the post we are creating.
    ##  """
    ##  return "%s/%s" %(new_id, filename)

    return "%s/%s" % (instance.slug, filename)


class Post(models.Model):

    # default=1 para superuser
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    # image = models.FileField(null=True, blank=True)

    # 'upload_to' altera o diretório onde as imagens serão armazenadas
    # A função 'upload_location' passa dinamicamente o nome desse diretório
    # instance.id passa o ID do post onde a imagem será exibida,
    # poderia ser, por exemplo, instance.user e armazenar mídias de
    # usuários separados, possivelmente uma imagem de exibição, por exemplo.

    # witdh_field e height_field exibem as dimensões da imagem na
    # página de admin

    image = models.ImageField(
            upload_to=upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    content = models.TextField()

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)

    # read_time =  models.IntegerField(default=0)
    read_time = models.TimeField(null=True, blank=True)

    # 'auto_now_add' - Exibe o momento que foi adicionado pela
    # primeira vez no banco de dados.
    # ' auto_now' - Exibe a última vez que foi atualizado no
    # banco de dados
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Esse método faz com que a string recebida no campo 'title' seja
    # exibida ao invés do tipo do objeto 'title'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_api_url(self):
        return reverse('posts-api:detail', kwargs={'slug': self.slug})


    # 'objects' foi instanciado como um objeto PostManager e será chamado
    # na 'view.py' como Post.objects.all()
    # o nome da instância 'objects' é uma convenção
    objects = PostManager()

    # Ordenando a lista do post do mais recente ao mais antigo
    class Meta:
        ordering = ["-timestamp", "-updated"]

    # implementa renderização de 'markdown' e permite o uso
    # de imagems responsivas
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):

    # 'slugify' pega o título do post e altera para um formato aplicável à
    # barra de endereço. Ex: "Nome do Post 1" --> "nome-do-post-1"
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    queryset = Post.objects.filter(slug=slug).order_by("-id")
    exists = queryset.exists()

    # Verifica se a string da variável 'slug' já existe. Caso exista,
    # adiciona o ID do post a string da variável 'slug'
    if exists:
        new_slug = "%s-%s" % (slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

# 'pre_save' significa que antes de salvar algo no banco de dados,
# algo será feito
pre_save.connect(pre_save_post_receiver, sender=Post)
