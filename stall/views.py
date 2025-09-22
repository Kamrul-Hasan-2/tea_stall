from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Sum, F, Count
from django.http import JsonResponse
from .models import Book, Category, Author, Member, BorrowRecord, BookCopy, Reservation
from .forms import BorrowForm, MemberForm, ReservationForm
from django.utils import timezone
from datetime import date, timedelta

def home(request):
    """Home page showing available books"""
    try:
        categories = Category.objects.all()
        books = Book.objects.filter(is_available=True).prefetch_related('authors')
        
        # Filter by category if specified
        category_id = request.GET.get('category')
        if category_id:
            books = books.filter(category_id=category_id)
        
        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(authors__first_name__icontains=search_query) |
                Q(authors__last_name__icontains=search_query)
            ).distinct()
        
        context = {
            'books': books,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_id
        }
        return render(request, 'stall/home.html', context)
    except Exception as e:
        # Handle any database errors gracefully
        context = {
            'books': [],
            'categories': [],
            'search_query': '',
            'selected_category': None,
            'error_message': f'Database error: {str(e)}'
        }
        return render(request, 'stall/home.html', context)

def book_detail(request, book_id):
    """Detail view for a specific book"""
    book = get_object_or_404(Book, id=book_id)
    available_copies = BookCopy.objects.filter(book=book, is_available=True)
    
    context = {
        'book': book,
        'available_copies': available_copies,
        'total_copies': book.copies.count(),
        'available_count': available_copies.count()
    }
    return render(request, 'stall/book_detail.html', context)

def borrow_book(request):
    """Create a new book borrowing record"""
    if request.method == 'POST':
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            # Get or create member
            email = member_form.cleaned_data['email']
            member, created = Member.objects.get_or_create(
                email=email,
                defaults={
                    'membership_id': member_form.cleaned_data['membership_id'],
                    'first_name': member_form.cleaned_data['first_name'],
                    'last_name': member_form.cleaned_data['last_name'],
                    'phone': member_form.cleaned_data['phone'],
                    'address': member_form.cleaned_data['address'],
                    'membership_type': member_form.cleaned_data['membership_type']
                }
            )
            
            request.session['current_member_id'] = member.id
            messages.success(request, f'Member {member.full_name} selected successfully!')
            return redirect('select_books_to_borrow', member_id=member.id)
    else:
        member_form = MemberForm()
    
    return render(request, 'stall/borrow_book.html', {'member_form': member_form})

def select_books_to_borrow(request, member_id):
    """Select books to borrow for a member"""
    member = get_object_or_404(Member, id=member_id)
    available_books = Book.objects.filter(is_available=True).prefetch_related('authors')
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        due_date_str = request.POST.get('due_date')
        
        book = get_object_or_404(Book, id=book_id)
        
        # Check if member already has this book
        existing_borrow = BorrowRecord.objects.filter(
            member=member,
            book=book,
            return_date__isnull=True
        ).exists()
        
        if existing_borrow:
            messages.error(request, f'{member.full_name} already has this book borrowed.')
            return redirect('select_books_to_borrow', member_id=member.id)
        
        # Create borrow record
        due_date = date.today() + timedelta(days=14)  # Default 14 days
        if due_date_str:
            try:
                due_date = date.fromisoformat(due_date_str)
            except:
                pass
        
        borrow_record = BorrowRecord.objects.create(
            member=member,
            book=book,
            due_date=due_date,
            issued_by=request.user if request.user.is_authenticated else None
        )
        
        # Update book availability if no more copies available
        available_copies = BookCopy.objects.filter(book=book, is_available=True)
        if available_copies.exists():
            copy = available_copies.first()
            copy.is_available = False
            copy.save()
        
        messages.success(request, f'Book "{book.title}" borrowed successfully!')
        return redirect('select_books_to_borrow', member_id=member.id)
    
    # Get member's current borrowings
    current_borrowings = BorrowRecord.objects.filter(
        member=member,
        return_date__isnull=True
    ).select_related('book')
    
    context = {
        'member': member,
        'available_books': available_books,
        'current_borrowings': current_borrowings
    }
    return render(request, 'stall/select_books_to_borrow.html', context)

def return_book(request, borrow_id):
    """Return a borrowed book"""
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_id)
    
    if request.method == 'POST':
        borrow_record.return_date = date.today()
        borrow_record.status = 'returned'
        
        # Calculate fine if overdue
        if borrow_record.is_overdue:
            days_overdue = borrow_record.days_overdue
            fine_per_day = 5  # BDT 5 per day
            borrow_record.fine_amount = days_overdue * fine_per_day
        
        borrow_record.save()
        
        # Make book copy available again
        copy = BookCopy.objects.filter(book=borrow_record.book, is_available=False).first()
        if copy:
            copy.is_available = True
            copy.save()
        
        messages.success(request, f'Book "{borrow_record.book.title}" returned successfully!')
        return redirect('borrowing_list')
    
    return render(request, 'stall/return_book.html', {'borrow_record': borrow_record})

def borrowing_list(request):
    """List all borrowing records"""
    borrowings = BorrowRecord.objects.all().select_related('member', 'book').order_by('-borrow_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        borrowings = borrowings.filter(status=status)
    
    # Filter by member
    member_id = request.GET.get('member')
    if member_id:
        borrowings = borrowings.filter(member_id=member_id)
    
    context = {
        'borrowings': borrowings,
        'status_choices': BorrowRecord.STATUS_CHOICES,
        'selected_status': status,
        'members': Member.objects.filter(is_active=True)
    }
    return render(request, 'stall/borrowing_list.html', context)

def member_detail(request, member_id):
    """Detail view for a specific member"""
    member = get_object_or_404(Member, id=member_id)
    borrowing_history = BorrowRecord.objects.filter(member=member).select_related('book')
    
    context = {
        'member': member,
        'borrowing_history': borrowing_history,
        'active_borrowings': member.active_borrowings,
        'overdue_books': member.overdue_books
    }
    return render(request, 'stall/member_detail.html', context)

def dashboard(request):
    """Dashboard with library statistics"""
    today = timezone.now().date()
    
    # Today's statistics
    today_borrowings = BorrowRecord.objects.filter(borrow_date=today)
    today_returns = BorrowRecord.objects.filter(return_date=today)
    
    # Overall statistics
    total_books = Book.objects.count()
    total_members = Member.objects.filter(is_active=True).count()
    active_borrowings = BorrowRecord.objects.filter(return_date__isnull=True).count()
    overdue_books = BorrowRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=today
    ).count()
    
    # Popular books
    popular_books = Book.objects.annotate(
        borrow_count=Count('borrowrecord')
    ).order_by('-borrow_count')[:5]
    
    # Recent activities
    recent_borrowings = BorrowRecord.objects.all().select_related('member', 'book')[:5]
    
    context = {
        'today_borrowings_count': today_borrowings.count(),
        'today_returns_count': today_returns.count(),
        'total_books': total_books,
        'total_members': total_members,
        'active_borrowings': active_borrowings,
        'overdue_books': overdue_books,
        'popular_books': popular_books,
        'recent_borrowings': recent_borrowings
    }
    return render(request, 'stall/dashboard.html', context)

def authors_list(request):
    """List all authors"""
    authors = Author.objects.all().order_by('last_name', 'first_name')
    
    search_query = request.GET.get('search')
    if search_query:
        authors = authors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(nationality__icontains=search_query)
        )
    
    context = {
        'authors': authors,
        'search_query': search_query
    }
    return render(request, 'stall/authors_list.html', context)

def author_detail(request, author_id):
    """Detail view for a specific author"""
    author = get_object_or_404(Author, id=author_id)
    books = author.books.filter(is_available=True)
    
    context = {
        'author': author,
        'books': books
    }
    return render(request, 'stall/author_detail.html', context)

def members_list(request):
    """List all members"""
    members = Member.objects.filter(is_active=True).order_by('last_name', 'first_name')
    
    search_query = request.GET.get('search')
    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(membership_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    context = {
        'members': members,
        'search_query': search_query
    }
    return render(request, 'stall/members_list.html', context)

# Chatbot Views
from .chatbot import LibraryChatbot
import json

def chatbot_page(request):
    """Chatbot page"""
    chatbot = LibraryChatbot()
    quick_responses = chatbot.get_quick_responses()
    
    context = {
        'quick_responses': quick_responses
    }
    return render(request, 'stall/chatbot.html', context)

def chatbot_api(request):
    """API endpoint for chatbot responses"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            chatbot = LibraryChatbot()
            response = chatbot.get_chat_response(user_message)
            
            return JsonResponse({
                'response': response,
                'status': 'success'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
