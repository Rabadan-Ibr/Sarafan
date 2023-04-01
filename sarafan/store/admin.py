from django.contrib import admin

from .models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug'
    ordering = 'slug',


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug'
    ordering = 'slug',


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug', 'price'
    ordering = 'slug',
