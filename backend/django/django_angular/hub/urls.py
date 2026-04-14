from django.urls import path

from hub import views

urlpatterns = [
    path("auth/register", views.RegisterView.as_view()),
    path("auth/login", views.LoginView.as_view()),
    path("auth/me", views.MeView.as_view()),
    path("tasks", views.TaskCollectionView.as_view()),
    path("tasks/<int:pk>", views.TaskDetailView.as_view()),
    path("executions", views.ExecutionCollectionView.as_view()),
    path("ratings", views.RatingCollectionView.as_view()),
]
