from django.urls import path
from .views import edit_base, get_model_objects

urlpatterns = [
    # Post views
    path('', edit_base, name='edit_base'),
    path('get-obj/', get_model_objects, name='get_model_objects'),

]