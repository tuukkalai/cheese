from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
	path('', view=views.index, name='index'),
	path('<int:question_id>/', views.detail, name='detail'),
	path('<int:question_id>/results/', views.results, name='results'),
	path('<int:question_id>/results/vote/', views.vote, name='vote'),
	path('question/', views.question, name='question'),
	path('question/<str:question_id>/', views.question, name='question'),
	path('create/', views.create, name='create'),
]