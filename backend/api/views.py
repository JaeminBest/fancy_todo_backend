from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from ..kobert_ner_extractor.webapp_helper import extract
from ..wsgi import tokenizer, model, decoder_from_res, db
import secrets

def healthcheck(request):
    if request.method=='GET':
        response = HttpResponse({'status':'ok'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response

@csrf_exempt
def todo_endpoint(request):
    if request.method == 'POST':
        queries = request.POST
        edit_flag = False
        if 'id' in queries:
            edit_flag = True
            item_id = queries['id']
            
        # handle multidict key error
        try:
            date = queries['date']
            text = queries['text']
            time = queries['time']
        except:
            response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
            add_access_control_headers(response)
            return response
        
        # handle create/update task
        status = False
        if edit_flag:
            status = create_todo_item(date,text,time)
        else:
            status = edit_todo_item(item_id,date,text,time)
        
        # async response
        if status:
            response = HttpResponse({'status':'ok'}, content_type=u"application/json; charset=utf-8")
        else:
            response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    

entity_list = ['PER','ORG','LOC']

def create_todo_item(date,text,time):
    ex_dict = extract(text, model, tokenizer, decoder_from_res)
    ret = {'PER':[],'ORG':[],'LOC':[]}
    try:
        for word, tag, prob in ex_dict['word']:
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