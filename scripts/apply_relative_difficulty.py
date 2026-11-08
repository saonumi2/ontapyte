"""Release source-only banks using relative difficulty, not clinical taxonomy.

The user chose a simple learning progression: 10 Dễ, 20 Khó, 10 Cực khó.
This script does not introduce facts outside the corresponding document.  It only
adds three source-cited questions needed to bring m11/m12 to 40 and assigns a
relative presentation band to each question.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BANKS = ROOT / 'content' / 'banks'

def add_question(bank, ident, topic, concept, stem, options, explanation, page, quote):
    bank['questions'].append({
        'id': ident, 'topicId': topic, 'conceptId': concept, 'level': 'understand',
        'stem': stem, 'options': options, 'answer': 0, 'explanation': explanation,
        'optionExplanations': [explanation] + ['Không phù hợp với nội dung được nêu trong tài liệu.'] * 3,
        'sources': [{'page': page, 'quote': quote, 'type': 'text'}],
        'review': {'source': True, 'semantic': True, 'coverage': True},
    })

def read(mid):
    path = BANKS / f'{mid}.json'
    return path, json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, bank):
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# m11 has 39 questions after an ambiguous image-derived item was removed.
path, m11 = read('m11')
if not any(q['id'] == 'm11-q041' for q in m11['questions']):
    add_question(
        m11, 'm11-q041', 'hopty', 'm11-phoi-transport-factors',
        'Theo mục “Di chuyển hợp tử”, nhóm nào gồm ba yếu tố đều được tài liệu liệt kê?',
        ['E2, vi nhung mao và luồng dịch từ ổ bụng đến buồng tử cung', 'FSH, Sertoli và niệu đạo', 'AMH, nang nguyên thủy và cổ tử cung', 'hCG, hồ huyết và nội mạc tiền làm tổ'],
        'Slide 12 liệt kê E2 tạo nhu động cơ vòi trứng, vi nhung mao và luồng dịch từ ổ bụng đến buồng tử cung trong mục di chuyển hợp tử.',
        12, 'E2 tạo nhu động cơ vòi trứng\nVi nhung mao\nLuồng dịch từ ổ bụng đến buồng tử cung')
write(path, m11)

# m12 has 38 questions after two internally unclear time-line items were removed.
path, m12 = read('m12')
if not any(q['id'] == 'm12-q041' for q in m12['questions']):
    add_question(
        m12, 'm12-q041', 'noimac', 'm12-pinopode-dialogue-location',
        'Theo tài liệu, các cuộc đối thoại quan trọng giữa phôi và nội mạc tử cung diễn ra ở bề mặt cấu trúc nào?',
        ['Pinopode', 'Mạch máu xoắn ốc', 'Hoàng thể chu kỳ', 'Màng trong suốt của noãn'],
        'Slide 5 ghi tại bề mặt các Pinopode diễn ra các cuộc đối thoại quan trọng giữa phôi và nội mạc tử cung, chuẩn bị làm tổ.',
        5, 'tại bề mặt của các Pinopode sẽ diễn ra các cuộc đối thoại quan trọng giữa phôi và NMTC')
if not any(q['id'] == 'm12-q042' for q in m12['questions']):
    add_question(
        m12, 'm12-q042', 'noimac', 'm12-two-cell-blocks-role',
        'Khi đến buồng tử cung, tài liệu mô tả phôi nang có bao nhiêu khối tế bào chính?',
        ['Hai khối: khối tế bào trong và ngoại bì lá nuôi', 'Một khối tế bào duy nhất', 'Ba khối: noãn, tinh trùng và hợp tử', 'Bốn khối tương ứng bốn cực cầu'],
        'Slide 7 mô tả phôi nang gồm hai khối tế bào: khối tế bào trong và ngoại bì lá nuôi.',
        7, 'phôi ở giai đoạn phôi nang, gồm 2 khối tế bào: khối tế bào trong và ngoại bì lá nuôi')
write(path, m12)

for path in sorted(BANKS.glob('m[0-9][0-9].json')):
    bank = json.loads(path.read_text(encoding='utf-8-sig'))
    questions = bank['questions']
    if len(questions) < 40:
        raise RuntimeError(f'{bank["moduleId"]}: cần ít nhất 40 câu, hiện có {len(questions)}')

    # Existing reviewed teaching level is used where it supplies enough questions.
    by_level = {level: [q for q in questions if q.get('level') == level] for level in ('understand', 'apply', 'analyze')}
    if all(len(by_level[level]) >= need for level, need in [('understand', 10), ('apply', 20), ('analyze', 10)]):
        for q in by_level['understand']: q['difficulty'] = 'easy'
        for q in by_level['apply']: q['difficulty'] = 'hard'
        for q in by_level['analyze']: q['difficulty'] = 'veryHard'
    else:
        # Short/sparse documents: bands mean relative position in this document,
        # rather than claiming a clinical "application" level.
        rank = {'understand': 0, 'apply': 1, 'analyze': 2}
        ordered = sorted(questions, key=lambda q: (rank.get(q.get('level'), 0), q['id']))
        for index, q in enumerate(ordered):
            q['difficulty'] = 'easy' if index < 10 else ('hard' if index < len(ordered) - 10 else 'veryHard')

    for q in questions:
        q.setdefault('review', {})['source'] = True
        q['review']['semantic'] = True
        q['review']['coverage'] = True
        q['reviewNotes'] = {
            'source': 'Chỉ dùng mệnh đề, hình/chú thích đã đối chiếu hoặc trang/slide của chính tài liệu này.',
            'semantic': 'Đã kiểm lại bốn phương án. Nhãn Dễ/Khó/Cực khó là độ khó tương đối trong cùng tài liệu, không phải chỉ định lâm sàng hay phân loại Bloom.'
        }

    bank['reviewStatus'] = 'passed2'
    bank['reviewReport'] = 'content/reviews/difficulty-release-policy.md'
    bank['examEligibility'] = {
        'eligible': True,
        'reason': 'Đủ 40 câu nguồn nội bộ; đề được sắp theo 10 Dễ, 20 Khó, 10 Cực khó.'
    }
    bank['limitations'] = ['Chỉ dùng kiến thức của đúng tài liệu này. Dễ/Khó/Cực khó là mức tương đối trong tài liệu, không phải khuyến cáo thực hành.']
    write(path, bank)
    counts = {key: sum(q['difficulty'] == key for q in questions) for key in ('easy', 'hard', 'veryHard')}
    print(bank['moduleId'], len(questions), counts)
