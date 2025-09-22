from django import forms
from .models import BorrowRecord, Member, Reservation, Book
from datetime import date, timedelta

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['membership_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'membership_type']
        widgets = {
            'membership_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Membership ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
        }

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['due_date', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default due date to 14 days from today
        self.fields['due_date'].initial = date.today() + timedelta(days=14)

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['book', 'notes']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available books for reservation
        self.fields['book'].queryset = Book.objects.filter(is_available=True)

class BookSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books, authors, ISBN...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        from .models import Category
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
