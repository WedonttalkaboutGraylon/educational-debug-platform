import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.countChar;
    const cases: [string,string,number,string][] = [["hello","l",2,"two ls"],["banana","a",3,"three as"],["hello","z",0,"not found"],["aaa","a",3,"all match"],["","a",0,"empty"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [s,t,exp,label] of cases){try{const r=f(s,t);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
