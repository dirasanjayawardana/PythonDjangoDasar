from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView

from article.models import Article


# Create your views here.
class ArticleViews(TemplateView):
    pass


class ListArticlesViews(ListView):
    model = Article
    template_name = "article_list.html"

    def head(self, *args, **kwargs):
        last_articles = self.get_queryset().latest("created_at")
        response = HttpResponse(
            headers={
                'last-modified': last_articles.created_at.strftime(
                    '%Y-%m-%d %H:%M:%S'
                )
            }
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['now'] = timezone.now()
        return context


class DetailArticleView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        obj = Article.objects.get(uuid=slug)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class PostArticleView(View):
    def get(self, request):
        context = {}

        if 'uuid' in request.GET:
            obj = Article.objects.get(uuid=request.GET.get('uuid'))
            context['object'] = obj

        template_name = "article_publish.html"
        return render(request, template_name, context=context)

    def post(self, request):
        template_name = "article_publish.html"

        title = request.POST.get('title')
        content = request.POST.get('content')
        created_by = request.user

        if 'uuid' in request.POST:
            obj = Article.objects.get(uuid=request.POST.get('uuid'))
            obj.title = title
            obj.content = content
        else:
            obj = Article(
                title=title,
                content=content,
                created_by=created_by
            )

        obj.save()
        context = {
            'status': "Article publish",
            'detail': obj.uuid,
            'title': obj.title
        }
        return render(request, template_name, context=context)

class DeleteArticleView(DeleteView):
    template_name = 'article_confirm_delete.html'
    model = Article
    success_url = '/articles/shows'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        obj = Article.objects.get(uuid=slug)
        return obj