import os
import logging
import torch
from typing import Optional

# Importing with error handling for external libraries
try:
    from datasets import load_dataset
    from transformers import (
        GPT2LMHeadModel, 
        GPT2Tokenizer, 
        Trainer, 
        TrainingArguments
    )
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install the following libraries:")
    print("- datasets")
    print("- transformers")
    print("- torch")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("training.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_model_and_tokenizer(
    model_name: str = "microsoft/DialoGPT-medium"
) -> tuple:
    """
    Load pre-trained model and tokenizer with error handling.
    
    Args:
        model_name (str): Hugging Face model identifier
    
    Returns:
        tuple: (model, tokenizer)
    """
    try:
        # Ensure model directory exists
        os.makedirs("./model_checkpoints", exist_ok=True)
        
        # Load tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained(
            model_name, 
            cache_dir="./model_checkpoints"
        )
        
        # Set pad token to ensure compatibility
        tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        model = GPT2LMHeadModel.from_pretrained(
            model_name, 
            cache_dir="./model_checkpoints"
        )
        
        logger.info(f"Successfully loaded model and tokenizer: {model_name}")
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {e}")
        raise

def load_data(
    dataset_name: str = "daily_dialog", 
    split: str = "train"
) -> Optional[object]:
    """
    Load a dataset with error handling.
    
    Args:
        dataset_name (str): Name of the dataset
        split (str): Dataset split to load
    
    Returns:
        Loaded dataset or None
    """
    try:
        dataset = load_dataset(
            dataset_name, 
            split=split, 
            trust_remote_code=True
        )
        
        if not dataset:
            logger.warning(f"No data found in {dataset_name} dataset")
            return None
        
        logger.info(f"Successfully loaded {dataset_name} dataset")
        return dataset
    
    except Exception as e:
        logger.error(f"Error loading dataset {dataset_name}: {e}")
        raise

def tokenize_data(
    dataset, 
    tokenizer, 
    max_length: int = 512
) -> object:
    """
    Tokenize dataset with error handling.
    
    Args:
        dataset: Input dataset
        tokenizer: Tokenizer to use
        max_length: Maximum sequence length
    
    Returns:
        Tokenized dataset
    """
    try:
        def tokenize_function(examples):
            # Convert dialogues to text, joining dialog parts
            if isinstance(examples['dialog'][0], list):
                # If dialog is a list of lists, join each dialog
                texts = [' '.join(dialog) for dialog in examples['dialog']]
            else:
                # If dialog is already a list of strings
                texts = examples['dialog']
            
            return tokenizer(
                texts, 
                padding="max_length", 
                truncation=True, 
                max_length=max_length,
                return_tensors="pt"
            )
        
        # Prepare the dataset
        tokenized_data = dataset.map(
            tokenize_function, 
            batched=True, 
            remove_columns=dataset.column_names
        )
        
        # Set format for PyTorch
        tokenized_data.set_format(
            type="torch", 
            columns=["input_ids", "attention_mask"]
        )
        
        logger.info("Successfully tokenized dataset")
        return tokenized_data
    
    except Exception as e:
        logger.error(f"Error tokenizing dataset: {e}")
        print(f"Dataset sample: {dataset[0]}")  # Print dataset sample for debugging
        raise

def train_model(
    model, 
    tokenized_data, 
    tokenizer, 
    output_dir: str = "./results"
) -> None:
    """
    Fine-tune the model with comprehensive error handling.
    
    Args:
        model: Model to train
        tokenized_data: Tokenized training dataset
        tokenizer: Tokenizer used
        output_dir: Directory to save model checkpoints
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("./logs", exist_ok=True)
        
        # Prepare training arguments with more robust configuration
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            logging_dir="./logs",
            logging_steps=100,
            save_steps=500,
            evaluation_strategy="steps",
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
        )
        
        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_data,
            eval_dataset=tokenized_data,
            tokenizer=tokenizer,
        )
        
        # Train the model
        logger.info("Starting model training...")
        trainer.train()
        
        # Save the final model
        trainer.save_model(os.path.join(output_dir, "final_model"))
        logger.info("Model training completed successfully!")
    
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise

def main():
    """
    Main function to orchestrate model fine-tuning process.
    """
    try:
        # Load model and tokenizer
        model, tokenizer = load_model_and_tokenizer()
        
        # Load dataset
        dataset = load_data()
        
        # Tokenize data
        tokenized_data = tokenize_data(dataset, tokenizer)
        
        # Train model
        train_model(model, tokenized_data, tokenizer)
    
    except Exception as e:
        logger.error(f"Training process failed: {e}")
        raise

if __name__ == "__main__":
    main()