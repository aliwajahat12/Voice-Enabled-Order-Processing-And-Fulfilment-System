from re import DEBUG
from flask import Flask, request, render_template, jsonify
import os
import datetime
from werkzeug.utils import secure_filename
import contextExtraction.get_category
import contextExtraction.get_store_and_order_info
import contextExtraction.get_store
import gcp_voice_recognition
import get_closest_name
import CommandTypeAnalysis.preprocessing as preprocessor
import CommandTypeAnalysis.query as query
app = Flask(__name__)
preprocessor.main()
app.config['UPLOAD_FOLDER'] = './audio-uploads/'
uploads_dir = os.path.join(app.instance_path, 'audio-uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("new.html")


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        audio_blob = request.data
        # audio_file = request.files['audio-file']
        audio_fname = f'{uploads_dir}/{secure_filename(str(datetime.datetime.now()))}.wav'
        print(audio_fname)
        with open(audio_fname, 'wb') as audio_file:
            audio_file.write(audio_blob)
        #sentence = voice_recong.localF(audio_fname)
        sentence = gcp_voice_recognition.transcribe_file(audio_fname)
        if (sentence == 'Unknown Value Error'):
            extracted_context = "Not Recognized"
            extracted_context['audio2text-sentence'] = "Not Recognized"
        else:
            extracted_context = {}
            commandTypeRankings = query.main(query=sentence)
            print(commandTypeRankings)
            if(len(commandTypeRankings) == 0):
                print("No command type found")
                extracted_context['audio2text-sentence'] = "Invalid Command"
            else:
                if(commandTypeRankings[0] == '1'):
                    print("Command Type 1")
                    extracted_context = contextExtraction.get_store_and_order_info.get_context_from_sentence(
                        sentence)
                    extracted_context['audio2text-sentence'] = sentence
                    extracted_context['command_type'] = 1
                if(commandTypeRankings[0] == '2'):
                    print("Command Type 2")
                    extracted_context['store'] = contextExtraction.get_store.get_store_name_from_sentence(
                        sentence)
                    extracted_context['audio2text-sentence'] = sentence
                    extracted_context['command_type'] = 2
                if(commandTypeRankings[0] == '3'):
                    print("Command Type 3")
                    extracted_context['command_type'] = 3
                    extracted_context['category'] = contextExtraction.get_category.get_category_from_sentence(
                        sentence)
                    extracted_context['audio2text-sentence'] = sentence
            extracted_context['audio2text-sentence'] = sentence

        print(extracted_context)
        extracted_context = get_closest_name.verifyJSON(extracted_context)
        print(extracted_context)
        return jsonify(extracted_context)


if __name__ == '__main__':
    app.run()
