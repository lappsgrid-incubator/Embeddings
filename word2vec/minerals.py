filepath2 = '/Users/ide/Dropbox/inProgress/Livny-project/experiment/lists/common_intervals.txt'
filepath1 = '/Users/ide/Dropbox/inProgress/Livny-project/experiment/lists/common_minerals.txt'

with open(filepath1) as fp1:  
   mineral = fp1.readline().replace('\n', '')
   while mineral:
        if mineral in model.wv.vocab:
            print(mineral,end = '\t')
            with open(filepath2) as fp2:
                interval = fp2.readline().replace('\n', '')
                while interval:
                    if interval in model.wv.vocab:
                        print(model.wv.similarity(interval,mineral),end = '\t')
                    interval = fp2.readline().replace('\n', '')
                print('\n')
        mineral = fp1.readline().replace('\n', '')
