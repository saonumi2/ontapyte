"""Reproducible reviewer corrections; only owns m13–m16 bank content."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[2]

def read(mid):return json.loads((ROOT/'content'/'banks'/f'{mid}.json').read_text(encoding='utf-8'))
def write(d):
    (ROOT/'content'/'banks'/f'{d["moduleId"]}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

def revise14():
    d=read('m14'); docs=json.loads((ROOT/'content'/'m14.json').read_text(encoding='utf-8-sig'))
    by={q['id']:q for q in d['questions']}
    def change(n,stem,choices,why,pages=None,level=None,concept=None):
        q=by[f'm14-q{n:03}'];q.update(stem=stem,options=choices,answer=0,explanation=why,
          optionExplanations=[why]+['Không phù hợp. '+why]*3)
        if pages:q['sources']=[{'page':p,'quote':docs['pages'][p-1]['text'].strip()} for p in pages]
        if level:q['level']=level
        if concept:q['conceptId']=concept
    change(19,'Người ra huyết nhiều có đoạn dưới tử cung phình dạng đồng hồ cát; siêu âm thấy túi thai ở vùng cổ tử cung. Trong các thể bài mô tả, thể nào cần được nghĩ đến?',
      ['Thai ở cổ tử cung, cần phân biệt với thai đang sẩy','Thai đoạn bóng được xác nhận chỉ từ ra máu','Thai trong ổ bụng vì có ra máu','Nang nước cạnh vòi được xác nhận từ hình đồng hồ cát'],
      'Trang 17 mô tả đoạn dưới tử cung phình, túi thai ở cổ tử cung và khả năng nhầm thai đang sẩy. Tổ hợp gợi thể cổ tử cung, không thay đánh giá phân biệt.',[17])
    change(22,'Người nghi thai ngoài tử cung xuất hiện đau tăng và dấu choáng. Khi tìm dấu siêu âm đi kèm tình trạng vỡ theo bài, cần chú ý phát hiện nào?',
      ['Dịch túi cùng sau hoặc dịch ổ bụng','Chỉ kích thước bàng quang','Chỉ hạch cổ','Chỉ hình nang noãn nguyên thủy'],
      'Trang 13 mô tả choáng do xuất huyết nội; trang 19 nêu tụ dịch túi cùng sau hoặc ổ bụng khi thai ngoài tử cung đã vỡ. Dịch không tự xác nhận cơ chế chỉ từ một dấu.',[13,19])
    change(23,'Cần một phương tiện vừa giúp xác định thai ngoài tử cung vừa có khả năng phẫu thuật bảo tồn hoặc cắt vòi khi phù hợp. Phương tiện nào trong bài đáp ứng cả hai mục tiêu?',
      ['Nội soi ổ bụng','Chỉ một lần định lượng β-hCG','Chỉ quan sát máu âm đạo','Chỉ chụp ảnh bên ngoài'],
      'Trang 20 nêu nội soi giúp chẩn đoán xác định và có thể phẫu thuật bảo tồn hoặc cắt vòi. Xét nghiệm hay nhìn bên ngoài không có hai chức năng này.',[20])
    change(25,'Hai hồ sơ có khối thai cùng vị trí, nhưng khác tình trạng sức khỏe khi nhập viện và nguyện vọng sinh con. Theo mục xử trí, cách đánh giá nào đúng?',
      ['Phải xét thêm sức khỏe và nguyện vọng, không quyết định chỉ từ vị trí','Cùng vị trí thì bắt buộc cùng cách xử trí','Chỉ chọn theo số con, bỏ sức khỏe','Bỏ qua mong muốn sinh con trong mọi trường hợp'],
      'Trang 22 liệt kê đặc điểm/vị trí khối cùng tình trạng sức khỏe, số con và nguyện vọng. Cùng một yếu tố không làm các hồ sơ tương đương toàn bộ.',[22])
    change(26,'Một kế hoạch ghi phải dùng nội soi cho mọi trường hợp, dù tình trạng bệnh không cho phép thực hiện. Cách sửa nào bám đúng phần điều trị tận gốc của bài?',
      ['Ưu tiên nội soi khi thực hiện được; bài còn nêu mổ bụng khi tình trạng bệnh không thực hiện được nội soi','Vẫn bắt buộc nội soi bất kể tình trạng bệnh','Bỏ mọi xử trí nếu không nội soi được','Chỉ lặp β-hCG để thay mọi phẫu thuật'],
      'Trang 23 nêu ưu tiên nội soi, nhưng còn phương án mổ bụng khi tình trạng bệnh không thực hiện được nội soi. Đây là đối chiếu điều kiện trong bài, không lựa chọn cách mổ cho bệnh nhân cụ thể.',[23],concept='surgicalfeasibility')
    change(27,'Một bảng sàng lọc điều kiện bảo tồn ghi người đang mạch nhanh, huyết áp tụt là “huyết động ổn định”. Cần sửa phần đối chiếu nào?',
      ['Dấu này thuộc mô tả choáng của bài, không đáp ứng điều kiện huyết động ổn định','Mạch nhanh và huyết áp tụt xác nhận ổn định','Không cần xét huyết động khi muốn bảo tồn','Chỉ kích thước khối đủ thay đánh giá sinh hiệu'],
      'Trang 13 mô tả mạch nhanh, huyết áp tụt ở choáng xuất huyết; trang 25 yêu cầu huyết động ổn định. Cần phân biệt điều kiện chưa đạt với quyết định điều trị hoàn chỉnh.',[13,25])
    change(29,'Sau xẻ vòi hút khối thai, kế hoạch chỉ ghi theo dõi triệu chứng và bỏ xét nghiệm mà bài nhắc để đề phòng sót nhau. Xét nghiệm cần bổ sung theo bài là gì?',
      ['β-hCG','IgG Chlamydia thay β-hCG','AMH thay β-hCG','Estradiol thay β-hCG'],
      'Trang 27 nhắc theo dõi β-hCG sau xẻ vòi hút khối thai trong phần đề phòng sót nhau. Câu không sử dụng liều hoặc chỉ định thuốc sau mổ.',[27])
    change(30,'Một người đọc mục tiên lượng rồi kết luận “phát hiện sớm chắc chắn vẫn vô sinh”. Cách sửa nào đúng mức khẳng định của nguồn?',
      ['Phát hiện sớm có tiên lượng tốt và có thể duy trì khả năng sinh sản; không bảo đảm kết quả tuyệt đối','Nguồn bảo đảm mọi người đều vô sinh','Nguồn bảo đảm mọi người đều có thai về sau','Thời điểm phát hiện hoàn toàn không liên quan tiên lượng'],
      'Trang 28 dùng “có thể duy trì” khi phát hiện sớm, không nói chắc chắn vô sinh hoặc chắc chắn có thai về sau.',[28])
    change(36,'Hai kế hoạch: A coi siêu âm là xét nghiệm hCG; B xem siêu âm cung cấp hình ảnh, còn nội soi vừa xác định vừa có thể xử trí. Kế hoạch nào phân biệt đúng công cụ và vai trò theo bài?',
      ['B: hình ảnh siêu âm và khả năng chẩn đoán/can thiệp của nội soi là các vai trò khác nhau','A: siêu âm và hCG là cùng một phép đo','Cả hai đều sai vì nội soi không giúp chẩn đoán','A đúng vì hCG có thể trực tiếp cắt vòi'],
      'Trang 19 trình bày hình ảnh siêu âm; trang 20 trình bày nội soi chẩn đoán/can thiệp; trang 21 nhấn mạnh phối hợp. Không đồng nhất công cụ xét nghiệm, hình ảnh và thủ thuật.',[19,20,21],concept='diagnosticmodalities')
    change(39,'Một bảng tư vấn sau nội soi chỉ ghi đã xác định thai ngoài tử cung, bỏ đánh giá tổn thương tử cung/phần phụ và viêm dính. Vai trò bổ sung nào của nội soi được bài nêu?',
      ['Đánh giá viêm dính, bệnh lý tử cung và hai phần phụ để góp phần tiên lượng sinh sản','Chỉ xác định màu tóc để tiên lượng','Tự bảo đảm chắc chắn sẽ có thai về sau','Không có vai trò đánh giá vùng chậu ngoài xác định khối thai'],
      'Trang 20 nêu nội soi còn đánh giá viêm dính, bệnh lý tử cung và hai phần phụ, tiên lượng khả năng sinh sản. Đây là vai trò khác với điều trị cắt/bảo tồn vòi.',[20],concept='pelvicfertilityassessment')
    # Avoid asking the same highest-frequency fact twice in a single attempt.
    by['m14-q011']['conceptId']='ampulla'
    # q045 explanation needs the combined diagnostic source explicitly.
    by['m14-q045']['sources'].append({'page':21,'quote':docs['pages'][20]['text'].strip()}) if not any(r['page']==21 for r in by['m14-q045']['sources']) else None
    for q in d['questions']:
        q['review'].update(source=True,semantic=True,coverage=False)
    # Sync TSV so later compilation cannot restore known defects; compile resets reviews by design.
    lines=[]
    for q in d['questions']:
        opts=[q['options'][q['answer']]]+[x for i,x in enumerate(q['options']) if i!=q['answer']]
        lines.append('|'.join([q['level'],q['topicId'],','.join(str(s['page']) for s in q['sources']),q['conceptId'],q['stem'],*opts,q['explanation']]))
    (ROOT/'content'/'m14-authoring.tsv').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write(d)

def supplement():
    data={
      'm15':[
       ('understand','hcg','hcg-molecular-forms',9,'Vì sao không nên coi mọi phân tử mang thành phần β được liệt kê trong bài là hCG nguyên vẹn có cùng hoạt tính?', ['Bài phân biệt nhiều dạng và nêu dạng phân ly/thoái giáng có thể không có hoạt tính sinh học','Bài nói chỉ có duy nhất hCG nguyên vẹn','Mọi tiểu đơn vị β tự do đều được gọi là hCG nguyên vẹn trong hình','Bài không đề cập dạng phân tử'], 'Trang 9 liệt kê intact, nicked, free β, nicked free β và β-core; ghi các phân tử phân ly/thoái giáng không có hoạt tính sinh học. Không đồng nhất cấu trúc với hoạt tính.'),
       ('apply','hcg','hcg-beta-core',9,'Một phiếu học cần đặt β-core fragment vào loại mẫu mà sơ đồ ghi bên cạnh riêng dạng này. Chọn loại mẫu nào?', ['Nước tiểu','Chỉ dịch não tủy','Chỉ máu cuống rốn','Chỉ dịch nang noãn'], 'Trang 9 đặt β-core fragment dưới ngoặc Urine và ghi β-core fragment (urine); không có các loại mẫu còn lại trong sơ đồ.')
      ],
      'm16':[
       ('apply','pathology','empty-ovum-duplication',9,'Theo sơ đồ, noãn không có bộ gen nhận một bộ 23X rồi xảy ra nhân đôi nội tại. Kết quả được ghi là gì?', ['46XX đồng hợp','69XXX','46XY không qua nhân đôi','69XXY'], 'Sơ đồ trang 9 vẽ Empty ovum +23X →23X →Endoreduplication →46XX Homozygous. Đây là cách đọc nhánh cụ thể, không khẳng định mọi46XX đều có cơ chế đó.'),
       ('analyze','pathology','same-karyotype-different-origin',9,'Hai nhánh ở sơ đồ cùng tạo46XX: một nhánh từ23X nhân đôi, một nhánh từ hai bộ23X. Phân biệt nào đúng theo nhãn của sơ đồ?', ['Nhánh nhân đôi ghi đồng hợp; nhánh hai bộ23X ghi dị hợp','Cả hai đều được hình ghi69XXX','Nhánh nhân đôi ghi dị hợp, nhánh hai bộ23X ghi đồng hợp','Hình cho rằng cùng46XX thì không thể khác nguồn hình thành'], 'Trang 9 phân biệt Homozygous ở nhánh endoreduplication và Heterozygous ở nhánh noãn rỗng nhận hai bộ23X. Cùng số nhiễm sắc thể không đồng nhất hai nhánh trong sơ đồ.'),
       ('apply','pathology','triploid-sum',9,'Trong nhánh noãn23X nhận hai bộ23X của sơ đồ, kết quả số nhiễm sắc thể và nhiễm sắc thể giới tính là gì?', ['69XXX','46XX','46XY','23X'], 'Nhánh phải trang9 vẽ23X +23X +23X →69XXX. Câu chỉ yêu cầu áp dụng phép cộng và đọc nhánh rõ của nguồn.'),
       ('analyze','diagnostics','ultrasound-complete-text',17,'Mô tả bằng chữ trong chú thích: khối tăng âm tử cung có nhiều khoang nang trống âm, dạng “bão tuyết”, không có thai hay túi ối. Chú thích gắn tổ hợp này với dạng nào?', ['Thai trứng toàn phần trong hình minh họa','Thai trứng bán phần có đầu thai cạnh bánh nhau nhiều nang','Nang hoàng tuyến đơn độc không có tổn thương tử cung','Một túi thai bình thường được chú thích'], 'Chú thích hình13-4A trang17 mô tả complete hydatidiform mole với snowstorm, nhiều anechoic cystic spaces và fetus/amniotic sac absent. Câu đối chiếu tổ hợp trong chú thích, không thay xác nhận GPB.'),
       ('apply','diagnostics','ultrasound-partial-text',17,'Chú thích hình mô tả đầu thai cạnh bánh nhau to, nhiều nang. Dạng thai trứng nào được chú thích này minh họa?', ['Thai trứng bán phần','Thai trứng toàn phần không có thai/túi ối theo hìnhA','Chỉ nang hoàng tuyến buồng trứng','Chỉ u xơ tử cung'], 'Hình13-4B trang17 là partial hydatidiform mole; fetal head nằm cạnh enlarged multicystic placenta. Không suy mọi trường hợp bán phần đều có toàn bộ hình ảnh này.')
      ]
    }
    visual={
      ('m15',9):'Numerous molecular forms of hCG present in pregnancy serum. Dissociated or degraded molecules with no biological activity. Key β-containing variants: Intact hCG; Nicked hCG; Free β subunit; Nicked free β subunit; β-core fragment (urine).',
      ('m16',9):'Empty ovum + 23X → 23X → Endoreduplication → 46XX Homozygous. Empty ovum + 23X + 23X → 46XX Heterozygous. Empty ovum + 23X + 23Y → 46XY. 23X + 23X + 23X → 69XXX. 23X + 23Y + 23Y → 69XYY. 23X + 23X + 23Y → 69XXY.',
      ('m16',17):'FIGURE 13-4 Sonograms of hydatidiform moles. A. Transverse view of a uterus with a complete hydatidiform mole. The characteristic “snowstorm” appearance reflects an echogenic uterine mass, marked by calipers, that has numerous anechoic cystic spaces. Notably, a fetus or amnionic sac is absent. B. In this sagittal image of a partial hydatidiform mole, the fetal head (arrow) lies adjacent to an enlarged, multicystic placenta.'
    }
    for mid,rows in data.items():
        d=read(mid)
        for level,topic,concept,page,stem,options,why in rows:
            if any(q['conceptId']==f'{mid}-{concept}' for q in d['questions']):continue
            d['questions'].append({'id':f'{mid}-q{len(d["questions"])+1:03}','topicId':topic,'conceptId':f'{mid}-{concept}','level':level,
              'stem':stem,'options':options,'answer':0,'explanation':why,'optionExplanations':[why]+['Không phù hợp với chú thích nguồn. '+why]*3,
              'sources':[{'page':page,'quote':visual[mid,page],'type':'visual','transcriptionVerified':True}],
              'review':{'source':True,'semantic':True,'coverage':False}})
        for t in d['topics']:
            t['pages']=sorted(set(t['pages'])|{s['page'] for q in d['questions'] if q['topicId']==t['id'] for s in q['sources']})
        write(d)

def consolidate():
    families={
      'm13':{'integrated-boundary':'integrated-crl-choice','mole-treatment-diagnosis':'mole-evacuation','integrated-evidence':'clinical-limit','integrated-mole-diagnostics':'mole-tests'},
      'm14':{'hcgnotlocation':'diagnosisintegration'},
      'm15':{'integrated-true-sac':'integrated-sac-pattern','integrated-route-resolution':'complementary-routes'},
      'm16':{'integrated-conflicting-pattern':'integrated-partial-pattern','integrated-fetal-exclusion':'embryo-presence','integrated-risk-comparison':'subsequent-gtn-risk'}
    }
    for mid,mapping in families.items():
        d=read(mid)
        for q in d['questions']:
            pref=mid+'-' if q['conceptId'].startswith(mid+'-') else ''
            c=q['conceptId'][len(pref):]
            if c in mapping:q['conceptId']=pref+mapping[c]
            if mid=='m13' and q['id']=='m13-q070':q['level']='apply'
            if mid=='m13' and q['id']=='m13-q072':q['level']='understand'
        write(d)
        if mid=='m14':
            lines=[]
            for q in d['questions']:
                opts=[q['options'][q['answer']]]+[x for i,x in enumerate(q['options']) if i!=q['answer']]
                lines.append('|'.join([q['level'],q['topicId'],','.join(str(s['page']) for s in q['sources']),q['conceptId'],q['stem'],*opts,q['explanation']]))
            (ROOT/'content'/'m14-authoring.tsv').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':
    revise14()
    supplement()
    consolidate()
