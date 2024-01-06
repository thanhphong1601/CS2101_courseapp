from django.contrib import admin
from django.forms import forms
from django import forms
from django.template.response import TemplateResponse

from .models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from courses import dao
class CourseAppAdminSite(admin.AdminSite):
    site_header = 'HeheBoiii'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_courses_by_cate()
        })


admin_site = CourseAppAdminSite(name='myapp')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class CourseForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'

class TagInlineAdmin(admin.StackedInline):
    model = Course.tags.through

#thay đổi cách show của model Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'updated_date', 'category', 'active']
    readonly_fields = ['img']
    form = CourseForm
    inlines = [TagInlineAdmin]

    def img(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=course.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }



# Register your models here.

admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Tag)
