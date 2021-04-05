from summarizer import Summarizer
from transformers import *
custom_config = AutoConfig.from_pretrained('config.json')
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained('vocab.txt')
custom_model = AutoModel.from_pretrained('bert-large-uncased-pytorch_model.bin', config=custom_config)
body="aasadasda sad asda"
model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer, sentence_handler=handler)
print(model(body, num_sentences=3))