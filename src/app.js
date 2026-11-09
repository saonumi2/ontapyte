const $ = (id) => document.getElementById(id);
const LEVELS = {easy:'Dễ',hard:'Khó',veryHard:'Cực khó'};
const COUNTS = {easy:10,hard:20,veryHard:10};
const shuffle = (array) => {const a=[...array];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
let catalog=[], current=null, quiz=[], index=0, results=[], chosen=null, shown=false;
function show(name){for(const id of ['home','quiz','result']) $(id).hidden=id!==name; window.scrollTo({top:0,behavior:'instant'})}
function sample(bank){
  const topics=new Set(bank.topics.map(t=>t.id));
  for(let attempt=0;attempt<500;attempt++){
    const covered=new Set(), coveredPages=new Set(), usedConcepts=new Set(), selection=[];
    let valid=true;
    for(const [level,count] of [['hard',20],['veryHard',10],['easy',10]]){
      for(let n=0;n<count;n++){
        const candidates=shuffle(bank.questions.filter(q=>q.difficulty===level&&!selection.includes(q)));
        if(!candidates.length){valid=false;break}
        const score=q=>(covered.has(q.topicId)?0:100)+(usedConcepts.has(q.conceptId)?0:10)+2*q.sources.filter(s=>!coveredPages.has(s.page)).length;
        const pick=candidates.reduce((best,q)=>score(q)>score(best)?q:best);
        selection.push(pick);covered.add(pick.topicId);usedConcepts.add(pick.conceptId);pick.sources.forEach(s=>coveredPages.add(s.page));
      }
      if(!valid)break;
    }
    if(valid&&[...topics].every(t=>covered.has(t))){
      const ordered=['easy','hard','veryHard'].flatMap(level=>selection.filter(q=>q.difficulty===level));
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
    const btn=document.createElement('button');btn.textContent=d.ready?'Làm 40 câu →':'Chưa phát hành';btn.disabled=!d.ready;btn.title=d.ready?'':d.readyReason;btn.addEventListener('click',()=>start(d));
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
  $('level').textContent=`(${LEVELS[q.difficulty]})`;
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
  const q=quiz[index];chosen=i;results.push({level:q.difficulty,correct:i===q.answer});
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
  for(const source of q.sources){const button=document.createElement('button');button.className='source-link';button.type='button';button.textContent=`Xem tài liệu tại đây · ${current.file.endsWith('.pdf')?'trang':'slide'} ${source.page}`;button.addEventListener('click',()=>openSource(source.page));target.append(button,document.createElement('br'))}
  target.hidden=false;$('show-explanation').hidden=true;shown=true;
}
function openSource(page){
  const url=`${current.file}#page=${page}`;
  const dialog=$('source-dialog');
  if(typeof dialog.showModal!=='function'){window.open(url,'_blank','noopener');return}
  $('source-title').textContent=`${current.title} · ${current.file.endsWith('.pdf')?'Trang':'Slide'} ${page}`;
  $('source-frame').src=url;
  $('source-direct').href=url;
  dialog.showModal();
}
function closeSource(){
  const dialog=$('source-dialog');
  if(dialog.open)dialog.close();
}
function finish(){show('result');$('result-title').textContent=current.title;$('result-score').textContent=`${results.filter(r=>r.correct).length} / 40 câu đúng`;
  $('result-breakdown').replaceChildren(...Object.keys(COUNTS).map(level=>{const span=document.createElement('span');const rows=results.filter(r=>r.level===level);span.textContent=`${LEVELS[level]}: ${rows.filter(r=>r.correct).length}/${rows.length}`;return span}));
}
$('back').addEventListener('click',()=>show('home'));
$('home-button').addEventListener('click',()=>show('home'));
$('retry').addEventListener('click',()=>start(current));
$('show-explanation').addEventListener('click',explain);
$('close-source').addEventListener('click',closeSource);
$('close-source-bottom').addEventListener('click',closeSource);
$('source-dialog').addEventListener('close',()=>{$('source-frame').src='about:blank'});
$('next').addEventListener('click',()=>{if(index===39)finish();else{index++;renderQuestion();window.scrollTo({top:0,behavior:'instant'})}});
try{const response=await fetch('data/catalog.json');if(!response.ok)throw new Error('Không tải được danh mục.');catalog=await response.json();renderCatalog()}catch(error){$('catalog').textContent=error.message}
