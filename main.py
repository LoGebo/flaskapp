from flask import Flask, request, render_template_string
import re
import os

##Desarrollado por Jesús Daniel Martínez y Luis Fernando Perez Robles.

from flask import Flask, request, render_template_string, render_template, make_response, jsonify

app = Flask(__name__)

# Las funciones y definiciones de lexer() .
def lexer(code_string):
    patterns = [
        ('reserved', r'\b(?:and|as|assert|break|continue|class|def|del|elif|else|except|finally|for|from|if|import|global|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'),
        ('operator', r'(-|\+|\*|/|\^|==|!=|<=|>=|<|>|&|\||!|%|\||~)'),
        ('literals_numerics', r'\b\d+(\.\d+)?\b'),
        ('literals_string', r'(?<![\w])(".*?"|\'.*?\')(?![\w])'),
        ('identifier', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('comment', r'(#.*|""".*?"""|\'\'\'.*?\'\'\')'),
        ('separators', r'(\(|\)|\[|\]|{|}|:|,|;|\.)')
    ]
    pattern = re.compile('|'.join('(?P<%s>%s)' % pair for pair in patterns))

    lines = code_string.split('\n')

    html = '<!DOCTYPE html><html><head><style>body {font-family: monospace;} .reserved {color: blue;} .operator {color: red;} .literals_numerics {color: green;} .literals_string {color: magenta;} .identifier {color: brown;} .comment {color: gray;} .separators {color: indigo;}</style></head><body><pre>'

    for line in lines:
          pos = 0
          while pos < len(line):
              match = pattern.match(line, pos)
              if match:
                  category = match.lastgroup
                  start, end = match.span()
                  html += line[pos:start] + '<span class="' + category + '">' + line[start:end] + '</span>'
                  pos = end
              else:
                  html += line[pos]
                  pos += 1
          html += '<br>'  # Añadir un salto de línea después de procesar cada línea
  
    html += '</pre></body></html>'
    
    return html


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/highlight', methods=['POST'])
def highlight_code():
    python_code = request.form['python_code']
    print("hola mundo")
    print("hola", python_code)
    output = lexer(python_code)
    print("hola html aqui", output)
    return jsonify({'output': output})



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
