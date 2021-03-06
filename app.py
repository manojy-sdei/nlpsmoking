from flask import Flask, request, make_response, render_template
from flask_restful import Resource, Api
from main import analyse_text, analyse_text_data
import os
from multiprocessing import Process
import asyncio
import requests
import wget

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config_flask_development.py')
file_path = app.config['SAVE_DOC']


# print(file_path)
# exit()
# res_format = {
#     'code': '200',
#     'message': 'Success'
# }


class AnalyzeData(Resource):
    def save_file(self, recno, url):
        r = requests.get(url)
        abs_path = os.path.join(file_path, recno)
        cmd = "wget -O " + abs_path + ".vtt " + url
        os.system(cmd)
        return abs_path+".vtt"

    def post(self):
        # print(request.headers['Authorization'])
        # print(app.config['TOKEN'])
        # if request.headers['Authorization'] == app.config['TOKEN']:
        json_data = request.get_json()
        recno = json_data['recno']
        url = json_data['vtt']
        abs_path = self.save_file(recno, url)
        asyncio.run(self._process_data(abs_path, recno, file_format='text/vtt'))
        # p = Process(target=self._process_data, args=(vtt_data, recno,))
        # p.start()
        res_format = {
            'code': '200',
            'message': 'Success'
        }
        return res_format
        # else:
        #     res_format = {
        #         'code': '401',
        #         'message': 'Invalid Token',
        #     }
        #     return res_format

    async def _process_data(self, file_path, recno, file_format):
        nicotin_result, nicotin_words, therapy_result, therapy_words, suicide_monitering_check, risk, pos, neg, suicide_related_words = analyse_text_data(
            file_path, file_format)
        """Nicotine Check fid  152 boolean
        Nicotine Check Words  fid 153 text
        Nicotine Therapy Provided fid  129 boolean
        Nicotine Therapy Words  fid 154 text
        Suicide Risk Checked  fid 77 boolean
        Suicide Risk Level  fid 78 - Values: Low Moderate High
        Suicide pos  fid 93 text
        neg fid 160
        Suicide Related Words  fid 94 text"""
        res_format = {"to": "bnw746y6w",
                 "data": [{
                 "3": {"value": int(recno)},
                 "77": {"value": suicide_monitering_check},
                 "78": {"value": risk},
                 "93": {"value": str(pos)},
                 "160": {"value": str(neg)},
                 "94": {"value": suicide_related_words},
                 "152": {"value": nicotin_result},
                 "153": {"value": nicotin_words},
                 "129": {"value": therapy_result},
                 "154": {"value": therapy_words},
                  }]
                  }
        headers = {'QB-Realm-Hostname': 'brighthearthealth.quickbase.com',
                   'Authorization': 'QB-USER-TOKEN b33nnm_k85g_vp75yvpxx9ce24qi3ibt75uhe'}
        response = requests.post('https://api.quickbase.com/v1/records', json=res_format, headers=headers)
        print(response.text)
        print(res_format)
        # return response.json
        # res_format['data'] = final_res
        # return res_format


class ShowData(Resource):
    def post(self):
        req_data = request.get_json()
        print(req_data)
        return req_data


class TextAnalyse(Resource):
    def _process_file(self, file_path, file_format):
        nicotin_result, nicotin_words, therapy_result, therapy_words, suicide_monitering_check, risk, pos, neg, suicide_related_words = analyse_text(
            file_path, file_format)
    # nicotin_result, nicotin_words, therapy_result, therapy_words, final_res = analyse_text(file_path, file_format)
        res_format = {"to": "bnw746y6w",
                      "data": [{
                          # "3": {"value": int(recno)},
                          "77": {"value": suicide_monitering_check},
                          "78": {"value": risk},
                          "93": {"value": str(pos)},
                          "160": {"value": str(neg)},
                          "94": {"value": suicide_related_words},
                          "152": {"value": nicotin_result},
                          "153": {"value": nicotin_words},
                          "129": {"value": therapy_result},
                          "154": {"value": therapy_words},
                      }]
                      }
        headers = {'QB-Realm-Hostname': 'brighthearthealth.quickbase.com',
                   'Authorization': 'QB-USER-TOKEN b33nnm_k85g_vp75yvpxx9ce24qi3ibt75uhe'}
        # response = requests.post('https://api.quickbase.com/v1/records', json=res_format, headers=headers)
        # print(response.text)
        # print(res_format)

        # res_format = {'nicotin_check': nicotin_result, 'therapy_check': therapy_result, 'nicotin_words': nicotin_words,
                      # 'therapy_words': therapy_words, 'suicide_monitoring_data': final_res}
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
        # patient_id = request.form.get('patient_id')
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
api.add_resource(AnalyzeData, '/analyse_data')
api.add_resource(ShowData, '/show_data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='8085')
