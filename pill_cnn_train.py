import os
import tensorflow as tf

print("Working dir:", os.getcwd())

# No validation_split
datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

dataset_path = os.path.join(os.getcwd(), 'pill_dataset')

# Load ALL images (no split)
train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(64, 64),
    batch_size=1,                 # small batch since dataset is small
    class_mode='binary',
    shuffle=True
)

print("Found training samples:", train_data.samples)

# Define CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train on small dataset
model.fit(train_data, epochs=5)

# Save model
os.makedirs("models", exist_ok=True)
model.save('models/pill_cnn_model.h5')
print("✅ Model trained and saved successfully!")
