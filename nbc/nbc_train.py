import csv, json, nltk, string, sys


def error(name):
    '''
    Print out the error and exit the program with -1
    input: name is the name of the error
    '''
    print(name, file=sys.stderr)
    exit(-1)


# Tokenize the list value
def tokenize(value):
    words = []
    for word in value:
        # Lemmatize the word
        word = word.translate(str.maketrans('', '', string.punctuation)).lower()
        word = nltk.WordNetLemmatizer().lemmatize(word)
        # Remove punctuations and make all words lower case
        words.append(word)
    return words


# classes = ['business','entertainment','politics','sport','tech']

#calc priors

class Train:
    def __init__(self,corpus):
        self.corpus = corpus
        self.priorList = []
        self.likelihoods = []
        self.vocab = []
        self.vocabCounts={}

    def getVocab(self):
        for document in self.corpus:
            for term in document['text'].split(): 
                self.vocab.append(term)
        
        for term in self.vocab:
            if term not in self.vocabCounts:
                self.vocabCounts[term] = {'business':0,'entertainment':0,'politics':0,'sport':0,'tech':0,'Total':0}

        for document in self.corpus:
            for term in document['text'].split():
                if document['category'] =='business':
                    self.vocabCounts[term]['business']+=1
                    self.vocabCounts[term]['Total']+=1
                if document['category'] =='entertainment':
                    self.vocabCounts[term]['entertainment']+=1
                    self.vocabCounts[term]['Total']+=1
                if document['category'] =='politics':
                    self.vocabCounts[term]['politics']+=1
                    self.vocabCounts[term]['Total']+=1
                if document['category'] =='sport':
                    self.vocabCounts[term]['sport']+=1
                    self.vocabCounts[term]['Total']+=1
                if document['category'] =='tech':
                    self.vocabCounts[term]['tech']+=1
                    self.vocabCounts[term]['Total']+=1



    def getPrior(self, writer):

        busTotal=0
        entertainTotal=0
        poliTotal = 0
        sportTotal=0
        techTotal = 0
        docTotal = 0
        for document in self.corpus:
            if document['category'] =='business':
                busTotal+=1
                docTotal+=1
            if document['category'] =='entertainment':
                entertainTotal+=1
                docTotal+=1
            if document['category'] =='politics':
                poliTotal+=1
                docTotal+=1
            if document['category'] =='sport':
                sportTotal+=1
                docTotal+=1
            if document['category'] =='tech':
                techTotal+=1
                docTotal+=1
        

        self.busPrior= busTotal/docTotal
        self.entertainPrior = entertainTotal/docTotal
        self.poliPrior = poliTotal/docTotal
        self.sportPrior=sportTotal/docTotal
        self.techPrior= techTotal/docTotal
        
        self.priorList = [{'business':self.busPrior},{'entertainment':self.entertainPrior},{'politics':self.poliPrior},{'sport':self.sportPrior},{'tech':self.techPrior}]
        writer.writerow(['prior','business',self.busPrior])
        writer.writerow(['prior','entertainment',self.entertainPrior])
        writer.writerow(['prior','politics', self.poliPrior])
        writer.writerow(['prior','sports',self.sportPrior])
        writer.writerow(['prior','tech',self.techPrior])
    #calc likelihood:

    def getLikelihood(self, writer):
        
        for term in self.vocabCounts:
         

            docType=['null',0]

            if self.vocabCounts[term]['business']>docType[1]:
                docType=[['business'],self.vocabCounts[term]['business']]
            if self.vocabCounts[term]['entertainment']>docType[1]:
                docType=[['entertainment'],self.vocabCounts[term]['entertainment']]
            if self.vocabCounts[term]['politics']>docType[1]:
                docType=[['politics'],self.vocabCounts[term]['politics']]

            if self.vocabCounts[term]['sport']>docType[1]:
                docType=[['sport'],self.vocabCounts[term]['sport']]
            if self.vocabCounts[term]['tech']>docType[1]:
                docType=[['tech'],self.vocabCounts[term]['tech']]
            
            writer.writerow(['Likelihood',docType[0][0],term,self.vocabCounts[term][docType[0][0]]/self.vocabCounts[term]['Total']])


def main():
    # Get the arguments and validate the number of arguments
    arguments = sys.argv
    if len(arguments) != 3:
        error("Invalid arguments")

    inputName = arguments[1]
    outputName = arguments[2]

    print(inputName, outputName)

    # Open the input json file for read
    try:
        inputFile = open(inputName, 'r')
    except IOError:
        error('Invalid file arguments')

    # Load and parse json data
    inputData = json.load(inputFile)
    inputFile.close()

    # Open the output file for write
    try:
        outputFile = open(outputName, 'w', newline='')
    except IOError:
        error('Invalid file arguments')
    theWriter = csv.writer(outputFile, delimiter='\t')

    train = Train(inputData)

    train.getVocab()
    train.getPrior(theWriter)
    train.getLikelihood(theWriter)
    outputFile.close()


if __name__ == "__main__":
    main()

    print('\nDone\n')
