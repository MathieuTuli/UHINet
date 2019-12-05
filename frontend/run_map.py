from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", methods=["GET"])
def map():
    f = open("input", "r")
    s = f.read().splitlines()[0]
    f.close()
    key = 'https://maps.googleapis.com/maps/api/js?key='+ s +'&libraries=drawing&callback=initMap'
    return render_template('map_single_polygon.html', key=key)

if __name__ == '__main__':
    app.run(debug=True)
