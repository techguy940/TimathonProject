from flask import Flask, request, jsonify
import flask
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from flask_restful import Resource, Api
import json
from flask_cors import CORS
from flask_cors import cross_origin

IMGUR_CLIENT_ID = ""
IMGUR_CLIENT_SECRET = ""

app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'application/json'
CORS(app, resources={r"/*": {"origins": "*"}})

def upload(data):
	h = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
	data = {"image": data}
	r = requests.post("https://api.imgur.com/3/image", headers=h, data=data)
	return r.json()

def make_meme(topText, bottomText, imgUrl):
	data = b''
	r = requests.get(imgUrl, stream=True).raw
	for ii in r:
		data += ii

	i = Image.open(io.BytesIO(data))

	top_text = topText.upper()
	bottom_text = bottomText.upper()

	width, height = i.size
	main = ImageDraw.Draw(i)

	font = ImageFont.truetype("impact.ttf", size=round(height/9))

	letter_height, letter_width = font.getsize("A")

	cpl = (width // letter_width) + 5

	top_text = textwrap.wrap(top_text, width=cpl)
	bottom_text = textwrap.wrap(bottom_text, width=cpl)

	y_coord = 10
	for x in top_text:
		l_width, l_height = font.getsize(x)
		x_coord = (width - l_width) / 2
		main.text((x_coord-1, y_coord-1), x, font=font, fill="black")
		main.text((x_coord+1, y_coord-1), x, font=font, fill="black")
		main.text((x_coord-1, y_coord+1), x, font=font, fill="black")
		main.text((x_coord+1, y_coord+1), x, font=font, fill="black")
		main.text((x_coord, y_coord), x, fill="white", font=font)
		y_coord += l_height

	y_coord = height - letter_height * len(bottom_text) - 70
	for x in bottom_text:
		l_width, l_height = font.getsize(x)
		x_coord = (width - l_width) / 2
		main.text((x_coord-1, y_coord-1), x, font=font, fill="black")
		main.text((x_coord+1, y_coord-1), x, font=font, fill="black")
		main.text((x_coord-1, y_coord+1), x, font=font, fill="black")
		main.text((x_coord+1, y_coord+1), x, font=font, fill="black")
		main.text((x_coord, y_coord), x, fill="white", font=font)
		y_coord += l_height

	main.rectangle([(width-4, height-4), (0, 0)], outline='white')

	buff = io.BytesIO()
	i.save(buff, format="PNG")
	return buff.getvalue()

# @app.route("/meme", methods=["POST"])
# def post():
# 	topText = request.form['topText']
# 	bottomText = request.form['bottomText']
# 	imgUrl = request.form['imgUrl']
# 	binaryData = make_meme(topText, bottomText, imgUrl)
# 	url = upload(binaryData)
# 	link = url['data']['link']
# 	# resp = flask.Response(json.dumps({"link": link}))
# 	# resp.headers['Access-Control-Allow-Origin'] = "*"
# 	# return resp
# 	return jsonify(link=link)
# 	# def get(self):
# 	# 	topText = request.form['topText']
# 	# 	bottomText = request.form['bottomText']
# 	# 	imgUrl = request.form['imgUrl']
# 	# 	binaryData = make_meme(topText, bottomText, imgUrl)
# 	# 	url = upload(binaryData)
# 	# 	link = url['data']['link']
# 	# 	return {"link": link}

# 	# def get(self):
# 	# 	topText = request.form['topText']
# 	# 	bottomText = request.form['bottomText']
# 	# 	imgUrl = request.form['imgUrl']
# 	# 	binaryData = make_meme(topText, bottomText, imgUrl)
# 	# 	url = upload(binaryData)
# 	# 	link = url['data']['link']
# 	# 	resp = flask.Response(json.dumps({"link": link}))
# 	# 	resp.headers['Access-Control-Allow-Origin'] = '*'
# 	# 	return resp

# # api.add_resource(Meme, "/meme")

@app.route("/")
def get():
	topText = request.headers['topText']
	bottomText = request.headers['bottomText']
	imgUrl = request.headers['imgUrl']
	binaryData = make_meme(topText, bottomText, imgUrl)
	url = upload(binaryData)
	link = url['data']['link']
	# resp = flask.Response(json.dumps({"link": link}))
	# resp.headers['Access-Control-Allow-Origin'] = "*"
	# return resp
	return json.dumps({"link": link})

app.run(threaded=True, debug=True)