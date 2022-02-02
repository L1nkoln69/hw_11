from django.urls import path

from new_hw.views import *

urlpatterns = [
    path('add_author', AddAuthor.as_view(), name='add_author'),

    path('see_author', SeeAuthor.as_view(), name='see_author'),
    path('see_author/<pk>', OneAuthor.as_view(), name='one_author'),
    path('update_author/<pk>', UpdateAuthor.as_view(), name='update_author'),
    path('delete_author/<pk>', DeleteAuthor.as_view(), name='delete_author'),

    path('<str:models>', models, name='models'),
    path('<str:models>/<int:pk>', models_id, name='models-id'),

]
