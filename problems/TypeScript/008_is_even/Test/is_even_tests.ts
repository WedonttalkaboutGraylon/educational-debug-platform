import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.isEven;
    const cases: [number,boolean,string][] = [[0,true,"zero"],[2,true,"two"],[4,true,"four"],[1,false,"one"],[7,false,"seven"],[100,true,"hundred"],[-2,true,"neg even"],[-3,false,"neg odd"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [n,exp,label] of cases){try{const r=f(n);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
