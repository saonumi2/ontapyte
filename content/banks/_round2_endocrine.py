"""Second-pass editorial corrections, applied after the four authoring files."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
banks={m:json.loads((ROOT/f'{m}.json').read_text(encoding='utf-8')) for m in ['m05','m06','m07','m08']}
def get(m,c): return next(q for q in banks[m]['questions'] if q['conceptId']==f'{m}-{c}')
def lower(m,concepts,level='understand'):
    for c in concepts.split(','): get(m,c)['level']=level
def edit(m,c,stem,options,explanation):
    q=get(m,c); q['stem']=stem; q['options']=options.split('~'); q['answer']=0; q['explanation']=explanation
    assert len(q['options'])==4
    q['optionExplanations']=[explanation if i==0 else 'Không phù hợp với tình huống. '+explanation for i in range(4)]

# Questions that merely name a structure, hormone, gene, or stage are understanding,
# even if their wording mentions a hypothetical diagram or cell.
lower('m05','encapsulation,stage-sequence,theca-lh,granulosa-fsh,e2-potency,dominant-name,prelh-oocyte,cumulus,rupture,peak-day')
lower('m05','two-steroids-same-source')
lower('m07','early-products,theca-pathway,aromatase-product,p4-source,muller-target,esr1-chromosome,esr2-chromosome,er-dimer,pgr-chromosome,pra-case,prb-case,regeneration-case')
lower('m07','luteal-e2-p4')
lower('m07','source-not-mechanism','apply')
lower('m08','e2-targets,who1-mechanism,who2-mechanism,who3-mechanism,primary-hypothalamus,primary-ovary,secondary-outflow,implant-hormones,lng-placement,ring-composition,lng-type')
lower('m08','drug-groups')
lower('m08','exclude-not-assume','apply')

edit('m05','location-scenario','Trong mô hình di trú của bài, tế bào từ túi noãn hoàng đã đi dọc mạc treo ruột nhưng bị chặn trước ụ sinh dục. Kết quả nào chưa đạt?',
     'Tế bào chưa đến được ụ sinh dục~Tế bào đã hoàn tất di trú vào ụ sinh dục~Đường di trú đã kết thúc ở tuyến yên~Đường di trú bình thường kết thúc tại tử cung',
     'Slide 3 xác định ụ sinh dục là đích của đường di trú; bị chặn trước đích nghĩa là chưa hoàn tất bước đến ụ sinh dục.')
edit('m05','mitosis-stop','Theo mô hình slide 6, tế bào sinh dục đã ngừng nguyên phân vĩnh viễn và đi vào giảm phân. Nhận định nào phù hợp về cách tăng số lượng bằng nguyên phân sau mốc này?',
     'Không thể tiếp tục tăng bằng nguyên phân ở chính nhóm tế bào đã ngừng này~Nhóm này tiếp tục nguyên phân như trước~Ngừng nguyên phân đồng nghĩa đã hoàn tất giảm phân II~Ngừng nguyên phân làm tế bào biến thành tuyến yên',
     'Trong phạm vi mô tả slide 6, sự ngừng nguyên phân là vĩnh viễn; không được suy giảm phân là tiếp tục nguyên phân.')
edit('m05','arrest-I','Một sơ đồ đặt việc tái tục giảm phân của nhóm nang được chiêu mộ hoàn toàn trước dậy thì. Cách sửa nào phù hợp slide 6?',
     'Đặt sự tái tục ở nang được chiêu mộ kể từ sau dậy thì~Đặt mọi noãn hoàn tất giảm phân II trước sinh~Bỏ hoàn toàn giai đoạn đình trệ giảm phân~Đổi giảm phân thành nguyên phân liên tục',
     'Slide 6 phân biệt giai đoạn đình trệ trong thai kỳ với sự tiếp tục sau dậy thì ở nhóm nang được chiêu mộ.')
edit('m05','gnrh-output','Trong mô hình bài, nếu tín hiệu xung GnRH đến tuyến yên bị gián đoạn, khâu đáp ứng nào trực tiếp mất kích thích này?',
     'Chế tiết FSH và LH ở tuyến yên~Di trú tế bào từ túi noãn hoàng~Chuyển bạch thể thành noãn nguyên thủy~Tạo cholesterol tại mạch cửa',
     'Slide 11 nêu tuyến yên đáp ứng xung GnRH bằng FSH và LH; câu hỏi chỉ suy khâu mất kích thích, không khẳng định mọi nồng độ về không.')
edit('m05','e1-direct','Trong mô hình chỉ xét bước thơm hóa androstenedione tại tế bào hạt, bước này bị chặn. Sản phẩm trực tiếp nào không còn được tạo qua chính bước đó?',
     'Estrone (E1)~Progesterone từ hoàng thể~GnRH từ nhân cung~LH từ tuyến yên',
     'Slide 13 nêu E1 là sản phẩm trực tiếp của thơm hóa androstenedione; không suy rằng các nguồn hormone khác đều bị chặn.')
edit('m05','surge-output','Một nang tạo E2 vượt ngưỡng đủ lâu và phản hồi dương đã được kích hoạt. Dạng đáp ứng LH nào phù hợp nhất với mô hình bài?',
     'Một đợt phóng thích lớn trong thời gian ngắn~LH thấp không thay đổi do phản hồi dương~LH biến mất vĩnh viễn ngay~LH được sản xuất trực tiếp trong noãn thay tuyến yên',
     'Slide 18 mô tả phản hồi dương tạo đỉnh LH, tức phóng thích lượng lớn trong thời gian ngắn.')
edit('m05','lh-meiosis','Sau đỉnh LH, một sơ đồ vẫn vẽ noãn giữ nguyên trạng thái trước đỉnh mà không hoàn tất giảm phân I. Bước cần bổ sung theo bài là gì?',
     'Hoàn tất giảm phân I rồi đi vào giảm phân II~Lặp lại nguyên phân tạo nhiều noãn~Hoàn tất ngay giảm phân II dù chưa có tinh trùng~Chuyển noãn thành tế bào vỏ',
     'Slide 19 nối đỉnh LH với hoàn tất giảm phân I và đi vào giảm phân II; noãn sau đó còn dừng chờ tinh trùng.')
edit('m05','fertilization-release','Một noãn đã đến kỳ giữa giảm phân II nhưng chưa có tinh trùng xâm nhập. Theo bài, có được ghi rằng toàn bộ giảm phân đã hoàn tất không?',
     'Không; vẫn ở điểm dừng chờ tinh trùng~Có; chỉ cần nang vỡ là đủ~Có; giảm phân II luôn hoàn tất trước LH~Không vì noãn chưa từng vào giảm phân I',
     'Slide 19 nêu điểm dừng metaphase II cho đến khi tinh trùng xâm nhập; không đồng nhất phóng noãn với hoàn tất giảm phân.')
edit('m05','vascularization','Nếu trong mô hình hoàng thể hóa, mạch máu chưa xâm nhập phần nang còn lại, nguồn cung mới nào được mô tả trong bài đang bị hạn chế?',
     'Cholesterol từ mạch máu vào cấu trúc nang~GnRH từ chính noãn bào~FSH do tế bào hạt tự tạo~DNA do hormone lưu hành tạo ra',
     'Slide 20 mô tả mạch máu xâm nhập để cung cấp cholesterol. Câu hỏi không suy rằng mọi cholesterol sẵn có đều đã hết.')
edit('m05','luteal-products','Sau phóng noãn, xét về mô hình nội tiết của bài, E2 vẫn được sản xuất đồng thời P4 xuất hiện nổi bật. Diễn giải nào phù hợp?',
     'Phần nang còn lại đã hoàng thể hóa, tiếp tục E2 và sản xuất thêm P4~E2 còn tồn tại chứng minh chưa thể có hoàng thể~P4 xuất hiện chứng minh toàn bộ E2 phải bằng không~P4 do tuyến yên thay FSH sản xuất',
     'Slide 20 mô tả hoàng thể tiếp tục sản xuất estradiol và đặc biệt sản xuất progesterone.')

# Carry the same second-pass decision to the overlapping concepts in m06, but retain
# the m06-only evidence and wording. No citation is borrowed across modules.
for c in ['stage-sequence','theca-lh','granulosa-fsh','dominant-name','prelh-oocyte','cumulus','rupture','peak-day','two-steroids-same-source']:
    get('m06',c)['level']='understand'
for c in ['gnrh-output','e1-direct','surge-output','fertilization-release','vascularization','luteal-products']:
    src=get('m05',c); dest=get('m06',c)
    for field in ['stem','options','answer','explanation','optionExplanations']:
        dest[field]=json.loads(json.dumps(src[field]))
    dest['stem']=dest['stem'].replace('slide 6','trang trích dẫn')
    dest['explanation']=replaced=__import__('re').sub(r'Slide \d+','Trang trích dẫn',dest['explanation'])
    dest['optionExplanations']=[replaced if j==dest['answer'] else 'Không phù hợp với tình huống. '+replaced for j in range(4)]

# Do not select two nearly identical prompts about one core fact in the same attempt.
aliases={
 'm05':{'feedback1':'e2-fsh-trend','two-receptors':'theca-lh','meiosis-arrest':'fertilization-release','luteal-support':'lh-dual-role','albicans':'lh-withdrawal','recruit-control':'recruit-local','aromatase':'e1-direct','receptor-advantage':'poor-receptors','feedback2-conditions':'high-e2-duration','substrate':'two-cell-dependence','reset':'cycle-reset-reason','p4-pulses':'p4-luteolysis-chain','luteal-products':'two-steroids-same-source'},
 'm06':{'feedback1':'e2-fsh-trend','two-receptors':'theca-lh','meiosis-arrest':'fertilization-release','luteal-support':'lh-dual-role','albicans':'lh-withdrawal','recruit-control':'recruit-local','aromatase':'e1-direct','receptor-advantage':'poor-receptors','feedback2-conditions':'high-e2-duration','substrate':'two-cell-dependence','reset':'cycle-reset-reason','p4-pulses':'p4-luteolysis-chain','luteal-products':'two-steroids-same-source','amh-source':'amh-peak','inhibin-action':'dual-control','whole-cycle':'duration-distinction','overlap':'successive-observation'},
 'm07':{'carbon':'carbon','mucus-e2':'midcycle-mucus','mucus-p4':'postovulation-mucus','secretory':'secretory-glycogen','menstruation':'withdrawal-case','genomic-location':'gpcra','af3':'pra-case','basal-reserve':'regeneration-case','pr-common-gene':'pgr-chromosome','e2-origin':'luteal-e2-p4','sequential':'unprepared','smooth-mechanism':'rapid-contraction','breast-exception':'source-not-mechanism'},
 'm08':{'who1':'classify1','who2':'classify2','who3':'classify3','early-fsh':'fsh-response','absent-luteum':'low-p4-secretory','early-short-cycle':'early-selection','coc-primary':'ee-fsh-case','coc-p4':'selected-no-ovulation','lng-local':'lng-not-full-lh','timing-mechanism':'timing-not-guarantee','exclusion':'exclude-not-assume','unopposed':'unopposed-chain','pop-purpose':'coc-vs-pop','pop-classic':'pop-subgroups'}
}
for mid,bank in banks.items():
    for q in bank['questions']:
        suffix=q['conceptId'][len(mid)+1:]
        q['conceptId']=mid+'-'+aliases[mid].get(suffix,suffix)
        q['review']['source']=True
        q['review']['semantic']=True
        q['review']['coverage']=False
    (ROOT/f'{mid}.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    from collections import Counter
    print(mid,len(bank['questions']),dict(Counter(q['level'] for q in bank['questions'])))
