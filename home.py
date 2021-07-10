from flask import Flask, render_template, request, redirect
import speech_recognition as sr
# import finApp

app = Flask(__name__)


@app.route("/speak", methods=["GET", "POST"])
def speak():
    data=""
    if request.method == "POST":
    # get audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            audio = r.listen(source)
        try:
            output = " " + r.recognize_google(audio, key=None)

        except sr.UnknownValueError:
            output = "Could not understand audio"
        except sr.RequestError as e:
            output = "Could not request results; {0}".format(e)

        data =output
        print("FILE DATA RECEIVED")

    return render_template('speech.html',data=data)

@app.route("/audio", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FILE DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file= request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            

    return render_template('wavfile.html', transcript=transcript)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
