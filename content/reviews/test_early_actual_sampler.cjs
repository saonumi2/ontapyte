// Execute the browser's actual sample() function in an isolated, seeded VM.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const code=fs.readFileSync(path.join(root,'src/app.js'),'utf8').split('function renderCatalog(){')[0];
const report=[];
for(const mid of ['m13','m14','m15','m16']){
 const file=path.join(root,'content/banks',`${mid}.json`),bank=JSON.parse(fs.readFileSync(file,'utf8'));
 const ctx=vm.createContext({Math:Object.create(Math)});vm.runInContext(code,ctx);ctx.bank=bank;
 let total=0;
 for(let seed=1;seed<=1000;seed++){
   let state=seed;ctx.Math.random=()=>((state=(1664525*state+1013904223)>>>0)/4294967296);
   const picked=vm.runInContext('sample(bank)',ctx);
   assert.equal(picked.length,40);assert.equal(new Set(picked.map(q=>q.id)).size,40);
   assert.equal(new Set(picked.map(q=>q.conceptId)).size,40);
   assert.equal(new Set(picked.map(q=>q.topicId)).size,bank.topics.length);
   picked.forEach((q,i)=>{
      assert.equal(q.level,i<10?'understand':i<30?'apply':'analyze');
      const original=bank.questions.find(x=>x.id===q.id);
      assert.equal(q.options[q.answer],original.options[original.answer]);
      assert.equal(q.optionExplanations[q.answer],original.optionExplanations[original.answer]);
      assert.equal(q.sources.length,original.sources.length);
   });total++;
 }
 report.push({moduleId:mid,bankSha256:require('node:crypto').createHash('sha256').update(fs.readFileSync(file)).digest('hex'),seeds:total,pass:true,checks:['40 unique question IDs','40 unique concept IDs','all declared topics covered','level order 10/20/10','shuffled answer text invariant','shuffled explanation invariant','source preservation']});
 console.log(mid,'PASS',total,'actual JavaScript sampler seeds');
}
fs.writeFileSync(path.join(__dirname,'early-actual-sampler.json'),JSON.stringify(report,null,2));
