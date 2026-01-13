from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ChatMessageForm, BookingForm
from .models import ChatSession, ChatMessage, Booking
from astrologers.models import AstrologerProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def book_astrologer(request, astrologer_id):
    astrologer_profile = get_object_or_404(AstrologerProfile, id=astrologer_id)
    consultation_type = request.GET.get('type', 'call')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.astrologer = astrologer_profile
            booking.consultation_type = consultation_type
            booking.save()
            return redirect('accounts:profile')
    else:
        form = BookingForm()
    
    price = astrologer_profile.call_price_per_minute if consultation_type == 'call' else astrologer_profile.chat_price_per_minute
    
    return render(request, 'consultations/book_astrologer.html', {
        'astrologer': astrologer_profile,
        'form': form,
        'consultation_type': consultation_type,
        'price': price
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-scheduled_at')
    return render(request, 'consultations/my_bookings.html', {'bookings': bookings})

@login_required
def astrologer_dashboard(request):
    # Check if user is an astrologer
    try:
        profile = request.user.astrologer_profile
    except:
        return redirect('home')
        
    bookings = Booking.objects.filter(astrologer=profile).order_by('-scheduled_at')
    active_sessions = ChatSession.objects.filter(astrologer=request.user, is_active=True)
    
    return render(request, 'consultations/astrologer_dashboard.html', {
        'bookings': bookings,
        'active_sessions': active_sessions
    })

@login_required
def start_chat_from_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if the logged-in user is the astrologer for this booking
    try:
        profile = request.user.astrologer_profile
        if booking.astrologer != profile:
            return redirect('home')
    except:
        # If user is not astrologer, check balance before starting chat
        if booking.user == request.user:
            min_minutes = 5
            required_balance = booking.astrologer.chat_price_per_minute * min_minutes
            if request.user.profile.wallet_balance < required_balance:
                # In a real app, redirect to recharge. For now, show error/stay on bookings
                # We can add a message framework logic here later
                # print(f"Insufficient balance: {request.user.profile.wallet_balance} < {required_balance}")
                return redirect('consultations:my_bookings')
        else:
            return redirect('home')
    
    # If it's a chat booking, start/get the session
    if booking.consultation_type == 'chat':
        session, created = ChatSession.objects.get_or_create(
            customer=booking.user,
            astrologer=booking.astrologer.user,
            is_active=True
        )
        return redirect('consultations:chat_room', session_id=session.id)
    
    return redirect('consultations:astrologer_dashboard')

@login_required
def start_call_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    try:
        if booking.astrologer != request.user.astrologer_profile:
            # Check balance for customer
            if booking.user == request.user:
                min_minutes = 5
                required_balance = booking.astrologer.call_price_per_minute * min_minutes
                if request.user.profile.wallet_balance < required_balance:
                     # print(f"Insufficient balance for call")
                     return redirect('consultations:my_bookings')
            else:
                return redirect('home')
    except:
        # If customer (no astro profile), balance check is handled above or here if needed
        if booking.user != request.user:
            return redirect('home')
        
    if booking.consultation_type == 'call':
        booking.status = 'approved'
        booking.save()
        return redirect('consultations:call_room', booking_id=booking.id)
    return redirect('consultations:astrologer_dashboard')

@login_required
def call_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: Only the booked user or the assigned astrologer can join
    is_astrologer = False
    try:
        if hasattr(request.user, 'astrologer_profile') and booking.astrologer == request.user.astrologer_profile:
            is_astrologer = True
    except:
        pass
        
    if not is_astrologer and booking.user != request.user:
        return redirect('home')
        
    context = {
        'booking': booking,
        'room_name': f"AstroCall_{booking.id}_{booking.scheduled_at.strftime('%Y%m%d')}",
        'user_display_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'consultations/call_room.html', context)


@login_required
def reschedule_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    try:
        if booking.astrologer != request.user.astrologer_profile:
            return redirect('home')
    except:
        return redirect('home')
    
    if request.method == 'POST':
        new_time = request.POST.get('new_time')
        if new_time:
            booking.proposed_reschedule_time = new_time
            booking.status = 'reschedule_proposed'
            booking.save()
            return redirect('consultations:astrologer_dashboard')
            
    return render(request, 'consultations/reschedule_form.html', {'booking': booking})

@login_required
def handle_reschedule(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only customer can accept/reject
    if booking.user != request.user:
        return redirect('home')
        
    action = request.POST.get('action')
    if action == 'accept':
        booking.scheduled_at = booking.proposed_reschedule_time
        booking.proposed_reschedule_time = None
        booking.status = 'approved'
        booking.save()
    elif action == 'reject':
        booking.proposed_reschedule_time = None
        booking.status = 'pending'
        booking.save()
        
    return redirect('consultations:my_bookings')

@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        from .models import Review
        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )
        
        # Update astrologer rating (simple average for now)
        profile = booking.astrologer
        reviews = Review.objects.filter(booking__astrologer=profile)
        total_rating = sum(r.rating for r in reviews)
        profile.rating = total_rating / reviews.count()
        profile.save()
        
    return redirect('consultations:my_bookings')



@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    try:
        if booking.astrologer != request.user.astrologer_profile:
            return redirect('home')
    except:
        return redirect('home')
    
    booking.status = 'completed'
    booking.save()
    return redirect('consultations:astrologer_dashboard')

@login_required
def start_chat(request, astrologer_id):
    # Determine who is the astrologer user
    try:
        astrologer_profile = AstrologerProfile.objects.get(id=astrologer_id)
        astrologer_user = astrologer_profile.user
    except AstrologerProfile.DoesNotExist:
        return redirect('astrologers:astrologer_list')

    # Create a new session or get existing active one
    session, created = ChatSession.objects.get_or_create(
        customer=request.user,
        astrologer=astrologer_user,
        is_active=True
    )
    
    return redirect('consultations:chat_room', session_id=session.id)

@login_required
def chat_room(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    
    # Security check: only allow participants
    if request.user != session.customer and request.user != session.astrologer:
        return redirect('home')
        
    messages = session.messages.all().order_by('timestamp')
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.session = session
            msg.sender = request.user
            msg.save()
            return redirect('consultations:chat_room', session_id=session.id)
    else:
        form = ChatMessageForm()
        
    return render(request, 'consultations/chat_room.html', {
        'session': session,
        'messages': messages,
        'form': form
    })

from django.http import JsonResponse
from django.utils import timezone

@login_required
def get_messages(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    if request.user != session.customer and request.user != session.astrologer:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    last_id = request.GET.get('last_id')
    messages = session.messages.all()
    if last_id:
        try:
            messages = messages.filter(id__gt=int(last_id))
        except ValueError:
            pass
    
    messages = messages.order_by('timestamp')
    
    data = [{
        'id': m.id,
        'sender_id': m.sender.id,
        'sender_name': m.sender.username,
        'content': m.content,
        'timestamp': m.timestamp.strftime('%H:%M')
    } for m in messages]
    
    return JsonResponse({'messages': data})

@login_required
def send_message_ajax(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(ChatSession, id=session_id)
        if request.user != session.customer and request.user != session.astrologer:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
        content = request.POST.get('content')
        if content:
            # Check if this is the first message from the astrologer to start the timer
            timer_started = False
            if request.user == session.astrologer and not session.actual_start_time:
                session.actual_start_time = timezone.now()
                session.save()
                timer_started = True

            msg = ChatMessage.objects.create(
                session=session,
                sender=request.user,
                content=content
            )
            return JsonResponse({
                'id': msg.id,
                'sender_id': msg.sender.id,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'iso_timestamp': msg.timestamp.isoformat(),
                'timer_started': timer_started,
                'is_astrologer': request.user == session.astrologer
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def end_chat(request, session_id):
    from django.utils import timezone
    session = get_object_or_404(ChatSession, id=session_id)
    
    # Only astrologer can end the chat
    if session.astrologer != request.user:
        return redirect('home')
    
    # Mark session as inactive and set end time
    session.is_active = False
    session.end_time = timezone.now()
    session.save()
    
    # Calculate duration and deduct wallet
    try:
        if session.actual_start_time:
            duration_minutes = (session.end_time - session.actual_start_time).total_seconds() / 60
            # Ensure at least 1 minute is charged if connected and timer started
            duration_minutes = max(1, duration_minutes)
            
            # Get price rate
            astrologer_profile = session.astrologer.astrologer_profile
            rate = astrologer_profile.chat_price_per_minute
            cost = getattr(rate, 'real', rate) * getattr(duration_minutes, 'real', duration_minutes)
            from decimal import Decimal
            cost = Decimal(cost)
            
            # Deduct from customer
            session.customer.profile.deduct_wallet(cost, description=f"Chat Consultation with {session.astrologer.username}")
            
            # Credit to astrologer
            session.astrologer.profile.credit_wallet(cost, description=f"Chat Consultation with {session.customer.username}")
            
            # print("Chat ended but timer never started (Astrologer didn't reply). No deduction.")
            
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        pass
    
    # Delete all messages in this session
    ChatMessage.objects.filter(session=session).delete()
    
    # Find and complete the associated booking
    try:
        # Try to find the most recent pending or approved chat booking
        booking = Booking.objects.filter(
            user=session.customer,
            astrologer__user=session.astrologer,
            consultation_type='chat'
        ).filter(
            status__in=['pending', 'approved']
        ).order_by('-scheduled_at').first()
        
        if booking:
            booking.status = 'completed'
            booking.save()
    except Exception as e:
        pass
    
    return redirect('consultations:astrologer_dashboard')
