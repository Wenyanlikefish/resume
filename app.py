
from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator
# from textblob import TextBlob
app = Flask(__name__)

person = {
    'first_name': '温砚',
    'last_name' : '',
    'address' : '湖北师范大学',
    'job': 'Python developer',
    'tel': '+86 173********',
    'email': '******@outlook.com',
    'description' : 'Knowledge is a kind of happiness, and curiosity is the bud of knowledge .',
    'social_media' : [
        {
            'link': 'https://www.facebook.com/nono',
            'icon' : 'fa-facebook-f'
        },
        {
            'link': 'https://github.com/',
            'icon' : 'fa-github'
        },
        {
            'link': 'linkedin.com/in/nono',
            'icon' : 'fa-linkedin-in'
        },
        {
            'link': 'https://twitter.com/nono',
            'icon' : 'fa-twitter'
        }
    ],
    'img': 'img/img_nono.jpg',
    'experiences' : [
        {
            'title' : '项目名称',
            'company': 'python爬虫',
            'description' : '爬取哔哩哔哩视频数据信息并可视化分析',
            'timeframe' : '2021.6-2021.7'
        },
        {
            'title' : '项目名称',
            'company': '文本识别小程序',
            'description' : '软件测试、运营维护',
            'timeframe' : '2021.4-2021.5'
        }
    ],
    'education' : [
        {
            'university': '湖北师范大学',
            'degree': '计算机与信息工程学院',
            'description' : '软件工程',
            'mention' : 'Bien',
            'timeframe' : '2018-2022'
        }
    ],
    'programming_languages' : {
        'HMTL' : ['fa-html5', '100'],
        'CSS' : ['fa-css3-alt', '100'],
        'SASS' : ['fa-sass', '90'],
        'JS' : ['fa-js-square', '90'],
        'Wordpress' : ['fa-wordpress', '80'],
        'Python': ['fa-python', '70'],
        'Mongo DB' : ['fa-database', '60'],
        'MySQL' : ['fa-database', '60'],
        'NodeJS' : ['fa-node-js', '50']
    },
    'languages' : {'French' : 'Native', 'English' : 'Professional', 'Spanish' : 'Professional', 'Italian' : 'Limited Working Proficiency'},
    'interests' : [{"inter":"旅行"},{"inter":"阅读"},{"inter":"学习"}],
    'tec':[{"tech":'python'},{"tech":'爬虫'},{"tech":'flask'},{"tech":'scrapy'},{"tech":'selenium'}],
    'evaluation':"本人能吃苦耐劳，适应性强，协调性好，对工作认真负责，工作积极、主动、上进，有良好的的心理素质，能正确的认识和评价自己，虚心接受他人的建议。拥有良好的表达和沟通能力，易于他人合作，形成融洽的合作关系。并有很强的团队合作精神和合作能力、注重工作效率。",
    'cloud':'我们在排行榜页面可以很容易获得100条视频的url,将这些url循环访问网页，爬取每个视频的tag标签，由于bilibili的tag标签分为三种所以我总过对三种标签进行xpath爬取统一放进tag列表中表存到txt文件，然后通过jieba分词搜索引擎的方法对文本进行分割，然后在打开一张bilibili的图片，使得词云呈现效果如图片一般。，'
}

@app.route('/')
def cv(person=person):
    return render_template('resume.html', person=person)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))

@app.route('/chart')
def index():
	return render_template('chartsajax.html',  graphJSON=gm())

def gm(province='安徽'):
	df = pd.read_csv('china_data_covid19.csv')

	fig = px.line(df, x="TIME", y=province)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON


@app.route('/bilibili_callback', methods=['POST', 'GET'])
def db():
	return xm(request.args.get('data'))

@app.route('/bilibili')
def index_bilibili():
    return render_template('bilibili_video.html', graphJSON_1=xm())

def xm(keyword='视频观看人数（万次）'):
    df =pd.read_csv('video.csv')
    fig = px.histogram(df, x="视频up主", y=keyword)
    graphJSON_1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON_1

@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}

	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if  'text' in row:
				nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else :
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
					'labels': top_ten_list_labels,
					'values': top_ten_list_vals,
					'type': 'pie',
					'insidetextfont': {'color': '#FFFFFF',
										'size': '14',
										},
					'textfont': {'color': '#FFFFFF',
										'size': '14',
								},
					}]

	layout = {'title': '<b>意见挖掘</b>'}

	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
  app.run(debug= True,port=5000,threaded=True)
