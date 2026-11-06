"""
URL mappings for the api_embeddings app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from api_embeddings import views


router = DefaultRouter()
router.register('embeddings', views.EmbeddingViewSet)

app_name = 'api_embeddings'

urlpatterns = [
    path('upload/', views.UploadDocumentView.as_view(), name='upload'),
    path('', include(router.urls)),
]
