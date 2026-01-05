from django.shortcuts import render
import requests
from datetime import datetime

def horoscope_list(request, period='daily', day='today'):
    zodiac_signs = [
        ('aries', 'Aries', 'March 21 - April 19'),
        ('taurus', 'Taurus', 'April 20 - May 20'),
        ('gemini', 'Gemini', 'May 21 - June 20'),
        ('cancer', 'Cancer', 'June 21 - July 22'),
        ('leo', 'Leo', 'July 23 - August 22'),
        ('virgo', 'Virgo', 'August 23 - September 22'),
        ('libra', 'Libra', 'September 23 - October 22'),
        ('scorpio', 'Scorpio', 'October 23 - November 21'),
        ('sagittarius', 'Sagittarius', 'November 22 - December 21'),
        ('capricorn', 'Capricorn', 'December 22 - January 19'),
        ('aquarius', 'Aquarius', 'January 20 - February 18'),
        ('pisces', 'Pisces', 'February 19 - March 20'),
    ]
    
    # Capitalize period/day for display
    display_period = period.capitalize()
    if period == 'daily':
        display_period = day.capitalize()
        
    context = {
        'zodiac_signs': zodiac_signs,
        'period': period,
        'day': day,
        'display_period': display_period
    }
    return render(request, 'horoscope/index.html', context)

def horoscope_detail(request, sign, period='daily', day='today'):
    # Handle Yearly which is not supported by API yet
    if period == 'yearly':
        return render(request, 'horoscope/detail.html', {
            'sign': sign.capitalize(),
            'description': "Yearly predictions coming soon! Stay tuned.",
            'date': f"Year {datetime.now().year}",
            'period': period,
            'day': day
        })

    # Construct API URL
    base_url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope"
    if period == 'daily':
        url = f"{base_url}/daily?sign={sign}&day={day}"
    else:
        url = f"{base_url}/{period}?sign={sign}"

    try:
        response = requests.get(url)
        data = response.json().get('data', {})
        
        # API returns different structure sometimes, handle safely
        if period == 'daily':
             description = data.get('horoscope_data', "Predictions not available right now.")
             date = data.get('date', datetime.now().strftime("%b %d, %Y"))
        else:
             description = data.get('horoscope_data', "Predictions not available right now.")
             # Weekly/Monthly might have extended info
             if not description and 'horoscope_data' in data:
                 description = data['horoscope_data']
             
             # Fallback date
             date = data.get('date', datetime.now().strftime("%B %Y"))

    except Exception:
        description = "Unable to fetch horoscope at this moment. Please try again later."
        date = datetime.now().strftime("%b %d, %Y")

    return render(request, 'horoscope/detail.html', {
        'sign': sign.capitalize(), 
        'description': description, 
        'date': date,
        'period': period,
        'day': day
    })
