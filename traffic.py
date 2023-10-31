import requests
import feedparser

def get_traffic_data():
    # Fetch traffic data from the specified sources
    bristol_post_traffic_url = "https://www.bristolpost.co.uk/all-about/traffic-travel?service=rss"
    highways_england_traffic_url = "http://m.highwaysengland.co.uk/feeds/rss/AllEvents/South%20West.xml"

    try:
        bristol_post_traffic_feed = feedparser.parse(bristol_post_traffic_url)
        highways_england_traffic_feed = feedparser.parse(highways_england_traffic_url)

        bristol_post_traffic = bristol_post_traffic_feed.entries[0].summary
        highways_england_traffic = highways_england_traffic_feed.entries[0].summary

        return f"Bristol Post Traffic: {bristol_post_traffic}\nHighways England Traffic: {highways_england_traffic}"
    except Exception as e:
        return f"Failed to fetch traffic data: {str(e)}"
