from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class BERTEmotionAnalyzer:
    def __init__(self, model_name='nateraw/bert-base-uncased-emotion'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

    @staticmethod
    def convert_emotion_label(label):
        mapping = {
            'joy': 'vui',
            'sadness': 'buon',
            'anger': 'soi dong',
            'love': 'thu gian',
            'fear': 'buon',
            'surprise': 'soi dong',
        }
        return mapping.get(label, None)

    def predict_emotion(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probs).item()
            raw_emotion = self.labels[predicted_class]
            return self.convert_emotion_label(raw_emotion), raw_emotion, probs[0][predicted_class].item()  # Fixed this line
        except Exception as e:
            print(f"Error using BERT model: {e}")
            return None, None, None


if __name__ == "__main__":
    analyzer = BERTEmotionAnalyzer()

    print("🔍 Paste your song lyrics below (end with Ctrl+D or Ctrl+Z + Enter):\n")
    print("------------------------------------------------------")
    import sys
    lyrics = sys.stdin.read()

    vn_emotion, en_emotion, confidence = analyzer.predict_emotion(lyrics)
    if vn_emotion:
        print("\n🎵 Emotion detected from lyrics:")
        print(f"🔹 English label: {en_emotion}")
        print(f"🔸 Vietnamese label: {vn_emotion}")
        print(f"✅ Confidence: {confidence:.2f}")
    else:
        print("❌ Could not detect emotion.")
