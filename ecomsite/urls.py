
from django.contrib import admin
from django.urls import path
from shop import views
from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm/', views.confirm, name='confirm'),
    path('history/<int:order_id>/', views.history, name='history'),
    path('orders/', views.orders, name='orders'),

    # URL routing for user authentication functions...
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', user_views.logout_user, name='logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)