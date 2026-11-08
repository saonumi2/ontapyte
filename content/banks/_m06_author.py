from _author_endocrine import build,ROOT
import json,re
build('m06',[
('origin','Chiêu mộ, AMH và điều hòa tại chỗ',list(range(3,14))),
('axis','Kisspeptin, GnRH và hai tế bào – hai hormone',list(range(14,22))),
('selection','Inhibin B, chọn lọc và phản hồi E2',list(range(22,33))),
('ovulation','Phóng noãn và hoàng thể',[34,35,36,37,39,40,41]),
('cycle','Đoàn hệ và thời gian chu kỳ',[44,45,47,48])
],r'''
origin|amh-source|U|Vì sao AMH được xem là tín hiệu từ nang đã được chiêu mộ?|Do tế bào hạt nang tiền hốc và hốc nhỏ chế tiết~Do nhân cung chế tiết~Do bạch thể chế tiết~Do tuyến yên chế tiết|Trang 7 xác định nguồn AMH ở các nang đã được chiêu mộ.|7
origin|amh-gate|U|Vai trò 'người gác cổng' của AMH chỉ việc gì?|Hạn chế số nang nguyên thủy được chiêu mộ~Đảm bảo mọi nang đều phóng noãn~Tăng LH không giới hạn~Đóng lỗ tử cung|Trang 8–10 mô tả AMH kiểm soát số nang đi vào chu kỳ.|8,10
origin|paracrine|U|AMH từ nang đã chiêu mộ tác động nang nguyên thủy lân cận là kiểu điều hòa nào?|Cận tiết~Xung thần kinh trực tiếp đến tuyến yên~Dẫn truyền trong lòng tử cung~Thay thế toàn bộ gonadotropin|Trang 8 gọi đây là vai trò cận tiết của AMH.|8
origin|pten-pi3k|U|Quan hệ PTEN và PI3K trong sơ đồ là gì?|Tác dụng trái ngược trên chuyển đổi PIP2/PIP3~Cùng biến PIP2 thành PIP3~Đều chỉ tổng hợp LH~Không liên quan chiêu mộ|Trang 9 mô tả hai chiều chuyển đổi ngược nhau.|9
axis|kndy-mediator|U|KNDy kiểm soát neuron GnRH qua chất trung gian nào được nhấn mạnh?|Kisspeptin~Cholesterol~Inhibin B~Androstenedione|Trang 14 xác định kisspeptin là peptide trung gian.|14
selection|inhibin-source|U|Nguồn Inhibin B được mô tả trong bài là gì?|Tế bào hạt nang thứ cấp~Tế bào mạch cửa~Bạch thể~Neuron GnRH|Trang 23 xác định tế bào hạt sản xuất Inhibin B.|23
selection|inhibin-action|U|Inhibin B phối hợp E2 kiểm soát tuyến yên theo hướng nào?|Ức chế chế tiết FSH~Tăng FSH không giới hạn~Biến FSH thành LH~Chỉ làm tăng cholesterol|Trang 23–24 mô tả kiểm soát kép làm FSH thiếu hụt.|23,24
cycle|whole-cycle|U|Khoảng 90–120 ngày trong bài được tính giữa hai mốc nào?|Chiêu mộ đoàn hệ đến hoàng thể thành bạch thể~Hai đỉnh LH liên tiếp~Thụ tinh đến sinh~Hai lần hành kinh luôn liên tiếp|Trang 44 định nghĩa rõ khoảng thời gian theo đời một đoàn hệ.|44
cycle|overlap|U|Vì sao tại một thời điểm có nhiều đoàn hệ nang khác nhau?|Chúng được chiêu mộ ở những thời điểm khác nhau~Một noãn tự biến thành mọi đoàn hệ~Mỗi nang đều cùng tuổi~Chỉ có một lần chiêu mộ suốt đời|Trang 47 mô tả sự tồn tại song song các đoàn hệ.|47
origin|amh-peak|A|Một nang ở giai đoạn tiền hốc/hốc nhỏ. Chế tiết AMH theo bài có đặc điểm nào?|Đạt mức cao nhất rồi giảm ở giai đoạn sau~Chưa bao giờ có AMH~Chỉ tăng sau thành bạch thể~Chỉ do LH tạo trực tiếp|Trang 7 nêu thời điểm chế tiết AMH cao nhất.|7
origin|amh-after-recruit|A|Một nang đã được chiêu mộ nhưng chưa nên bước sớm vào giai đoạn lệ thuộc gonadotropin. Yếu tố nào được bài nêu giúp kìm tốc độ?|AMH~Đỉnh LH~Bạch thể~Androstenedione ngoại vi|Trang 12 mô tả AMH kìm hãm tiến triển quá sớm.|12
origin|amh-protect|A|Ngoài kìm tốc độ phát triển, nhiệm vụ AMH trên nang đã chiêu mộ được nêu là gì?|Bảo vệ khỏi thoái triển~Ép tất cả nang phóng noãn~Tạo thụ thể ở tuyến yên~Làm noãn hoàn tất giảm phân II ngay|Trang 12 nêu chức năng bảo vệ nang đã chiêu mộ.|12
origin|pi3k-product|A|Theo sơ đồ, PI3K hoạt động sẽ thúc đẩy chuyển đổi nào?|PIP2 thành PIP3~PIP3 thành PIP2~E2 thành FSH~LH thành GnRH|Trang 9 chỉ rõ chiều tác động của PI3K.|9
origin|pten-product|A|Trong cùng sơ đồ, PTEN tác động theo chiều nào?|PIP3 trở về PIP2~PIP2 thành PIP3~Progesterone thành LH~E1 thành FSH|PTEN được mô tả có chiều chuyển đổi ngược PI3K.|9
origin|foxo3|A|FOXO3 được phosphoryl hóa trong sơ đồ. Điều gì xảy ra với sự phong tỏa DNA?|Không còn phong tỏa, tế bào được kích hoạt~Phong tỏa tăng vĩnh viễn~DNA biến thành AMH~Tế bào lập tức thành bạch thể|Trang 9 liên kết phosphoryl hóa FOXO3 với giải phóng phong tỏa DNA.|9
origin|mtor|A|Nhánh Akt–TSC1/TSC2 kích hoạt mTOR. Kết quả nào được bài nêu?|Thúc đẩy dịch mã RNA~Ngừng mọi tổng hợp protein~Tạo trực tiếp đỉnh LH~Hủy mọi thụ thể FSH|Trang 9 mô tả mTOR thúc đẩy dịch mã.|9
axis|slow-pulse|A|Tần số xung GnRH thưa. Tuyến yên ưu tiên đáp ứng nào theo bài?|FSH~LH~AMH~Progesterone|Trang 17 phân biệt ưu thế FSH khi xung thưa.|17
axis|fast-pulse|A|Tần số xung GnRH dồn dập. Tuyến yên ưu tiên đáp ứng nào theo bài?|LH~AMH~Inhibin B~Estradiol|Trang 17 phân biệt ưu thế LH khi xung dồn dập.|17
axis|kisspeptin-effect|A|Kisspeptin kích thích neuron GnRH. Đầu ra trực tiếp nào được bài mô tả?|Xung GnRH vào mạch cửa~AMH vào dịch nang~Bạch thể mới~Progesterone từ tuyến yên|Trang 15 mô tả tác dụng dương tính của kisspeptin lên GnRH.|15
selection|inhibin-class|A|Phân tử do nang tiết, thuộc nhóm TGF-β và ức chế FSH, là gì?|Inhibin B~Estradiol~Progesterone~Cholesterol|Trang 23 mô tả Inhibin B là hormone protein thuộc nhóm TGF-β.|23
selection|inhibin-mass|A|Tổng khối tế bào hạt tăng trong mô hình bài. Nồng độ Inhibin B có chiều biến thiên nào?|Thuận chiều tổng khối tế bào hạt~Luôn nghịch chiều~Luôn bằng không~Chỉ phụ thuộc bạch thể|Trang 23 nêu quan hệ biến thiên thuận.|23
selection|dual-control|A|Một sơ đồ chỉ ghi E2 kiểm soát FSH trong pha nang. Hormone buồng trứng nào cần bổ sung theo bài?|Inhibin B~GnRH~LH~FSH|Trang 24 mô tả kiểm soát kép E2 và Inhibin B.|24
cycle|visible-part|A|Theo bài, biến đổi hình thái và nội tiết quan sát được chủ yếu thuộc phần nào của đời đoàn hệ?|28 ngày cuối, lệ thuộc gonadotropin~Toàn bộ giai đoạn từ lúc phôi thai~Chỉ lúc nang đang nghỉ~Chỉ thời gian đã thành bạch thể|Trang 48 giới hạn phần quan sát được ở giai đoạn cuối.|48
cycle|early-independence|A|Đoàn hệ đang ở hơn 60 ngày đầu sau chiêu mộ. Bài mô tả quan hệ với hormone trục HPO thế nào?|Phát triển độc lập với hormone trục~Bắt buộc có đỉnh LH hằng ngày~Đã tiết P4 như hoàng thể~Đã hoàn tất toàn bộ chu kỳ|Trang 44 mô tả phần đầu không lệ thuộc hormone trục.|44
ovulation|prostaglandin-local|A|Theo bài, bề mặt buồng trứng tại nang mỏng dần trước vỡ có liên quan yếu tố tại chỗ nào?|Prostaglandin~Inhibin B từ tuyến yên~GnRH trong lòng nang~Bạch thể từ cổ tử cung|Trang 35 nêu prostaglandin tại chỗ làm bề mặt mỏng dần.|35
origin|amh-two-functions|H|Một người cho rằng AMH chỉ ngăn chiêu mộ nên không có vai trò sau chiêu mộ. Phân tích nào đúng?|AMH còn bảo vệ nang và kìm bước quá sớm vào giai đoạn lệ thuộc gonadotropin~AMH chỉ do tuyến yên sản xuất~AMH luôn làm mọi nang thoái triển~AMH thay toàn bộ FSH ở nang lớn|Trang 8 nói về hạn chế chiêu mộ; trang 12 bổ sung vai trò sau chiêu mộ.|8,12
origin|signal-chain|H|Chuỗi nào phù hợp sơ đồ hoạt hóa nang qua PI3K?|PIP3 tăng → AKT/FOXO3 phosphoryl hóa → giải phong tỏa DNA~PIP3 tăng → FOXO3 phong tỏa DNA mãi~PTEN và PI3K luôn cùng chiều~AMH trực tiếp trở thành DNA|Trang 9 nối chuyển đổi phosphoinositide với hoạt hóa tế bào.|9
selection|amh-inhibin-compare|H|Hai hormone cùng từ tế bào hạt nhưng AMH và Inhibin B không thể coi là đồng chức năng vì sao?|AMH điều hòa chiêu mộ; Inhibin B cùng E2 kiểm soát gonadotropin tuyến yên~AMH chỉ từ hạ đồi còn Inhibin B từ tử cung~Cả hai đều trực tiếp tạo đỉnh LH~Cả hai đều là steroid giống E2|Trang 25 phân biệt giai đoạn và đích tác động của hai hormone.|8,25
axis|signal-order|H|Chuỗi truyền tín hiệu nào giải thích đáp ứng LH trong phản hồi dương?|KNDy → kisspeptin → neuron GnRH → tuyến yên~LH → tạo nhân cung → AMH~Tế bào vỏ → GnRH trực tiếp trong noãn~Bạch thể → kisspeptin → noãn nguyên thủy|Trang 32 mô tả thứ tự liên hệ từ KNDy đến phóng thích gonadotropin.|32
cycle|duration-distinction|H|Một người nói 'chu kỳ dài 90–120 ngày' nên hình thái nội tiết quan sát được phải kéo dài trọn thời gian đó. Sai ở đâu?|Nhầm toàn đời đoàn hệ với phần cuối lệ thuộc gonadotropin~Bài không hề mô tả đoàn hệ~Mọi nang chỉ sống 28 ngày từ lúc chiêu mộ~Bạch thể là giai đoạn đầu|Trang 44 định nghĩa toàn đời đoàn hệ; trang 45 và 48 giới hạn phần cuối biểu hiện rõ.|44,45,48
cycle|successive-observation|H|Vì sao khi đoàn hệ đang quan sát kết thúc vẫn có đoàn hệ tiếp nối, theo mô hình bài?|Nhiều đoàn hệ ở các giai đoạn khác nhau đã tồn tại song song~Bạch thể biến trực tiếp thành nang de Graaf~Chỉ lúc hành kinh mới tạo tế bào sinh dục mới~Mọi đoàn hệ đều kết thúc cùng lúc|Trang 47–48 giải thích sự chồng lấp và phần cuối quan sát được.|47,48
''')
# These concepts also occur in m05. Each is rechecked against the pictured m06 page(s),
# with source text replaced entirely by this document's verified transcription.
mapping={4:[5,6],6:[15],7:[18],8:[19],9:[19],10:[22],11:[26],12:[30,31],13:[34],14:[36],15:[40],20:[5,6],21:[11],22:[17],23:[17],24:[19],25:[19],26:[19],28:[18],29:[20],30:[22],31:[26],32:[27],33:[28],34:[30,31],35:[32],37:[34],38:[35],39:[35],40:[36],41:[37],42:[39],43:[39],44:[40],45:[41],46:[5,18],47:[19],48:[18,19],49:[21],50:[22,26],51:[22,26],52:[22,30],53:[27,29,30],55:[34,35],56:[35,36],57:[30,36],58:[39,40],59:[41],60:[37,39]}
p=ROOT/'banks'/'m06.json'; result=json.loads(p.read_text(encoding='utf-8'))
other=json.loads((ROOT/'banks'/'m05.json').read_text(encoding='utf-8'))['questions']
excerpts=json.loads((ROOT/'banks'/'_m06-verified-excerpts.json').read_text(encoding='utf-8'))
for n,pages in mapping.items():
    q=json.loads(json.dumps(other[n-1]))
    q['id']=f'm06-q{len(result["questions"])+1:03}'
    q['conceptId']=q['conceptId'].replace('m05-','m06-')
    q['stem']=re.sub(r'(?:slide|Slide) \d+','trang trích dẫn',q['stem'])
    q['explanation']=re.sub(r'(?:Slide|slide) \d+(?:[–-]\d+)?(?: và \d+)?','Trang trích dẫn',q['explanation'])
    q['sources']=[{'page':pg,'quote':excerpts[str(pg)],'type':'visual','transcriptionVerified':True} for pg in pages]
    # Terminology used by this document.
    q['stem']=q['stem'].replace('Cumulus oophora','Đám mây noãn bào').replace('cumulus oophora','đám mây noãn bào')
    q['options']=[v.replace('Cumulus oophora','Đám mây noãn bào').replace('cumulus oophora','đám mây noãn bào') for v in q['options']]
    q['explanation']=q['explanation'].replace('cumulus oophora','đám mây noãn bào')
    q['optionExplanations']=[q['explanation'] if j==q['answer'] else 'Không phù hợp trong tình huống này. '+q['explanation'] for j in range(4)]
    result['questions'].append(q)
p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('m06 final',len(result['questions']))
