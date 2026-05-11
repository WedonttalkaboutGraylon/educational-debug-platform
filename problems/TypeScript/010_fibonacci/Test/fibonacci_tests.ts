import * as path from "path";
async function load(fp: string) { return await import(path.resolve(fp.replace(/\.ts$/,""))); }
async function runTests(fp: string) {
    const m = await load(fp); const f = m.fibonacci;
    const cases: [number,number,string][] = [[0,0,"f(0)"],[1,1,"f(1)"],[2,1,"f(2)"],[3,2,"f(3)"],[4,3,"f(4)"],[5,5,"f(5)"],[6,8,"f(6)"],[7,13,"f(7)"]];
    let passed=0,failed=0; const results: any[]=[];
    for(const [n,exp,label] of cases){try{const r=f(n);if(r===exp){passed++;results.push({test:label,status:"pass"})}else{failed++;results.push({test:label,status:"fail",expected:exp,got:r})}}catch(e:any){failed++;results.push({test:label,status:"error",message:e.message})}}
    return {passed,failed,total:cases.length,results};
}
const fp=process.argv[2]??"starter.ts"; runTests(fp).then(o=>console.log(JSON.stringify(o,null,2)));
