import json
import pandas as pd
from collections import defaultdict
from pprint import pprint

keyword = 'merger'
filename='positive'

with open('./../../data/text_sent_ent_keywords/'+keyword+'/'+filename+'.json') as f:
    matches = json.load(f)

pprint(matches)
mydict = defaultdict(list)

for match_id,match in enumerate(matches):
    ent_1_name = match['ent_1']['name']
    ent_2_name = match['ent_2']['name']
    sents = match['sents']
    pprint(match['sents'])
    for sent_id, sent in enumerate(sents):
        target_sent_num = sent['sent_num']
        target_text     = sent['text']
        try:
            mention_contexts = sent['mention_contexts']
        except KeyError:
            print('key: mention_contexts not found.')
            final_text = sent['text']
            mention_contexts = []
            mydict['match_id'].append(match_id+1)
            mydict['evidence_id'].append(sent_id+1)
            mydict['num_mention_context'].append('--')
            mydict['ent_1_name'].append(ent_1_name)
            mydict['ent_2_name'].append(ent_2_name)
            mydict['current_sent_num'].append('--')
            mydict['target_sent_num'].append('--')
            mydict['final_text'].append(final_text)


        for i, context in enumerate(mention_contexts):
            current_sent_num = context['sent_num']
            current_sent_text = context['text']

            if current_sent_num < target_sent_num:
                final_text = current_sent_text + target_text
            elif current_sent_num > target_sent_num:
                final_text = target_text + current_sent_text
            else:
                raise RuntimeError('Check comparison of current_sent_num < target_sent_num')
            mydict['match_id'].append(match_id+1)
            mydict['evidence_id'].append(sent_id+1)
            mydict['num_mention_context'].append(i+1)
            mydict['ent_1_name'].append(ent_1_name)
            mydict['ent_2_name'].append(ent_2_name)
            mydict['current_sent_num'].append(current_sent_num)
            mydict['target_sent_num'].append(target_sent_num)
            mydict['final_text'].append(final_text)

df = pd.DataFrame(mydict, columns=['match_id','evidence_id','num_mention_context','ent_1_name','ent_2_name','current_sent_num','target_sent_num','final_text'])
df.to_csv('./../../data/text_sent_ent_keywords/'+keyword+'/'+filename+'.csv', index=False)