# Arabic to English Translation
Hi! سلام!

Machine translation is a specialized area within computational linguistics that is dedicated to the automated conversion of text in one language to another language. In this process, the input text is already composed of symbols from a particular language, and the machine translation program must convert these symbols into symbols that correspond to another language.

Neural machine translation (NMT) is a machine translation approach that involves using an artificial neural network to predict the probability of a sequence of words. This method typically employs a single integrated model to generate translations of entire sentences. Due to the capabilities of neural networks, NMT has become the most powerful algorithm for machine translation. This cutting-edge algorithm utilizes deep learning techniques, where large datasets of translated sentences are utilized to train a model that can effectively translate between any two languages.

To date, limited research has been conducted in the area of Arabic language processing. Here, a Recurrent Neural network (RNN) was built to to translate Arabic text into English using Keras. 

Preprocess
For this project, the text will be converted into sequence of integers using the following preprocess methods: 

1- Tokenize the words into ids

2- Add padding to make all the sequences the same length.

### Tokenization

In order for a neural network to perform predictions on text data, the text must first be transformed into a format that the network can comprehend. Text data, such as "dog," is essentially a sequence of ASCII character encodings, which is not directly compatible with the multiplication and addition operations of a neural network. Therefore, the input data needs to be represented as numbers.

To achieve this, one can either assign a unique numerical value to each character or each word in the text data. The former is known as character ids, while the latter is referred to as word ids. Character ids are typically used for models that make predictions on a character-by-character basis, whereas word ids are utilized in models that generate predictions for each word in the text. Word-level models are generally preferred since they are less complex and tend to learn more effectively. Consequently, we will use word ids for our model.

### Padding

When processing a sequence of word ids in batches, it is necessary for each sequence to have the same length. As sentences in a text corpus can vary in length, it is possible to achieve uniformity in sequence length by adding padding at the end of each sequence. This way, all sequences will have the same length, making it easier for the neural network to process them.

### Predictions 

Convert back the final prediction by our model into text format.

# Results 
Translation from Arabic to English

![Capture](https://user-images.githubusercontent.com/39967400/226687796-914205c0-5ec7-4963-b9ab-e3874a4a6da9.PNG)

