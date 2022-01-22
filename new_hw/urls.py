from django.urls import path

from new_hw import views

app_name = 'new_hw'
urlpatterns = [
    path('<str:models>', views.models, name='models'),
    path('<str:models>/<int:pk>', views.models_id, name='models-id'),
]
