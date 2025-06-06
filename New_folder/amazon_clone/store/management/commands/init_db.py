from django.core.management.base import BaseCommand
from store.models import Product
from datetime import datetime

class Command(BaseCommand):
    help = 'Initialize database with products'

    def handle(self, *args, **kwargs):
        # List of products to populate the database
        products = [
            # Electronics
            ("MacBook Air M2", "Apple", 94500, "13.6-inch Liquid Retina display, Apple M2 chip, 8GB RAM, 256GB SSD storage.", "2023-06-15"),
            ("PlayStation 5 Digital Edition", "Sony", 54000, "Next-gen gaming console with 825GB SSD, 4K support, and DualSense controller.", "2020-11-12"),
            ("LG C2 65-Inch OLED TV", "LG", 52999, "4K OLED Smart TV with AI-powered processing, perfect blacks, and G-SYNC compatibility.", "2023-03-10"),
            ("Canon EOS R6 Mark II", "Canon", 267999, "Full-frame mirrorless camera with 24.2MP sensor, 4K video, and advanced autofocus.", "2022-11-02"),
            
            # Smart Home
            ("Ring Video Doorbell Pro 2", "Amazon", 7999, "1536p HDR video doorbell with 3D motion detection and Bird's Eye View.", "2023-03-31"),
            ("Philips Hue Starter Kit", "Philips", 2600, "Smart lighting bundle with bridge and 4 color-changing bulbs.", "2023-01-15"),
            ("Nest Learning Thermostat", "Google", 11618, "Smart thermostat that learns your preferences and helps save energy.", "2022-09-20"),
            
            # Kitchen Appliances
            ("Ninja Foodi 9-in-1 Deluxe XL", "Ninja", 21249, "Pressure cooker, air fryer, and more with 9 cooking functions and 8-quart capacity.", "2023-05-01"),
            ("KitchenAid Pro 5 Plus", "KitchenAid", 38250, "Professional 5-quart stand mixer with 10 speeds and bowl-lift design.", "2023-02-28"),
            ("Vitamix A3500 Blender", "Vitamix", 55250, "Smart blender with touchscreen controls, wireless connectivity, and 5 program settings.", "2023-04-15"),
            
            # Fitness
            ("Peloton Bike+", "Peloton", 218580, "Premium smart exercise bike with 24-inch rotating display and auto-follow resistance.", "2022-09-09"),
            ("Fitbit Sense 2", "Fitbit", 19550, "Advanced health smartwatch with ECG, stress tracking, and built-in GPS.", "2022-09-01"),
            ("Bowflex SelectTech 552", "Bowflex", 36550, "Adjustable dumbbells that replace 15 sets of weights, adjustable from 5 to 52.5 lbs.", "2023-01-10"),
            
            # Books and Media
            ("Lessons in Chemistry", "Bonnie Garmus", 1530, "A debut novel about a female chemist who becomes a cooking show host in the 1960s.", "2023-04-05"),
            ("Tomorrow x3", "James Clear", 1700, "A groundbreaking book about building better habits for productivity and success.", "2023-07-11"),
            ("The Light We Carry", "Michelle Obama", 1870, "Practical wisdom and powerful strategies for staying hopeful in uncertain times.", "2022-11-15"),
            
            # Gaming
            # Gaming (continued)
            ("Xbox Series X", "Microsoft", 42500, "Next-gen gaming console with 1TB SSD, 4K gaming, and Quick Resume feature.", "2020-11-10"),
            ("Nintendo Switch OLED", "Nintendo", 29750, "Gaming console with 7-inch OLED screen and enhanced audio.", "2021-10-08"),
            ("Razer Blade 14", "Razer", 170000, "Gaming laptop with AMD Ryzen 9, RTX 4060, 16GB RAM, and 1TB SSD.", "2023-03-23"),
            
            # Audio
            ("AirPods Max", "Apple", 47600, "Over-ear headphones with active noise cancellation and spatial audio.", "2020-12-15"),
            ("Sonos Era 300", "Sonos", 42500, "Smart speaker with spatial audio and room-filling sound.", "2023-03-28"),
            ("Shure SM7B", "Shure", 34000, "Professional dynamic microphone for broadcasting and podcast recording.", "2023-01-05"),
            
            # Cameras
            ("DJI Air 3", "DJI", 93500 , "Drone with dual cameras, 4K/60fps video, and 46-minute flight time.", "2023-08-09"),
            ("GoPro HERO12 Black", "GoPro", 34000, "Action camera with 5.3K video, HDR, and enhanced stabilization.", "2023-09-15"),
            ("Fujifilm X-T5", "Fujifilm", 144500, "Mirrorless camera with 40MP sensor, 6.2K video, and advanced color science.", "2022-11-17"),
            
            # Smart Home Security
            ("Arlo Pro 5", "Arlo", 21414, "2K security camera with color night vision and built-in spotlight.", "2023-06-20"),
            ("SimpliSafe 8-Piece Kit", "SimpliSafe", 22000, "Home security system with professional monitoring and wireless sensors.", "2023-04-12"),
            ("Eufy Video Doorbell E340", "Eufy", 17114, "Dual camera video doorbell with package detection and local storage.", "2023-07-19"),
            
            # Gift Cards
            ("Amazon Gift Card", "Amazon", 8800, "Digital gift card for use on Amazon.com, never expires.", "2024-01-01"),
            ("Netflix Gift Card", "Netflix", 4400, "Gift card for streaming service subscription.", "2024-01-01"),
            ("Spotify Premium Gift", "Spotify", 2640, "Three months of ad-free music streaming.", "2024-01-01")
        ]

        # Check if products exist and add them if they don't
        for name, manufacturer, price, description, release_date in products:
            if not Product.objects.filter(name=name).exists():
                Product.objects.create(
                    name=name,
                    manufacturer=manufacturer,
                    price=price,
                    description=description,
                    release_date=datetime.strptime(release_date, "%Y-%m-%d").date()
                )
                self.stdout.write(self.style.SUCCESS(f'Added product: {name}'))
            else:
                self.stdout.write(f'Product already exists: {name}')

        self.stdout.write(self.style.SUCCESS('Database initialized successfully'))