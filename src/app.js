const $ = (id) => document.getElementById(id);
const LEVELS = {understand:'Thông hiểu',apply:'Vận dụng',analyze:'Vận dụng cao'};
const COUNTS = {understand:10,apply:20,analyze:10};
const shuffle = (array) => {const a=[...array];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
let catalog=[], current=null, quiz=[], index=0, results=[], chosen=null, shown=false;
function show(name){for(const id of ['home','quiz','result']) $(id).hidden=id!==name; window.scrollTo({top:0,behavior:'instant'})}
function sample(bank){
  const topics=new Set(bank.topics.map(t=>t.id));
  for(let attempt=0;attempt<500;attempt++){
    const usedConcepts=new Set(), covered=new Set(), selection=[];
    let valid=true;
    for(const [level,count] of [['apply',20],['analyze',10],['understand',10]]){
      for(let n=0;n<count;n++){
        const candidates=shuffle(bank.questions.filter(q=>q.level===level&&!usedConcepts.has(q.conceptId)));
        if(!candidates.length){valid=false;break}
        const uncovered=candidates.filter(q=>!covered.has(q.topicId));
        const pick=(uncovered.length?uncovered:candidates)[0];
        selection.push(pick);usedConcepts.add(pick.conceptId);covered.add(pick.topicId);
      }
      if(!valid)break;
    }
    if(valid&&[...topics].every(t=>covered.has(t))){
      const ordered=['understand','apply','analyze'].flatMap(level=>selection.filter(q=>q.level===level));
      return ordered.map(q=>{
        const order=shuffle([0,1,2,3]);
        return {...q,options:order.map(i=>q.options[i]),optionExplanations:order.map(i=>q.optionExplanations[i]),answer:order.indexOf(q.answer)};
      });
    }
  }
  throw new Error('Ngân hàng hiện không tạo được đề đủ 40 câu bao quát các chủ đề.');
}
function renderCatalog(){
  $('summary').textContent=`${catalog.length} tài liệu · ${catalog.filter(x=>x.ready).length} phần đã duyệt`;
  $('catalog').replaceChildren(...catalog.map((d,i)=>{
    const card=document.createElement('article');card.className='card';
    const num=document.createElement('span');num.className='num';num.textContent=`PHẦN ${String(i+1).padStart(2,'0')}`;
    const title=document.createElement('h3');title.textContent=d.title;
    const bottom=document.createElement('div');bottom.className='bottom';
    const meta=document.createElement('span');meta.textContent=`${d.pageCount} trang/slide · ${d.questionCount} câu`;
    const btn=document.createElement('button');btn.textContent=d.ready?'Làm 40 câu →':'Đang kiểm duyệt';btn.disabled=!d.ready;btn.addEventListener('click',()=>start(d));
    bottom.append(meta,btn);card.append(num,title,bottom);return card;
  }));
}
async function start(d){
  try{
    const response=await fetch(`data/${d.id}.json`);
    if(!response.ok)throw new Error('Không tải được ngân hàng câu hỏi.');
    const bank=await response.json();quiz=sample(bank);current={...d,topics:Object.fromEntries(bank.topics.map(t=>[t.id,t.title]))};index=0;results=[];renderQuestion();show('quiz');
  }catch(error){alert(error.message)}
}
function renderQuestion(){
  const q=quiz[index];chosen=null;shown=false;
  $('quiz-title').textContent=current.title;
  $('progress-fill').style.width=`${index/40*100}%`;
  $('number').textContent=`CÂU ${index+1} / 40`;
  $('level').textContent=`(${LEVELS[q.level]})`;
  $('topic').textContent=current.topics[q.topicId]||'';
  $('stem').textContent=q.stem;
  $('feedback').hidden=true;$('explanation').hidden=true;$('show-explanation').hidden=true;$('next').hidden=true;
  $('options').replaceChildren(...q.options.map((option,i)=>{
    const button=document.createElement('button');button.className='option';button.type='button';
    const letter=document.createElement('span');letter.className='letter';letter.textContent='ABCD'[i];
    const value=document.createElement('span');value.textContent=option;button.append(letter,value);
    button.addEventListener('click',()=>answer(i));return button;
  }));
}
function answer(i){
  if(chosen!==null)return;
  const q=quiz[index];chosen=i;results.push({level:q.level,correct:i===q.answer});
  [...$('options').children].forEach((button,n)=>{button.disabled=true;if(n===q.answer)button.classList.add('correct');if(n===i&&i!==q.answer)button.classList.add('wrong')});
  $('feedback').hidden=false;$('feedback').className=`feedback ${i===q.answer?'good':'bad'}`;
  $('feedback').textContent=i===q.answer?'Chính xác!':`Chưa đúng. Đáp án đúng là ${'ABCD'[q.answer]}.`;
  $('show-explanation').hidden=false;$('next').hidden=false;
  $('next').textContent=index===39?'Xem kết quả →':'Câu tiếp theo →';
  try{localStorage.setItem(`module-san-last-${current.id}`,JSON.stringify({at:new Date().toISOString(),answered:index+1,correct:results.filter(r=>r.correct).length}))}catch{}
}
function explain(){
  const q=quiz[index];const target=$('explanation');target.replaceChildren();
  const heading=document.createElement('strong');heading.textContent='Giải thích';target.append(heading);
  const p=document.createElement('p');p.textContent=q.explanation;target.append(p);
  if(chosen!==q.answer&&q.optionExplanations?.[chosen]){const wrong=document.createElement('p');wrong.textContent=`Lựa chọn ${'ABCD'[chosen]}: ${q.optionExplanations[chosen]}`;target.append(wrong)}
  for(const source of q.sources){const a=document.createElement('a');a.href=`${current.file}#page=${source.page}`;a.target='_blank';a.rel='noopener';a.textContent=`Mở tài liệu gốc · ${current.file.endsWith('.pdf')?'trang':'slide'} ${source.page} ↗`;target.append(a,document.createElement('br'))}
  target.hidden=false;$('show-explanation').hidden=true;shown=true;
}
function finish(){show('result');$('result-title').textContent=current.title;$('result-score').textContent=`${results.filter(r=>r.correct).length} / 40 câu đúng`;
  $('result-breakdown').replaceChildren(...Object.keys(COUNTS).map(level=>{const span=document.createElement('span');const rows=results.filter(r=>r.level===level);span.textContent=`${LEVELS[level]}: ${rows.filter(r=>r.correct).length}/${rows.length}`;return span}));
}
$('back').addEventListener('click',()=>show('home'));
$('home-button').addEventListener('click',()=>show('home'));
$('retry').addEventListener('click',()=>start(current));
$('show-explanation').addEventListener('click',explain);
$('next').addEventListener('click',()=>{if(index===39)finish();else{index++;renderQuestion();window.scrollTo({top:0,behavior:'instant'})}});
try{const response=await fetch('data/catalog.json');if(!response.ok)throw new Error('Không tải được danh mục.');catalog=await response.json();renderCatalog()}catch(error){$('catalog').textContent=error.message}
