import google.generativeai as genai

from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

# Temporary storage for code (for demo purposes)
processed_code = {
    'html': '',
    'css': '',
    'js': ''
}
filename1 = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/main")
def main_():
    return render_template("main.html")


@app.route("/how-to-use")
def how():
    return render_template("how_to_use.html")


@app.route("/wrong")
def wrong():
    return "Sorry that was a wrong png"


@app.route("/credits")
def credits():
    return render_template("credits.html")


@app.route("/upload_image", methods=["POST"])
def upload_image():
    global filename1
    if 'file' not in request.files:
        return jsonify({"success": False})
    file = request.files['file']
    if file and file.filename.endswith('.png'):
        filename1 = "upload/" + file.filename
        file.save(filename1)
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/process_code", methods=["POST"])
def process_code():
    global processed_code
    global filename1
    key = open("api.txt", 'r').readline()  # replace with your api key
    genai.configure(api_key=key)

    sample_file = genai.upload_file(filename1)
    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content([sample_file,
                                       '''does the image i sent contains 30 words related to HTML tags, and all of 
                                       them are crossed within the grid. ,

                                        ANswer in "True" or "False" only'''])
    if response.text.__contains__("als"):
        return jsonify({"redirect_url": url_for("wrong")})

    data = request.json
    processed_code['html'] = data.get("html", "")
    processed_code['css'] = data.get("css", "")
    processed_code['js'] = data.get("js", "")

    # Send a success response and redirect URL
    return jsonify({"redirect_url": url_for("render_code")})


@app.route("/render_code")
def render_code():
    return render_template("rendered_code.html",
                           html_code=processed_code['html'],
                           css_code=processed_code['css'],
                           js_code=processed_code['js'])


if __name__ == "__main__":
    app.run(port=9999, debug=True)
