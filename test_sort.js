const PRIORITY_ORDER={Critical:1,High:2,Medium:3,Low:4};
function getPriority(syms,age){
  if(syms.some(s=>["chest pain","shortness of breath","blurred vision","tremors"].includes(s))||age>70)return"Critical";
  if(syms.some(s=>["fever","dizziness","sweating","vomiting","nausea"].includes(s))||age>60)return"High";
  if(syms.length>=3)return"Medium";
  return"Low";
}
let patientQueue=[
  {id:1,name:"Ravi Kumar",age:58,gender:"Male",symptoms:["chest pain","shortness of breath"],status:"Waiting",token:"C001",priority:"Critical",severityScore:94.2, timestamp: Date.now()-50000},
  {id:2,name:"Priya Sharma",age:34,gender:"Female",symptoms:["fever","cough","fatigue"],status:"Consulting",token:"H001",priority:"High",severityScore:78.5, timestamp: Date.now()-40000},
];
const patientObject = {
        id: Date.now(),
        name: "Pratik",
        age: 23,
        gender: "Male",
        symptoms: ["abdominal pain", "anxiety"],
        status: "Waiting",
        token: "M003",
        priority: "Medium",
        severityScore: 40.1,
        timestamp: Date.now()
};
patientQueue.push(patientObject);
try {
patientQueue.sort((a,b)=>{
        const pa=a.priority || getPriority(a.symptoms,a.age);
        const pb=b.priority || getPriority(b.symptoms,b.age);
        if(PRIORITY_ORDER[pa]!==PRIORITY_ORDER[pb]) return PRIORITY_ORDER[pa]-PRIORITY_ORDER[pb];
        const sa = a.severityScore || 0;
        const sb = b.severityScore || 0;
        if (sa !== sb) return sb - sa;
        return a.token.localeCompare(b.token);
});
console.log("Sort successful");
} catch(e) { console.error("Sort failed", e); }
