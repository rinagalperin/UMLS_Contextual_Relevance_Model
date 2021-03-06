import tensorflow as tf
from bert.bert_code import run_classifier
from bert.dataloader.contextual_relevance import ContextualRelevance
from bert.umls_classification.cfg import *
from bert.utilty.utilty import model_fn_builder, create_tokenizer_from_hub_module


def get_prediction(in_sentences):
    # labels = ["Negative", "Positive"]
    labels = [0, 1]
    input_examples = [run_classifier.InputExample(guid="", text_a=x[0], text_b=x[1], label=0) for x in
                      in_sentences]  # here, "" is just a dummy label
    input_features = run_classifier.convert_examples_to_features(input_examples, label_list, MAX_SEQ_LENGTH, tokenizer)
    predict_input_fn = run_classifier.input_fn_builder(features=input_features, seq_length=MAX_SEQ_LENGTH,
                                                       is_training=False, drop_remainder=False)
    predictions = estimator.predict(predict_input_fn, checkpoint_path=checkpoint_path)
    return [(sentence, prediction['probabilities'], labels[prediction['labels']]) for sentence, prediction in
            zip(in_sentences, predictions)]


model_fn = model_fn_builder(
    num_labels=len(label_list),
    learning_rate=LEARNING_RATE,
    num_train_steps=num_train_steps,
    num_warmup_steps=num_warmup_steps,
    bert_model_hub=BERT_MODEL_HUB)

estimator = tf.compat.v1.estimator.Estimator(model_fn, params={"batch_size": BATCH_SIZE})
tokenizer = create_tokenizer_from_hub_module(BERT_MODEL_HUB)


_, test = ContextualRelevance(data_flie_path, False).get_data()

data = list(zip(test[DATA_COLUMN].to_list(), test[ANSWER_COLUMN].to_list()))
data[0] = list(data[0])
data[0][0] = 'האם קיים דלקת מעיים חריפה שיכול לעזור לי'
data[0][1] = 'דלקת מעיים חריפה'

data[1] = list(data[1])
data[1][0] = 'האם קיים חיסון לשפעת העופות שיכול לעזור לי'
data[1][1] = 'העופות שיכול לעזור'

data[2] = list(data[2])
data[2][0] = 'האם קיים חיסון לשפעת העופות שיכול לעזור לי'
data[2][1] = 'חיסון לשפעת העופות'

predictions = get_prediction(data)

for i, p in enumerate(predictions):
    #if p[2] != test['Labels'][i]:
    print('sentence: ', p[0][0])
    print('HRM match:',  p[0][1])
    print('UMLS classifier answer:', 'Right' if p[2] else 'Wrong')
    real_answer = p[2] == test['Labels'][i]
    print('classifier success:', real_answer, 'the answer is:', test['Annotations_UMLS'][i])
    print()

