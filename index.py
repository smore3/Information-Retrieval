#Python 3.5.2
import re
import os
import collections
import time

class index:
    def __init__(self,path):
        self.path = path
        self.index=index
        self.buildIndex()

    def tokenize(self,line):
        lines = str(line.lower().split())
        tokens = re.sub(r'[^A-Za-z ]+', '', lines)
        return tokens

    def buildIndex(self):
        """
        function to read documents from collection, tokenize and build the index with tokens
        index should also contain positional information of the terms in the document --- term: [(ID1,[pos1,pos2,..]), (ID2, [pos1,pos2,…]),….]
        use unique document IDs
        """
        start=time.time()
        self.index =collections.defaultdict(list)
        self.map_filename,i=[],0                  #mapping of the document ID to the filename

        for filename in os.listdir(self.path):
            self.map_filename.append(filename)    #append the filename to the mapping array
            with open(self.path+filename,'r') as f:
                doc = f.read()
                tokens = self.tokenize(doc)
                doc_pos = collections.defaultdict(list)    #dictionary which contains the docID and the positions
                for pos,term in enumerate(tokens.split()):
                        doc_pos[term].append(pos)

                for term,pos in doc_pos.items():
                    self.index[term].append((self.map_filename.index(filename),pos))  #insert the docID and the above dictionary into index
            i+=1

        print("Index built in ",time.time()-start,"seconds")


    def and_query(self, query_terms):
        """
        #function for identifying relevant docs using the index
        """
        start = time.time()
        rel_docs = []                               #documents retrived for given query terms
        docs_counter = [0]*len(self.map_filename)   #contains the count for terms in query_terms i.e. the value indicate number of query terms 	                                                   occured in that particular document
        max_len = len(query_terms)                  #Document which contains all the required query terms (i.e max_len) is the relevant document

        for term in query_terms:
            term_list = [doc[0] for doc in self.index[term]] #get the docID and posting list for the query term
            for document in term_list:
                docs_counter[document]+=1

        for pos,val in enumerate(docs_counter):
            if val == max_len:
                rel_docs.append(self.map_filename[pos])

        rel_docs = [str(i) for i in rel_docs]
        print("Results for the Query: "," AND ".join(query_terms))
        print("Total Docs retrieved: ",len(rel_docs))
        print('\n'.join(rel_docs))
        print("Retrieved in ",time.time() - start," seconds")


    def print_dict(self):
        """
        #function to print the terms and posting list in the index
        """
        for key,value in sorted(self.index.items()):
            print(key,value)

    def print_doc_list(self):
        """
        # function to print the documents and their document id
        """
        for pos,val in enumerate(self.map_filename):

            print("Doc ID:",pos,"==>",val)

    #---------------------------------------------EXTRA WORK-----------------------------------------#
    """
    The following logic is similar to one taught in class, though it runs little slower
    """

    def merge(self,list1,list2):
        result = []
        c1,c2 = 0,0   #counters for the two lists
        while True:
                if c1<len(list1) and c2<len(list2):  #iterate until we reach end of one of the lists
                    if list1[c1] == list2[c2]:
                        result.append(list1[c1])
                        c1+=1
                        c2+=1
                    elif list1[c1]<list2[c2]:
                        c1+=1
                    elif list1[c1]>list2[c2]:
                        c2+=1
                else:
                    return result
        return result

    def and_query_1(self, query_terms):
        start = time.time()
        rel_docs,rel = [], []                               #documents retrived for given query terms

        for term in query_terms:
            term_list = [doc[0] for doc in self.index[term]] #get the docID and posting list for the query term
            rel_docs.append(term_list)

        rel_docs.sort(key = len)
        #print(rel_docs)
        for i,list in enumerate(rel_docs):
            if i==0:
                result = self.merge(rel_docs[i],rel_docs[i+1])

            if i>=2:
                result = self.merge(result,rel_docs[i])

        #for i in result:
        #    rel.append(self.map_filename[i])

        rel = [str(self.map_filename[i]) for i in result]
        print("Results for the Query: ", " AND ".join(query_terms))
        print("Total Docs retrieved: ", len(rel))
        print('\n'.join(rel))
        print("Retrieved in ", time.time() - start, " seconds")

""""
def main():
    ind=index('/home/sheetal/PycharmProjects/Information_Retrieval/collection/')
    ind.and_query(['with','without','yemen','yemeni'])
    x=a.and_query(['nuclear', 'power', 'country','war','communist'])
    ind.print_dict()


if __name__ == '__main__':
    main()
"""
