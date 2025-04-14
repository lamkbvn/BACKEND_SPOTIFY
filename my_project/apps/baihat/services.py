from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
from ..baihat.data_preprocessing import preprocess_text
from ..baihat.text_tokenization import tokenize_text
from ..baihat.ml_models.bert_emotion_model import BERTEmotionAnalyzer




analyzer = BERTEmotionAnalyzer()

def analyze_song_emotion(lyrics):
    if not lyrics:
        return "unknown"
    try:
        # Tokenize lời bài hát
        tokens = tokenize_text(lyrics)
        
        # Tiền xử lý lời bài hát
        processed_lyrics = preprocess_text(lyrics)
        
        # Phân tích cảm xúc sau khi xử lý
        emotion = analyzer.predict_emotion(' '.join(tokens))
        
        if emotion:
            return emotion
        else:
            raise ValueError("Không thể xác định cảm xúc bằng BERT.")
    except Exception as e:
        print(f"BERT Emotion analysis failed, falling back to VADER: {e}")
        # Fall back to SentimentIntensityAnalyzer if BERT fails
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(lyrics)
        if scores['compound'] >= 0.5:
            return 'vui'
        elif scores['compound'] <= -0.5:
            return 'buon'
        elif scores['pos'] > scores['neg']:
            return 'tinh_yeu'
        else:
            return 'soi_dong'
        


       