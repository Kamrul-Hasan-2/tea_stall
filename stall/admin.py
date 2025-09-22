from django.contrib import admin
from .models import Category, Author, Publisher, Book, Member, BorrowRecord, BookCopy, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality', 'birth_date']
    search_fields = ['first_name', 'last_name', 'nationality']
    list_filter = ['nationality']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'established_year', 'created_at']
    search_fields = ['name']
    list_filter = ['established_year']

class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_names', 'category', 'publisher', 'isbn', 'is_available']
    list_filter = ['category', 'language', 'is_available', 'publication_date']
    search_fields = ['title', 'isbn', 'authors__first_name', 'authors__last_name']
    filter_horizontal = ['authors']
    list_editable = ['is_available']
    inlines = [BookCopyInline]

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['membership_id', 'first_name', 'last_name', 'email', 'membership_type', 'is_active']
    list_filter = ['membership_type', 'is_active', 'date_joined']
    search_fields = ['membership_id', 'first_name', 'last_name', 'email']
    list_editable = ['is_active']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue']
    list_filter = ['status', 'borrow_date', 'due_date', 'return_date']
    search_fields = ['book__title', 'member__first_name', 'member__last_name', 'member__membership_id']
    list_editable = ['status', 'return_date']
    readonly_fields = ['borrow_date', 'is_overdue', 'days_overdue']
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['book', 'copy_number', 'condition', 'is_available', 'location_shelf']
    list_filter = ['condition', 'is_available', 'acquisition_date']
    search_fields = ['book__title', 'copy_number', 'location_shelf']
    list_editable = ['condition', 'is_available', 'location_shelf']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'reservation_date', 'status', 'expiry_date']
    list_filter = ['status', 'reservation_date', 'expiry_date']
    search_fields = ['book__title', 'member__first_name', 'member__last_name']
    list_editable = ['status']
