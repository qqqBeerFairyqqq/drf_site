from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from movies.models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Review



class MovieAdminForm(forms.ModelForm):
	description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

	class Meta:
		model = Movie
		fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "url")
	list_display_links = ("name", "id")
	# какие поля будут ссылками


class ReviewInLine(admin.TabularInline):
	# TabularInLine - вывод всех полей горизонтально
	# StackedInLine - вывод всех полей вертикально
	model = Review
	# наша модель будет использоваться в админке MovieAdmin
	extra = 1
	# дополнительное пустое сообщение
	readonly_fields = ("name", "email")
	# поля только для чтения


class MovieShotsInLine(admin.TabularInline):
	model = MovieShots
	extra = 1
	readonly_fields = ("get_image", )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="100" height="110">')

	get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "url", "draft")
	# отображение полей в листе фильмов
	list_filter = ("category", "year")
	# фильтрация по..
	search_fields = ("title", "category__name")
	# поиск по..
	inlines = [MovieShotsInLine, ReviewInLine]
	# используем модель отзывов, кадров
	save_on_top = True
	# кнопки для сохранения, дозаписи и тд переносим вверх
	save_as = True
	# сохраняем как новый объект, за место правки
	list_editable = ("draft", )
	# включаем черновик не заходя в фильм
	actions = ["publish", "unpublish", ]
	form = MovieAdminForm
	readonly_fields = ("get_image", )
	fieldsets = (
		("Name", {
			'fields': (("title", "tagline"), )
		}),
		(None, {
			'fields': ("description", ("poster", "get_image"))
		}),
		("Time", {
			'fields': (("year", "world_premiere", "country"), )
		}),
		("Film", {
			'classes': ("collapse", ),
			'fields': (("actors", "directors", "genres", "category"), )
		}),
		("Fees", {
			'fields': (("budget", "fees_in_usa", "fees_in_world"), )
		}),
		("Options", {
			'fields': (("url", "draft"), )
		}),
	)
	# настройка полей

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.poster.url} width="150" height="180">')

	def unpublish(self, request, queryset):
		'''Снять с публикации'''
		row_update = queryset.update(draft=True)
		if row_update == 1:
			message_bit = '1 запись была обновлена'
		else:
			message_bit = f'{row_update} записей были обновлены'
		self.message_user(request, f'{message_bit}')

	def publish(self, request, queryset):
		'''Опубликовать'''
		row_update = queryset.update(draft=False)
		if row_update == 1:
			message_bit = '1 запись была обновлена'
		else:
			message_bit = f'{row_update} записей были обновлены'
		self.message_user(request, f'{message_bit}')

	publish.short_description = "Опубликовать"
	publish.allowed_permissions = ("change", )

	unpublish.short_description = "Снять с публикации"
	unpublish.allowed_permissions = ("change", )

	get_image.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "movie", "id")
	readonly_fields = ("name", "email")


@ admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
	list_display = ("name", "age", "get_image")
	readonly_fields = ("get_image", )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

	get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
	list_display = ("title", "movie", "get_image")
	readonly_fields = ("get_image", )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

	get_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
# за место администрирования джанго, будет джанго мувис

