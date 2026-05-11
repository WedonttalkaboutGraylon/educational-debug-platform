import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.removeDuplicates;
    const cases: [number[],number[],string][] = [[[1,2,2,3,3,3],[1,2,3],"basic"],[[1,1,1],[1],"all same"],[[1,2,3],[1,2,3],"no dups"],[[],[],  "empty"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [nums,exp,label] of cases){try{const r=f(nums);if(JSON.stringify(r)===JSON.stringify(exp)){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
