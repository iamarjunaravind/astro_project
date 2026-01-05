from django.core.management.base import BaseCommand
from blog.models import Post
from accounts.models import User
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Populate initial blog posts'

    def handle(self, *args, **options):
        self.stdout.write('Populating blog posts...')
        
        # Ensure a user exists
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username='admin', email='admin@example.com', password='password')

        posts = [
            {
                'title': 'The Impact of Retrograde Mercury',
                'content': 'Mercury retrograde is an optical illusion which means looking back from Earth, the planet appears to go backwards in its orbit. In astrology, this period is often associated with communication mishaps, technology failures, and travel delays. However, it is also a powerful time for reflection, reviewing past decisions, and reconnecting with old friends.'
            },
            {
                'title': 'Understanding Your Moon Sign',
                'content': 'While your Sun sign dictates your personality, your Moon sign represents your emotional inner world. It governs your instincts, subconscious reactions, and what you need to feel secure. Knowing your Moon sign can explain why you might feel different on the inside than you appear to the outside world.'
            },
            {
                'title': 'Vedic vs. Western Astrology',
                'content': 'Vedic astrology (Jyotish) and Western astrology share common roots but diverge significantly in their calculation methods. Vedic astrology uses the Sidereal zodiac, which accounts for the precession of equinoxes, while Western astrology uses the Tropical zodiac, fixed to the seasons. This means your sign might shift back by one in the Vedic system!'
            },
            {
                'title': 'Gemstones for Prosperity',
                'content': 'For centuries, gemstones have been used to balance planetary energies. Yellow Sapphire is often worn for Jupiter to attract wealth and wisdom. Emerald acts for Mercury, enhancing business acumen and communication. Always consult a qualified astrologer before wearing a gemstone, as an unsuitable stone can have adverse effects.'
            },
             {
                'title': 'The Power of Mantras',
                'content': 'Mantras are sacred sounds or vibrations that, when chanted with devotion, can alter the frequency of your mind and environment. In Vedic astrology, specific planetary mantras are often prescribed as remedial measures to appease malefic planets and strengthen benefic ones.'
            }
        ]

        for post_data in posts:
            Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': user,
                    'content': post_data['content'],
                    'slug': slugify(post_data['title'])
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated blog posts'))
