import pandas as pd
from pathlib import Path
from model import Tweet


class CSVSave:
    def save(self, tweets: list[Tweet], output_csv: str = "tweets.csv"):
        """Save tweet data to CSV using pandas."""
        if not tweets:
            print("⚠️ No tweets to save.")
            return

        # Convert list of Tweet objects to list of dictionaries
        data = [tweet.to_dict() for tweet in tweets]

        df = pd.DataFrame(data)
        output_path = Path(output_csv)

        # Save to CSV
        df.to_csv(output_path, mode="a", sep="|", index=False, encoding="utf-8")

        print(f"✅ Data saved to: {output_path.resolve()}")
