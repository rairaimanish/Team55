from flask import Flask, render_template, request, jsonify
import vertexai
from cathayapi import get_passenger_detail
from vertexai.preview.language_models import TextGenerationModel, ChatModel, InputOutputTextPair

import os


app = Flask(__name__)
app.static_url_path = '/static'
PROJECT_ID = os.environ.get('GCP_PROJECT') # Your Google Cloud Project ID
LOCATION = os.environ.get('GCP_REGION')   # Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)

chat_model = None  # Global variable to store the chat model and conversation
pid = "510892B000014EBB"

def create_session():
    global chat_model
    global attribute_model
    global itinerary_model
    chat_model = ChatModel.from_pretrained("chat-bison@001")

    with open('tuning_data\context\chat_context.txt', 'r') as file:
        chat_context = file.read()
    with open('tuning_data\context\\attributes_context.txt', 'r') as file:
        attributes_context = file.read()
    with open('tuning_data\context\itinerary_context.txt', 'r') as file:
        itinerary_context = file.read()

    if(pid != ""):
        chat_model = chat_model.start_chat(
            context= chat_context+ get_passenger_detail(pid),
            examples=[
                InputOutputTextPair(
                    input_text='Recommend a travel destination for a budget-conscious female solo traveler interested in history and culture.',
                    output_text='Explore the ancient ruins of Rome, Italy, and immerse yourself in its rich history.',
                ),
            ]
        )
    else:
        chat_model = chat_model.start_chat(
            context= chat_context+ get_passenger_detail(pid),
            examples=[
                InputOutputTextPair(
                    input_text='Recommend a travel destination for a budget-conscious female solo traveler interested in history and culture.',
                    output_text='Explore the ancient ruins of Rome, Italy, and immerse yourself in its rich history.',
                ),
            ]
        )
        # prompt_response = model.predict("prompt",**parameters)
    attribute_model = ChatModel.from_pretrained("chat-bison@001")  # Load the tuned AI model
    attribute_model = attribute_model.start_chat(
        context= attributes_context,
        examples=[
            InputOutputTextPair(
                input_text='What are the persons interests?. The given text: Recommend a travel destination for a budget-conscious female solo traveler interested in history and culture. Explore the ancient ruins of Rome, Italy, and immerse yourself in its rich history.',
                output_text='Rome, solo, female, italy, history, culture, ancient, budget-friendly',
            ),
        ]
    )
    itinerary_model = ChatModel.from_pretrained("chat-bison@001")  # Load the tuned AI model
    itinerary_model = itinerary_model.start_chat(
        context= itinerary_context,
        examples=[
            InputOutputTextPair(
                input_text = '''Istanbul, historical landmarks, adventures, museums, art galleries, cuisine, Bosphorus cruise, hamams, shopping, ceremony, street-art, music, dance, Palace''',
                output_text='''
                Day 1:
                - 8:00 am: Wake up and get ready for the day.
                - 9:00 am: Start your day with a hearty breakfast at a local café near your accommodation.
                - 10:00 am: Visit Topkapi Palace to explore its historical landmarks and admire the stunning architecture.
                - 1:00 pm: Enjoy a leisurely lunch at a nearby restaurant, savoring local Turkish cuisine.
                - 2:00 pm: Continue your exploration by visiting the Hagia Sophia, Blue Mosque, and Basilica Cistern.
                - 5:00 pm: Take a break and have a cup of Turkish tea or coffee at a cozy café.
                - 7:00 pm: Head to a popular rooftop restaurant with panoramic views of the city for dinner and enjoy a delicious meal.
                - 9:00 pm: Return to your accommodation and rest for the night.

                Day 2:

                - 8:00 am: Wake up and have breakfast at a nearby café.
                - 9:00 am: Explore the vibrant street art scene in neighborhoods such as Kadikoy and Karakoy.
                - 12:00 pm: Stop for lunch at a local eatery and try some street food specialties.
                - 2:00 pm: Visit the Istanbul Archaeology Museums and the Istanbul Modern Art Museum to immerse yourself in art and culture.
                - 5:00 pm: After a day of exploration, relax and rejuvenate at a traditional Turkish hammam.
                - 7:00 pm: Enjoy dinner at a charming restaurant offering authentic Turkish cuisine.
                - 9:00 pm: Return to your accommodation and rest for the night.

                Day 3:

                - 8:00 am: Wake up and have breakfast at a local café.
                - 9:00 am: Embark on a Bosphorus cruise to enjoy the scenic views of Istanbul.
                - 12:00 pm: Indulge in a leisurely lunch on board the cruise, savoring delicious Turkish dishes.
                - 3:00 pm: Continue your exploration with a visit to the Grand Bazaar and enjoy shopping for unique souvenirs.
                - 6:00 pm: Take a break and enjoy a cup of Turkish tea or coffee at a traditional tea house.
                - 8:00 pm: Experience the Whirling Dervishes ceremony and witness the mesmerizing Sufi dance performance.
                - 9:00 pm: Head to a nearby restaurant for dinner, trying out local delicacies.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 4:

                - 8:00 am: Wake up and have breakfast at a nearby café.
                - 9:00 am: Take a day trip to the Princes' Islands and explore the serene atmosphere and charming horse-drawn carriages.
                - 1:00 pm: Enjoy a leisurely lunch at a waterfront restaurant on one of the islands, savoring fresh seafood.
                - 3:00 pm: Return to Istanbul and attend a Turkish music and dance performance to immerse yourself in the cultural heritage.
                - 6:00 pm: Head to a rooftop restaurant with scenic views for a farewell dinner, enjoying a mix of traditional and modern Turkish cuisine.
                - 9:00 pm: Return to your accommodation and rest for the night.''',),
            InputOutputTextPair(
                input_text='''Paris, art, museums, architecture, fashion, gourmet cuisine, shopping, historical landmarks, photography''',
                output_text= '''

                Day 1:

                - 8:00 am: Wake up and get ready for the day.
                - 9:00 am: Start your day with a croissant and coffee at a local Parisian café.
                - 10:00 am: Visit the Louvre Museum and immerse yourself in world-renowned art masterpieces.
                - 1:00 pm: Enjoy a leisurely lunch at a traditional French bistro, savoring classic dishes.
                - 3:00 pm: Explore the charming neighborhood of Montmartre and capture photographs of the Sacré-Cœur Basilica.
                - 5:00 pm: Indulge in some shopping at the fashionable boutiques along the Champs-Élysées.
                - 7:00 pm: Experience a gourmet dinner at a Michelin-starred restaurant, savoring exquisite French cuisine.
                - 9:00 pm: Take a romantic evening stroll along the Seine River and capture the illuminated cityscape.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 2:

                - 8:00 am: Wake up and have breakfast at a local patisserie.
                - 9:00 am: Visit the Musée d'Orsay and admire its impressive collection of Impressionist and Post-Impressionist art.
                - 11:00 am: Explore the iconic Eiffel Tower and capture panoramic views of the city from the top.
                - 1:00 pm: Enjoy a picnic lunch at the Luxembourg Gardens, surrounded by picturesque landscapes.
                - 3:00 pm: Take a stroll along the elegant streets of Le Marais and explore its unique boutiques and art galleries.
                - 5:00 pm: Visit the Centre Pompidou and discover modern and contemporary art.
                - 7:00 pm: Dine at a charming French brasserie, trying out traditional dishes paired with fine wine.
                - 9:00 pm: Attend a live music performance or a cabaret show for a lively evening entertainment experience.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 3:

                - 8:00 am: Wake up and have breakfast at a local café.
                - 9:00 am: Visit the Palace of Versailles and explore its opulent gardens and grand interiors.
                - 12:00 pm: Enjoy a luxurious lunch at a Michelin-starred restaurant near the palace.
                - 2:00 pm: Take a boat cruise along the River Seine and capture photos of iconic landmarks.
                - 4:00 pm: Explore the trendy neighborhood of Le Marais and indulge in some shopping at its unique boutiques.
                - 6:00 pm: Visit the Musée de l'Orangerie and marvel at Claude Monet's famous Water Lilies paintings.
                - 8:00 pm: Experience a traditional French wine and cheese tasting at a local cellar.
                - 10:00 pm: Enjoy a farewell dinner at a romantic restaurant, savoring gourmet French cuisine.
                - 12:00 am: Return to your accommodation and rest for the night.’

                input_text=’Tokyo, technology, anime, manga, traditional culture, temples, gardens, street food, shopping, photography’

                output_text=’

                Day 1:

                - 8:00 am: Wake up and get ready for the day.
                - 9:00 am: Start your day with a hearty Japanese breakfast at a local café.
                - 10:00 am: Visit the bustling neighborhood of Akihabara and explore its electronic stores and anime merchandise shops.
                - 12:00 pm: Enjoy a lunch of delicious street food from one of the many food stalls in Harajuku.
                - 2:00 pm: Immerse yourself in Japanese traditional culture by visiting the Meiji Shrine and taking part in a traditional tea ceremony.
                - 4:00 pm: Explore the beautiful gardens of the Rikugien or Shinjuku Gyoen National Garden and capture photos of serene landscapes.
                - 6:00 pm: Experience the vibrant nightlife of Shinjuku and visit a themed café or bar.
                - 8:00 pm: Indulge in a dinner of authentic Japanese cuisine, such as sushi or ramen, at a local restaurant.
                - 10:00 pm: Return to your accommodation and rest for the night.

                Day 2:

                - 8:00 am: Wake up and have breakfast at a nearby café.
                - 9:00 am: Visit the historic district of Asakusa and explore Senso-ji, Tokyo's oldest Buddhist temple.
                - 11:00 am: Take a boat cruise along the Sumida River and capture scenic views of Tokyo's skyline.
                - 1:00 pm: Enjoy a traditional lunch ata local restaurant, trying out dishes like tempura or tonkatsu.
                - 3:00 pm: Discover the modern side of Tokyo by visiting the teamLab Borderless digital art museum in Odaiba.
                - 5:00 pm: Explore the Odaiba waterfront area and capture photos of iconic landmarks like the Rainbow Bridge.
                - 7:00 pm: Dine at a traditional izakaya (Japanese pub) and experience the lively atmosphere and delicious small plates.
                - 9:00 pm: Visit a karaoke bar and enjoy singing your favorite anime theme songs.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 3:

                - 8:00 am: Wake up and have breakfast at a local café.
                - 9:00 am: Explore the trendy neighborhood of Shibuya and capture photos of the famous Shibuya Crossing.
                - 11:00 am: Visit the Ghibli Museum to immerse yourself in the world of Studio Ghibli's iconic anime films.
                - 1:00 pm: Enjoy a lunch of delicious sushi or sashimi at a traditional sushi restaurant.
                - 3:00 pm: Discover the serene atmosphere of the Hamarikyu Gardens and participate in a traditional tea ceremony.
                - 5:00 pm: Explore the shopping district of Ginza and indulge in some retail therapy at luxury boutiques.
                - 7:00 pm: Dine at a traditional kaiseki restaurant and savor a multi-course meal of seasonal Japanese delicacies.
                - 9:00 pm: Experience the vibrant nightlife of Roppongi and visit a lively bar or club.
                - 11:00 pm: Return to your accommodation and rest for the night.''',),
            InputOutputTextPair(
                input_text='''Rome, ancient history, architecture, art, Vatican City, Roman ruins, gelato, pasta, piazzas, photography''',
                output_text='''
                Day 1:

                - 8:00 am: Wake up and get ready for the day.
                - 9:00 am: Start your day with a cappuccino and cornetto at a local café.
                - 10:00 am: Visit the Colosseum and explore the iconic Roman amphitheater.
                - 12:00 pm: Enjoy a traditional Roman lunch at a trattoria, trying dishes like carbonara or cacio e pepe.
                - 2:00 pm: Explore the Roman Forum and Palatine Hill, capturing photos of ancient ruins and panoramic views of the city.
                - 4:00 pm: Visit the Pantheon and admire its impressive architecture and magnificent dome.
                - 6:00 pm: Take a leisurely stroll through the charming streets of Trastevere and capture the vibrant atmosphere.
                - 8:00 pm: Indulge in a dinner of traditional Roman cuisine at a local osteria, paired with a glass of local wine.
                - 10:00 pm: Enjoy a gelato from a renowned gelateria and savor the flavors while exploring the city at night.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 2:

                - 8:00 am: Wake up and have breakfast at a nearby café.
                - 9:00 am: Visit the Vatican City and explore St. Peter's Basilica and the Vatican Museums.
                - 12:00 pm: Enjoy a lunch of authentic Italian pizza at a local pizzeria.
                - 2:00 pm: Marvel at the Sistine Chapel and admire Michelangelo's famous ceiling frescoes.
                - 4:00 pm: Explore the picturesque Piazza Navona and capture photos of its beautiful fountains and Baroque architecture.
                - 6:00 pm: Visit the Trevi Fountain and toss a coin for good luck.
                - 8:00 pm: Dine at a rooftop restaurant with a view of the city, enjoying a romantic dinner.
                - 10:00 pm: Take a nighttime walking tour of Rome and capture the city's illuminated landmarks.
                - 11:00 pm: Return to your accommodation and rest for the night.

                Day 3:

                - 8:00 am: Wake up and have breakfast at a local café.
                - 9:00 am: Visit the Borghese Gallery and admire its impressive collection of Renaissance and Baroque art.
                - 11:00 am: Explore the charming neighborhood of Trastevere and capture photos of its colorful streets and hidden gems.
                - 1:00 pm: Enjoy a leisurely lunch at a traditional Roman trattoria, trying dishes like amatriciana or saltimbocca.
                - 3:00 pm: Take a stroll through the Villa Borghese Gardens and rent a rowboat on the lake for a relaxing experience.
                - 5:00 pm: Visit the Spanish Steps and capture photos of the iconic staircase and the surrounding area.
                - 7:00 pm: Indulge in aperitivo, enjoying drinks and small bites at a local wine bar.''',
                            ),]
                )
    return

def get_model_response(message):
    global chat_model
    parameters = {
        "temperature": 0.3,
        "max_output_tokens": 1024,
        "top_p": 0.90,
        "top_k": 40
    }

    response = chat_model.send_message(message, **parameters)
    return response.text

def get_attribute_response(message):
    global attribute_model
    parameters = {
            "temperature": 0.2,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40
        }
    prompt_response = attribute_model.send_message(message,**parameters)
    return prompt_response.text

def get_itinerary(message):
    global itinerary_model
    parameters = {
            "temperature": 0.2,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40
        }
    itinerary_response = itinerary_model.send_message(message,**parameters)
    return itinerary_response.text

@app.route('/')
def index():
    return render_template('index-original.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']

    if not chat_model:
        create_session()

    content = get_model_response(user_input)
    cords = get_model_response("what is the google map api coordinate of the destination/location in our last conversation")
    attributes_content = get_attribute_response(str("What are the person's interests? Also, return what language the given text is in. The given text:"+ user_input + " " + content))
    generated_itinerary = get_itinerary(attributes_content)

    print(attributes_content)

    return jsonify(content=content, cords= cords, attributes_content = attributes_content, generated_itinerary = generated_itinerary)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')