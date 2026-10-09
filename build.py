"""Parse theory_questions.txt and theory_answers.txt into data.js for index.html."""
import hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = 'אבגד'

def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()

answers = {}
for line in read('theory_answers.txt').splitlines()[2:]:
    m = re.match(r'(\d+)\. ([אבגד]) - ', line)
    answers[int(m.group(1))] = LETTERS.index(m.group(2))

questions = []
for block in re.split(r'\n(?=שאלה \d+\.)', read('theory_questions.txt'))[1:]:
    m = re.match(r'שאלה (\d+)\. (.*)', block)
    qid = int(m.group(1))
    topic = re.search(r'\[נושא: ([^|]+?) \|', block).group(1)
    tags = re.search(r'סוגי רישיון: ([^\]]*)\]', block).group(1)
    # The source uses Cyrillic 'В' (U+0412) for license B; normalize to Latin.
    licenses = [t.strip().replace('\u0412', 'B') for t in tags.split(',')]
    img = re.search(r'^תמונה: (.*)$', block, re.M)
    options = re.findall(r'^   [אבגד]\. (.*)$', block, re.M)
    assert len(options) == 4, qid
    questions.append({
        'id': qid,
        'text': m.group(2).strip(),
        'topic': topic,
        'licenses': licenses,
        'image': img.group(1).strip() if img else None,
        'options': options,
        'answer': answers[qid],
    })

assert len(questions) == len(answers)
with open(os.path.join(HERE, 'data.js'), 'w', encoding='utf-8') as f:
    f.write('window.QUESTIONS = ')
    json.dump(questions, f, ensure_ascii=False)
    f.write(';\n')
# Bump the data.js?v= cache-buster in index.html so browsers never pair new code with stale data.
with open(os.path.join(HERE, 'data.js'), 'rb') as f:
    version = hashlib.sha1(f.read()).hexdigest()[:10]
page = os.path.join(HERE, 'index.html')
with open(page, encoding='utf-8') as f:
    html = re.sub(r'data\.js\?v=\w+', f'data.js?v={version}', f.read())
with open(page, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'wrote {len(questions)} questions to data.js (v={version})')
