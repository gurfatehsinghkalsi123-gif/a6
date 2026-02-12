import time, pandas as pd
from textblob import TextBlob

try :
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print("error: the file 'imdb_top_1000.csv' was not found")
    raise SystemExit

genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(', ')for g in xs})

def senti(p):
    return 'positive 😎' if p > 0 else 'negative 😔' if p < 0 else 'neutral😑'
def recommend(genre = None,mood = None, rating = None, n=5):
    d = df
    if genre:
        d = d[d['Genre'].str.contains(genre, case = False, na = False)]
    if rating is not None:
        d = d[d["IMDB_Rating"]>= rating]
    if d.empty:
        return 'no movie recomendations found'
    d = d.sample(frac=1).reset_index(drop=True)
    need_nonneg = bool(mood)
    out=[]
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov):
            continue
        pol = TextBlob(ov).sentiment.polarity
        if(not need_nonneg) or pol >=0:
            out.append((r['Series_Title'], pol))
            if len(out) == n:
                break
    return out if out else "no suitable movie recomendations found."
def show(recs, name):
    print(f"\n🍿 AI-Analyzed Movie Recommendations for {name}:")
    for i, (t, p) in enumerate(recs, 1):
        print(f"{i}. 🎥 {t} (Polarity: {p:.2f}, {senti(p)})")

def get_genre():
    print("Available Genres: ")
    for i, g in enumerate(genres, 1):
        print(f"{i}. {g}")
    print()

    while True:
        x = input("Enter genre number or name: ").strip()
        if x.isdigit() and 1 <= int(x) <= len(genres):
            return genres[int(x) - 1]
        x = x.title()
        if x in genres:
            return x
        print("Invalid input. Try again.\n")

def get_rating():
    while True:
        x = input("Enter minimum IMDB rating (7.6-9.3) or 'skip': ").strip()
        if x.lower() == "skip":
            return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3:
                return r
            print("Rating out of range. Try again.\n")
        except ValueError:
            print("Invalid input. Try again.\n")

print("🎥 Welcome to your Personal Movie Recommendation Assistant! 🎥\n")

name = input("What's your name? ").strip()
print(f"\nGreat to meet you, {name}!\n")
print("\n🔍 Let's find the perfect movie for you!\n")

genre = get_genre()
mood = input("How do you feel today? (Describe your mood): ").strip()

print("\nAnalyzing mood", end="", flush=True)


mp = TextBlob(mood).sentiment.polarity
md = "positive 😊" if mp > 0 else "negative 😞" if mp < 0 else "neutral 😐"
print(f"\nYour mood is {md} (Polarity: {mp:.2f}).\n")

rating = get_rating()

print(f"\nFinding movies for {name}", end="", flush=True)


recs = recommend(genre=genre, mood=mood, rating=rating, n=5)

if isinstance(recs, str):
    print(recs + "\n")
else:
    show(recs, name)

while True:
    a = input("\nWould you like more recommendations? (yes/no): ").strip().lower()
    if a == "no":
        print(f"\nEnjoy your movie picks, {name}! 🎬🍿\n")
        break
    elif a == "yes":
        recs = recommend(genre=genre, mood=mood, rating=rating, n=5)
        if isinstance(recs, str):
            print(recs + "\n")
        else:
            show(recs, name)
    else:
        print("Invalid choice. Try again.\n")
