# ------------------------------------------------------------
# Stylish Sentiment Analysis Web App (No Emojis — Professional UI)
# ------------------------------------------------------------
# Features:
# ✔ Sentence or word input
# ✔ Positive / Negative / Neutral detection
# ✔ Rating from 1 to 10
# ✔ Visual strength meter (like analytics dashboard)
# ✔ Clean professional interface
# ------------------------------------------------------------

from flask import Flask, request, render_template_string
from textblob import TextBlob

app = Flask(__name__)

# ------------------------------------------------------------
# Function to analyze sentiment
# ------------------------------------------------------------

from textblob import TextBlob

from textblob import TextBlob

def analyze_text(user_text):

    # -----------------------------------
    # Step 1: Detect if input is a word list (comma-separated)
    # -----------------------------------
    is_word_list = "," in user_text

    if is_word_list:
        words = [w.strip() for w in user_text.split(",")]

        total_polarity = 0
        for word in words:
            blob_word = TextBlob(word)
            total_polarity += blob_word.sentiment.polarity

        # Average polarity of all words
        polarity = total_polarity / len(words)

        positive_count = 0
        negative_count = 0

    else:
        # Normal sentence analysis
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity

        # Word-level check (for detecting mixed sentiment)
        words = user_text.split()
        positive_count = 0
        negative_count = 0

        for word in words:
            word_blob = TextBlob(word)
            score = word_blob.sentiment.polarity

            if score > 0:
                positive_count += 1
            elif score < 0:
                negative_count += 1

    # -----------------------------------
    # Step 2: Decide sentiment label
    # -----------------------------------
    if polarity > 0.3:
        sentiment = "Positive"
        color = "#28a745"   # Green

    elif polarity < -0.3:
        sentiment = "Negative"
        color = "#dc3545"   # Red

    else:
        sentiment = "Balanced"
        color = "#ffc107"   # Yellow

    # Detect Mixed Sentiment ONLY for sentences
    if not is_word_list and positive_count > 0 and negative_count > 0:
        sentiment = "Mixed"
        color = "#fd7e14"   # Orange

    # -----------------------------------
    # Step 3: Calculate intensity (confidence)
    # -----------------------------------
    strength = abs(polarity)

    if strength < 0.2:
        intensity = "Weak"
    elif strength < 0.5:
        intensity = "Moderate"
    else:
        intensity = "Strong"

    sentiment_display = f"{intensity} {sentiment}"

    # -----------------------------------
    # Step 4: Convert to 1–10 score
    # -----------------------------------
    score_1_10 = round((polarity + 1) * 4.5 + 1, 2)

    # Meter value for UI bar
    meter_value = (score_1_10 / 10) * 100

    # -----------------------------------
    # Final Return (DO NOT CHANGE — UI needs this)
    # -----------------------------------
    return sentiment_display, score_1_10, color, meter_value




# ------------------------------------------------------------
# Professional Styled UI
# ------------------------------------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Sentiment Analyzer</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(18px);
            padding: 40px;
            width: 480px;
            border-radius: 20px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.08);
        }

        h1 {
            margin-bottom: 10px;
            font-weight: 600;
            letter-spacing: 1px;
            text-align: center;
        }

        p.subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 25px;
        }

        textarea {
            width: 100%;
            height: 110px;
            border-radius: 12px;
            border: none;
            padding: 15px;
            font-size: 15px;
            resize: none;
            outline: none;
        }

        button {
            margin-top: 20px;
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg,#6366f1,#8b5cf6);
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s ease;
        }

        button:hover {
            transform: scale(1.03);
            box-shadow: 0 10px 25px rgba(99,102,241,0.6);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 15px;
            background: rgba(255,255,255,0.06);
        }

        .badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
        }

        .meter {
            height: 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
        }

        .meter-fill {
            height: 100%;
            transition: width 0.6s ease;
        }

        .score {
            color: #cbd5e1;
            font-size: 14px;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>AI Sentiment Analyzer</h1>
    <p class="subtitle">Text Emotion Intelligence Dashboard</p>

    <form method="POST">
        <textarea name="sentence" placeholder="Enter text to analyze sentiment..." required></textarea>
        <button type="submit">Analyze Sentiment</button>
    </form>

    {% if sentiment %}
    <div class="result">
        <div class="badge" style="background: {{color}}20; color: {{color}};">
            {{sentiment}}
        </div>

        <div class="meter">
            <div class="meter-fill" style="width: {{meter_value}}%; background: {{color}};"></div>
        </div>

        <div class="score">Emotion Strength: {{score}} / 10</div>
    </div>
    {% endif %}
    
</div>

</body>
</html>
"""


# ------------------------------------------------------------
# Route Handling
# ------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = score = color = meter_value = None

    if request.method == "POST":
        sentence = request.form["sentence"]
        sentiment, score, color, meter_value = analyze_text(sentence)

    return render_template_string(
        HTML_PAGE,
        sentiment=sentiment,
        score=score,
        color=color,
        meter_value=meter_value
        
    )


# ------------------------------------------------------------
# Run Server
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
