import os.path

def parse_scores(write_dir):
    scores = []
    with open(os.path.join(write_dir,"rigid.out_scored.mol2"), "r") as f:
          line = f.readline()
          while line:
              if('Contact_Score' in line):
                  line = line.rstrip('\n')
                  sc = float(line[-20:])
                  if(sc>0):
                      sc=-sc
                  scores.append(sc)
              line = f.readline()
       
    print(len(scores), ' scores found')
    return scores
