from home import views
from django.contrib import admin
from django.urls import path, include
from .views import UpdatePostView


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('login/register/', views.registerPage, name='register'),
    path("application_form/", views.application_form, name="application_form"),
    path("edit_application/", views.edit_application, name="edit_application"),
    path("status/", views.status, name="status"),

    path("handle_admin/", views.handle_admin, name="handle_admin"),
    path("users/", views.users, name="users"),
    path("student_application/<int:myid>/",
         views.student_application, name="student_application"),
    path("application_status/<int:pk>/",
         UpdatePostView.as_view(), name="application_status"),
    path("approved_applications/", views.approved_applications,
         name="approved_applications"),
    path("pending_applications/", views.pending_applications,
         name="pending_applications"),
    path("rejected_applications/", views.rejected_applications,
         name="rejected_applications"),
]
