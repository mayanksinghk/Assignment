import sys

class Evaluate:

    def __init__(self):
        self.time = 0
        self.vocab_len = 0
        self.V = {}
        self.K = 0
        self.gene_seqs = []
        self.CC = 0
        self.MC = []
        
    def read_input(self, fname):

        with open(fname, 'r') as f:
            try:
                self.time = float(f.readline().strip())
                self.len_vocab = int(f.readline().strip())
                vocab = f.readline().strip().split(',') # split on comma and strip the spaces
                for i in range(self.len_vocab):
                    self.V[i] = vocab[i].strip()
                self.K = int(f.readline().strip())
                for i in range(self.K):
                    self.gene_seqs.append(f.readline().strip())
                self.CC = float(f.readline().strip())
                for i in range(self.vocab_len + 1):
                    self.MC.append(list(map(float, f.readline().strip().split())))
            except:
                print("Error while reading Input!")
            
    def create_output(self, fname):

        with open(fname, 'w') as f:
            max_len = 0
            for i in self.gene_seqs:
                max_len = max(max_len, len(i))
            
            for i in range(len(self.gene_seqs)):
                f.write(self.gene_seqs[i] + '-'*(max_len-len(self.gene_seqs[i])) + '\n')
    

if __name__ == "__main__":

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    soln = Evaluate()
    soln.read_input(input_file_name)
    soln.create_output(output_file_name)