from django.core.management.base import BaseCommand
from stall.models import Category, Author, Publisher, Book, Member, BookCopy
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with sample library data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample library data...')

        # Create categories
        categories_data = [
            {'name': 'Fiction', 'description': 'Fictional stories and novels'},
            {'name': 'Non-Fiction', 'description': 'Educational and informational books'},
            {'name': 'Science', 'description': 'Scientific books and research'},
            {'name': 'History', 'description': 'Historical books and biographies'},
            {'name': 'Technology', 'description': 'Technology and programming books'},
            {'name': 'Literature', 'description': 'Classic and contemporary literature'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create publishers
        publishers_data = [
            {'name': 'Penguin Random House', 'established_year': 1927},
            {'name': 'HarperCollins', 'established_year': 1989},
            {'name': 'University Press Limited', 'established_year': 1975},
            {'name': 'Prothoma Prokashon', 'established_year': 1986},
            {'name': "O'Reilly Media", 'established_year': 1978},
        ]

        for pub_data in publishers_data:
            publisher, created = Publisher.objects.get_or_create(
                name=pub_data['name'],
                defaults={'established_year': pub_data['established_year']}
            )
            if created:
                self.stdout.write(f'Created publisher: {publisher.name}')

        # Create authors
        authors_data = [
            {'first_name': 'Rabindranath', 'last_name': 'Tagore', 'nationality': 'Bengali'},
            {'first_name': 'Kazi Nazrul', 'last_name': 'Islam', 'nationality': 'Bengali'},
            {'first_name': 'Humayun', 'last_name': 'Ahmed', 'nationality': 'Bangladeshi'},
            {'first_name': 'Jahanara', 'last_name': 'Imam', 'nationality': 'Bangladeshi'},
            {'first_name': 'Sarat Chandra', 'last_name': 'Chattopadhyay', 'nationality': 'Bengali'},
            {'first_name': 'Bankim Chandra', 'last_name': 'Chattopadhyay', 'nationality': 'Bengali'},
            {'first_name': 'Manik', 'last_name': 'Bandopadhyay', 'nationality': 'Bengali'},
            {'first_name': 'Bibhutibhushan', 'last_name': 'Bandopadhyay', 'nationality': 'Bengali'},
        ]

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                defaults={'nationality': author_data['nationality']}
            )
            if created:
                self.stdout.write(f'Created author: {author.full_name}')

        # Create books
        books_data = [
            {
                'title': 'Gitanjali',
                'authors': ['Rabindranath Tagore'],
                'category': 'Literature',
                'publisher': 'University Press Limited',
                'isbn': '9789840471157',
                'pages': 120,
                'language': 'bn',
                'description': 'A collection of 103 English poem translations of songs from Rabindranath Tagore.',
                'price': 250.00
            },
            {
                'title': 'Himu Series - Mayurakkhi',
                'authors': ['Humayun Ahmed'],
                'category': 'Fiction',
                'publisher': 'Prothoma Prokashon',
                'isbn': '9789844122345',
                'pages': 180,
                'language': 'bn',
                'description': 'A popular novel featuring the character Himu.',
                'price': 300.00
            },
            {
                'title': 'Ekattorer Dingulie',
                'authors': ['Jahanara Imam'],
                'category': 'History',
                'publisher': 'University Press Limited',
                'isbn': '9789840456789',
                'pages': 250,
                'language': 'bn',
                'description': 'A memoir about the Bangladesh Liberation War of 1971.',
                'price': 400.00
            },
            {
                'title': 'Devdas',
                'authors': ['Sarat Chandra Chattopadhyay'],
                'category': 'Literature',
                'publisher': 'Penguin Random House',
                'isbn': '9789844567890',
                'pages': 200,
                'language': 'bn',
                'description': 'A classic Bengali novel about love and tragedy.',
                'price': 280.00
            },
            {
                'title': 'Anandamath',
                'authors': ['Bankim Chandra Chattopadhyay'],
                'category': 'Literature',
                'publisher': 'University Press Limited',
                'isbn': '9789844678901',
                'pages': 300,
                'language': 'bn',
                'description': 'A political novel that helped inspire the Indian independence movement.',
                'price': 350.00
            },
            {
                'title': 'Putul Nacher Itikatha',
                'authors': ['Manik Bandopadhyay'],
                'category': 'Literature',
                'publisher': 'Prothoma Prokashon',
                'isbn': '9789844789012',
                'pages': 180,
                'language': 'bn',
                'description': 'A novel depicting the lives of rural people in Bengal.',
                'price': 320.00
            },
            {
                'title': 'Pather Panchali',
                'authors': ['Bibhutibhushan Bandopadhyay'],
                'category': 'Literature',
                'publisher': 'University Press Limited',
                'isbn': '9789844890123',
                'pages': 250,
                'language': 'bn',
                'description': 'A coming-of-age novel set in rural Bengal.',
                'price': 380.00
            },
            {
                'title': 'Rupali Shoikote Rawhoshyo',
                'authors': ['Humayun Ahmed'],
                'category': 'Fiction',
                'publisher': 'Prothoma Prokashon',
                'isbn': '9789844901234',
                'pages': 160,
                'language': 'bn',
                'description': 'A mystery novel set in a college campus.',
                'price': 280.00
            }
        ]

        for book_data in books_data:
            # Get category
            category = Category.objects.get(name=book_data['category'])
            
            # Get publisher
            publisher = Publisher.objects.get(name=book_data['publisher'])
            
            # Create book
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                isbn=book_data['isbn'],
                defaults={
                    'category': category,
                    'publisher': publisher,
                    'pages': book_data['pages'],
                    'language': book_data['language'],
                    'description': book_data['description'],
                    'price': book_data['price']
                }
            )
            
            if created:
                # Add authors
                for author_name in book_data['authors']:
                    name_parts = author_name.split(' ')
                    if len(name_parts) >= 2:
                        first_name = name_parts[0]
                        last_name = ' '.join(name_parts[1:])
                    else:
                        first_name = name_parts[0]
                        last_name = ''
                    
                    try:
                        author = Author.objects.get(first_name=first_name, last_name=last_name)
                        book.authors.add(author)
                    except Author.DoesNotExist:
                        self.stdout.write(f'Author not found: {author_name}')
                        continue
                
                # Create book copies
                for i in range(1, 4):  # Create 3 copies of each book
                    BookCopy.objects.create(
                        book=book,
                        copy_number=f'C{book.id:03d}-{i:02d}',
                        condition='good',
                        location_shelf=f'Shelf-{(book.id % 10) + 1}'
                    )
                
                self.stdout.write(f'Created book: {book.title}')

        # Create sample members
        members_data = [
            {
                'membership_id': 'STU001',
                'first_name': 'Rahim',
                'last_name': 'Ahmed',
                'email': 'rahim.ahmed@email.com',
                'phone': '01712345678',
                'address': 'Dhaka, Bangladesh',
                'membership_type': 'student'
            },
            {
                'membership_id': 'FAC001',
                'first_name': 'Fatima',
                'last_name': 'Khan',
                'email': 'fatima.khan@email.com',
                'phone': '01887654321',
                'address': 'Chittagong, Bangladesh',
                'membership_type': 'faculty'
            },
            {
                'membership_id': 'GEN001',
                'first_name': 'Karim',
                'last_name': 'Rahman',
                'email': 'karim.rahman@email.com',
                'phone': '01956789012',
                'address': 'Sylhet, Bangladesh',
                'membership_type': 'general'
            }
        ]

        for member_data in members_data:
            member, created = Member.objects.get_or_create(
                membership_id=member_data['membership_id'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created member: {member.full_name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated the database with sample library data!')
        )
