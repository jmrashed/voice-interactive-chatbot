# Python Voice Interactive Chatbot
This project is a Python-based conversational AI chatbot that allows voice-based interactions using speech recognition (for input) and text-to-speech (for output). It uses a pre-trained model (DialoGPT) and can be fine-tuned on custom datasets using training.py.



## Video Demonstration

Check out this demonstration of the Python Voice Interactive Chatbot:

[![Watch the video](https://img.youtube.com/vi/4CSBaI247H0/0.jpg)](https://youtu.be/4CSBaI247H0)

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
  - [Code Style](#code-style)
  - [Pull Request Guidelines](#pull-request-guidelines)
- [License](#license)
- [Contact Information](#contact-information)

## Project Description

The **Voice Interactive Chatbot** project is a Python-based conversational AI that allows users to interact with a chatbot via voice commands. Using speech recognition for input and text-to-speech for output, the chatbot can converse with users, answering questions and engaging in dialogue based on a pre-trained model (e.g., DialoGPT). Additionally, the chatbot model can be fine-tuned on custom datasets using `training.py` for personalized responses.

The project consists of two main components:
- **chatbot.py**: The core script that runs the voice interaction logic.
- **training.py**: A script for fine-tuning the chatbot model on custom data to improve its conversational abilities.

This project is available at: [https://github.com/jmrashed/voice-interactive-chatbot.git](https://github.com/jmrashed/voice-interactive-chatbot.git)

## Features

- **Voice Input and Output**: Interact with the chatbot using natural voice commands and receive spoken responses.
- **Conversational Model**: Built using the pre-trained `DialoGPT` model, fine-tuned for better performance.
- **Custom Training**: Use `training.py` to fine-tune the chatbot on a custom dataset for more relevant responses.
- **Speech Recognition**: Recognizes spoken text using Google Speech Recognition API.
- **Text-to-Speech**: Responds to users using Python's `pyttsx3` library.
- **Simple Command to Exit**: Users can exit the chatbot by saying "exit" or "bye".

## Technologies Used

- **Python 3.x**
- **SpeechRecognition** for speech-to-text conversion.
- **pyttsx3** for text-to-speech output.
- **transformers** from Hugging Face for using and fine-tuning the conversational model (DialoGPT).
- **torch** for model training and inference.
- **datasets** from Hugging Face to load conversational datasets.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/jmrashed/voice-interactive-chatbot.git
   cd voice-interactive-chatbot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have `requirements.txt`, you can manually install the dependencies:
   ```bash
   pip install SpeechRecognition pyttsx3 transformers torch datasets
   ```

3. (Optional) Download additional dependencies such as `model weights` if required by your model.

## Usage

### Configuration

You can configure the voice chatbot in two main ways:

- **Model Configuration**: Modify the `training.py` file to use your custom dataset for fine-tuning the model.
- **Speech Settings**: You can change the speech rate, volume, and voice by adjusting the `pyttsx3` engine settings in `chatbot.py`.

### Running the Application

1. To run the chatbot with voice interaction:
   ```bash
   python chatbot.py
   ```

2. To fine-tune the model using a custom dataset:
   ```bash
   python training.py
   ```

   This will train the `DialoGPT` model on the dataset and save the fine-tuned model in the `./results` directory.

## API Documentation

### `chatbot.py`
- **recognize_speech()**: Listens for speech input and converts it into text.
- **speak(response)**: Converts text response into speech and outputs it.
- **chat()**: Main loop for interacting with the chatbot, processing user input, and generating responses.

### `training.py`
- **load_data()**: Loads the dataset for training the model.
- **tokenize_data()**: Tokenizes the conversational data for the model.
- **train_model()**: Fine-tunes the pre-trained chatbot model.

## Testing

### Unit Tests

Unit tests can be written for individual functions. Example:

- Test the **speech-to-text** conversion to verify the recognizer works well.
- Test the **text-to-speech** functionality to ensure the output is correct.

### Integration Tests

- Ensure that the entire pipeline, from speech input to model output and voice response, works as expected.
- Test different conversational scenarios to ensure the chatbot responds properly.

## Deployment

For deploying the chatbot:
- **Local Deployment**: The chatbot can be run locally on your machine using Python.
- **Web Deployment**: You can integrate the chatbot into a web app using a framework like Flask or FastAPI.
- **Cloud Deployment**: You can deploy it to cloud platforms like AWS, GCP, or Azure using Docker containers.

## Contributing

### Code Style

Please follow the **PEP 8** Python coding standards when contributing to the project.

### Pull Request Guidelines

- Fork the repository and create a new branch.
- Make changes in your branch.
- Ensure that your changes don't break existing functionality by testing the system.
- Submit a pull request with a clear description of the changes and why they were made.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information

For any inquiries or suggestions, you can reach out to:
- **Email**: jmrashed@gmail.com
- **GitHub**: [github.com/jmrashed](https://github.com/jmrashed)
- **Website**: [rasheduzzaman.com](https://rasheduzzaman.com) 