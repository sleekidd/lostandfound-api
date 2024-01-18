from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LostItemViewSet,
    FoundItemViewSet,
    UserProfileViewSet,
    user_details,
)

# Create a router for viewsets
router = DefaultRouter()
router.register(r'lost-items', LostItemViewSet)
router.register(r'found-items', FoundItemViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('user-profile/', user_details, name='user_details'),
]

# Include the router's URLs
urlpatterns += router.urls

