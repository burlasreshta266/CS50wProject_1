from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("newPage", views.new_page, name="new_page"),
    path("EditPage", views.edit, name="edit"),
    path("SaveEditPage", views.save_edit, name="save_edit"),
    path("<str:title>", views.display_page, name="display_page"),
]
