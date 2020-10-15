from flask import Flask, redirect, url_for, render_template, request
import difflib
from flask import Flask, redirect, url_for, render_template
from gector.model import load_model
from gector.predict import predict_for_string

app = Flask(__name__) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    model = load_model(vocab_path='./gector/data/output_vocabulary/',
                   model_paths=['./static/nn_models/xlnet_0_gector.th'])
    text = request.args.get('jsdata')
    corrected_text = predict_for_string(text, model)
    return show_diff(text, corrected_text)


def show_diff(text, n_text):
    """
    compares two strings
    gives the correct css classes accordingly
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append('<span class="delta-insert">' + seqm.b[b0:b1] + '</span>')
        elif opcode == 'delete':
            output.append('<span class="delta-delete">' + seqm.a[a0:a1] + '</span>')
        elif opcode == 'replace':
            output.append('<span class="delta-replace">' + seqm.b[b0:b1] + "</span>")
        else:
            raise RuntimeError("unexpected opcode")
    return ''.join(output)


if __name__ == "__main__":
    app.run(debug = True)
