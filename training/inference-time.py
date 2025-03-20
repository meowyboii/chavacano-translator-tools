import time
import pandas as pd
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, AutoTokenizer, AutoModelForSeq2SeqLM

def load_model_and_tokenizer():
    mbart_path = 'D:/Downloads/JN/mbart_finetuned_2e-4_16/checkpoint-326'
    mbart_model = MBartForConditionalGeneration.from_pretrained(mbart_path).to("cuda")
    mbart_tokenizer = MBart50TokenizerFast.from_pretrained(mbart_path)

    helsinki_path = 'D:/Downloads/JN/helsinki_finetuned_1e-4_16/checkpoint-574'
    helsinki_model = AutoModelForSeq2SeqLM.from_pretrained(helsinki_path).to("cuda")
    helsinki_tokenizer = AutoTokenizer.from_pretrained(helsinki_path)

    return mbart_model, mbart_tokenizer, helsinki_model, helsinki_tokenizer

mbart_model, mbart_tokenizer, helsinki_model, helsinki_tokenizer = load_model_and_tokenizer()

test_file = "test.csv"
df = pd.read_csv(test_file, encoding="latin1")

# Warm-up phase
dummy_input = "test"
mbart_model.generate(**mbart_tokenizer(dummy_input, return_tensors="pt").to("cuda"), forced_bos_token_id=mbart_tokenizer.convert_tokens_to_ids("<cbk_XX>"))
helsinki_model.generate(**helsinki_tokenizer(dummy_input, return_tensors="pt").to("cuda"))

averageMbart = 0
averageHelsinki = 0

for index, row in df.iterrows():
    input_text = row['source']

    # Helsinki NLP Translation and Timing
    start_time_helsinki = time.time()
    inputs = helsinki_tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = helsinki_model.generate(**inputs)
    translated_text_helsinki = helsinki_tokenizer.decode(outputs[0], skip_special_tokens=True)
    end_time_helsinki = time.time()
    inference_time_helsinki = end_time_helsinki - start_time_helsinki

    # mBART50 Translation and Timing
    start_time_mbart = time.time()
    inputs = mbart_tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = mbart_model.generate(**inputs, forced_bos_token_id=mbart_tokenizer.convert_tokens_to_ids("<cbk_XX>"))
    translated_text_mbart = mbart_tokenizer.decode(outputs[0], skip_special_tokens=True)
    end_time_mbart = time.time()
    inference_time_mbart = end_time_mbart - start_time_mbart

    print(f"mBART Inference Time: {inference_time_mbart:.4f} seconds")
    print(f"Helsinki Inference Time: {inference_time_helsinki:.4f} seconds")
    averageMbart += inference_time_mbart
    averageHelsinki += inference_time_helsinki

print(f"mBART Average Inference Time: {averageMbart/len(df):.4f} seconds")
print(f"Helsinki Average Inference Time: {averageHelsinki/len(df):.4f} seconds")