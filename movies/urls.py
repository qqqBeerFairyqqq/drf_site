from django.urls import path
from . import views


urlpatterns = [
	path('movie/', views.MovieListView.as_view(), name='movie-list'),
	path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
	path('review/', views.ReviewCreateView.as_view(), name='review-create'),
	path('rating/', views.AddStarRatingView.as_view(), name='rating')
]