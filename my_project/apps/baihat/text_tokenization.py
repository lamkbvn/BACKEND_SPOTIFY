from nltk.tokenize import word_tokenize
import nltk

# Tải các tài nguyên cần thiết cho tokenization
nltk.download('punkt_tab')

# Hàm thực hiện tokenization văn bản
def tokenize_text(text):
    """
    Tiến hành tokenization văn bản: phân tách câu thành các từ.
    """
    # Tokenization văn bản thành danh sách các từ
    tokens = word_tokenize(text)
    return tokens
