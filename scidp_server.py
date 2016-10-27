from bottle import route, run
from bottle import get, post, request # or route

import warnings
import sys
import codecs
import numpy
import argparse
import theano
import json
import pickle

from rep_reader import RepReader
from util import read_passages, evaluate, make_folds

from keras.models import Sequential, Graph, model_from_json
from keras.layers.core import TimeDistributedDense, Dropout
from keras.layers.recurrent import LSTM, GRU
from keras.callbacks import EarlyStopping

from attention import TensorAttention
from keras_extensions import HigherOrderTimeDistributedDense

from nn_passage_tagger import PassageTagger

@get('/scidp') # or @route('/scidp')
def scidp():
    return '''
        <form action="/scidp" method="post">
            <textarea rows="20" cols="50">
                Please enter the document text here
            </textarea>
            <input value="Submit" type="submit">
        </form>
    '''
    
@post('/scidp') # or @route('/login', method='POST')
def run_scidp_tagger():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return "<p>Your login information was correct.</p>"

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Train, cross-validate and run LSTM discourse tagger")
    argparser.add_argument('--repfile', type=str, help="Gzipped word embedding file")
    argparser.add_argument('--use_attention', help="Use attention over words? Or else will average their representations", action='store_true')
    argparser.add_argument('--att_context', type=str, help="Context to look at for determining attention (word/clause)")
    argparser.set_defaults(att_context='word')
    argparser.add_argument('--bidirectional', help="Bidirectional LSTM", action='store_true')
    argparser.add_argument('--show_attention', help="When testing, if using attention, also print the weights", action='store_true')
    args = argparser.parse_args()
    repfile = args.repfile
    use_attention = args.use_attention
    att_context = args.att_context
    bid = args.bidirectional
    show_att = args.show_attention

    model_ext = "att=%s_cont=%s_bi=%s"%(str(use_attention), att_context, str(bid))
    model_config_file = open("model_%s_config.json"%model_ext, "r")
    model_weights_file_name = "model_%s_weights"%model_ext
    model_label_ind = "model_%s_label_ind.json"%model_ext
    model_rep_reader = "model_%s_rep_reader.pkl"%model_ext
    rep_reader = pickle.load(open(model_rep_reader, "rb"))
    print >>sys.stderr, "Loaded pickled rep reader"
    nnt = PassageTagger(pickled_rep_reader=rep_reader)
    nnt.tagger = model_from_json(model_config_file.read(), custom_objects={"TensorAttention":TensorAttention, "HigherOrderTimeDistributedDense":HigherOrderTimeDistributedDense})
    print >>sys.stderr, "Loaded model:"
    print >>sys.stderr, nnt.tagger.summary()
    nnt.tagger.load_weights(model_weights_file_name)
    print >>sys.stderr, "Loaded weights"
    label_ind_json = json.load(open(model_label_ind))
    label_ind = {k: int(label_ind_json[k]) for k in label_ind_json}
    print >>sys.stderr, "Loaded label index:", label_ind
    
    run(host='localhost', port=8080, debug=True)

