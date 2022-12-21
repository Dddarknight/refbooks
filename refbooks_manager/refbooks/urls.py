from django.urls import path

from refbooks_manager.refbooks import views


urlpatterns = [
    path('', views.RefBooksView.as_view(), name="refbooks"),
    path(
        '<int:pk>/elements',
        views.RefBookElementsView.as_view(),
        name="elements",
    ),
    path(
        '<int:pk>/check_element',
        views.ValidateElementView.as_view(),
        name="check-element",
    ),
]
