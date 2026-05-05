from django.core.management.base import BaseCommand
from core.models import Category, Meal

MEAL_DATA = [
    {
        'name': 'Breakfast', 'slug': 'breakfast', 'icon': '🍳', 'order': 1,
        'meals': [
            {'name': 'Egg Roll', 'price': 1.50, 'description': 'Crispy golden egg rolls filled with seasoned eggs, a beloved Nigerian street breakfast.', 'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600&q=80'},
            {'name': 'Akara', 'price': 1.00, 'description': 'Deep-fried bean cakes made from ground black-eyed peas, crispy outside and fluffy inside.', 'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=600&q=80'},
            {'name': 'Noodles', 'price': 1.00, 'description': 'Spicy West African-style stir-fried noodles with vegetables and seasoning.', 'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80'},
            {'name': 'Gari and Peanuts', 'price': 2.00, 'description': 'Toasted cassava flakes paired with roasted groundnuts — a classic comfort breakfast.', 'image_url': 'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=600&q=80'},
        ]
    },
    {
        'name': 'Lunch', 'slug': 'lunch', 'icon': '🍛', 'order': 2,
        'meals': [
            {'name': 'Jollof Rice', 'price': 3.00, 'description': 'The legendary West African party rice — slow-cooked in a rich tomato base with spices.', 'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600&q=80'},
            {'name': 'Fried Rice', 'price': 3.00, 'description': 'Colourful Nigerian fried rice with mixed vegetables, liver, and aromatic seasoning.', 'image_url': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=600&q=80'},
            {'name': 'Draw Soup', 'price': 3.00, 'description': 'A thick, viscous okra soup with assorted meats and rich palm oil base — comfort in a bowl.', 'image_url': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80'},
            {'name': 'Egusi Soup', 'price': 3.00, 'description': 'Melon seed soup with leafy greens, palm oil and assorted proteins — a Nigerian staple.', 'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80'},
        ]
    },
    {
        'name': 'Supper', 'slug': 'supper', 'icon': '🌙', 'order': 3,
        'meals': [
            {'name': 'Nsala Soup', 'price': 3.00, 'description': 'White soup from Eastern Nigeria — delicate, peppery broth with catfish and uziza leaves.', 'image_url': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80'},
            {'name': 'Bitterleaf Soup', 'price': 3.00, 'description': 'Rich Igbo soup made with fresh bitterleaf, cocoyam, and assorted smoked meats.', 'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80'},
            {'name': 'Afro-Style Pizza', 'price': 3.00, 'description': 'Artisanal pizza topped with suya-spiced chicken, plantain, and jollof sauce.', 'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80'},
            {'name': 'Pepper Soup', 'price': 3.00, 'description': 'Aromatic spiced broth with goat meat and traditional herbs — warming and bold.', 'image_url': 'https://images.unsplash.com/photo-1578020190125-f4f7c18bc9cb?w=600&q=80'},
        ]
    },
    {
        'name': 'Beverages', 'slug': 'beverages', 'icon': '🥤', 'order': 4,
        'meals': [
            {'name': 'Palm Wine', 'price': 2.00, 'description': 'Freshly tapped palm wine — naturally sweet, lightly fermented, and authentically African.', 'image_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=600&q=80'},
            {'name': 'Coconut Milk', 'price': 1.00, 'description': 'Creamy, fresh-pressed coconut milk — naturally sweet and refreshing.', 'image_url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=600&q=80'},
            {'name': 'Cocoa Milk', 'price': 1.00, 'description': 'Rich West African cocoa blended into a smooth, indulgent chocolate milk.', 'image_url': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600&q=80'},
            {'name': 'Malt', 'price': 1.00, 'description': 'Classic African malt drink — sweet, energy-giving, and non-alcoholic.', 'image_url': 'https://images.unsplash.com/photo-1561758033-7e924f619b47?w=600&q=80'},
        ]
    },
]

class Command(BaseCommand):
    help = 'Seed database with menu data'

    def handle(self, *args, **kwargs):
        for cat_data in MEAL_DATA:
            meals = cat_data.pop('meals')
            category, _ = Category.objects.update_or_create(slug=cat_data['slug'], defaults=cat_data)
            for meal_data in meals:
                Meal.objects.update_or_create(name=meal_data['name'], category=category, defaults=meal_data)
        self.stdout.write(self.style.SUCCESS('Database seeded!'))
