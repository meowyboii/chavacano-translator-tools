# Function to extract words ending with a colon from a text file
def extract_words_with_colon(file_path):
    # Initialize an empty list to store the words
    words_with_colon = []

    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read each line of the file
        for line in file:
            # Split the line into words
            words = line.split()
            # Check each word if it ends with a colon
            for word in words:
                if word.endswith(':'):
                    # Store the word (removing the colon)
                    words_with_colon.append(word[:-1])

    return words_with_colon


def output_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as output_file:
        for word in words:
            output_file.write(f"{word}\n")

file_path = 'sample.txt'
output_path = 'output.txt'
words = extract_words_with_colon(file_path)
output_words(output_path, words)

print(words)