from flask import Flask, render_template
from flask_caching import Cache
import random
import pandas as pd
import datetime

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Carrega o arquivo XLSX
def load_phrases():
    df = pd.read_excel('frases.xlsx')
    return df['Frases'].tolist()

# Retorna a frase do dia ou atualiza se for um novo dia
def get_random_phrase_of_day():
    phrases = load_phrases()
    random_phrase = random.choice(phrases)
    return random_phrase

# Rota principal
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/frase-do-dia')
def index():
    today_phrase = cache.get('phrase_of_day')
    if today_phrase is None:
        today_phrase = get_random_phrase_of_day()
        cache.set('phrase_of_day', today_phrase, timeout=86400)  # Cache expira após 24 horas
    return render_template('index.html', phrase=today_phrase)

if __name__ == '__main__':
    app.run(debug=True)
