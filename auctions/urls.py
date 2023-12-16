from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listings/<int:pk>", views.open_listing, name="open-listing"),
    path("listings/<int:pk>/close", views.close_listing, name="close-listing"),
    path("listings/<int:pk>/watchlist-add", views.watchlist_add, name="watchlist-add"),
    path("listings/<int:pk>/watchlist-remove", views.watchlist_remove, name="watchlist-remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:pk>/comment", views.comment, name="comment")
]
