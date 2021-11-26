from django.urls import path
from .views import (SMSCreateView, SMSListView, SMSDetailView, ContactCreateView, ContactListView, ContactDetailView,
                    ContactUpdateView, ContactDeleteView, GroupCreateView, GroupListView, GroupDetailView,
                    GroupDeleteView)
from . import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('', SMSCreateView.as_view(), name='sms-home'),
    path('sms/', SMSListView.as_view(), name='view-sms'),
    path('sms/<int:pk>/', SMSDetailView.as_view(), name='sms-detail'),
    path('ajax/load-contacts/', views.load_contacts, name='ajax_load_contacts'),
    path('contact/new/', ContactCreateView.as_view(), name='add-contact'),
    path('contact/', ContactListView.as_view(), name='view-contact'),
    path('contact/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contact/<int:pk>/update/', ContactUpdateView.as_view(), name='update-contact'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='delete-contact'),
    path('group/new/', GroupCreateView.as_view(), name='create-group'),
    path('group/', GroupListView.as_view(), name='view-group'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view(), name='delete-group')
]
