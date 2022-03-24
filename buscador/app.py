from flask import Flask, request, render_template

# modulos proprios
from search_engine import SearchEngine

app = Flask(__name__)

print("Inicializando search engine")
se = SearchEngine()
import nltk
#nltk.download('gutenberg')
full_gutenberg = [nltk.corpus.reuters.raw(f) for f in nltk.corpus.reuters.fileids()]
se.indexar(full_gutenberg)
print("Search engine inicializada")

@app.route('/', methods=['GET'])
def index():
    global se
    if 'termos' in request.args.keys():
        termos = request.args['termos']
        results = se.ranquear(termos)
        return render_template('index.html', results=results, termos=termos)
    else:
        return render_template('index.html')



