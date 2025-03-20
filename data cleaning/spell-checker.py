import unicodedata
import re
import Levenshtein
from unidecode import unidecode


# Function to extract words and punctuation while keeping track of spaces
def extract_words_and_punctuation(sentence):
    return re.findall(r'\b\w+\b|[^\w\s]|\s+', sentence)


# Function to normalize text (remove or standardize diacritics and handle case insensitivity)
def normalize_text(text):
    # Decompose the text into base characters and diacritics, and convert to lowercase
    return unicodedata.normalize('NFD', text).lower()

# Function to load the misspelled words and correct words into a dictionary
def load_spelling_dict(misspelled_file, correct_file):
    # Read the misspelled words and the correct spellings
    with open(misspelled_file, 'r', encoding='utf-8') as f_misspelled:
        misspelled_words = [line.strip() for line in f_misspelled.readlines()]

    with open(correct_file, 'r', encoding='utf-8') as f_correct:
        correct_words = [line.strip() for line in f_correct.readlines()]

    # Create a dictionary mapping normalized misspelled words to correct words
    spelling_dict = {normalize_text(misspelled): correct for misspelled, correct in
                     zip(misspelled_words, correct_words)}
    return spelling_dict

# Function to load the correct words into a set (for fast lookup)
def load_spellings(correct_file):
    with open(correct_file, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f}


# Get the closest matches using Levenshtein distance
def spell_check(word, correct_words, max_distance=2):
    word = unidecode(word).lower() # Normalize the word
    distances = {correct_word: Levenshtein.distance(word, unidecode(correct_word)) for correct_word in correct_words}

    # Find the minimum distance
    min_distance = min(distances.values(), default=max_distance + 1)

    # Return words with the minimum distance, only if it's within the threshold
    if min_distance <= max_distance:
        return [correct_word for correct_word, dist in distances.items() if dist == min_distance]
    return []


# Function to check and correct a word while preserving its original case
def correct_spelling(word, correct_words, spelling_dict, corrected_words, not_found_words, is_first_word):
    # Skip correction for numbers or capitalized words that are not the first word
    if word.isdigit() or (word[0].isupper() and not is_first_word):
        return word

    # Normalize the input word for comparison
    normalized_word = unidecode(normalize_text(word))

    if normalized_word.lower() in spelling_dict:
        corrected_word = spelling_dict[normalized_word]
    else:
        # Otherwise, try to find the closest match using Levenshtein distance
        suggestions = spell_check(normalized_word, correct_words)
        if len(suggestions) == 1:
            corrected_words[word] = suggestions[0]
            corrected_word = suggestions[0]
            spelling_dict[normalized_word] = corrected_word

        elif len(suggestions) > 1:
            # Optional: Handle case where there are multiple suggestions (can return original word or choose one)
            corrected_words[word+"*"] = suggestions[0]
            corrected_word = suggestions[0]
        else:
            # If no suggestion found, return the word and mark it as not found
            corrected_word = word
            not_found_words.add(word)

    if word.isupper():
        corrected_word = corrected_word.upper()
    elif word[0].isupper():
        corrected_word = corrected_word.capitalize()

    return corrected_word


# Function to check and correct words in a sentence while preserving punctuation and spaces
def check_and_correct_sentence(sentence, correct_words, spelling_dict, corrected_words, not_found_words):
    parts = extract_words_and_punctuation(sentence)
    corrected_parts = []
    is_first_word = True

    for part in parts:
        if part.isalnum():  # Only correct alphanumeric words
            corrected_parts.append(
                correct_spelling(part, correct_words, spelling_dict, corrected_words, not_found_words, is_first_word))
            is_first_word = False  # After the first word, set this flag to False
        else:
            corrected_parts.append(part)  # Keep punctuation and spaces as is

    return ''.join(corrected_parts)


# Function to check and correct sentences loaded from a file
def correct_sentences_from_file(input_file, correct_words, spelling_dict):
    corrected_sentences = []
    not_found_words = set()
    corrected_words = {}

    with open(input_file, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f.readlines()]

    for sentence in sentences:
        corrected_sentence = check_and_correct_sentence(sentence, correct_words, spelling_dict, corrected_words, not_found_words)
        corrected_sentences.append(corrected_sentence)

    return corrected_sentences, corrected_words, not_found_words


# Example usage
if __name__ == '__main__':
    correct_file = 'target.txt'
    misspelled_file = 'source.txt'
    input_file = 'folklit.txt'

    # Load the correct words (a set for fast lookup)
    correct_words = load_spellings(correct_file)

    # Load the spelling dictionary
    spelling_dict = load_spelling_dict(misspelled_file, correct_file)

    # Correct the sentences and get the not-found words
    corrected_sentences, corrected_words, not_found_words = correct_sentences_from_file(input_file, correct_words, spelling_dict)


    # Print out the corrected sentences
    print("Corrected Sentences:")
    for idx, sentence in enumerate(corrected_sentences, start=1):
        print(f"{sentence}")

    # Print out the words that were corrected, sorted alphabetically
    print(f"\nWords corrected ({len(corrected_words)}):")
    for idx, (key, value) in enumerate(sorted(corrected_words.items()), start=1):
        print(f"{idx}. {key}: {value}")

    # Print out the words that were not found
    print(f"\nWords not found in the dictionary ({len(not_found_words)}):")
    for idx, word in enumerate(sorted(not_found_words), start=1):
        print(f"{idx}. {word}")