"""Defines URL patterns for mems_apps"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # home page for admin
    path('',views.index, name='index'),
    
    # page for admin to add new extras to the menu.
    path('new_extra', views.new_extra, name='new_extra'),

    # path that removes extras from menu
    path('remove_extra/<int:extra_id>', views.remove_extra, name='remove_extra'),

    # page for admin to see the orders for the day
    path('todays_orders', views.todays_orders, name='todays_orders'),

    # ======================================

    # register page for students
    path('student_register/', views.student_register, name='student_register'),
    
    # login page for student
    path('student_login/', auth_views.LoginView.as_view(template_name='mems_apps/student_login.html'), name='student_login'),

    # home page for student
    path('student_index/', views.student_index, name='student_index'),

    # logout for student user
    path('student_logout/', views.logout_view, name='student_logout'),

    # Student's page to add extras to "plate"
    path('add_to_plate/', views.add_to_plate, name='add_to_plate'),

    # remove selected extra from plate
    path('remove_from_plate/<int:order_id>', views.remove_from_plate, name='remove_from_plate'),

    path('see_plate/', views.see_plate, name='see_plate'),

    # page to show student has confirmed the extras on his plate
    path('confirmation/', views.confirmation, name='confirmation'),

    # page to show student her totals
    path('see_totals/', views.see_totals, name='see_totals'),

]