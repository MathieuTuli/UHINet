from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route("/", methods=["GET"])
def map():
    f = open("input", "r")
    s = f.read().splitlines()[0]
    f.close()
    key = 'https://maps.googleapis.com/maps/api/js?key='+ s +'&libraries=drawing&callback=initMap'
    return render_template('map_single_polygon.html', key=key)

@app.route("/send_coordinates")
def add_numbers():
    a = request.args.get('a')
    print('\n')
    print(a)
    print('\n')
    image_name = str('image.png')
    return jsonify(image_name)

if __name__ == '__main__':
    app.run(debug=True)
