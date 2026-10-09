"""Parse the per-language question/answer text files into data_<lang>.js for index.html."""
import hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

# File suffix and the labels each language's text files use.
LANGS = {
    'he': dict(suffix='', q='שאלה', topic='נושא', lic='סוגי רישיון', img='תמונה', letters='אבגד',
               topics={'חוקי התנועה': 'laws', 'בטיחות': 'safety', 'תמרורים': 'signs', 'הכרת הרכב': 'vehicle'}),
    'en': dict(suffix='_en', q='Question', topic='Topic', lic='Licenses', img='Image', letters='ABCD',
               topics={'Traffic laws': 'laws', 'Safety': 'safety', 'Traffic signs': 'signs', 'Know your vehicle': 'vehicle'}),
    'ar': dict(suffix='_ar', q='سؤال', topic='الموضوع', lic='أنواع الرخص', img='صورة', letters='أبجد',
               topics={'قوانين المرور': 'laws', 'السلامة على الطرق': 'safety', 'إشارات المرور': 'signs', 'معرفة المركبة': 'vehicle'}),
}

def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()

def parse(L):
    letters = L['letters']
    answers = {}
    for line in read(f"theory_answers{L['suffix']}.txt").splitlines()[2:]:
        m = re.match(rf'(\d+)\. ([{letters}]) - ', line)
        answers[int(m.group(1))] = letters.index(m.group(2))

    questions = []
    for block in re.split(rf"\n(?={L['q']} \d+\.)", read(f"theory_questions{L['suffix']}.txt"))[1:]:
        m = re.match(rf"{L['q']} (\d+)\. (.*)", block)
        qid = int(m.group(1))
        topic = re.search(rf"\[{L['topic']}: ([^|]+?) \|", block).group(1)
        tags = re.search(rf"{L['lic']}: ([^\]]*)\]", block).group(1)
        # The source uses Cyrillic 'В' (U+0412) for license B; normalize to Latin.
        licenses = [t.strip().replace('В', 'B') for t in tags.split(',')]
        img = re.search(rf"^{L['img']}: (.*)$", block, re.M)
        options = re.findall(rf'^   [{letters}]\. (.*)$', block, re.M)
        assert len(options) == 4, qid
        questions.append({
            'id': qid,
            'text': m.group(2).strip(),
            'topic': L['topics'][topic],
            'licenses': licenses,
            'image': img.group(1).strip() if img else None,
            'options': options,
            'answer': answers[qid],
        })
    assert len(questions) == len(answers)
    return questions

versions = {}
for lang, L in LANGS.items():
    questions = parse(L)
    body = (f'(window.QUESTIONS = window.QUESTIONS || {{}}).{lang} = '
            + json.dumps(questions, ensure_ascii=False) + ';\n')
    with open(os.path.join(HERE, f'data_{lang}.js'), 'w', encoding='utf-8') as f:
        f.write(body)
    versions[lang] = hashlib.sha1(body.encode()).hexdigest()[:10]
    print(f'wrote {len(questions)} questions to data_{lang}.js (v={versions[lang]})')

# Update the cache-busting versions in index.html so browsers never pair new code with stale data.
page = os.path.join(HERE, 'index.html')
html = re.sub(r'const DATA_VERSIONS = .*;', f'const DATA_VERSIONS = {json.dumps(versions)};', read('index.html'))
with open(page, 'w', encoding='utf-8') as f:
    f.write(html)
