import feedparser
from flask import Flask, render_template, request, jsonify, send_file
import openai
from elevenlabs import generate, save, set_api_key
import random
import requests
import yfinance as yf  # Import yfinance for stock data
from stock import get_stock_prices
from  traffic import get_traffic_data  
from  weather import get_weather    
from qoute import get_inspirational_quote
import keys  
import json
app = Flask(__name__)
dialog = ""


# Define Bristol-related RSS feed URLs
bristol_rss_sources = {
    "Bristol Post": "https://www.bristolpost.co.uk/all-about/traffic-travel?service=rss",
    "Highways England": "http://m.highwaysengland.co.uk/feeds/rss/AllEvents/South%20West.xml",
    "BBC Bristol": "https://www.bbc.co.uk/news/england/bristol/rss.xml",
    "The Guardian Bristol": "https://www.theguardian.com/uk/bristol/rss","Bristol Rovers FC": "https://www.bristolpost.co.uk/all-about/bristol-rovers-fc?service=rss",
    "Bristol City FC": "https://www.bristolpost.co.uk/all-about/bristol-city-fc?service=rss",
    "Bristol Bears": "https://www.bristolpost.co.uk/all-about/bristol-bears?service=rss"
}

# Initialize an empty list to store articles
articles = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    selected_sources = request.form.getlist('sources')
    selected_sports_teams = request.form.getlist('sports_teams')
    articles.clear()

    for source in selected_sources:
        rss_url = bristol_rss_sources[source]
        feed = feedparser.parse(rss_url)

        if feed.bozo == 0:
            recent_entries = feed.entries[:2]
            for entry in recent_entries:
                articles.append(entry)
        else:
            return jsonify({"error": f"Failed to parse the RSS feed at {rss_url}"})

    for team in selected_sports_teams:
        rss_url = bristol_rss_sources[team]
        feed = feedparser.parse(rss_url)

        if feed.bozo == 0:
            recent_entries = feed.entries[:2]
            for entry in recent_entries:
                articles.append(entry)
        else:
            return jsonify({"error": f"Failed to parse the RSS feed for {team}"})

    articles_data = []
    for entry in articles:
        articles_data.append({
            "title": entry.title,
            "link": entry.link
        })

    return jsonify({"articles": articles_data})
@app.route('/remove_article/<article_title>', methods=['POST'])
def remove_article(article_title):
    # Find the article with the given title in the articles list
    article_to_remove = next((article for article in articles if article.title == article_title), None)

    if article_to_remove:
        articles.remove(article_to_remove)
        return jsonify({"message": f"Article '{article_title}' removed successfully"})
    else:
        return jsonify({"error": f"Article '{article_title}' not found"})


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    global dialog
    news_input = ""
    
    # Get the list of active articles from the frontend
    active_articles = json.loads(request.form.get('active_articles'))
    
    # Filter the articles based on the list of active articles
    updated_articles = [entry for entry in articles if entry.title in active_articles]

    # Generate the summary using the updated articles
    news_input = ""
    for entry in updated_articles:
        news_input += f"Title: {entry.title}\nText: {entry.summary}\n"

    # Include weather data if the checkbox is selected
    if request.form.get('weather_checkbox') == 'include_weather':
        location = "Bristol"  # You can change this to the desired location
        api_key = "7edd7f6c7c02a7cdebb4dbb1dc0b0d9e"  # Replace with your actual API key
        weather_data = get_weather(api_key, location)
        news_input += weather_data

    # Include traffic data if the checkbox is selected
    if request.form.get('traffic_checkbox') == 'include_traffic':
        traffic_data = get_traffic_data()
        news_input += f"Traffic Data: {traffic_data}\n\n"
    
    # Include sport team if provided
    sport_team = request.form.get('sport_team')
    if sport_team:
        news_input += f"Supported Sport Team: {sport_team}\n\n"

    # Include stock/crypto tickers if provided
    tickers = request.form.get('tickers')
    if tickers:
        stock_prices = get_stock_prices(tickers)
        for ticker, price in stock_prices.items():
            news_input += f"Stock Price ({ticker}): {price}\n\n"

    # Include inspirational quote if selected
    selected_person = request.form.get('inspirational_dropdown')
    if selected_person:
        quote = get_inspirational_quote(selected_person)
        news_input += f"Inspirational Quote from {selected_person}: {quote}\n\n"

    # Include horoscope data if the checkbox is selected
    if request.form.get('horoscope_checkbox') == 'include_horoscope':
        horoscope_data = get_horoscope()
        news_input += f"Horoscope: {horoscope_data}\n\n"

    messages = [
        {"role": "system", "content": "You are Hana, a Bristol newsreader:"},
        {"role": "user", "content": "Give a very short news summary of this information in a news reader style. Be nice and have lots of segways." + news_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=3000  # Adjust the max_tokens as needed for the desired length
    )

    reply = response["choices"][0]["message"]["content"]
    dialog = reply

    return jsonify({"summary": reply})


# Generate a random integer between a specified range (e.g., 1 to 100)
ids = random.randint(1, 1050)
ids = str(ids)


@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    global dialog
    text = dialog
    voice = generate(text=text, voice="Bella")
    save(voice, ids + '.wav')

    return jsonify({"message": "Audio generated successfully!"})

@app.route('/download_audio')
def download_audio():
    return send_file(ids + '.wav', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

