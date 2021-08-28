# imports
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# create instance
bot = ChatBot(
    "Bob",
    preprocessors=['chatterbot.preprocessors.clean_whitespace'])

# set up sql database
bot = ChatBot(
    'Bob',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.50
        },


        # 'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///database.sqlite3'
)

# train bot - custom corpus
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "data/conversation.yml",
    "data/faq.yaml",
    "data/greetings.yaml",
    "data/orders.yaml"
)

# #train bot - english corpus
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

#train and save into sql

