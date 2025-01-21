import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Step 1: Load the GGUF model (if possible) or convert it to Hugging Face format
# Note: You may need to use a tool like `llama.cpp`'s conversion scripts to export the model to Hugging Face format.

#model in huggingface_model format
model_name = "path_huggingface_model"  # Replace with the path to your converted model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Step 2: Load new data for fine-tuning
new_data = pd.read_csv("data/new_sql_data.csv")

# Convert the data to a Hugging Face Dataset
dataset = Dataset.from_pandas(new_data)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["prompt"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Step 3: Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",          # Directory to save the fine-tuned model
    per_device_train_batch_size=4,  # Batch size for training
    num_train_epochs=3,             # Number of training epochs
    logging_dir="./logs",           # Directory for logs
    save_steps=500,                 # Save model every 500 steps
    save_total_limit=2,             # Keep only the last 2 saved models
    evaluation_strategy="steps",    # Evaluate every few steps
    eval_steps=500,                 # Evaluation frequency
    learning_rate=5e-5,             # Learning rate
    weight_decay=0.01,              # Weight decay
)

# Step 4: Fine-tune the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# Step 5: Save the fine-tuned model
trainer.save_model("models/finetuned_sql_model")
tokenizer.save_pretrained("models/finetuned_sql_model")

# Step 6: (Optional) Convert the fine-tuned model back to GGUF format
# Use a conversion script (e.g., from llama.cpp) to convert the Hugging Face model back to GGUF.