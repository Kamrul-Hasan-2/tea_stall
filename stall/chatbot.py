import google.generativeai as genai
from django.conf import settings
from .models import Book, Author, Category, Member, BorrowRecord
from django.db.models import Q
import json

class LibraryChatbot:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def get_library_context(self):
        """Get current library context for the chatbot"""
        total_books = Book.objects.count()
        available_books = Book.objects.filter(is_available=True).count()
        total_members = Member.objects.count()
        categories = list(Category.objects.values_list('name', flat=True))
        
        context = {
            'total_books': total_books,
            'available_books': available_books,
            'total_members': total_members,
            'categories': categories,
        }
        return context
    
    def search_books(self, query):
        """Search for books based on user query"""
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(description__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()[:5]
        
        book_list = []
        for book in books:
            book_list.append({
                'title': book.title,
                'authors': book.author_names,
                'category': book.category.name,
                'available': book.is_available,
                'isbn': book.isbn
            })
        return book_list
    
    def get_chat_response(self, user_message):
        """Generate response using Gemini AI"""
        try:
            # Get library context
            context = self.get_library_context()
            
            # Check if user is asking about specific books
            search_results = None
            if any(keyword in user_message.lower() for keyword in ['book', 'author', 'find', 'search', 'looking for']):
                # Extract potential search terms
                search_terms = user_message.lower().replace('book', '').replace('author', '').replace('find', '').replace('search', '').replace('looking for', '').strip()
                if search_terms:
                    search_results = self.search_books(search_terms)
            
            # Create system prompt
            system_prompt = f"""
            You are a helpful library assistant chatbot for a digital library management system. 
            
            Current Library Information:
            - Total books: {context['total_books']}
            - Available books: {context['available_books']}
            - Total members: {context['total_members']}
            - Categories: {', '.join(context['categories'])}
            
            Your role is to:
            1. Help users find books and information about the library
            2. Answer questions about library services, policies, and procedures
            3. Provide book recommendations
            4. Help with general library-related queries
            5. Be friendly, helpful, and informative
            
            Guidelines:
            - Keep responses concise but informative
            - Be friendly and professional
            - If you don't know something specific about this library, say so
            - Focus on library-related topics
            - Provide helpful suggestions when possible
            
            User message: {user_message}
            """
            
            if search_results:
                system_prompt += f"\n\nRelevant books found: {json.dumps(search_results, indent=2)}"
            
            response = self.model.generate_content(system_prompt)
            return response.text
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"
    
    def get_quick_responses(self):
        """Get predefined quick response options"""
        return [
            "How do I borrow a book?",
            "What are your library hours?",
            "Can you recommend some popular books?",
            "How do I return a book?",
            "What categories of books do you have?",
            "How many books can I borrow at once?"
        ]
