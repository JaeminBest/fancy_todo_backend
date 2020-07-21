from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from . import add_access_control_headers
from ..kobert_ner_extractor.webapp_helper import extract
from ..wsgi import tokenizer, model, decoder_from_res, db
import secrets
import json

def healthcheck(request):
    if request.method=='GET':
        response = HttpResponse(json.dumps({'status':'ok'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)
    else:
        response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)

@csrf_exempt
def todo_endpoint(request):
    if request.method == 'POST':
        print("enter todo_endpoint -1",flush=True)
        raw_data = request.body.decode('utf-8')
        queries = json.loads(raw_data)
        edit_flag = False
        if 'id' in queries:
            edit_flag = True
            item_id = queries["id"]
            
        # handle multidict key error
        try:
            date = queries["date"]
            text = queries["text"]
            time = queries["time"]
        except:
            response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
            response = add_access_control_headers(response)
            return response
        print("enter todo_endpoint -2",flush=True)
        # handle create/update task
        status = False
        if edit_flag:
            status = edit_todo_item(item_id,date,text,time)
        else:
            status = create_todo_item(date,text,time)
            
        
        # async response
        if status:
            response = HttpResponse(json.dumps({'status':'ok'}), content_type=u"application/json; charset=utf-8")
        else:
            response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)
    else:
        response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)
    

entity_list = ['PER','ORG','LOC']

def create_todo_item(date,text,time):
    ex_dict = extract(text, model, tokenizer, decoder_from_res)
    print("extracted: ",ex_dict,flush=True)
    ret = {'PER':[],'ORG':[],'LOC':[]}
    try:
        for el in ex_dict['word']:
            word = el['word']
            tag = el['tag']
            if tag in entity_list:
                ret[tag].append(word)
        doc_ref = db.collection(u'todos').document(date).collection('items').document(u'{}'.format(secrets.token_hex(16)))
        doc_ref.set({
            u'time': time,
            u'text': text,
            u'place': ret['LOC'],
            u'org' : ret['ORG'],
            u'people' : ret['PER'],
        })
    except:
        return False
    return True

def edit_todo_item(item_id,date,text,time):
    ex_dict = extract(text, model, tokenizer, decoder_from_res)
    ret = {'PER':[],'ORG':[],'LOC':[]}
    try:
        for word, tag, prob in ex_dict['word']:
            if tag in entity_list:
                ret[tag].append(word)
        doc_ref = db.collection(u'todos').document(date).collection('items').document(item_id)
        doc_ref.set({
            u'time': time,
            u'text': text,
            u'place': ret['LOC'],
            u'org' : ret['ORG'],
            u'people' : ret['PER'],
        })
    except:
        return False
    return True