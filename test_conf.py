import pandas as pd

df = pd.read_csv('dataset/smartphones.csv')
brand = 'ObscureBrand'
ram = 3
storage = 16
processor = 'UnknownProcessor Gen X'

brand_matches = (df['Brand'] == brand).sum()
spec_matches = ((df['RAM'] == ram) & (df['Storage'] == storage)).sum()

proc_words = processor.split()
if len(proc_words) >= 2:
    proc_tier = f"{proc_words[0]} {proc_words[1]}"
elif len(proc_words) == 1:
    proc_tier = proc_words[0]
else:
    proc_tier = ''

proc_matches = df['Processor'].astype(str).str.contains(proc_tier, case=False, na=False, regex=False).sum()

confidence = 65.0
confidence += min(10.0, (brand_matches / 40.0) * 10.0)
confidence += min(10.0, (spec_matches / 60.0) * 10.0)
confidence += min(11.0, (proc_matches / 30.0) * 11.0)

confidence = int(round(confidence))
confidence = max(65, min(96, confidence))

print(f'Brand matches: {brand_matches}')
print(f'Spec matches: {spec_matches}')
print(f'Proc tier: {proc_tier}, matches: {proc_matches}')
print(f'Confidence: {confidence}')
