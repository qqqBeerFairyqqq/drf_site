from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from . import serializers as sr
from .services import get_client_ip, MovieFilter


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
	'''output film list'''
	filter_backends = (DjangoFilterBackend,)
	filterset_class = MovieFilter

	def get_queryset(self):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', 
				filter=models.Q(ratings__ip=get_client_ip(self.request)))
		).annotate(
			middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
		)
		return movies

	def get_serializer_class(self):
		if self.action == 'list':
			return sr.MovieListSerializer
		elif self.action == 'retrieve':
			return sr.MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
	'''adding film reviews'''
	serializer_class = sr.ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
	'''adding film rating'''
	serializer_class = sr.CreateRatingSerializer

	def perform_create(self, serializer):
		serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
	'''output film actors & directors'''
	queryset = Actor.objects.all()

	def get_serializer_class(self):
		if self.action == 'list':
			return sr.ActorListSerializer
		elif self.action == 'retrieve':
			return sr.ActorDetailSerializer
