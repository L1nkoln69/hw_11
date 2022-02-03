from django.urls import path
from django.views.decorators.cache import cache_page
from new_hw.views import *

urlpatterns = [
    path('add_author', AddAuthor.as_view(), name='add_author'),

    path('see_author', cache_page(60)(SeeAuthor.as_view()), name='see_author'),
    path('see_book', cache_page(60)(SeeBooks.as_view()), name='see_book'),
    path('see_author/<pk>', cache_page(60)(OneAuthor.as_view()), name='one_author'),
    path('see_book/<pk>', cache_page(60)(OneBook.as_view()), name='one_book'),
    path('update_author/<pk>', UpdateAuthor.as_view(), name='update_author'),
    path('delete_author/<pk>', DeleteAuthor.as_view(), name='delete_author'),

    path('<str:models>', models, name='models'),
    path('<str:models>/<int:pk>', models_id, name='models-id'),

]
