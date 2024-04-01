from flask import Flask, request, render_template
from pytube import YouTube
import google.generativeai as genai

app = Flask(__name__)

# Configure GenerativeAI with the gemini-pro model for sentiment analysis
genai.configure(api_key="AIzaSyCZqeMqO_p6aCYzp8AoSpxDtz-Q_1-fEqs")
model = genai.GenerativeModel(model_name="gemini-pro")

# Function to detect clickbait
def detect_clickbait(video_title, video_description):
    # Concatenate title and description for analysis
    if video_description:
        text_for_analysis = f"{video_title}\n{video_description}"
    else:
        text_for_analysis = video_title

    # Sentiment analysis prompt
    prompt = f"Analyze the following text: {text_for_analysis}\n  - Is the title or description likely clickbait reply with yes or no? Why or why not? Reason:"

    # Perform analysis using the configured model
    response = model.generate_content(prompt)
    
    # Check if response is valid
    if response and response.text:
        result = response.text.strip().lower()
        reason = response.text.strip().split("Reason:")[-1].strip()
        if "yes" in result:
            return "Clickbait Detected", reason
        else:
            return "Not Clickbait", reason
    else:
        return "Unable to analyze the video.", ""

# Function to fetch thumbnail URL from YouTube
def get_thumbnail_url(url):
    yt = YouTube(url)
    return yt.thumbnail_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json['url']
    # Fetch video data from YouTube
    yt = YouTube(url)
    video_title = yt.title
    video_description = yt.description
    thumbnail_url = get_thumbnail_url(url)  # Fetch thumbnail URL
    
    # Detect clickbait
    result, reason = detect_clickbait(video_title, video_description)
    
    return {
        'thumbnail_url': thumbnail_url,
        'result': result,
        'reason': reason
    }

if __name__ == '__main__':
    app.run(debug=True)
