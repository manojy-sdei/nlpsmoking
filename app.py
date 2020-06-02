from flask import Flask, request, make_response, render_template
from flask_restful import Resource, Api
from main import analyse_text
import os
# import json

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config_flask_development.py')
file_path = app.config['SAVE_DOC']
# print(file_path)
# exit()
res_format = {
    'code': '200',
    'message': 'Success'
}


class TextAnalyse(Resource):
    def _process_file(self, file_path, file_format):
        nicotin_result, nicotin_words, therapy_result, therapy_words = analyse_text(file_path, file_format)
        res_format['nicotin_check'] = nicotin_result
        res_format['therapy_check'] = therapy_result
        res_format['nicotin_words'] = nicotin_words
        res_format['therapy_words'] = therapy_words
        # res_format['data'] = final_res
        return res_format

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('main.html'), 200, headers)
        # return {'result': app.config['TEST_CONFIG']}

    def post(self):
        # try:
        # print(request.form.get())
        file = request.files.get('file')
        patient_id = request.form.get('patient_id')
        if file is None:
            return {'error': 'file is not found in the form data'}
        Fname = file.filename
        format = Fname.split('.')[-1]
        if format == 'vtt':
            File_format = 'text/vtt'
        elif format == 'csv':
            File_format = 'text/csv'
        else:
            return {'error': 'Invalid file format'}
        abs_path = os.path.join(file_path, Fname)
        print(abs_path)
        file.save(abs_path)
        result = self._process_file(abs_path, file_format=File_format)
        print(result)
        # result['data'][0]['patient_id'] = patient_id
        # r = json.dumps(result['data'])
        # loaded_r = json.loads(r)
        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template("output.html", result=loaded_r), 200, headers)
        return result
        # except Exception as e:
        #     print(e)
        #     return {'error': str(e)}


class ParseReport(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('main.html'), 200, headers)


class Visualize(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('visualize.html'), 200, headers)


api.add_resource(Visualize, '/visualize')
api.add_resource(ParseReport, '/home')
api.add_resource(TextAnalyse, '/analyse_text')

if __name__ == '__main__':
    app.run(debug=True, port='8001')
