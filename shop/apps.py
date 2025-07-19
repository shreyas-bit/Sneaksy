"""Application configuration for the shop application."""

from django.apps import AppConfig
"""Configuration for the shop application."""
class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
