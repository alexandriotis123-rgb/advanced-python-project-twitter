# ----------------------
# Question 1 – MATI Relevant Tweets
# ----------------------

import pandas as pd
import string
from tqdm import tqdm
import spacy
from spacy.lang.el.stop_words import STOP_WORDS
import os

#----------------------------------
# FLAGS
#----------------------------------
RUN_LEMMATIZATION =True
# True: to run Lemmatization
# False: to skip it

DEBUG_SAMPLES = True
#True: to run samples of relevant/irrelevant tweets
#False: to skip this step

SAVE_PREPROCESSED=True
#True if you wish to save the file

#-----------------------------
# PATH
#-----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #script file
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

PREPROCESSED_FILE = os.path.join(DATA_DIR, "mati_preprocessed.csv")

# ----------------------
# PREPROCESS TEXT
# ----------------------
def preprocess_text(text):
    def remove_punctuation_from_words(line):
        words = line.split()
        cleaned_words = [
            word.translate(str.maketrans("", "", string.punctuation))
            for word in words]
        return " ".join(cleaned_words)

    text = text.astype(str).str.lower()
    text = text.str.replace(r"@\w+", "", regex=True)
    text = text.str.replace(r"\brt\b", "", regex=True)
    text = text.str.replace(r"http\S+|www\S+", "", regex=True)
    text = text.str.replace(r"#", "", regex=True)
    text = text.apply(remove_punctuation_from_words)

    # emojis & symbols
    text = text.str.replace(
        r"[\U0001F600-\U0001FAFF\U00002600-\U000027BF]+",
        "",
        regex=True)

    # small tokens
    text = text.str.replace(r"\b\w{1,3}\b", "", regex=True)

    # accent removal (μάτι → ματι)
    text = (
        text.str.normalize("NFD")
        .str.replace(r"[\u0300-\u036f]", "", regex=True))

    text = text.str.replace(r"\s+", " ", regex=True).str.strip()
    return text


# ----------------------
# LEMMATIZATION
# ----------------------
def lemmatize_texts(texts):
    nlp = spacy.load("el_core_news_sm")

    extra_stopwords = {
        "ειναι", "ηταν", "θα", "να", "και",
        "με", "για", "στο", "στη", "του",
        "των", "της"}
    custom_stopwords = STOP_WORDS.union(extra_stopwords)

    cleaned_texts = []

    for doc in tqdm(
        nlp.pipe(texts, batch_size=1000, disable=["parser", "ner", "tagger"]),
        total=len(texts),
        desc="Lemmatization"):
        tokens = [
            token.text
            for token in doc
            if token.is_alpha
            and not token.is_stop
            and token.text not in custom_stopwords
            and len(token.text) >= 4]
        cleaned_texts.append(" ".join(tokens))

    return cleaned_texts


# ----------------------
# MAIN FUNCTION
# ----------------------
def process_mati_data(csv_path):

    os.makedirs(DATA_DIR, exist_ok=True)

    if RUN_LEMMATIZATION or not os.path.exists(PREPROCESSED_FILE):
        print(" Running preprocessing & lemmatization...")

        df = pd.read_csv(
            csv_path,
            header=None,
            names=[
                "author_id", "created_at", "geo", "tweet_id", "lang",
                "like_count", "quote_count", "reply_count",
                "retweet_count", "source", "text"])

        print("Raw dataset size:", df.shape)
        df = df[df["lang"] == "el"].copy()
        print("Greek tweets only:", df.shape)
        df["clean_text"] = preprocess_text(df["text"])
        df["lemmatized_text"] = lemmatize_texts(df["clean_text"])

        df.to_csv(PREPROCESSED_FILE, index=False)
        print(" Preprocessed file saved:", PREPROCESSED_FILE)

    else:
        print(" Loading preprocessed file...")
        df = pd.read_csv(PREPROCESSED_FILE)

    # ----------------------
    # KEYWORD FILTERING
    # ----------------------

    Location_keywords=["ματι","ραφηνα","ραφινα","κινετα","νεο βουτζα","νεα βουτζα"]
    Event_keywords=["φωτια","πυρκαγια","εκκενωση","καταστροφη","τραγωδια","καπνος","φλογα"]
    Casualty_keywords=["νεκρος","νεκροι","θυμα","θυματα","103","104","πνιγμος","καμμενος"]
    Authority_keywords=["λιμενικο","τσιπρας","αστυνομια"]

    def is_relevant_mati_tweet(text):
        if not isinstance(text,str):
            return False

        has_location=any(loc in text for loc in Location_keywords)
        has_event=any(evt in text for evt in Event_keywords)
        has_casualty=any(cas in text for cas in Casualty_keywords)
        has_authority=any(auth in text for auth in Authority_keywords)

        return (has_location and has_event) or (has_location and has_casualty) or(has_location and has_authority)


    df["lemmatized_text"] = df["lemmatized_text"].fillna("")
    df["is_relevant"] = df["lemmatized_text"].apply(is_relevant_mati_tweet)


    # ----------------------
    # PRINTS
    # ----------------------
    relevant_count = df["is_relevant"].sum()
    irrelevant_count = len(df) - relevant_count

    print("\n QUESTION 1 RESULTS")
    print("Σχετικά tweets:", relevant_count)
    print("Μη σχετικά tweets:", irrelevant_count)
    print(f"Ποσοστό σχετικών: {relevant_count / len(df) * 100:.2f}%")
    if DEBUG_SAMPLES:
        print("\n Sample relevant tweets:")
        print(df[df["is_relevant"]].sample(10)[["text"]])
        print("\n Sample irrelevant tweets:")
        print(df[~df["is_relevant"]].sample(10)[["text"]])

    df_relevant = df[df["is_relevant"]].copy()
    print("\n Dataset μετά το filtering:", df_relevant.shape)

    return df_relevant


# ----------------------
# EXECUTION
# ----------------------
if __name__ == "__main__":

    RAW_CSV = r"mati.csv"

    df_relevant = process_mati_data(RAW_CSV)

    output_file = os.path.join(DATA_DIR, "mati_q1_relevant.csv")
    df_relevant.to_csv(output_file, index=False)

    print("\n Q1 completed successfully")
    print(" Saved:", output_file)