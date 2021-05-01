from rest_framework import generics
from django.db import models
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from . import serializers as sr
from movies.services import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
	'''output movie list'''

	serializer_class = sr.MovieListSerializer
	filter_backends = (DjangoFilterBackend, )
	filterset_class = MovieFilter

	def get_queryset(self):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', 
				filter=models.Q(ratings__ip=get_client_ip(self.request)))
			).annotate(
				middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
			)
		return movies


class MovieDetailView(generics.RetrieveAPIView):
	'''output movie detail'''
	queryset = Movie.objects.filter(draft=False)
	serializer_class = sr.MovieDetailSerializer



class ReviewCreateView(generics.CreateAPIView):
	'''adding reviews in film'''
	serializer_class = sr.ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
	'''adding film rating'''
	serializer_class = sr.CreateRatingSerializer

	def perform_create(self, serializer):
		serializer.save(ip=get_client_ip(self.request))



class ActorListView(generics.ListAPIView):
	queryset = Actor.objects.all()
	serializer_class = sr.ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
	queryset = Actor.objects.all()
	serializer_class = sr.ActorDetailSerializer
