import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.findMax;
    const cases: [number[],number,string][] = [[[3,7,2,9,4],9,"max at end"],[[1,2,3,4,5],5,"sorted"],[[5,4,3,2,1],5,"desc"],[[42],42,"single"],[[-1,-5,-2],-1,"negatives"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [nums,exp,label] of cases){try{const r=f(nums);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
