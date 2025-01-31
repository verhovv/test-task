from django import forms
from django.contrib import admin
from django.apps import apps
from django.db import models
from .models import *

@admin.register(
    User, UserBucket,
    Category, Subcategory, SubcategoryCategory, SubcategoryGoods
)

@admin.register(FAQ, Goods, NewsLetter)
class AdminModel(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs={'rows': 1, 'cols': 50})},
    }
