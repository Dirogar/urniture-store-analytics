from django.urls import include, path

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
#router.register('cats', CatViewSet)
#router.register('owners', OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]