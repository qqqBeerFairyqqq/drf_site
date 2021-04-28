from rest_framework import serializers
from .models import Movie, Review


class FilterReviewListSerializer(serializers.ListSerializer):
	def to_representation(self, data):
		data = data.filter(parent=None)
		return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

	def to_representation(self, value):
		serializer = self.parent.parent.__class__(value, content=self.content)
		return serializer.data


class MovieListSerializer(serializers.ModelSerializer):
	'''movie list'''

	class Meta:
		model = Movie
		fields = ('title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
	'''comments'''

	class Meta:
		model = Review
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

	children = RecursiveSerializer(many=True)

	class Meta:
		list_serializer_class = FilterReviewListSerializer
		model = Review
		fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
	'''movie detail'''
	category = serializers.SlugRelatedField(slug_field='name', read_only=True)
	directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	reviews = ReviewCreateSerializer(many=True)

	class Meta:
		model = Movie
		exclude = ('draft', )


