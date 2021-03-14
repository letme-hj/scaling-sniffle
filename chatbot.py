import pandas as pd
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/message', methods=['POST'])
def Message():
    intent = request.get_json()
    intent = intent['intent']['name']
    content = request.get_json()

    if intent == '키워드 검색':
        content = content['action']['detailParams']['news_keyword']['value']
        keyword = pd.read_csv("entity_keyword.csv")
        keyword = keyword[keyword['entity'] == content]
        keyword.reset_index(drop=True, inplace=True)

        item = []
        for i in range(len(keyword)):
            item += [{
                "title": keyword['title'][i],
                "description": keyword['description'][i],
                "thumbnail": {
                    "imageUrl": keyword['image'][i],
                    "link": {"web": keyword['link'][i]}
                        }
                    }]

        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": item
                            }
                        }
                    ]
                }
            }

    elif intent == '브랜드 검색':
        content = content['action']['detailParams']['news_brand']['value']
        brand = pd.read_csv("entity_brand.csv")
        brand = brand[brand['entity'] == content]
        brand.reset_index(drop=True, inplace=True)

        item = []
        for i in range(len(brand)):
            item += [{
                "title": brand['title'][i],
                "description": brand['description'][i],
                "thumbnail": {
                    "imageUrl": brand['image'][i],
                    "link": {"web": brand['link'][i]}
                        }
                    }]

        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": item
                            }
                        }
                    ]
                }
            }

    elif intent == '피드백 안내':
        user = content['userRequest']['user']['id']
        utter = content['action']['detailParams']['feedback']['value']
        fdback = pd.DataFrame({'user': [user], 'utterance': [utter]})
        fdback['user'][len(fdback)] = user
        fdback['utterance'][len(fdback)] = utter
        fdback.to_csv('feedback.csv', index=False, mode='a', encoding='utf-8', header=False)

        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": '소중한 의견 감사해요!\n앞으로도 발전하는 왓츠뉴가 되겠습니다!'
                        }
                    ]}

                }
    elif intent == '최신 뉴스':
        brand = pd.read_csv("entity_brand.csv")
        brand.reset_index(drop=True, inplace=True)
        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": brand['description'][0],
                                "thumbnail": {
                                    "imageUrl": brand['image'][0],
                                    "link": {"web": brand['link'][0]}
                                }
                            }
                        }
                    ]
                }
            }

    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
