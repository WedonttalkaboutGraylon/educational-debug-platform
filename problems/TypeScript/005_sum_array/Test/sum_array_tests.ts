import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.sumArray;
    const cases: [number[],number,string][] = [[[1,2,3,4,5],15,"basic"],[[10,20],30,"two"],[[0],0,"zero"],[[100],100,"single"],[[-1,-2,-3],-6,"negatives"],[[1,2,3],6,"three"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [nums,exp,label] of cases){try{const r=f(nums);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
