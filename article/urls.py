from django.urls import path

from article.views import ListArticlesViews, DetailArticleView, PostArticleView, DeleteArticleView

urlpatterns = [
    path('shows/', ListArticlesViews.as_view()),
    path('read/<slug:slug>/', DetailArticleView.as_view()),
    path('', PostArticleView.as_view()),
    path('<slug:slug>/delete/', DeleteArticleView.as_view())
]