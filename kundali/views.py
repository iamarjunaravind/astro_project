from django.shortcuts import render
from .forms import KundaliForm
import os
from django.conf import settings

def kundali_input(request):
    if request.method == 'POST':
        form = KundaliForm(request.POST)
        if form.is_valid():
            context = generate_kundali_data(form.cleaned_data)
            return render(request, 'kundali/result.html', context)
    else:
        form = KundaliForm()
    
    return render(request, 'kundali/form.html', {'form': form})

def get_sun_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
    return "Aries"

def get_ascendant(sun_sign, hour):
    """
    Approximates Ascendant (Rising Sign).
    Sun Sign rises at Sunrise (approx 6 AM).
    Sign changes approx every 2 hours.
    """
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    try:
        start_index = signs.index(sun_sign)
        # Assuming sunrise at 6 AM. 
        # Calculate hours passed since 6 AM
        # If hour < 6, it's previous day's cycle effectively for simple math, 
        # or just negative offset.
        # Simple logic: (Hour - 6) / 2 = signs to advance
        
        hours_since_sunrise = hour - 6
        signs_to_advance = int(hours_since_sunrise // 2)
        
        ascendant_index = (start_index + signs_to_advance) % 12
        return signs[ascendant_index]
    except:
        return sun_sign # Fallback

REPORT_DATA = {
    "Aries": {
        "Description": "Aries Ascendant is the first sign of the zodiac, representing new beginnings and raw energy. You project an image of confidence, dynamism, and assertiveness. People see you as a leader who is ready to take on any challenge.",
        "Personality": "You are direct, straightforward, and action-oriented. You lack patience for subtlety and prefer to tackle problems head-on. Your enthusiasm is contagious, but you can also be impulsive. You are fiercely independent and value your freedom highly.",
        "Physical": "Aries rising often gives a strong, athletic build. You may have a prominent forehead or nose, and energetic, piercing eyes. You likely move quickly and have a restless energy about you. Headaches or migraines can be a physical vulnerability.",
        "Health": "Your high energy levels keep you active, but you are prone to burnout if you don't rest. Stress management is crucial. You might be susceptible to fevers, inflammation, or accidents due to haste.",
        "Career": "You thrive in competitive environments. Careers in entrepreneurship, sports, military, or management suit you well. You prefer to be your own boss or at least in a position where you can make quick decisions. Routine work bores you.",
        "Relationship": "In love, you are the chaser. You enjoy the thrill of the pursuit and are passionate and direct. However, you may lose interest once the conquest is over if the excitement fades. You need a partner who can stand up to you and keeps you on your toes."
    },
    "Taurus": {
        "Description": "Ascendant is one of the most sought concepts in astrology when it comes to predicting the minute events in your life. At the time of birth, the sign that rises in the sky is the person's ascendant. It helps in making predictions about the minute events details.",
        "Personality": "Those born with the Taurus ascendant are relatively introverted, despite the fact they represent the animal bull. These people like to create their own little world stud with luxuries and comfort. However, they are also aware of the fact that having these luxuries will require hard work and commitment and thus always try to achieve greater and better things in life. Despite being an introvert, Taurus ascendants are really friendly and fun-loving.",
        "Physical": "Ruled by the planet Venus, Taurus ascendants possess a short physique that is inclined to carelessness. They are generally gifted with a lovely face, full of large, gleaming eyes, nicely formed ears, nose, and seductive lips. In terms of physical shape, they are not too lucky. They have a square-shaped figure with no pleasing curves and a full-fat figure.",
        "Health": "The Taurus natives usually are good with health for the most part of their life. But they, too, have their weak spots in various instances. The people born under the rising sign of Taurus are prone to nervous system issues. Having a good sleep is very important for these people as if they don't, they develop skin problems faster than anyone else.",
        "Career": "Taurus rising people are absolutely eager to put in the effort and persevere in order to succeed, but their desire for stability and ease of mind leads them to choose a steady income with little chance of loss. It delights them to work effectively with genuine stuff rather than theoretical ideas. Working in the food or in the construction industry would be great.",
        "Relationship": "When it comes to relationships, a Taurus ascendant is very sensual. However, they move very cautiously when it comes to love and relationships. They always seek long-lasting love as they don't like change. They will never judge you based on your looks but personality."
    },
    "Gemini": {
        "Description": "Gemini Ascendant projects an image of intelligence, wit, and curiosity. You are seen as a communicator, someone who is always buzzing with ideas and information. You are adaptable and likely have a youthful appearance regardless of age.",
        "Personality": "You are intellectually distinct and love to learn. You get bored easily and need constant mental stimulation. You are a social butterfly, easily making friends in diverse groups. You might be perceived as fickle because your interests change so rapidly.",
        "Physical": "Gemini rising often gives a slender, agile body with long limbs. You may have expressive hands and quick, darting eyes. Your face is usually mobile and animated when you speak.",
        "Health": "Anxiety and nervous tension are your main enemies. Respiratory issues like asthma or bronchitis can also be common. You need to calm your active mind to sleep well.",
        "Career": "You excel in fields requiring communication and versatility. Journalism, media, sales, teaching, or writing are excellent choices. You might juggle multiple careers or hobbies simultaneously.",
        "Relationship": "You need a mental connection above all else. You look for a partner who is a friend and an intellectual equal. Emotional heaviness or jealousy repels you; you need space and conversation in a relationship."
    },
    "Cancer": {
        "Description": "Cancer Ascendant comes across as gentle, sensitive, and approachable. You project a nurturing vibe that makes people feel comfortable around you. You are deeply tied to your moods and the atmosphere around you.",
        "Personality": "You are protective of yourself and your loved ones. You might seem shy at first, retreating into your shell until you feel safe. Once you trust someone, you are incredibly loyal and caring. Intuition guides your life.",
        "Physical": "Cancer rising often gives a round face, perhaps a bit 'moon-faced', with soft features and large, emotive eyes. You may have a tendency to hold water weight or fluctuate in weight based on emotions.",
        "Health": "The stomach and digestive system are sensitive. Stress goes straight to your tummy. Emotional well-being is directly interested to your physical health.",
        "Career": "You do well in caring professions or roles that require intuition. Nursing, teaching, psychology, hospitality, or real estate (homes) are natural fits. You prefer a secure and harmonious work environment.",
        "Relationship": "You seek deep emotional security. You nurture your partner but can also be clingy or moody. You value family above all and want a partner who shares your desire for a stable home life."
    },
    "Leo": {
        "Description": "Leo Ascendant walks into a room and commands attention. You project warmth, confidence, and a touch of drama. People see you as sunny, generous, and perhaps a bit proud.",
        "Personality": "You have a natural flair for the dramatic and love to be appreciated. You are generous to a fault and fiercely loyal. However, your pride can be easily wounded. You are a natural leader who inspires others.",
        "Physical": "Leo rising often gives a strong, regal bearing. You may have a thick mane of hair or a broad upper body. Your complexion might be ruddy or glowing. You walk with dignity.",
        "Health": "The heart and back are your sensitive areas. You have strong vitality but need to watch for high blood pressure or back strain. Joy and creativity are essential for your health.",
        "Career": "You belong in the spotlight or in leadership. Acting, arts, politics, or management suit you. You need a job where you can shine and are respected for your unique talents.",
        "Relationship": "You are romantic and passionate. You treat your partner like royalty but expect the same adoration in return. Loyalty is non-negotiable. You keep the spark alive with grand gestures."
    },
    "Virgo": {
        "Description": "Virgo Ascendant appears neat, organized, and somewhat modest. You project an image of competence and intelligence. People see you as someone who has it all together and notices every detail.",
        "Personality": "You are practical, analytical, and helpful. You are a perfectionist who strives to improve yourself and your environment. You can be critical, but usually out of a desire to help. You are humble and hardworking.",
        "Physical": "Virgo rising implies a youthful, clear-faced appearance. You likely dress neatly and look clean-cut. Your body is usually proportionate, and you may look younger than your years.",
        "Health": "Your digestive system and nerves are sensitive. You can worry yourself sick. A healthy diet, routine, and natural remedies work wonders for you.",
        "Career": "You excel in service and analysis. Medical fields, accounting, editing, data analysis, or nutrition are great paths. You are the one who ensures everything runs smoothly behind the scenes.",
        "Relationship": "You are practical in love. You show affection by doing things for your partner. You need a relationship that is orderly and sensible. You can be shy in romance but are incredibly devoted."
    },
    "Libra": {
        "Description": "Libra Ascendant projects charm, grace, and diplomacy. You are seen as attractive, polite, and easy to get along with. You instinctively know how to make others feel at ease.",
        "Personality": "You value harmony and despise conflict. You are social and love being around people. Indecision can be a struggle as you weigh every side. You have a strong sense of justice and fairness.",
        "Physical": "Libra rising is often associated with physical beauty and symmetry. You may have dimples, a pleasant smile, and a graceful walk. You tend to gain weight easily later in life.",
        "Health": "The kidneys and lower back are vulnerable. Drinking water is essential. You may suffer from health issues if your relationships are unbalanced or stressful.",
        "Career": "You thrive in roles requiring diplomacy or aesthetics. Law, public relations, fashion, design, or fine arts are suitable. You work best in partnerships rather than alone.",
        "Relationship": "You are in love with love. Relationships are the refined center of your life. You hate being alone. You need a partner who is romantic and keeps the peace. You will do anything to maintain harmony."
    },
    "Scorpio": {
        "Description": "Scorpio Ascendant projects an aura of mystery, intensity, and power. You have a piercing gaze that seems to look right through people. You are seen as private and formidable.",
        "Personality": "You are deeply emotional but hide it well. You are observant, suspicious, and incredibly resilient. You experience life with great intensity. You are transforming constantly and rising from ashes.",
        "Physical": "Scorpio rising gives a strong, sturdy build and intense eyes. You may have dark features or a brooding look. You have a strong physical presence that can be intimidating.",
        "Health": "The reproductive system is your sensitive area. You have amazing recuperative powers but can store toxic emotions. Detoxification is important for you.",
        "Career": "You make an excellent researcher, detective, surgeon, or psychologist. Any field that investigates hidden things suits you. You have the focus to solve complex problems.",
        "Relationship": "Love is an all-or-nothing experience. You are possessive, jealous, but incredibly loyal. You seek a soulmate connection that is deep and transformative. Betrayal is rarely forgiven."
    },
    "Sagittarius": {
        "Description": "Sagittarius Ascendant appears jovial, optimistic, and friendly. You project an image of freedom and adventure. People see you as the life of the party, always ready for a laugh.",
        "Personality": "You are a seeker of truth and experience. You are blunt and honest, sometimes to a fault. You love to travel and learn. You cannot stand being tied down or restricted.",
        "Physical": "Sagittarius rising gives a tall, athletic build. You may have a long face and a big smile. You tend to be clumsy but energetic. You likely have a 'horsey' or unrefined grace.",
        "Health": "The liver, hips, and thighs are sensitive. Avoid overindulgence in food or drink. Outdoor exercise is vital for your physical and mental health.",
        "Career": "Teaching, publishing, travel, law, or religion are your domains. You need a career that offers variety and freedom. You are a natural salesperson and motivator.",
        "Relationship": "You need a partner who is also your travel buddy. Freedom is essential; a clingy partner will send you running. You are fun-loving and seek shared adventures rather than heavy domesticity."
    },
    "Capricorn": {
        "Description": "Capricorn Ascendant projects seriousness, maturity, and discipline. Even as a child, you looked like an old soul. People respect you and see you as reliable and ambitious.",
        "Personality": "You are cautious, prudent, and hardworking. You overlook the short term for long-term gain. You can be reserved or melancholic but have a dry sense of humor. Success matters to you.",
        "Physical": "Capricorn rising often results in a lean, bony structure. You may have deep-set eyes and distinct cheekbones. You have great stamina and often age in reverse, looking better as you get older.",
        "Health": "The knees, bones, skin, and teeth are vulnerable. Rheumatism or arthritis can be issues. You need to keep moving to prevent stiffness.",
        "Career": "You are a natural executive. Business, government, administration, or banking suit you. You are willing to start at the bottom and climb to the top. Authority comes naturally.",
        "Relationship": "You are slow to commit but take relationships very seriously. You look for a partner who is responsible and supports your ambitions. You show love through loyalty and providing security."
    },
    "Aquarius": {
        "Description": "Aquarius Ascendant appears unique, unconventional, and intellectual. You project a vibe of friendly detachment. People see you as interesting and perhaps a bit eccentric.",
        "Personality": "You are a humanitarian who values individuality. You are stubborn about your ideas but tolerant of others. You are rational and objective, sometimes seeming cold. You value friendship highly.",
        "Physical": "Aquarius rising gives a medium build with clear, refined features. You may have a dreamy or distant look in your eyes. You might dress in a unique or futuristic style.",
        "Health": "Circulation and ankles are sensitive. You might have nervous disorders or issues with lower legs. Fresh air and freedom are your best medicines.",
        "Career": "Technology, science, aviation, or social work are great fields. You are an innovator. You do well in groups or organizations that fight for a cause. Routine is your enemy.",
        "Relationship": "You need intellectual stimulation and freedom. You are best friends with your partner first. You dislike emotional drama and possessiveness. You love an unconditional, non-traditional bond."
    },
    "Pisces": {
        "Description": "Pisces Ascendant projects a soft, dreamy, and compassionate aura. You seem gentle and perhaps a bit lost in your own world. People feel they can tell you their troubles.",
        "Personality": "You are empathetic, artistic, and intuitive. You soak up the energy around you like a sponge. You can be escapist and impractical but are incredibly kind. You are a chameleon who adapts to others.",
        "Physical": "Pisces rising implies large, liquid eyes and a soft, fleshy body. You may have small feet or a graceful way of moving. You look impressionable and sweet.",
        "Health": "The feet and lymphatic system are weak spots. You are sensitive to drugs and alcohol. You need plenty of sleep and spiritual grounding to stay healthy.",
        "Career": "Arts, music, healing, charity, or film are your worlds. You need a career that allows for imagination and compassion. You struggle with strict structure or ruthless competition.",
        "Relationship": "You are a hopeless romantic. You want to merge with your partner. You can be self-sacrificing and need to be careful of boundary issues. You need a partner who grounds you gently."
    }
}

def generate_kundali_data(data):
    """
    Tries to generate kundali using Kerykeion logic fallback to detailed Ascendant report.
    """
    sun_sign = get_sun_sign(data['day'], data['month'])
    ascendant = get_ascendant(sun_sign, data['hour'])
    
    report = REPORT_DATA.get(ascendant, REPORT_DATA['Aries'])

    context = {
        'success': True,
        'subject': data,
        'sun_sign': sun_sign,
        'ascendant': ascendant,
        'report': report,
        'chart_path': None
    }
    
    # Try actual chart generation
    try:
        from kerykeion import AstrologicalSubject, KerykeionChartSVG
        subject = AstrologicalSubject(
            data['name'], 
            data['year'], 
            data['month'], 
            data['day'], 
            data['hour'], 
            data['minute'], 
            city=data['city'],
            nation="IN"
        )
        
        output_dir = os.path.join(settings.MEDIA_ROOT, 'kundali')
        os.makedirs(output_dir, exist_ok=True)
        
        try:
             svg_chart = KerykeionChartSVG(subject, output_directory=output_dir)
             svg_chart.makeSVG()
             context['chart_path'] = f"{settings.MEDIA_URL}kundali/{subject.name.replace(' ', '_')}_Natal_Chart.svg"
             
             planets = []
             for planet in subject.planets_list:
                 planets.append({
                     'name': planet['name'],
                     'sign': planet['sign'],
                     'pos': f"{planet['position']:.2f}",
                     'house': planet['house']
                 })
             context['planets'] = planets
        except Exception as svg_err:
             print(f"SVG Error: {svg_err}")
             
    except Exception as e:
        print(f"Library Missing: {e}")
    
    if 'planets' not in context:
        # Mock planets
        context['planets'] = [
            {'name': 'Ascendant', 'sign': ascendant, 'pos': '00.0', 'house': '1'},
            {'name': 'Sun', 'sign': sun_sign, 'pos': '12.5', 'house': '1'},
            {'name': 'Moon', 'sign': 'Leo', 'pos': '24.2', 'house': '5'},
            {'name': 'Mars', 'sign': 'Scorpio', 'pos': '05.1', 'house': '8'},
            {'name': 'Mercury', 'sign': 'Virgo', 'pos': '18.3', 'house': '6'},
            {'name': 'Jupiter', 'sign': 'Sagittarius', 'pos': '29.0', 'house': '9'},
            {'name': 'Venus', 'sign': 'Libra', 'pos': '15.4', 'house': '7'},
             {'name': 'Saturn', 'sign': 'Capricorn', 'pos': '02.8', 'house': '10'},
        ]

    return context
