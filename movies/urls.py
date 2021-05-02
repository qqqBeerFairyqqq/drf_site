from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views


urlpatterns = format_suffix_patterns([
	path('movie/', views.MovieViewSet.as_view({'get': 'list'})),
	path('movie/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'})),
	path('review/', views.ReviewCreateViewSet.as_view({'post': 'create'})),
	path('rating/', views.AddStarRatingViewSet.as_view({'post': 'create'})),
	path('actor/', views.ActorViewSet.as_view({'get': 'list'})),
	path('actor/<int:pk>/', views.ActorViewSet.as_view({'get': 'retrieve'})),
])



'''
urlpatterns = [
	path('movie/', views.MovieListView.as_view(), name='movie-list'),
	path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
	path('review/', views.ReviewCreateView.as_view(), name='review-create'),
	path('rating/', views.AddStarRatingView.as_view(), name='rating'),
	path('actors/', views.ActorListView.as_view(), name='actors'),
	path('actors/<int:pk>/', views.ActorDetailView.as_view(), name='actor-detail'),	
]'''