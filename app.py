# ------------------------------------------------------------
# Stylish Sentiment Analysis Web App (Validated Input Version)
# ------------------------------------------------------------
# Now Accepts:
# ✔ Only alphabets and spaces
# Blocks:
# ✖ Numbers
# ✖ Special characters
# ------------------------------------------------------------

from flask import Flask, request, render_template_string
from textblob import TextBlob
import re  # For input validation

app = Flask(__name__)

# ------------------------------------------------------------
# INPUT VALIDATION FUNCTION
# ------------------------------------------------------------

def is_valid_text(text):
    """
    Allows ONLY letters and spaces.
    Rejects numbers and special characters.
    """
    pattern = r'^[A-Za-z\s]+$'
    return re.match(pattern, text) is not None


# ------------------------------------------------------------
# Function to analyze sentiment
# ------------------------------------------------------------

def analyze_text(user_text):

    # Detect if input is a comma-separated word list
    is_word_list = "," in user_text

    if is_word_list:
        words = [w.strip() for w in user_text.split(",")]

        total_polarity = 0
        for word in words:
            blob_word = TextBlob(word)
            total_polarity += blob_word.sentiment.polarity

        polarity = total_polarity / len(words)
        positive_count = 0
        negative_count = 0

    else:
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity

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

    # Decide sentiment
    if polarity > 0.3:
        sentiment = "Positive"
        color = "#28a745"

    elif polarity < -0.3:
        sentiment = "Negative"
        color = "#dc3545"

    else:
        sentiment = "Balanced"
        color = "#ffc107"

    if not is_word_list and positive_count > 0 and negative_count > 0:
        sentiment = "Mixed"
        color = "#fd7e14"

    # Intensity
    strength = abs(polarity)

    if strength < 0.2:
        intensity = "Weak"
    elif strength < 0.5:
        intensity = "Moderate"
    else:
        intensity = "Strong"

    sentiment_display = f"{intensity} {sentiment}"

    # Convert to 1–10 scale
    score_1_10 = round((polarity + 1) * 4.5 + 1, 2)
    meter_value = (score_1_10 / 10) * 100

    return sentiment_display, score_1_10, color, meter_value


# ------------------------------------------------------------
# UI TEMPLATE
# ------------------------------------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AI Sentiment Analyzer</title>
<style>
body {
margin:0;
font-family:'Segoe UI',sans-serif;
background:linear-gradient(135deg,#0f172a,#1e293b);
height:100vh;
display:flex;
justify-content:center;
align-items:center;
color:white;
}

.card {
background:rgba(255,255,255,0.05);
backdrop-filter:blur(18px);
padding:40px;
width:480px;
border-radius:20px;
box-shadow:0 25px 60px rgba(0,0,0,0.6);
}

textarea {
width:100%;
height:110px;
border-radius:12px;
border:none;
padding:15px;
font-size:15px;
}

button {
margin-top:20px;
width:100%;
padding:12px;
border:none;
border-radius:10px;
background:linear-gradient(90deg,#6366f1,#8b5cf6);
color:white;
font-size:16px;
cursor:pointer;
}

.error {
margin-top:15px;
background:#ffe6e6;
color:#b00020;
padding:10px;
border-radius:8px;
font-size:14px;
}

.result {
margin-top:25px;
padding:20px;
border-radius:15px;
background:rgba(255,255,255,0.06);
}

.meter {
height:12px;
background:rgba(255,255,255,0.1);
border-radius:10px;
overflow:hidden;
margin:15px 0;
}

.meter-fill {
height:100%;
}
</style>
</head>
<body>

<div class="card">
<h2>AI Sentiment Analyzer</h2>

<form method="POST">
<textarea name="sentence" placeholder="Enter text (letters only)..." required></textarea>
<button type="submit">Analyze</button>
</form>

{% if error %}
<div class="error">{{error}}</div>
{% endif %}

{% if sentiment %}
<div class="result">
<strong style="color:{{color}}">{{sentiment}}</strong>

<div class="meter">
<div class="meter-fill" style="width:{{meter_value}}%;background:{{color}}"></div>
</div>

Score: {{score}} / 10
</div>
{% endif %}

</div>
</body>
</html>
"""


# ------------------------------------------------------------
# ROUTE
# ------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = score = color = meter_value = None
    error = None

    if request.method == "POST":
        sentence = request.form["sentence"].strip()

        # Validate input BEFORE analysis
        if not is_valid_text(sentence):
            error = "Only alphabets and spaces allowed. Numbers & special characters are blocked."
        else:
            sentiment, score, color, meter_value = analyze_text(sentence)

    return render_template_string(
        HTML_PAGE,
        sentiment=sentiment,
        score=score,
        color=color,
        meter_value=meter_value,
        error=error
    )


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
