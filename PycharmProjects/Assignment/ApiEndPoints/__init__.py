from flask import Flask, url_for,request
from Test.Utilities import BasicUtils
from Test.jsonComparison import CompareJson

app = Flask(__name__)
utils = BasicUtils()


@app.route('/v1/diff/left/', methods=['POST'])
def read_json_left():
    utils.save_left_json(request.form['JSON'])
    return "Successfully accepted the JSON"


@app.route('/v1/diff/right/', methods=['POST'])
def read_json_right():
    utils.save_right_json(request.form['JSON'])
    return "Successfully accepted the JSON"


@app.route('/v1/diff/', methods=['POST'])
def compare_json():
    # Create json diff Object.
    difference = CompareJson()

    # Check the equality of 2 Json.
    output_msg=difference.compare_json(utils.left_file_path, utils.right_file_path)
    return output_msg


if __name__ == '__main__':
    app.debug=True
    app.run()
