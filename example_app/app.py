# imports
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import json
#import mypreprocessors

def create_app():
    app = Flask(__name__)

    # create instance
    # set up sql database
    bot = ChatBot(
        'Bob',
        response_selection_method=get_random_response,
        #preprocessors=["chatterbot.preprocessors.clean_whitespace", "mypreprocessors.lower"],
        preprocessors=["chatterbot.preprocessors.clean_whitespace"],
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                'default_response': 'I am sorry, but I do not understand. To find out more, please call our friendly hotline at +65 1234 5678, open daily from 8am to 8pm.',
                'maximum_similarity_threshold': 0.7
            },
            'chatterbot.logic.MathematicalEvaluation'
            #'chatterbot.logic.TimeLogicAdapter'
        ],
        database_uri='sqlite:///database.sqlite3'
    )

    # train bot - custom corpus
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(
        "../data/conversation.yml",
        "../data/faq.yaml",
        "../data/greetings.yaml",
        "../data/orders.yaml",
        "../data/dhlexpress.yaml"
    )

    # #train bot - english corpus
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english")

    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/send-message", methods=['POST'])
    def get_bot_response():
        data = request.get_json(force=True)
        response = str(bot.get_response(str(data['message']).lower()))
        return response
    
    return app

if __name__ == "__main__":
    app=create_app()
    app.run()
