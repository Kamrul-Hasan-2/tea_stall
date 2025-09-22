from django.core.management.base import BaseCommand
from stall.models import Category, TeaItem, Customer, Order, OrderItem, Inventory

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create Categories
        categories_data = [
            {'name': 'Black Tea', 'description': 'Traditional black tea varieties'},
            {'name': 'Green Tea', 'description': 'Healthy green tea options'},
            {'name': 'Herbal Tea', 'description': 'Natural herbal infusions'},
            {'name': 'Specialty Tea', 'description': 'Special tea blends and flavors'},
            {'name': 'Iced Tea', 'description': 'Refreshing cold tea beverages'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Tea Items
        tea_items_data = [
            # Black Tea
            {'name': 'Classic Chai', 'category': 'Black Tea', 'price': 15.00, 'description': 'Traditional Indian spiced tea with milk', 'prep_time': 5},
            {'name': 'Masala Chai', 'category': 'Black Tea', 'price': 18.00, 'description': 'Rich spiced tea with cardamom, ginger, and cinnamon', 'prep_time': 7},
            {'name': 'Cutting Chai', 'category': 'Black Tea', 'price': 10.00, 'description': 'Half cup of strong tea, perfect for quick breaks', 'prep_time': 3},
            {'name': 'Irani Chai', 'category': 'Black Tea', 'price': 20.00, 'description': 'Mildly sweet tea served in traditional Irani style', 'prep_time': 6},
            
            # Green Tea
            {'name': 'Green Tea', 'category': 'Green Tea', 'price': 25.00, 'description': 'Pure green tea leaves for a healthy refreshment', 'prep_time': 4},
            {'name': 'Lemon Green Tea', 'category': 'Green Tea', 'price': 30.00, 'description': 'Green tea with fresh lemon and honey', 'prep_time': 5},
            {'name': 'Mint Green Tea', 'category': 'Green Tea', 'price': 28.00, 'description': 'Refreshing green tea with fresh mint leaves', 'prep_time': 5},
            
            # Herbal Tea
            {'name': 'Ginger Tea', 'category': 'Herbal Tea', 'price': 22.00, 'description': 'Warming ginger tea perfect for cold weather', 'prep_time': 6},
            {'name': 'Tulsi Tea', 'category': 'Herbal Tea', 'price': 24.00, 'description': 'Holy basil tea with medicinal properties', 'prep_time': 5},
            {'name': 'Cardamom Tea', 'category': 'Herbal Tea', 'price': 26.00, 'description': 'Aromatic tea with fresh cardamom pods', 'prep_time': 6},
            
            # Specialty Tea
            {'name': 'Kashmiri Kahwa', 'category': 'Specialty Tea', 'price': 35.00, 'description': 'Traditional Kashmiri green tea with saffron and almonds', 'prep_time': 8},
            {'name': 'Earl Grey', 'category': 'Specialty Tea', 'price': 32.00, 'description': 'Classic English tea with bergamot oil', 'prep_time': 5},
            {'name': 'Chocolate Tea', 'category': 'Specialty Tea', 'price': 40.00, 'description': 'Rich tea blend with chocolate flavor', 'prep_time': 6},
            
            # Iced Tea
            {'name': 'Iced Lemon Tea', 'category': 'Iced Tea', 'price': 35.00, 'description': 'Chilled tea with lemon and ice cubes', 'prep_time': 4},
            {'name': 'Iced Mint Tea', 'category': 'Iced Tea', 'price': 38.00, 'description': 'Refreshing iced tea with fresh mint', 'prep_time': 4},
        ]

        for item_data in tea_items_data:
            category = Category.objects.get(name=item_data['category'])
            tea_item, created = TeaItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': category,
                    'price': item_data['price'],
                    'description': item_data['description'],
                    'preparation_time': item_data['prep_time'],
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(f'Created tea item: {tea_item.name}')
                
                # Create inventory for each tea item
                Inventory.objects.get_or_create(
                    tea_item=tea_item,
                    defaults={
                        'current_stock': 50,
                        'minimum_stock': 10
                    }
                )

        # Create Sample Customers
        customers_data = [
            {'name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'MG Road, Bangalore'},
            {'name': 'Priya Patel', 'phone': '9876543211', 'email': 'priya@example.com', 'address': 'Connaught Place, Delhi'},
            {'name': 'Arjun Kumar', 'phone': '9876543212', 'email': 'arjun@example.com', 'address': 'Park Street, Kolkata'},
            {'name': 'Sneha Gupta', 'phone': '9876543213', 'email': 'sneha@example.com', 'address': 'FC Road, Pune'},
            {'name': 'Vikram Singh', 'phone': '9876543214', 'email': 'vikram@example.com', 'address': 'Linking Road, Mumbai'},
        ]

        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                phone=cust_data['phone'],
                defaults={
                    'name': cust_data['name'],
                    'email': cust_data['email'],
                    'address': cust_data['address']
                }
            )
            if created:
                self.stdout.write(f'Created customer: {customer.name}')

        # Create Sample Orders
        if Customer.objects.exists() and TeaItem.objects.exists():
            customers = Customer.objects.all()
            tea_items = list(TeaItem.objects.all())
            
            import random
            from decimal import Decimal
            
            for i in range(5):
                customer = random.choice(customers)
                order = Order.objects.create(
                    customer=customer,
                    status=random.choice(['pending', 'preparing', 'ready', 'completed']),
                    notes=f'Sample order {i+1}'
                )
                
                # Add 1-3 items to each order
                num_items = random.randint(1, 3)
                selected_items = random.sample(tea_items, num_items)
                total = Decimal('0.00')
                
                for tea_item in selected_items:
                    quantity = random.randint(1, 3)
                    order_item = OrderItem.objects.create(
                        order=order,
                        tea_item=tea_item,
                        quantity=quantity,
                        price=tea_item.price
                    )
                    total += order_item.price * order_item.quantity
                
                order.total_amount = total
                order.save()
                self.stdout.write(f'Created order #{order.id} for {customer.name}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.WARNING('Admin credentials:'))
        self.stdout.write(self.style.WARNING('Username: admin'))
        self.stdout.write(self.style.WARNING('Password: 123'))
