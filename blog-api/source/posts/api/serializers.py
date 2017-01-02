from rest_framework.serializers import (
        HyperlinkedIdentityField,
        ModelSerializer,
        SerializerMethodField,
        )

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentListSerializer
from comments.models import Comment
from posts.models import Post


def hyperlinked(absolute_url):
    url = HyperlinkedIdentityField(
            view_name=absolute_url,
            lookup_field='slug',
            )
    return url


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # 'id',
            'title',
            # 'slug',
            'content',
            'publish',
        ]


class PostDetailSerializer(ModelSerializer):

    """
    É necessário implementar um método cujo nome inicie por 'get_'

    Exceção: 'PostDetailSerializer' object has no attribute 'get_meu_campo'

    meu_campo = SerializerMethodField()

    class Meta:
        model = MeuModel
        fields = [
            'meu_campo',
        ]

    def get_meu_campo(self, obj):
        return alguma_coisa

    """

    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'image',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'comments',
        ]

    def get_html(self, obj):
        return obj.get_markdown() # get_markdown foi implementado fora da API

    # def get_user(self, obj):
    #     return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        cmts_qs = Comment.objects.filter_by_instance(obj)

        # Foi necessário passar "context={'request': None}"
        # http://www.django-rest-framework.org/api-guide/serializers/#absolute-and-relative-urls
        comments = CommentListSerializer(
                        cmts_qs,
                        many=True,
                        context={'request': None}
                        ).data
        return comments


class PostListSerializer(ModelSerializer):

   # url = HyperlinkedIdentityField(
   #         # view_name é similar ao get_absolute_url
   #         view_name='posts-api:detail',
   #         # o default é a pk (primary key)
   #         lookup_field='slug',
   #         )

    url = hyperlinked('posts-api:detail')

    # delete_url = hyperlinked('posts-api:delete')

    # update_url = hyperlinked('posts-api:update')

    user = UserDetailSerializer(read_only=True)

    # image = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            # 'update_url',
            'user',
            'title',
            'slug',
            'content',
            'publish',
            'image',
            # 'delete_url'
        ]

    # def get_image(self, obj):
    #     try:
    #         image = obj.image.url
    #     except:
    #         image = None
    #     return image

    # def get_user(self, obj):
    #     return str(obj.user.username)


"""
# Serializando dados do banco de dados & serializando dicionários e inserindo
# no banco de dados

>>> obj = Post.objects.first()
>>> obj
<Post: Post 2>
>>> obj.title
'Post 2'
>>> obj_json = PostSerializer(obj)
>>> obj_json.data
{'slug': 'post-2', 'title': 'Post 2', 'id': 2, 'publish': '2016-01-01',
        'content': 'Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun
        Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem
        Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun
        Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem
        Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun
        Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem
        Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem Ipsun
        Lorem Ipsun Lorem Ipsun Lorem Ipsun Lorem'}
>>> obj_json.data['slug']
'post-2'

>>> dic_data = {
    'title': 'TESTE',
    'content': 'Teste teste teste.',
    'publish': '2016-01-01',
}

>>> new_item = PostSerializer(data=dic_data)

>>> if new_item.is_valid():
        new_item.save()
    else:
        print(new_item.errors)

{'slug': ['This field is required.']}

>>> dic_data = {'title': 'TESTE', 'slug': 'teste','content': 'Teste teste teste.',
'publish': '2016-01-01', }

>>> new_item = PostSerializer(data=dic_data)

>>> if new_item.is_valid():
        new_item.save()
    else:
        print(new_item.errors)

<Post: TESTE>


>>> new_item.data
{'slug': 'teste', 'title': 'TESTE', 'id': 3, 'publish': '2016-01-01',
'content': 'Teste teste teste.'}
>>> new_item.id
Traceback (most recent call last):
    File "<console>", line 1, in <module>
AttributeError: 'PostSerializer' object has no attribute 'id'

# O ID só é acessível através do atributo 'data' porque não é um objeto Post (model) e sim um objeto
# PostSerializer. O objeto Post permite acessar o id como um atributo:

>>> obj = Post.objects.first()
>>> obj
<Post: TESTE>
>>> obj.id
3

###############################################################3#############


>>> from posts.models import Post
>>> from posts.api.serializers import PostDetailSerializer


>>> dic_data = {
...     'title': 'TESTE',
...     'content': 'Teste teste teste.',
...     'publish': '2016-01-01',
...     'slug': 'teste',
... }


>>> obj = Post.objects.get(id=3)

>>> new_item = PostDetailSerializer(obj, data=dic_data)

>>> if new_item.is_valid():
        new_item.save()
    else:
        print(new_item.errors)

<Post: TESTE>

>>> new_item.data
{'content': 'Teste teste teste.', 'id': 3, 'publish': '2016-01-01', 'title':
'TESTE', 'slug': 'teste'}

>>> obj
<Post: TESTE>
>>> obj.delete()
(1, {'posts.Post': 1})
>>> obj                             # Embora a variável ainda exista na shell,
<Post: TESTE>                       # o objeto foi apagado
>>> obj = Post.objects.get(id=3)
Traceback (most recent call last):
  [...]
  posts.models.DoesNotExist: Post matching query does not exist.

"""
