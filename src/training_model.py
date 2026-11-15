import os
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, Input  # Import Input layer
from tensorflow.keras.preprocessing.image import ImageDataGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
TRAINER_DIR = os.path.join(PROJECT_ROOT, "trainer")

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

dataset_dir = DATASET_DIR

trainer_dir = TRAINER_DIR

model_dir = os.path.join(trainer_dir, "trained_model.h5")

# Ensure required folders exist
assure_path_exists(dataset_dir)
assure_path_exists(trainer_dir)

# Create a data generator
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, vertical_flip=True, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    dataset_dir,
    batch_size=32,
    target_size=(128, 128),
    class_mode='sparse',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    dataset_dir,
    batch_size=32,
    target_size=(128, 128),
    class_mode='sparse',
    subset='validation'
)

# Load the pre-trained model
pretrained_model_path = os.path.join(MODELS_DIR, "base_model.h5")

pretrained_model = load_model(pretrained_model_path)

# Build the model
model = Sequential()
model.add(Input(shape=(128, 128, 3)))  # Add Input layer with the desired shape
for layer in pretrained_model.layers[:-1]:
    model.add(layer)

# Freeze the weights of the pre-trained layers
for layer in model.layers:
    layer.trainable = False

# Add new output layer with a unique name
model.add(Dense(train_generator.num_classes, activation='softmax', name='output_layer'))

# Compile the model
model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(train_generator, epochs=25, validation_data=val_generator, verbose=1)

# Save the model
model.save(model_dir)
