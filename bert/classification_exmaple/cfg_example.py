DATA_COLUMN = 'sentence'
LABEL_COLUMN = 'polarity'

# label_list is the list of labels, i.e. True, False or 0, 1 or 'dog', 'cat'
label_list = [0, 1]

OUTPUT_DIR = '../output_model'  # @param {type:"string"}
checkpoint_path = '../output_model/model.ckpt-468'
BERT_MODEL_HUB = "https://tfhub.dev/google/bert_multi_cased_L-12_H-768_A-12/1"

BATCH_SIZE = 32
LEARNING_RATE = 2e-5
NUM_TRAIN_EPOCHS = 3.0
# Warmup is a period of time where hte learning rate
# is small and gradually increases--usually helps training.
WARMUP_PROPORTION = 0.1
# Model configs
SAVE_CHECKPOINTS_STEPS = 500
SAVE_SUMMARY_STEPS = 100
# Compute # train and warmup steps from batch size
num_train_steps = 0
num_warmup_steps = int(num_train_steps * WARMUP_PROPORTION)

# utilty'll set sequences to be at most 128 tokens long.
MAX_SEQ_LENGTH = 128

