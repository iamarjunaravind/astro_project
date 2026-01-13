import os
import django
import sys
from decimal import Decimal

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from astromall.models import Category, Product

def populate_south_indian_poojas():
    # 1. Ensure Category Exists
    pooja_category, created = Category.objects.get_or_create(name='Pooja')
    if created:
        print(f"Created category: {pooja_category.name}")
    else:
        print(f"Found category: {pooja_category.name}")

    # 2. Define 50 South Indian Poojas
    south_indian_poojas = [
    {"name": "Ganapathi Homam", "price": "3000.00", "description": "Dedicated to Lord Ganesha to remove obstacles and ensure success in new ventures."},
    {"name": "Navagraha Homam", "price": "4500.00", "description": "Pacifies the nine planets to reduce malefic effects and bring harmony."},
    {"name": "Sudarshana Homam", "price": "5000.00", "description": "Invokes Lord Sudarshana for protection against negative forces and enemies."},
    {"name": "Ayush Homam", "price": "3500.00", "description": "Performed for longevity, good health, and removing the fear of death."},
    {"name": "Maha Mrityunjaya Homam", "price": "11000.00", "description": "A powerful ritual for overcoming severe illness and extending life."},
    {"name": "Dhanvantri Homam", "price": "4000.00", "description": "Dedicated to the Divine Physician for curing diseases and ensuring health."},
    {"name": "Lakshmi Kubera Homam", "price": "5500.00", "description": "Attracts wealth, financial stability, and prosperity."},
    {"name": "Saraswathi Homam", "price": "3000.00", "description": "Enhances wisdom, knowledge, and academic success."},
    {"name": "Subramanya Homam", "price": "4000.00", "description": "Invokes Lord Murugan for courage, victory, and removing Naga Dosha."},
    {"name": "Chandi Homam", "price": "15000.00", "description": "A major ritual invoking Goddess Chandi for power and removing negativity."},
    {"name": "Durga Deepa Namaskara", "price": "2500.00", "description": "Worship of Goddess Durga using lamps to remove darkness and sorrow."},
    {"name": "Lalitha Sahasranama Archana", "price": "1500.00", "description": "Chanting 1000 names of Goddess Lalitha for marital bliss and prosperity."},
    {"name": "Vishnu Sahasranama Archana", "price": "1500.00", "description": "Chanting 1000 names of Lord Vishnu for peace and mental clarity."},
    {"name": "Rudra Abhishekam", "price": "2500.00", "description": "Hydration ceremony for Lord Shiva to wash away sins and bring peace."},
    {"name": "Pradosha Pooja", "price": "2000.00", "description": "Performed during Pradosham time to liberate from karma and fulfill wishes."},
    {"name": "Satyanarayan Pooja", "price": "2500.00", "description": "Common household pooja for family welfare, truth, and prosperity."},
    {"name": "Vara Lakshmi Vratam", "price": "3000.00", "description": "Observed by married women for the well-being of their husband and family."},
    {"name": "Karadaiyan Nombu", "price": "2000.00", "description": "Fast observed by Tamil women for the longevity of their husbands."},
    {"name": "Aavani Avittam (Upakarma)", "price": "1500.00", "description": "Changing of the sacred thread, signifying a renewal of spiritual duties."},
    {"name": "Karthigai Deepam Pooja", "price": "2000.00", "description": "Festival of lights dedicated to Lord Shiva and Murugan."},
    {"name": "Thai Poosam Pooja", "price": "2500.00", "description": "Dedicated to Lord Murugan, celebrating his victory over demons."},
    {"name": "Panguni Uthiram Pooja", "price": "2500.00", "description": "Celebrates divine marriages like Shiva-Parvati and Rama-Sita."},
    {"name": "Vaikunta Ekadasi Pooja", "price": "3000.00", "description": "Special worship of Vishnu on this auspicious day for salvation."},
    {"name": "Masi Magam Pooja", "price": "2500.00", "description": "A festival where deities are taken for a holy bath, washing away sins."},
    {"name": "Adi Pooram Pooja", "price": "2500.00", "description": "Dedicated to Goddess Andal, seeking blessings for children and prosperity."},
    {"name": "Navarathri Pooja (9 Days)", "price": "9000.00", "description": "Nine nights of worship of the Divine Mother in her various forms."},
    {"name": "Skanda Sashti Pooja", "price": "3500.00", "description": "Six-day worship of Lord Murugan ending in the destruction of Soorapadman."},
    {"name": "Gokulashtami (Janmashtami) Pooja", "price": "2500.00", "description": "Celebrates the birth of Lord Krishna with special offerings."},
    {"name": "Rama Navami Pooja", "price": "2500.00", "description": "Celebrates the birth of Lord Rama, the embodiment of dharma."},
    {"name": "Hanuman Jayanthi Pooja", "price": "2500.00", "description": "Worship of Lord Hanuman for strength, devotion, and protection."},
    {"name": "Naga Chaturthi Pooja", "price": "2000.00", "description": "Worship of the Snake God for fertility and removing Naga Dosha."},
    {"name": "Garuda Panchami Pooja", "price": "2000.00", "description": "Worship of Garuda for protection from snakes and skin diseases."},
    {"name": "Kuja Dosha Nivarana Pooja", "price": "3500.00", "description": "Remedial pooja for Mars affliction (Mangal Dosha) in the horoscope."},
    {"name": "Kala Sarpa Dosha Nivarana", "price": "5000.00", "description": "Alleviates the effects of Kala Sarpa Yoga in the natal chart."},
    {"name": "Rahukala Deepam", "price": "500.00", "description": "Lighting lamps during Rahu Kalam to remove obstacles and darkness."},
    {"name": "Vilva Archana", "price": "1000.00", "description": "Offering Vilva leaves to Lord Shiva, highly sacred and merit-giving."},
    {"name": "Kumkuma Archana", "price": "1000.00", "description": "Worship of the Goddess with Kumkum for marital bliss and protection."},
    {"name": "Tulsi Archana", "price": "1000.00", "description": "Offering Tulsi leaves to Lord Vishnu, purifying the mind and body."},
    {"name": "Swayamvara Parvathi Homam", "price": "6000.00", "description": "For removing delays in marriage and finding a suitable life partner."},
    {"name": "Santhana Gopala Homam", "price": "5500.00", "description": "For couples seeking the blessing of a child (progeny)."},
    {"name": "Vidya Ganapathi Homam", "price": "3500.00", "description": "Specific form of Ganesha worship for success in education."},
    {"name": "Ashta Dravya Homam", "price": "4000.00", "description": "Offering eight sacred substances to Ganesha for wealth and prosperity."},
    {"name": "Tila Homam", "price": "4000.00", "description": "Performed for ancestors (Pitrus) to bring them peace."},
    {"name": "Bhairava Pooja", "price": "3000.00", "description": "Worship of Lord Bhairava for protection and removing fear."},
    {"name": "Varahi Amman Pooja", "price": "3000.00", "description": "Worship of Varahi for victory over enemies and legal success."},
    {"name": "Pratyangira Devi Homam", "price": "7000.00", "description": "Fierce protection against black magic and evil eyes."},
    {"name": "Annapoorneshwari Pooja", "price": "2500.00", "description": "Ensures that the household never lacks food and nourishment."},
    {"name": "Dakshinamurthy Pooja", "price": "3000.00", "description": "Worship of the Guru aspect of Shiva for wisdom and clarity."},
    {"name": "Hayagriva Pooja", "price": "3000.00", "description": "Worship of Lord Hayagriva for knowledge and concentration."},
    {"name": "Gayatri Homam", "price": "4000.00", "description": "Invokes the Gayatri Mantra for spiritual enlightenment and purification."}
]

    # 3. Create Products
    for item in south_indian_poojas:
        product, created = Product.objects.get_or_create(
            name=item['name'],
            category=pooja_category,
            defaults={
                "description": item['description'],
                "price": Decimal(item['price']),
                "stock_quantity": 999 
            }
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")

if __name__ == '__main__':
    populate_south_indian_poojas()
