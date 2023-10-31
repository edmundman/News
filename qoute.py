
def get_inspirational_quote(person):
    # Replace this with your quote fetching logic
    quotes = {
        "Albert Einstein": "Imagination is more important than knowledge.",
        "Mahatma Gandhi": "Be the change that you wish to see in the world.",
        "Maya Angelou": "We may encounter many defeats, but we must not be defeated.",
        "Nelson Mandela": "It always seems impossible until it's done.",
        "Oprah Winfrey": "The biggest adventure you can take is to live the life of your dreams."
    }
    return quotes.get(person, "No quote found for this person.")