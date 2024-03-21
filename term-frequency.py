import nltk
from nltk.corpus import stopwords
#nltk.download("punkt")
#nltk.download("stopwords")

# Class definition for student
class Student:

    def __init__(self, student_id, hobby):
        # to store student's id
        self.student_id = student_id
        # to store hobby text
        self.hobby = hobby
        # to store tokens from student's hobby text
        self.tokens = []
        # a dictionary to store term frequency of a student's hobby
        self.term_frequency = {}

    # removes periods and commas from a list of tokens and save filtered tokens to self.tokens
    def removePeriods(self):
        # removes periods and commas until all of them are removed from token
        # remove method of list can remove only the first item in the list
        while "," in self:
            self.tokens.remove(",")
        while "." in self:
            self.tokens.remove(".")
        return self.tokens


    # convert all tokens to lower cases and save filtered tokens to self.tokens
    def convertLower(self):
        length = len(self.tokens)
        for num in range(length):
            self.tokens[num] = self.tokens[num].lower()
        return self.tokens


    # remove stopwords from tokens and save filtered tokens to self.tokens
    def removeStopWords(self):
        # create stopwords list
        stop_words = stopwords.words("english")

        tokens_filtered = []

        for t in self.tokens:
            if t not in stop_words:
                tokens_filtered.append(t)
        return tokens_filtered

    # calculate term frequency for student's hobby text and save it to self.term_frequency
    def calTermFreq(self):
        term_freq = {}
        for key in self.tokens:
            if key not in term_freq:
                term_freq[key] = 1
            elif key in term_freq:
                term_freq[key] += 1

        return term_freq


    # create tokens for student's hobby text
    def setTokens(self):
        self.tokens = nltk.word_tokenize(self.hobby)

class Document:
    def __init__(self):
        # a dictionary to store term frequency for all students. A nested dictionary
        self.term_frequency_per_doc = {}
        # a dictionary to store document frequency
        self.doc_frequency = {}
        # to store a file object
        self.file = None
        # to save objects of students. The program append student's object to this list
        self.student_list = []
        # to control the index of student_list when the program refer to a specific object in the list
        self.index = 0

    # calculate document frequency and set it to self.doc_frequency
    def calDocFreq(self):
        for key in self.student_list.term_frequency:
            if key not in self.doc_frequency:
                self.doc_frequency[key] = 1
            elif key in self.doc_frequency:
                self.doc_frequency[key] += 1



    # control file opening and check whether file name is correct
    def readDataFromFile(self):
        # Prime the loop to read file
        file_name = None

        while (file_name == None):
            try:
                # Assuming no exceptions, we read in all lines of the file and return the iterable.  Exceptions are caught
                # and the user is asked to re-enter the file name.
                file_name = input("Please enter the name of the input data file: ")
                self.file = open(file_name, "r")

            except FileNotFoundError:
                file_name = None
                print("The file you requested was not found.  Please try again.\n")

    # control the program
    def processData(self):
        # Process all input data lines, 2 at a time.
        index = 0
        for line in self.file:
            try:
                if index % 2 == 0:
                    student_id = line.rstrip()
                else:
                    hobby_text = line.rstrip()
            except Exception as err:
                print("Error in parsing input data file. Aborting.",sep="")
                print(err)
                return

            # Do all text processing such as tokenizing, removing periods and commas, etc.
            # Also do counting term frequency and document frequency.
            if index % 2 == 1:
                # Create new Student object and append it to the student_list attribute
                self.student_list.append(Student(student_id, hobby_text))

                ## More parts should be implemented.
                # tokenize hobby text
                tokens = nltk.word_tokenize(hobby_text)

                # removes periods and commas from a list of tokens
                tokens = self.student_list.removePeriods(tokens)

                # convert all tokens to lower cases
                tokens = self.student_list.convertLower(tokens)

                print("This is tokens")
                print(tokens)

                # remove stopwords from tokens
                print("This is tokens_filtered")
                #tokens_filtered = removeStopWords(tokens)
                #removeStopWords(tokens)
                tokens_filtered = self.student_list.removeStopWords()   # changed to return list
                print(tokens_filtered)

                # calculate term frequency for student's hobby text
                #print("This is term_freq")
                self.student_list.term_frequency = self.student_list.calTermFreq()
                print(self.student_list.term_frequency)

                # Map the created term frequency for each student to the outer dictionary in the nested dictionary
                # For each student_id (key), value is its dict of term_frequency
                print("This is term_frequency_per_doc")
                # Map the term_frequency dictionary to each student_id key making a nested dictionary
                self.term_frequency_per_doc[student_id] = self.student_list.term_frequency
                # Print the nested dictionary
                print(self.term_frequency_per_doc)

                # calculate document frequency
                # num lines word shows up
                print("This is doc_frequency")
                doc_frequency = self.calDocFreq()
                print(doc_frequency)

    # function for search and display
    def searchWord(self):
        user_token = input("Enter a word to search: ")

        # Loop over each key in the dictionary of dictionaries
        for key in self.term_frequency_per_doc:
            # Check if the search key is in the inner dictionary
            if user_token in self.term_frequency_per_doc[key]:
                # If the search key is found, print the corresponding key
                print(self.term_frequency_per_doc[key])



# The main function for this program which orchestrates the overall process.
def main():
    doc = Document()

    # Open the grade file for reading and retrieve all lines in the file.
    doc.readDataFromFile()

    # Run a method that control most parts of the program
    doc.processData()

    # Run a method of user input and display
    doc.searchWord()


# Run the program!
main()
