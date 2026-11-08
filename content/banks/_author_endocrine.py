from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent.parent
def norm(s): return ' '.join(s.split())
def build(mid,topics,rows):
    doc=json.loads((ROOT/f'{mid}.json').read_text(encoding='utf-8-sig'))
    texts={p['page']:norm(p['text']) for p in doc['pages']}
    # For scanned pages, only the manually transcribed excerpts below may be used.
    manual=ROOT/'banks'/f'_{mid}-verified-excerpts.json'
    visualPages=set()
    if manual.exists():
        visualPages={int(k) for k in json.loads(manual.read_text(encoding='utf-8'))}
        texts.update({int(k):v for k,v in json.loads(manual.read_text(encoding='utf-8')).items()})
    qs=[]
    for line in rows.strip().splitlines():
        if not line.strip() or line.startswith('#'): continue
        topic,concept,level,stem,opts,exp,refs=line.split('|')
        options=opts.split('~')
        assert len(options)==4 and len(set(options))==4,line
        pages=[int(v) for v in refs.split(',')]
        i=len(qs); shift=i%4
        options=options[shift:]+options[:shift]
        answer=(-shift)%4
        qs.append(dict(id=f'{mid}-q{i+1:03}',topicId=topic,conceptId=f'{mid}-{concept}',level={'U':'understand','A':'apply','H':'analyze'}[level],stem=stem,options=options,answer=answer,explanation=exp,optionExplanations=[exp if j==answer else f'Không phù hợp trong tình huống này. {exp}' for j in range(4)],sources=[{'page':p,'quote':texts[p],**({'type':'visual','transcriptionVerified':True} if p in visualPages else {})} for p in pages],review={'source':True,'semantic':True,'coverage':False}))
    result={'moduleId':mid,'title':doc['title'],'sourceSha256':doc['sha256'],'topics':[{'id':i,'title':t,'pages':ps} for i,t,ps in topics],'questions':qs}
    (ROOT/'banks'/f'{mid}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(mid,len(qs),{k:sum(q['level']==k for q in qs) for k in ('understand','apply','analyze')})

def contacts():
    from PIL import Image,ImageDraw
    fs=sorted(ROOT.glob('m06-page-*.jpg'))
    for n in range(0,len(fs),6):
        canvas=Image.new('RGB',(2400,2100),'white')
        for i,f in enumerate(fs[n:n+6]):
            canvas.paste(Image.open(f).resize((1200,675)),(i%2*1200,i//2*700+25))
            ImageDraw.Draw(canvas).text((i%2*1200+10,i//2*700+5),f.name,fill='black')
        canvas.save(ROOT/'banks'/f'_m06-contact-{n//6+1}.jpg')
if __name__=='__main__': contacts()
