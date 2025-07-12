from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/<int:item_id>/request/', views.request_swap, name='request_swap'),
    path('items/<int:item_id>/redeem/', views.redeem_item, name='redeem_item'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('requests/<int:req_id>/<str:action>/', views.respond_request, name='respond_request'),

    # Admin-only item approval
    path('admin/approve/', views.admin_approve_list, name='admin_approve_list'),
    path('admin/approve/<int:item_id>/', views.approve_item, name='approve_item'),
    path('admin/reject/<int:item_id>/', views.reject_item, name='reject_item'),
]
