import tkinter as tk
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet

# NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('omw-1.4', quiet=True)

def get_positive_synonyms(word):
    """
    Finds synonyms with a positive connotation for a given word using WordNet,
    aiming to enhance text positivity without changing its original intent.
    """
    synonyms = []  # Initialize an empty list to store potential synonyms
    for syn in wordnet.synsets(word):  # Explore each synonym set for the given word
        for lemma in syn.lemmas():  # Inspect each synonym (lemma) within the set
            # Ensure the synonym is different from the original word and lacks negative antonyms
            if lemma.name().lower() != word and not lemma.antonyms():
                synonyms.append(lemma.name().replace('_', ' '))  # Format and collect synonyms
    return list(set(synonyms))  # Return a unique list of synonyms

def improve_sentence(sentence):
    """
    Enhances a sentence by replacing negative adjectives with positive synonyms,
    thereby improving its overall sentiment.
    """
    words = nltk.word_tokenize(sentence)  # Tokenize the input sentence
    tagged_words = nltk.pos_tag(words)  # Tag each word with its grammatical role
    improved_words = []  # List to hold the modified sentence
    
    for word, tag in tagged_words:
        if tag.startswith('JJ'):  # Focus on adjectives ('JJ' tag)
            analysis = TextBlob(word).sentiment  # Analyze the sentiment of the adjective
            if analysis.polarity < 0:  # Check for negative sentiment
                synonyms = get_positive_synonyms(word)  # Search for positive synonyms
                if synonyms:
                    improved_words.append(synonyms[0])  # Use the first positive synonym found
                else:
                    improved_words.append(word)  # Retain the original word if no synonyms found
            else:
                improved_words.append(word)  # Include positive and neutral adjectives unchanged
        else:
            improved_words.append(word)  # Non-adjective words are included unchanged
    
    return ' '.join(improved_words)  # Reassemble the sentence from the list of words

def analyze_sentiment():
    """
    Analyzes the sentiment of user-provided text, displaying both the numerical score and categorical sentiment,
    and updates the text to reflect a positive tone if necessary.
    """
    user_input = text_input.get("1.0", "end-1c")  # Retrieve text from the user input field
    analysis = TextBlob(user_input)  # Perform sentiment analysis
    polarity = analysis.sentiment.polarity  # Obtain the numerical sentiment score
    
    # Determine the categorical sentiment based on polarity and update the GUI accordingly
    if polarity > 0:
        sentiment_label.set(f"Sentiment: Positive (Score: {polarity:.2f})")
        output_text.set("Text is already positive. No changes needed.")
    elif polarity == 0:
        sentiment_label.set(f"Sentiment: Neutral (Score: {polarity:.2f})")
        output_text.set("Text is neutral. Consider adding more emotional expression.")
    else:
        sentiment_label.set(f"Sentiment: Negative (Score: {polarity:.2f})")
        improved_text = improve_sentence(user_input)  # Improve the sentence if it's negative
        output_text.set("Fixed Text: " + improved_text)

    output_display.config(state='normal')
    output_display.delete("1.0", "end")
    output_display.insert("1.0", output_text.get())
    output_display.config(state='disabled')

def clear_text():
    """
    Clears all interactive fields in the GUI to allow for a fresh start in analyzing new text.
    """
    text_input.delete("1.0", "end")
    output_display.config(state='normal')
    output_display.delete("1.0", "end")
    output_display.config(state='disabled')
    sentiment_label.set("")
    output_text.set("")

# Main window setup
root = tk.Tk()
root.title("Social Media Sentiment Fixer")

# Frames for organizing layout
score_frame = tk.Frame(root)
score_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output_frame = tk.Frame(root)
output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Text input area configuration
text_input = tk.Text(score_frame, height=20, width=40)
text_input.pack()

# Buttons for analyzing and clearing text
analyze_button = tk.Button(score_frame, text="Analyze Sentiment", command=analyze_sentiment)
analyze_button.pack(pady=10)

clear_button = tk.Button(score_frame, text="Clear", command=clear_text)
clear_button.pack()

# Labels and text areas for displaying results
sentiment_label = tk.StringVar()
sentiment_display = tk.Label(score_frame, textvariable=sentiment_label)
sentiment_display.pack()

output_text = tk.StringVar()
output_display = tk.Text(output_frame, height=10, width=50, state='disabled')
output_display.pack()

# Start the GUI event loop
root.mainloop()
