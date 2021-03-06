from flask import Flask, request, render_template

# modulos proprios
from search_engine import SearchEngine

app = Flask(__name__)

print("Inicializando search engine")
se = SearchEngine()
print("Search engine inicializada")

@app.route('/', methods=['GET'])
def index():
    global se
    if 'termos' in request.args.keys():
        query = request.args['termos']
        results = se.search(query)
        if results[1] is not None:
            query = results[1]
        return render_template('index.html', results=results[0], termos=query)
    return render_template('index.html')