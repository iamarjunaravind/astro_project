from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('start/<int:astrologer_id>/', views.start_chat, name='start_chat'),
    path('start-booking/<int:booking_id>/', views.start_chat_from_booking, name='start_chat_from_booking'),
    path('start-call/<int:booking_id>/', views.start_call_booking, name='start_call_booking'),
    path('call/<int:booking_id>/', views.call_room, name='call_room'),
    path('reschedule/<int:booking_id>/', views.reschedule_booking, name='reschedule_booking'),
    path('handle-reschedule/<int:booking_id>/', views.handle_reschedule, name='handle_reschedule'),
    path('review/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('complete/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('end-chat/<int:session_id>/', views.end_chat, name='end_chat'),
    path('room/<int:session_id>/', views.chat_room, name='chat_room'),
    path('book/<int:astrologer_id>/', views.book_astrologer, name='book_astrologer'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('dashboard/', views.astrologer_dashboard, name='astrologer_dashboard'),
    path('api/messages/<int:session_id>/', views.get_messages, name='get_messages'),
    path('api/send/<int:session_id>/', views.send_message_ajax, name='send_message_ajax'),
]
