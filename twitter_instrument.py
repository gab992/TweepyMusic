import tweepy
import pandas as pd
import numpy as np
import json
import sys
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep
import re
import string
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from gensim.models import KeyedVectors
import pickle
import os

consumer_key = 'ywojVZT3SBZWLHXKYoMl39Eqx'
consumer_secret = 'O4dfBtDiirV5QMO4H6CqM2br63FndUoYuNQjZGaPjgxoiblypk'
access_token = '1281680128351903751-UdocdoBWHyGOvGeYkIMszubKJcVBnc'
access_token_secret = 'VL0uMsDmhaGwRy3CVe0iHUoBCZV0ElLTChoSJTg578IoI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener,self).__init__()
        self.output_file = output_file
    def on_status(self, status):
        if len(prep_text(status.text))>0:
            #print(get_vec(prep_text(status.text)).shape)
            #sender.send_message('/play_this', get_vec(prep_text(status.text)).tolist()) NOT WORKING
            try:
                #print(get_vec(prep_text(status.text)).max(),get_vec(prep_text(status.text)).min())
                vals = ((get_vec(prep_text(status.text))))
                        #*70).round()
                sender.send_message('/play_this', vals[0:14].tolist())
                #print(vals)
            except:
                pass
    def on_error(self, status_code):
        print(status_code)
        return False

listener = Listener()

tokenizer = RegexpTokenizer('\s+', gaps=True)
def prep_text(text):
    '''takes tweet as input and returns all lower case nouns and adjectives from the tweet as a list'''
    try:
        text = re.search(r'(?<=: ).*',text)[0]
    except:
        pass
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = re.sub(r"(\w)([A-Z])", r"\1 \2", text)
    toked = tokenizer.tokenize((text.lower()))
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    nouns_adj = [word for (word, pos) in pos_tag(toked) if is_noun_adj(pos)]
    return nouns_adj

if 'word2vec.pickle' not in os.listdir():
    pretrained_embeddings_path = "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
    word2vec = KeyedVectors.load_word2vec_format(pretrained_embeddings_path, binary=True)
    pickle.dump(word2vec, open('word2vec.pickle','wb'))
else:
    word2vec=pickle.load(open('word2vec.pickle','rb'))

def get_vec(word_list):
    return np.mean([word2vec[word] for word in word_list if word in word2vec.vocab], axis=0)

topic = ''
while (topic != 'stop'):
    topic = input('Enter topic you would like to streeam (type stop to end program):')
    if topic != 'stop':
        try:
            stream = Stream(auth=api.auth, listener=listener)
            stream.filter(track=[topic])

            print('Start streaming.')
            stream.sample(languages=['en']).items(1)
        except KeyboardInterrupt:
            print("Stopped.")
        finally:
    #        print('Done.')
            stream.disconnect()
    #        output.close()
