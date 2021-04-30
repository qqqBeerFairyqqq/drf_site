from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from django.db.models import Q

from .models import Movie
from . import serializers as sr
from movies.services import get_client_ip


class MovieListView(APIView):
	'''output movie list'''
	def get(self, request):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', 
				filter=models.Q(ratings__ip=get_client_ip(request)))
			).annotate(
				middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
			)
		serializer = sr.MovieListSerializer(movies, many=True)
		return Response(serializer.data)


class MovieDetailView(APIView):
	'''output movie detail'''
	def get(self, request, pk):
		movie = Movie.objects.get(id=pk, draft=False)
		serializer = sr.MovieDetailSerializer(movie)
		return Response(serializer.data)


class ReviewCreateView(APIView):
	'''adding reviews in film'''
	def post(self, request):
		review = sr.ReviewCreateSerializer(data=request.data)
		if review.is_valid():
			review.save()
		return Response(status=201)


class AddStarRatingView(APIView):
	'''adding film rating'''

	def post(self, request):
		serializer = sr.CreateRatingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(ip=get_client_ip(request))
			return Response(status=201)
		else:
			return Response(status=400)
