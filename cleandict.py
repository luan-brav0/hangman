with open('english.txt', encoding='utf-8', mode='r') as e, open('dictionary.txt', encoding='utf-8', mode='w') as d:
    for w in e:
        w = w.strip()
        if " " in w or (w[0].isalpha() == False or w[-1].isalpha() == False):
            continue
        d.write(w + '\n')
        
print(f"Completed with {len(open('dictionary.txt', encoding='utf-8').readlines())} from {len(open('english.txt', encoding='utf-8').readlines())}" )
