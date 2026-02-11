from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# NLTK data download - Deployment aur local dono ke liye zaroori
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app) # React frontend se connection allow karne ke liye

ps = PorterStemmer()

# Exact Preprocessing Logic jo aapne model training ke waqt use ki thi
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)

# Model aur Vectorizer load ho rahe hain
try:
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
    print("✅ Success: Model and Vectorizer loaded successfully!")
except Exception as e:
    print(f"❌ Error loading files: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # User se data receive karna
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message found in request'}), 400
            
        input_sms = data['message']

        # 1. Text ko transform karna (Preprocessing)
        transformed_sms = transform_text(input_sms)
        
        # 2. Vectorize karna (TF-IDF transformation)
        vector_input = tfidf.transform([transformed_sms])
        
        # 3. Model se prediction lena
        result = model.predict(vector_input)[0]
        
        # JSON response wapas bhejna
        return jsonify({'prediction': int(result)})
    
    except Exception as e:
        # Agar koi error aaye toh terminal mein print hoga
        print(f"⚠️ Prediction Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Port 5000 par server start karna
    app.run(debug=True, port=5000)