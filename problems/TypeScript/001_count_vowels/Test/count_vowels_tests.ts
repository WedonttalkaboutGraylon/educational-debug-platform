import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.countVowels;
    const cases: [string,number,string][] = [["hello",2,"basic"],["Hello World",3,"mixed case"],["AEIOU",5,"all upper"],["aeiou",5,"all lower"],["rhythm",0,"no vowels"],["Apple",2,"cap A"],["",0,"empty"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [s,exp,label] of cases){try{const r=f(s);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
