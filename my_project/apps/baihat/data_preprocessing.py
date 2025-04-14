import re
import nltk
from nltk.corpus import stopwords

# Tải các từ dừng (stopwords) tiếng Anh
nltk.download('stopwords')

# Hàm tiền xử lý văn bản tiếng Anh
def preprocess_text(text):
    # Chuyển thành chữ thường
    text = text.lower()

    # Loại bỏ ký tự đặc biệt nhưng GIỮ tiếng Việt (Unicode)
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)

    # Danh sách từ dừng tiếng Anh
    stop_words = set(stopwords.words('english'))

    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)
