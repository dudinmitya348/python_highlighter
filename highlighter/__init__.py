"""Flask module
file: __init__.py
date: 12.12.2012
author smith@example.com
license: MIT"""

from flask import Flask, render_template, request, Markup


def create_app():
    """Create flask app for binding."""
    app = Flask(__name__)

    template_file_name = 'index.html'

    @app.route('/', methods=['GET'])
    def index():
        return render_template(template_file_name)

    @app.route('/', methods=['POST'])
    def process():
        search_text = request.form['search']
        text = request.form['text']
        is_sensetive = request.form.get('is_sensetive', '0')
        highlighted_text = highlight_text(text, search_text, is_sensetive)
        result = {'text': text,
                  'highlighted_text': Markup(highlighted_text),
                  }
        return render_template(template_file_name, **result)

    def markup_text(text):
        """Markup given text.
        This is supplementary method that helps you to wrap marked text in tags.
        @:param text - string text to be marked
        @:return marked text, e.g., <mark>highlighted text</mark>."""
        result = "<mark>" + text + "</mark>"
        return result

    def replacement_list(expr, text):
        """Conducts text processing to obtain all forms of the search text.
        @: param text - the text of the line to be marked
        @: return a list of unique word forms."""
        result = []
        index = 0
        while index >= 0:
            index = text.lower().find(expr.lower(), index)
            if index < 0: break
            separator = ''
            result.append(separator.join([text[x] for x in range(index, index+len(expr))]))
            index += len(expr)
        result = set(result)
        return result

    def highlight_text(text, expr, is_sensetive='0'):
        """Markup searched string in given text.
        @:param text - string text to be processed (e.g., 'The sun in the sky')
        @:param expr - string pattern to be searched in the text (e.g., 'th')
        @:return marked text, e.g., "<mark>Th</mark>e sun in <mark>th</mark>e sky"."""
        if is_sensetive == '1':
            text = text.replace(expr, markup_text(expr))
        else:
            replacement = replacement_list(expr, text)
            for token in replacement:
                text = text.replace(token, markup_text(token))
        return text

    return app
