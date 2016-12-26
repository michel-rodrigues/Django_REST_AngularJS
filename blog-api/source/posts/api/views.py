from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
        )

from rest_framework.generics import (
        CreateAPIView,
        DestroyAPIView,
        ListAPIView,
        #UpdateAPIView,
        RetrieveAPIView,
        RetrieveUpdateAPIView,
        )

from rest_framework.pagination import (
        LimitOffsetPagination,
        PageNumberPagination,
        )

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly,
        )

from posts.models import Post

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from .serializers import (
        PostCreateUpdateSerializer,
        PostDetailSerializer,
        PostListSerializer,
        )


class PostCreateAPIView(CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # Por padrão, é procurado pela 'pk', implementa a busca pelo 'slug'
    # Implica na regex em urls.py
    lookup_field = "slug"


class PostDetailAPIView(RetrieveAPIView):

    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # Por padrão, é procurado pela 'pk', implementa a busca pelo 'slug'
    # Implica na regex em urls.py
    lookup_field = "slug"


class PostListAPIView(ListAPIView):

    permission_classes = [AllowAny]

    # 'PostListAPIView' should either include a `serializer_class` attribute,
    # or override the `get_serializer_class()` method.
    # Exibe a aba "HTML form"
    serializer_class = PostListSerializer

    # SearchFilter: passando como um atributo built-in do rest_framework para buscas através de querys
    # exemplo.com/?search=palavras chave
    # OrderingFilter para ordenar os resultado, é passado pela query também.
    # O sinal de menos inverte a ordem
    # exemplo.com/?search=palavras%20chave&ordering=critério # algum campo do
    # modelo
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__first_name'] # ['title', 'content']

    # Paginação através de query:
    # exemplo.com/?limit=2&offset=2 
    # Limita 2 objetos por página e acessa a segunda página
    # Acrescenta ao json o número total de objetos o e endereço da próxima
    # página e da página anterior
    # pagination_class = LimitOffsetPagination

    # Paginação implementada em pagination.py
    # pagination_class = PostLimitOffsetPagination

    # Paginação implementada em pagination.py
    # Similar a paginação do django
    # exemplo.com/?page=2
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset = super(PostListAPIView, self).get_queryset(*args, **kwargs)

        ## implementa busca no banco de dados passando uma query pelo navegador
        #  exemplo.com/?q=alguma expressão
        #  "alguma expressão" é corrigida pela barra de endereço para se
        #  tornar uma "url-encoded text"
        #  É possível codificar um texto para uma 'url-encoded text' usando
        #  a o método 'quote'
        #  >>> from urllib.parse import quote
        #  >>> string_encoded = quote("Uma string qualquer")

        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        ##

        # Utilizando o 'serch' do rest_framework e o query do django é
        # possível fazer buscas como:
        # exemplo.com/?search=alguma%20coisa&q=outra%20coisa

        return queryset_list


class PostUpdateAPIView(RetrieveUpdateAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # Por padrão, é procurado pela 'pk', implementa a busca pelo 'slug'
    # Implica na regex em urls.py
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
