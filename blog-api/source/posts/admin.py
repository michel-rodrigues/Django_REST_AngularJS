from django.contrib import admin

from .models import Post

#
# A classe 'Meta' implementa uma relação entre
# a classe 'PostModelAdmin', que herda de
# 'admin.ModelAdmin', para usar seus métodos
# Ex: 'list_display' vai exibir o título do post, a data e a hora
# do post e o último update.
#
# '__str__' e 'title' fazem referência a mesma variável
#


class PostModelAdmin(admin.ModelAdmin):

    # 'list_editable' exibe o campo sempre editável
    # 'list_display_links' exibe o campo como um link para a página
    # de alterações
    #
    # list_editable = ['title']
    # list_display_links = ["updated"]

    # exibe os campos em colunas
    list_display = ['__str__', 'updated', 'timestamp']

    # implementa um campo de filtro à esquerda da página
    list_filter = ['updated', 'timestamp']

    # imprelementa um campo de busca
    search_fields = ['title', 'content']

    class Meta:
        model = Post


# Implementa a classe 'Post' declarada em 'models.py'
# e a classe 'PostModelAdmin' dentro da página 'admin'
admin.site.register(Post, PostModelAdmin)
