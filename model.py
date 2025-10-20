class Tweet:
    def __init__(self, user, text, views, likes, datetime):
        self.user = user
        self.text = text
        self.views = views
        self.likes = likes
        self.datetime = datetime

    def __str__(self):
        return (
            f"tweet-user: {self.user}\n"
            f"tweet-text: {self.text}\n"
            f"tweet-views: {self.views}\n"
            f"tweet-likes: {self.likes}\n"
            f"tweet-time: {self.datetime}\n"
        )

    def to_dict(self):
        """Convert Tweet object to dictionary for CSV saving."""
        return {
            "user": self.user,
            "text": self.text,
            "views": self.views,
            "likes": self.likes,
            "datetime": self.datetime,
        }
