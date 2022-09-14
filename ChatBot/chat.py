from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import torch 

# Sumamos los traductores
english_model_name = "Helsinki-NLP/opus-mt-en-es"
spanish_model_name = "Helsinki-NLP/opus-mt-es-en"
translator_en_es = pipeline("translation", model=english_model_name)
translator_es_en = pipeline("translation", model=spanish_model_name)

model_name = 'facebook/blenderbot-400M-distill'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def obtener_respuesta(user_input_es, history):
    # user_input_es = input(">> Ingresar texto:")
    user_input_en = translator_es_en(user_input_es)[0]['translation_text']
    # print(user_input_en)

    new_user_input_ids = tokenizer.encode( user_input_en + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([torch.LongTensor(history), new_user_input_ids], dim=-1)
    history = model.generate(bot_input_ids, 
                             max_length=500, 
                             pad_token_id=tokenizer.eos_token_id,  
                             temperature=0.8).tolist()
    
    response = tokenizer.decode(history[0], skip_special_tokens=True)
    response_es = translator_en_es(response)[0]['translation_text']
    # print(user_input_es)
    # print(response_es)
    return response_es, history