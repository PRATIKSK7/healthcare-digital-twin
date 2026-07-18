
let window = {};
let document = {
  getElementById: (id) => ({ 
    value: id === 'pName' ? 'Pratik' : (id === 'pAge' ? '23' : (id === 'pGender' ? 'Male' : '')), 
    textContent: '', 
    innerHTML: '',
    style: {},
    appendChild: ()=>{},
    classList: { add: ()=>{}, remove: ()=>{} }
  }),
  createElement: () => ({ classList: {add: ()=>{}, remove: ()=>{}}, appendChild: ()=>{} }),
  querySelectorAll: () => [
    {classList: {add: ()=>{}, remove: ()=>{}}},
    {classList: {add: ()=>{}, remove: ()=>{}}},
    {classList: {add: ()=>{}, remove: ()=>{}}},
    {classList: {add: ()=>{}, remove: ()=>{}}},
    {classList: {add: ()=>{}, remove: ()=>{}}},
    {classList: {add: ()=>{}, remove: ()=>{}}}
  ]
};
const Chart = class { constructor() {} };
const fetch = async () => ({
  ok: true,
  json: async () => ({
    severity_score: 40.1,
    priority_category: "Medium",
    waiting_priority: "60 mins",
    initial_clinical_risk: "Significant Discomfort/Risk",
    explanations: []
  })
});
let alert = console.log;
let setInterval = () => {};


// ─── DATA ─────────────────────────────────────────────────────────────────
let currentPatient = null;

const ALL_SYMPTOMS=["abdominal pain","anxiety","appetite loss","back pain","blurred vision","chest pain","cough","depression","diarrhea","dizziness","fatigue","fever","headache","insomnia","joint pain","muscle pain","nausea","rash","runny nose","shortness of breath","sneezing","sore throat","sweating","swelling","tremors","vomiting","weight gain","weight loss"];
const ALL_DISEASES=["Allergy","Anemia","Anxiety","Arthritis","Asthma","Bronchitis","COVID-19","Chronic Kidney Disease","Common Cold","Dementia","Depression","Dermatitis","Diabetes","Epilepsy","Food Poisoning","Gastritis","Heart Disease","Hypertension","IBS","Influenza","Liver Disease","Migraine","Obesity","Parkinson's","Pneumonia","Sinusitis","Stroke","Thyroid Disorder","Tuberculosis","Ulcer"];
const DISEASE_COUNTS={Anxiety:911,Arthritis:896,"Food Poisoning":871,Depression:859,Allergy:858,Bronchitis:856,Dermatitis:856,"Thyroid Disorder":855,Migraine:854,Diabetes:850,"COVID-19":839,Ulcer:833,Hypertension:833,Epilepsy:832,"Liver Disease":830,IBS:830,Pneumonia:830,"Parkinson's":826,Influenza:824,Dementia:823,Obesity:819,Tuberculosis:814,Anemia:814,"Chronic Kidney Disease":807,"Common Cold":805,"Heart Disease":804,Gastritis:804,Sinusitis:795,Stroke:790,Asthma:782};
const SYM_FREQ={"appetite loss":4595,sneezing:4562,headache:4555,"muscle pain":4515,anxiety:4506,depression:4497,fever:4496,"weight loss":4491,swelling:4490,"sore throat":4487};
const MODEL_RESULTS={"Logistic Regression":{accuracy:4.02,precision:4.13,recall:4.02,f1:3.78,color:"#06b6d4"},"Random Forest":{accuracy:3.62,precision:3.61,recall:3.62,f1:3.61,color:"#10b981"},"Gradient Boosting":{accuracy:3.30,precision:3.25,recall:3.30,f1:3.25,color:"#f59e0b"},"Naive Bayes":{accuracy:3.74,precision:3.74,recall:3.74,f1:3.06,color:"#8b5cf6"}};
const DISEASE_SYMPTOM_MAP={"Allergy":["sneezing","runny nose","rash","cough"],"Asthma":["shortness of breath","cough","chest pain"],"COVID-19":["fever","cough","shortness of breath","fatigue"],"Common Cold":["runny nose","sneezing","sore throat","cough","headache"],"Heart Disease":["chest pain","shortness of breath","fatigue","swelling"],"Diabetes":["weight loss","blurred vision","fatigue"],"Hypertension":["headache","dizziness","blurred vision","chest pain"],"Influenza":["fever","muscle pain","fatigue","cough","sore throat"],"Migraine":["headache","nausea","blurred vision"],"Pneumonia":["fever","cough","shortness of breath","chest pain"]};

const CTIP={backgroundColor:"#0f172a",borderColor:"#334155",borderWidth:1,titleColor:"#f1f5f9",bodyColor:"#94a3b8"};
const CLEG={color:"#94a3b8",font:{size:11}};
const CGRID={color:"#334155"};
function hsl(i,n=15){return `hsl(${200+i*(140/n)},70%,55%)`;}

// ─── CLOCK ────────────────────────────────────────────────────────────────
setInterval(()=>{const n=new Date();document.getElementById("clock").textContent=`🟢 ${n.toLocaleDateString()} ${n.toLocaleTimeString()}`;},1000);

// ─── TABS ─────────────────────────────────────────────────────────────────
function showTab(i,btn){
  document.querySelectorAll(".tab-content").forEach(t=>t.classList.remove("active"));
  document.querySelectorAll(".nav-tab").forEach(b=>b.classList.remove("active"));
  document.getElementById("tab"+i).classList.add("active");
  btn.classList.add("active");
}

// ─── CHARTS ───────────────────────────────────────────────────────────────
// Age
new Chart(document.getElementById("ageChart"),{type:"bar",data:{labels:["<18","18-30","30-45","45-60","60+"],datasets:[{data:[5118,3337,4061,4216,8268],backgroundColor:"#06b6d4",borderRadius:6}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b"},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID}}}});
// Gender
new Chart(document.getElementById("genderChart"),{type:"doughnut",data:{labels:["Other","Female","Male"],datasets:[{data:[8393,8336,8271],backgroundColor:["#8b5cf6","#ec4899","#06b6d4"],borderWidth:0,hoverOffset:8}]},options:{responsive:true,plugins:{legend:{position:"bottom",labels:CLEG},tooltip:CTIP}}});
// Disease top15
const t15=Object.entries(DISEASE_COUNTS).sort((a,b)=>b[1]-a[1]).slice(0,15);
new Chart(document.getElementById("diseaseChart"),{type:"bar",data:{labels:t15.map(([n])=>n),datasets:[{data:t15.map(([,v])=>v),backgroundColor:t15.map((_,i)=>hsl(i)),borderRadius:4}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b",font:{size:10},maxRotation:35},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID}}}});
// Symptom cards
const sc=document.getElementById("symCards");
Object.entries(SYM_FREQ).forEach(([s,c],i)=>{sc.innerHTML+=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:800;color:hsl(${180+i*15},70%,55%)">${c.toLocaleString()}</div><div style="font-size:11px;color:#94a3b8;margin-top:4px;text-transform:capitalize">${s}</div></div>`;});

// Model metric bars
function mBar(label,val,color){return `<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span style="color:#64748b;font-size:11px;text-transform:capitalize">${label}</span><span style="color:${color};font-weight:700;font-size:12px">${val}%</span></div><div style="height:4px;background:#334155;border-radius:2px"><div style="height:100%;width:${val*20}%;background:${color};border-radius:2px"></div></div></div>`;}
[["lr","Logistic Regression"],["rf","Random Forest"],["gb","Gradient Boosting"],["nb","Naive Bayes"]].forEach(([id,name])=>{const m=MODEL_RESULTS[name];document.getElementById(id+"_m").innerHTML=["accuracy","precision","recall","f1"].map(k=>mBar(k,m[k],m.color)).join("");});

// Accuracy chart
const mNames=Object.keys(MODEL_RESULTS);
new Chart(document.getElementById("accChart"),{type:"bar",data:{labels:mNames.map(n=>n.split(" ")[0]),datasets:[{label:"Accuracy %",data:mNames.map(n=>MODEL_RESULTS[n].accuracy),backgroundColor:mNames.map(n=>MODEL_RESULTS[n].color),borderRadius:6}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b"},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID,min:0,max:5}}}});
// All metrics
new Chart(document.getElementById("allMetrics"),{type:"bar",data:{labels:mNames.map(n=>n.split(" ")[0]),datasets:[{label:"Accuracy",data:mNames.map(n=>MODEL_RESULTS[n].accuracy),backgroundColor:"#06b6d4",borderRadius:3},{label:"Precision",data:mNames.map(n=>MODEL_RESULTS[n].precision),backgroundColor:"#10b981",borderRadius:3},{label:"Recall",data:mNames.map(n=>MODEL_RESULTS[n].recall),backgroundColor:"#f59e0b",borderRadius:3},{label:"F1 Score",data:mNames.map(n=>MODEL_RESULTS[n].f1),backgroundColor:"#8b5cf6",borderRadius:3}]},options:{responsive:true,plugins:{legend:{labels:CLEG},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b"},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID,min:0,max:5}}}});

// Analytics charts
const tp10=Object.entries(DISEASE_COUNTS).sort((a,b)=>b[1]-a[1]).slice(0,10);
new Chart(document.getElementById("top10Chart"),{type:"line",data:{labels:tp10.map(([n])=>n),datasets:[{data:tp10.map(([,v])=>v),borderColor:"#06b6d4",backgroundColor:"#06b6d420",fill:true,tension:0.4,pointBackgroundColor:"#06b6d4",pointRadius:5}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b",font:{size:10},maxRotation:30},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID}}}});
const sfE=Object.entries(SYM_FREQ).sort((a,b)=>b[1]-a[1]);
new Chart(document.getElementById("symFreqChart"),{type:"bar",data:{labels:sfE.map(([n])=>n),datasets:[{data:sfE.map(([,v])=>v),backgroundColor:sfE.map((_,i)=>`hsl(${180+i*15},70%,55%)`),borderRadius:4}]},options:{indexAxis:"y",responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b"},grid:CGRID},y:{ticks:{color:"#64748b",font:{size:11}},grid:CGRID}}}});
const allDE=Object.entries(DISEASE_COUNTS).sort((a,b)=>b[1]-a[1]);
new Chart(document.getElementById("allDisChart"),{type:"bar",data:{labels:allDE.map(([n])=>n),datasets:[{data:allDE.map(([,v])=>v),backgroundColor:allDE.map((_,i)=>`hsl(${190+i*5},65%,55%)`),borderRadius:3}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:CTIP},scales:{x:{ticks:{color:"#64748b",font:{size:9},maxRotation:40},grid:CGRID},y:{ticks:{color:"#64748b"},grid:CGRID}}}});

// Heatmap
const hmSyms=ALL_SYMPTOMS.slice(0,16);
let ht=`<table style="border-collapse:collapse;font-size:11px"><thead><tr><th style="color:#64748b;padding:6px 10px;text-align:left;min-width:130px;background:#0f172a;font-weight:600">Disease</th>`;
hmSyms.forEach(s=>{ht+=`<th style="color:#64748b;padding:2px;text-align:center;min-width:30px;writing-mode:vertical-rl;transform:rotate(180deg);height:80px;font-size:10px;background:#0f172a;font-weight:400">${s}</th>`;});
ht+=`</tr></thead><tbody>`;
Object.entries(DISEASE_SYMPTOM_MAP).forEach(([d,ss])=>{
  ht+=`<tr><td style="color:#94a3b8;padding:5px 10px;font-weight:600;border-bottom:1px solid #0f172a">${d}</td>`;
  hmSyms.forEach(sym=>{const has=ss.includes(sym);ht+=`<td style="padding:3px;text-align:center;border-bottom:1px solid #0f172a"><div style="width:24px;height:24px;margin:0 auto;border-radius:3px;background:${has?"#06b6d4":"#334155"};opacity:${has?1:0.3}"></div></td>`;});
  ht+=`</tr>`;
});
document.getElementById("heatmap").innerHTML=ht+`</tbody></table><div style="color:#64748b;font-size:11px;margin-top:8px">🔵 Cyan = symptom associated with disease</div>`;

// ─── SYMPTOM PILLS ────────────────────────────────────────────────────────
let selSyms=[],selQSyms=[];
function buildPills(cid,arr,fn){
  const c=document.getElementById(cid);c.innerHTML="";
  ALL_SYMPTOMS.forEach(s=>{const b=document.createElement("button");b.className="pill"+(arr.includes(s)?" on":"");b.textContent=s;b.onclick=()=>fn(s);c.appendChild(b);});
}
function toggleSym(s){selSyms=selSyms.includes(s)?selSyms.filter(x=>x!==s):[...selSyms,s];document.getElementById("symCount").textContent=selSyms.length;buildPills("symptomPills",selSyms,toggleSym);}
function toggleQSym(s){selQSyms=selQSyms.includes(s)?selQSyms.filter(x=>x!==s):[...selQSyms,s];buildPills("queuePills",selQSyms,toggleQSym);}
buildPills("symptomPills",selSyms,toggleSym);
buildPills("queuePills",selQSyms,toggleQSym);

// ─── AI PREDICT ───────────────────────────────────────────────────────────

async function predict(){
  const key="dev_secret_key_123";
  const errEl=document.getElementById("aiErr");
  const resEl=document.getElementById("aiResult");
  errEl.style.display="none";
  
  const pName=document.getElementById("pName").value.trim();
  if(!pName){errEl.textContent="⚠ Please enter the Patient Name.";errEl.style.display="block";return;}
  if(selSyms.length===0){errEl.textContent="⚠ Please select at least one symptom.";errEl.style.display="block";return;}
  
  const btn=document.getElementById("predictBtn");
  btn.textContent="🔄 Analyzing...";btn.disabled=true;
  resEl.innerHTML=`<div class="card" style="text-align:center;padding:48px"><div style="font-size:40px;margin-bottom:12px">⚙️</div><div style="color:#06b6d4;font-size:15px;font-weight:700">Backend AI is analyzing your symptoms...</div></div>`;
  currentPatient={
    name: pName,
    age:parseInt(document.getElementById("pAge").value||45),
    gender:document.getElementById("pGender").value,
    symptoms:selSyms,
    hr:parseInt(document.getElementById("pHr").value||75),
    sbp:parseInt(document.getElementById("pSbp").value||120),
    smoking:document.getElementById("pSmoking").value === "true",
    symptom_duration_days:parseInt(document.getElementById("pDuration").value||5),
    symptom_severity:parseInt(document.getElementById("pSeverity").value||5)
  };
  try{
    const res=await fetch("http://127.0.0.1:8000/api/v1/predict/frontend",{method:"POST",headers:{"Content-Type":"application/json","X-API-Key":key},body:JSON.stringify(currentPatient)});
    if(!res.ok)throw new Error("Backend error "+res.status);
    const parsed=await res.json();
    currentPatient.prediction = parsed;
    const pcat = parsed.priority_category;
    const sc=pcat==="Critical"?"#ef4444":pcat==="High"?"#f97316":pcat==="Medium"?"#eab308":"#22c55e";
    const score = parsed.severity_score;
    
    let html=`<div class="card" style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
        <span style="color:#f1f5f9;font-weight:700;font-size:15px">Triage Risk Assessment</span>
        <span class="badge" style="background:${sc};color:#fff">${pcat} Priority</span>
      </div>
      <div style="text-align:center;margin-bottom:20px">
        <div style="font-size:42px;font-weight:800;color:${sc};line-height:1">${score}<span style="font-size:18px;color:#94a3b8">/100</span></div>
        <div style="color:#64748b;font-size:13px;margin-top:4px">Calculated Severity Score</div>
      </div>
      <div style="height:10px;background:#334155;border-radius:5px;overflow:hidden;margin-bottom:24px">
        <div style="height:100%;width:${score}%;background:${sc};border-radius:5px;transition:width 1s ease"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:16px;background:#1e293b;padding:12px;border-radius:8px">
        <div>
          <div style="color:#94a3b8;font-size:12px;margin-bottom:2px">Clinical Risk</div>
          <div style="color:#f1f5f9;font-weight:600;font-size:14px">${parsed.initial_clinical_risk}</div>
        </div>
        <div style="text-align:right">
          <div style="color:#94a3b8;font-size:12px;margin-bottom:2px">Est. Wait Time</div>
          <div style="color:${sc};font-weight:600;font-size:14px">${parsed.waiting_priority}</div>
        </div>
      </div>
      <div style="color:#f1f5f9;font-weight:600;font-size:13px;margin-bottom:10px">Top Contributing Factors:</div>`;
      
    if(parsed.explanations && parsed.explanations.length>0){
      parsed.explanations.forEach(e=>{
        const isInc = e.contribution.includes('+');
        const col=isInc?'#ef4444':'#22c55e';
        const icon = isInc?'⬆️':'⬇️';
        html+=`<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #334155">
          <span style="color:#cbd5e1;font-size:13px;font-weight:500;text-transform:capitalize">${e.feature.replace(/_/g, ' ')}</span>
          <span style="color:${col};font-size:13px;font-weight:600">${icon} ${e.contribution}</span>
        </div>`;
      });
    }
    
    html+=`</div>
    <div style="display:flex;gap:12px">
      <button class="btn-primary" onclick="addPatientFromPredictor()" style="flex:1;font-size:15px">📥 Add to Queue</button>
      <button onclick="resetPredictor()" style="background:transparent;border:1px solid #334155;color:#64748b;border-radius:8px;padding:14px;font-size:15px;cursor:pointer;font-weight:700;font-family:inherit">🔄 Reset</button>
    </div>`;
    resEl.innerHTML=html;
  }catch(e){errEl.textContent="❌ Error: "+e.message;errEl.style.display="block";resEl.innerHTML=`<div class="card" style="text-align:center;padding:48px"><div style="font-size:52px;margin-bottom:12px">🩺</div><div style="color:#64748b">Select symptoms and try again.</div></div>`;}
  btn.textContent="🏥 Assess Triage Priority";btn.disabled=false;
}

function resetPredictor() {
    document.getElementById("pName").value = "";
    document.getElementById("pAge").value = "";
    document.getElementById("pHr").value = "";
    document.getElementById("pSbp").value = "";
    document.getElementById("pDuration").value = "";
    document.getElementById("pSeverity").value = "5";
    document.getElementById("pSeverityVal").textContent = "5";
    selSyms = [];
    buildPills("symptomPills", selSyms, toggleSym);
    document.getElementById("aiResult").innerHTML = `<div class="card" style="text-align:center;padding:48px"><div style="font-size:52px;margin-bottom:12px">🩺</div><div style="color:#64748b;font-size:15px">Select symptoms and click Predict to get AI-powered disease predictions</div></div>`;
    currentPatient = null;
}

function addPatientFromPredictor() {
    if (!currentPatient || !currentPatient.prediction) {
        alert("Please assess the patient first.");
        return;
    }
    
    console.log("Current Patient", currentPatient);
    console.log("Prediction", currentPatient.prediction);
    console.log("Queue Before", patientQueue);
    
    // Add to global patients array
    const priority = currentPatient.prediction.priority_category;
    const token = generateToken(priority);
    
    const patientObject = {
        id: Date.now(),
        name: currentPatient.name,
        age: currentPatient.age,
        gender: currentPatient.gender,
        symptoms: [...currentPatient.symptoms],
        vitals: {
            hr: currentPatient.hr,
            sbp: currentPatient.sbp,
            smoking: currentPatient.smoking,
            duration: currentPatient.symptom_duration_days
        },
        status: "Waiting",
        token: token,
        baseline: currentPatient,
        priority: priority,
        severityScore: currentPatient.prediction.severity_score,
        estimatedWait: currentPatient.prediction.waiting_priority,
        shapExplanation: currentPatient.prediction.explanations,
        timestamp: Date.now()
    };
    
    patientQueue.push(patientObject);
    
    // Immediately sort the queue
    patientQueue.sort((a,b)=>{
        const pa=a.priority || getPriority(a.symptoms,a.age);
        const pb=b.priority || getPriority(b.symptoms,b.age);
        if(PRIORITY_ORDER[pa]!==PRIORITY_ORDER[pb]) return PRIORITY_ORDER[pa]-PRIORITY_ORDER[pb];
        const sa = a.severityScore || 0;
        const sb = b.severityScore || 0;
        if (sa !== sb) return sb - sa;
        return a.token.localeCompare(b.token);
    });
    
    renderQueue();
    resetPredictor();
    
    // Switch to Tab 4 (Queue)
    const tabBtns = document.querySelectorAll(".nav-tab");
    showTab(4, tabBtns[4]);
}

// ─── QUEUE ────────────────────────────────────────────────────────────────
// Token prefix by severity: C = Critical, H = High, M = Medium, L = Low
// Token format: C001, H001, M001, L001 — lower number = seen sooner within same tier
const PC={Critical:"#ef4444",High:"#f97316",Medium:"#eab308",Low:"#22c55e"};
const SC={Waiting:"#3b82f6",Consulting:"#f59e0b",Completed:"#22c55e"};
const PRIORITY_ORDER={Critical:1,High:2,Medium:3,Low:4};
const TOKEN_PREFIX={Critical:"C",High:"H",Medium:"M",Low:"L"};
const TOKEN_COUNTERS={Critical:1,High:1,Medium:1,Low:1};
const TOKEN_ICON={Critical:"🚨",High:"⚠️",Medium:"🔔",Low:"✅"};
const WAIT_MINS={Critical:0,High:10,Medium:20,Low:35};

function getPriority(syms,age){
  if(syms.some(s=>["chest pain","shortness of breath","blurred vision","tremors"].includes(s))||age>70)return"Critical";
  if(syms.some(s=>["fever","dizziness","sweating","vomiting","nausea"].includes(s))||age>60)return"High";
  if(syms.length>=3)return"Medium";
  return"Low";
}

function generateToken(priority){
  const num=String(TOKEN_COUNTERS[priority]).padStart(3,"0");
  TOKEN_COUNTERS[priority]++;
  return TOKEN_PREFIX[priority]+num;
}

function getEstWait(p, sortedWaiting){
  if(p.status==="Consulting") return"🟡 In Progress";
  if(p.status==="Completed") return"✅ Done";
  // Fallback to queue rank if model hasn't estimated it
  if (p.wait_time) return p.wait_time;
  
  const rank=sortedWaiting.findIndex(x=>x.id===p.id);
  const base=WAIT_MINS[p.priority || getPriority(p.symptoms,p.age)];
  const totalWait=base+(rank*8);
  if(totalWait===0) return"⚡ Immediate";
  return`~${totalWait} min`;
}

let patientQueue=[
  {id:1,name:"Ravi Kumar",age:58,gender:"Male",symptoms:["chest pain","shortness of breath"],status:"Waiting",token:"C001",priority:"Critical",severityScore:94.2, timestamp: Date.now()-50000},
  {id:2,name:"Priya Sharma",age:34,gender:"Female",symptoms:["fever","cough","fatigue"],status:"Consulting",token:"H001",priority:"High",severityScore:78.5, timestamp: Date.now()-40000},
  {id:3,name:"Arjun Mehta",age:72,gender:"Male",symptoms:["tremors","dizziness"],status:"Waiting",token:"C002",priority:"Critical",severityScore:85.4, timestamp: Date.now()-30000},
  {id:4,name:"Sunita Devi",age:28,gender:"Female",symptoms:["headache","nausea","rash"],status:"Waiting",token:"M001",priority:"Medium",severityScore:55.0, timestamp: Date.now()-20000},
  {id:5,name:"Kiran Patel",age:45,gender:"Male",symptoms:["cough"],status:"Waiting",token:"L001",priority:"Low",severityScore:24.1, timestamp: Date.now()-10000},
];
// Sync counters with demo data
TOKEN_COUNTERS.Critical=3;TOKEN_COUNTERS.High=2;TOKEN_COUNTERS.Medium=2;TOKEN_COUNTERS.Low=2;

function sortPatients(list){
  return [...list].sort((a,b)=>{
    const pa=a.priority || getPriority(a.symptoms,a.age);
    const pb=b.priority || getPriority(b.symptoms,b.age);
    if(PRIORITY_ORDER[pa]!==PRIORITY_ORDER[pb]) return PRIORITY_ORDER[pa]-PRIORITY_ORDER[pb];
    
    const sa = a.severityScore || 0;
    const sb = b.severityScore || 0;
    if (sa !== sb) return sb - sa;
    
    return a.token.localeCompare(b.token);
  });
}

function renderQueue(){
  document.getElementById("cntW").textContent=patientQueue.filter(p=>p.status==="Waiting").length;
  document.getElementById("cntC").textContent=patientQueue.filter(p=>p.status==="Consulting").length;
  document.getElementById("cntD").textContent=patientQueue.filter(p=>p.status==="Completed").length;
  const body=document.getElementById("queueBody");
  if(!patientQueue.length){body.innerHTML=`<tr><td colspan="9" style="text-align:center;padding:40px;color:#64748b">No patients in queue</td></tr>`;return;}

  // The queue is now kept sorted in-place, but just in case we re-sort for rendering safety
  patientQueue.sort((a,b)=>{
        const pa=a.priority || getPriority(a.symptoms,a.age);
        const pb=b.priority || getPriority(b.symptoms,b.age);
        if(PRIORITY_ORDER[pa]!==PRIORITY_ORDER[pb]) return PRIORITY_ORDER[pa]-PRIORITY_ORDER[pb];
        const sa = a.severityScore || 0;
        const sb = b.severityScore || 0;
        if (sa !== sb) return sb - sa;
        return a.token.localeCompare(b.token);
  });
  
  const sortedWaiting=patientQueue.filter(p=>p.status==="Waiting");

  body.innerHTML=patientQueue.map((p,rank)=>{
    const pr=p.priority || getPriority(p.symptoms,p.age);
    const score = p.severityScore ? p.severityScore.toFixed(1) : "—";
    const pc=PC[pr],sc=SC[p.status];
    const w=getEstWait(p,sortedWaiting);
    const st=p.symptoms.slice(0,3).join(", ")+(p.symptoms.length>3?` +${p.symptoms.length-3}`:"");
    const isTop=p.status==="Waiting"&&sortedWaiting[0]?.id===p.id;
    const rowBg=isTop?"background:#1e3a2f;":"";
    // Token cell styled by severity
    const tokenBg=`background:${pc}22;color:${pc};border:1px solid ${pc}55;padding:5px 10px;border-radius:8px;font-weight:800;font-size:13px;letter-spacing:1px;display:inline-block`;
    return `<tr style="${rowBg}">
      <td><span style="${tokenBg}">${TOKEN_ICON[pr]} ${p.token}</span></td>
      <td style="color:#f1f5f9;font-weight:600">${p.name}${isTop?` <span style="background:#10b981;color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;margin-left:6px">NEXT</span>`:""}</td>
      <td style="color:#94a3b8">${p.age}</td>
      <td style="color:#94a3b8;font-size:12px">${st||"—"}</td>
      <td style="color:${pc};font-weight:700">${score}</td>
      <td><span class="badge" style="background:${pc}33;color:${pc}">${pr}</span></td>
      <td><span class="badge" style="background:${sc}20;color:${sc}">${p.status}</span></td>
      <td style="color:#94a3b8;font-size:12px">${w}</td>
      <td><div style="display:flex;gap:6px;flex-wrap:wrap">
        ${p.status!=="Consulting"?`<button class="btn-sm" style="background:#f59e0b;color:#fff" onclick="consultPatient(${p.id})">Consult</button>`:""}
        ${p.status!=="Completed"?`<button class="btn-sm" style="background:#22c55e;color:#fff" onclick="setSt(${p.id},'Completed')">Done</button>`:""}
        <button class="btn-sm" style="background:transparent;border:1px solid #ef4444;color:#ef4444" onclick="rmP(${p.id})">Remove</button>
      </div></td>
    </tr>`;
  }).join("");
}
function setSt(id,s){patientQueue=patientQueue.map(p=>p.id===id?{...p,status:s}:p);renderQueue();}
function rmP(id){patientQueue=patientQueue.filter(p=>p.id!==id);renderQueue();}

function consultPatient(id) {
    // Set status to consulting
    setSt(id, 'Consulting');
    
    // Switch to Digital Twin tab
    const tabBtns = document.querySelectorAll(".nav-tab");
    showTab(5, tabBtns[5]);
    
    // Load patient into Digital Twin
    document.getElementById("dtPatientSelect").value = id;
    loadTwinPatient();
}
renderQueue();

// ─── DIGITAL TWIN ─────────────────────────────────────────────────────────

// Populate symptom pills for Digital Twin tab
let dtSelSyms = [];
function buildDtPills() {
  const c = document.getElementById("dtSymPills"); c.innerHTML = "";
  ALL_SYMPTOMS.forEach(s => {
    const b = document.createElement("button"); b.className = "pill" + (dtSelSyms.includes(s) ? " on" : "");
    b.textContent = s; b.onclick = () => { dtSelSyms = dtSelSyms.includes(s) ? dtSelSyms.filter(x => x !== s) : [...dtSelSyms, s]; buildDtPills(); };
    c.appendChild(b);
  });
}
buildDtPills();

// Populate patient dropdown from queue
function refreshDtDropdown() {
  const sel = document.getElementById("dtPatientSelect");
  sel.innerHTML = '<option value="">— Select a patient —</option>';
  patientQueue.forEach(p => {
    const o = document.createElement("option"); o.value = p.id; o.textContent = `${p.token} — ${p.name} (${p.age}y, ${p.gender})`;
    sel.appendChild(o);
  });
}

function loadTwinPatient() {
  const id = parseInt(document.getElementById("dtPatientSelect").value);
  if (!id) return;
  const p = patientQueue.find(x => x.id === id);
  if (!p) return;
  document.getElementById("dtCustomName").value = p.name;
  document.getElementById("dtAge").value = p.age;
  document.getElementById("dtGender").value = p.gender;
  dtSelSyms = [...p.symptoms];
  buildDtPills();
  // Auto-fill baseline vitals based on symptoms
  autofillVitals(p.symptoms, p.age);
}

function autofillVitals(syms, age) {
  const hasFever = syms.includes("fever");
  const hasChest = syms.includes("chest pain") || syms.includes("shortness of breath");
  const hasDiz = syms.includes("dizziness");
  document.getElementById("dtHR").value = hasChest ? 98 : hasFever ? 104 : 72;
  document.getElementById("dtSBP").value = hasChest ? 145 : hasDiz ? 90 : 120;
  document.getElementById("dtDBP").value = hasChest ? 95 : hasDiz ? 60 : 80;
  document.getElementById("dtTemp").value = hasFever ? 38.8 : 37.0;
  document.getElementById("dtSpO2").value = syms.includes("shortness of breath") ? 91 : 98;
  document.getElementById("dtGlucose").value = age > 55 ? 115 : 95;
  document.getElementById("dtBMI").value = syms.includes("weight gain") ? 28.4 : syms.includes("weight loss") ? 19.2 : 23.5;
  document.getElementById("dtCRP").value = hasFever ? 12.4 : hasChest ? 6.1 : 1.5;
}

// Show tab 5 triggers dropdown refresh
const origShowTab = showTab;
window.showTab = function (i, btn) {
  origShowTab(i, btn);
  if (i === 5) refreshDtDropdown();
};

function resetTwin() {
  document.getElementById("dtOutput").style.display = "none";
  document.getElementById("dtLoading").style.display = "none";
  document.getElementById("dtError").style.display = "none";
}

async function runDigitalTwin() {
  const name = document.getElementById("dtCustomName").value.trim() || "Unknown Patient";
  const age = parseInt(document.getElementById("dtAge").value) || 45;
  const gender = document.getElementById("dtGender").value;
  const scenario = document.getElementById("dtScenario").value;
  const apiKey = document.getElementById("dtApiKey").value.trim() || "dev_secret_key_123";
  const hr = document.getElementById("dtHR").value || 72;
  const sbp = document.getElementById("dtSBP").value || 120;
  const dbp = document.getElementById("dtDBP").value || 80;
  const temp = document.getElementById("dtTemp").value || 37.0;
  const spo2 = document.getElementById("dtSpO2").value || 98;
  const glucose = document.getElementById("dtGlucose").value || 95;
  const bmi = document.getElementById("dtBMI").value || 23.5;
  const crp = document.getElementById("dtCRP").value || 1.5;
  const syms = dtSelSyms.length ? dtSelSyms : ["fatigue", "headache"];

  document.getElementById("dtError").style.display = "none";
  document.getElementById("dtOutput").style.display = "none";
  document.getElementById("dtLoading").style.display = "block";

  const loadMsgs = ["Initializing physiological model...", "Mapping organ systems...", "Calibrating vital baselines...", "Running scenario simulation...", "Generating clinical narrative..."];
  let mi = 0;
  const loadInterval = setInterval(() => { document.getElementById("dtLoadMsg").textContent = loadMsgs[mi++ % loadMsgs.length]; }, 900);

  const scenarioLabels = { progression: "Disease Progression (3-month)", treatment: "Treatment Response", stress: "Physiological Stress Test", surgery: "Pre-Surgery Risk", lifestyle: "Lifestyle Intervention", medication: "Medication Interaction" };

  let twinData = null;
  try {
    const dtPayload = {
      name, age, gender, symptoms: syms, hr: parseInt(hr), sbp: parseInt(sbp), dbp: parseInt(dbp), temp: parseFloat(temp), spo2: parseInt(spo2), glucose: parseInt(glucose), bmi: parseFloat(bmi), crp: parseFloat(crp), scenario: scenarioLabels[scenario]
    };
    const res = await fetch("http://127.0.0.1:8000/api/v1/simulate/frontend", {
      method: "POST", headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
      body: JSON.stringify(dtPayload)
    });
    if(!res.ok) throw new Error("Backend error "+res.status);
    twinData = await res.json();
  } catch (e) {
    clearInterval(loadInterval);
    document.getElementById("dtLoading").style.display = "none";
    document.getElementById("dtError").textContent = "❌ API Error: " + e.message;
    document.getElementById("dtError").style.display = "block";
    return;
  }

  clearInterval(loadInterval);
  renderTwin(twinData, name, age, gender, scenarioLabels[scenario]);
  
  // Sync back to queue if it's an existing patient
  const pid = parseInt(document.getElementById("dtPatientSelect").value);
  if (pid) {
      const pIdx = patientQueue.findIndex(x => x.id === pid);
      if (pIdx !== -1) {
          patientQueue[pIdx].priority = twinData.overallRisk;
          
          // Extract score and wait time from stats
          const scoreStat = twinData.stats.find(s => s.label === "CatBoost Severity");
          if (scoreStat) {
              const scoreMatch = scoreStat.value.match(/(\d+(?:\.\d+)?)/);
              if (scoreMatch) patientQueue[pIdx].severityScore = parseFloat(scoreMatch[1]);
          }
          
          const waitStat = twinData.stats.find(s => s.label === "Est. Wait Time");
          if (waitStat) {
              patientQueue[pIdx].estimatedWait = waitStat.value;
          }
          
          renderQueue(); // Re-sort and render
      }
  }
}

function applyTreatment(treatment, dose) {
    const hrEl = document.getElementById("dtHR");
    const spoEl = document.getElementById("dtSpO2");
    const sbpEl = document.getElementById("dtSBP");
    const tempEl = document.getElementById("dtTemp");
    
    // Heuristic vital adjustments based on treatment
    if (treatment === 'Oxygen Therapy') {
        spoEl.value = Math.min(100, parseInt(spoEl.value || 90) + 5);
        hrEl.value = Math.max(60, parseInt(hrEl.value || 90) - 8);
    } else if (treatment === 'IV Fluids') {
        sbpEl.value = Math.min(140, parseInt(sbpEl.value || 90) + 15);
        hrEl.value = Math.max(60, parseInt(hrEl.value || 110) - 10);
    } else if (treatment === 'Vasopressors') {
        sbpEl.value = Math.min(180, parseInt(sbpEl.value || 70) + 25);
    } else if (treatment === 'Antipyretics') {
        tempEl.value = Math.max(36.5, parseFloat(tempEl.value || 39.0) - 1.2).toFixed(1);
        hrEl.value = Math.max(60, parseInt(hrEl.value || 100) - 12);
    } else if (treatment === 'Bronchodilators') {
        spoEl.value = Math.min(100, parseInt(spoEl.value || 92) + 3);
        hrEl.value = parseInt(hrEl.value || 80) + 10;
    }
    
    // Trigger Digital Twin Run immediately
    runDigitalTwin();
}

function generateDemoTwin(name, age, gender, syms, hr, sbp, dbp, temp, spo2, glucose, bmi, crp, scenario) {
  // Function removed, handled by backend.
  return null;
}

let dtChart = null;
function renderTwin(data, name, age, gender, scenarioLabel) {
  document.getElementById("dtLoading").style.display = "none";
  document.getElementById("dtOutput").style.display = "block";

  document.getElementById("dtTwinName").textContent = "🧬 " + name + " — Digital Twin";
  document.getElementById("dtTwinMeta").textContent = `${age}y • ${gender} • Scenario: ${scenarioLabel}`;

  // Risk badges
  const riskColor = { Low: "#22c55e", Moderate: "#f59e0b", High: "#ef4444", Critical: "#ef4444" };
  const rc = riskColor[data.overallRisk] || "#94a3b8";
  document.getElementById("dtRiskBadges").innerHTML = `
    <span style="background:${rc}22;color:${rc};border:1px solid ${rc}55;padding:6px 16px;border-radius:8px;font-weight:800;font-size:13px">${data.overallRisk} Risk</span>
    <span style="background:#7c3aed22;color:#a78bfa;border:1px solid #7c3aed55;padding:6px 16px;border-radius:8px;font-weight:700;font-size:12px">🔬 ${data.primaryCondition}</span>`;

  // Stat cards
  document.getElementById("dtStatCards").innerHTML = (data.stats || []).map(s =>
    `<div class="dt-stat" style="border-top:3px solid ${s.color}">
      <div style="font-size:20px;font-weight:800;color:${s.color};margin:6px 0">${s.value}</div>
      <div style="color:#64748b;font-size:12px">${s.label}</div>
    </div>`).join("");

  // Vitals
  const flagColors = { Normal: "#22c55e", High: "#ef4444", Low: "#f97316", Critical: "#ef4444", Borderline: "#f59e0b" };
  document.getElementById("dtVitalsDisplay").innerHTML = (data.vitalStatus || []).map(v => {
    const fc = flagColors[v.flag] || "#94a3b8";
    return `<div class="dt-vital"><span style="color:#94a3b8;font-size:13px">${v.label}</span><div style="display:flex;align-items:center;gap:8px"><span style="color:#f1f5f9;font-weight:700">${v.value}</span><span class="dt-badge" style="background:${fc}22;color:${fc}">${v.flag}</span></div></div>`;
  }).join("");

  // Organ systems
  document.getElementById("dtOrganGrid").innerHTML = (data.organSystems || []).map(o => {
    const hc = o.health >= 80 ? "#22c55e" : o.health >= 60 ? "#f59e0b" : "#ef4444";
    return `<div class="organ-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <span style="font-size:18px">${o.icon}</span>
        <span style="color:${hc};font-weight:800;font-size:14px">${o.health}%</span>
      </div>
      <div style="color:#f1f5f9;font-size:11px;font-weight:600;margin-bottom:6px">${o.name}</div>
      <div style="height:4px;background:#334155;border-radius:2px"><div style="height:100%;width:${o.health}%;background:${hc};border-radius:2px;transition:width .8s"></div></div>
      <div style="color:${hc};font-size:10px;margin-top:4px">${o.status}</div>
    </div>`;
  }).join("");

  // Sandbox Init
  document.getElementById("dtNarrative").innerHTML = `<span style="color:#06b6d4">Simulation Initialized.</span> Baseline severity score calculated. Ready for interventions.`;

  // Narrative
  document.getElementById("dtNarrative").innerHTML = data.narrative || "No narrative available.";

  // Recommendations
  document.getElementById("dtRecommendations").innerHTML = (data.recommendations || []).map(r =>
    `<div style="background:#0f172a;border-left:3px solid #10b981;border-radius:8px;padding:12px;color:#94a3b8;font-size:13px;line-height:1.5">${r}</div>`).join("");

  // Chart
  if (dtChart) { dtChart.destroy(); dtChart = null; }
  const td = data.projectedTrends;
  dtChart = new Chart(document.getElementById("dtTrendChart"), {
    type: "line",
    data: {
      labels: td.labels,
      datasets: [
        { label: "Heart Rate (bpm)", data: td.heartRate, borderColor: "#ef4444", backgroundColor: "#ef444415", fill: true, tension: 0.4, pointRadius: 4 },
        { label: "Systolic BP (mmHg)", data: td.systolicBP, borderColor: "#f59e0b", backgroundColor: "#f59e0b15", fill: true, tension: 0.4, pointRadius: 4 },
        { label: "SpO2 (%)", data: td.spo2, borderColor: "#06b6d4", backgroundColor: "#06b6d415", fill: true, tension: 0.4, pointRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: CLEG }, tooltip: CTIP },
      scales: {
        x: { ticks: { color: "#64748b" }, grid: CGRID },
        y: { ticks: { color: "#64748b" }, grid: CGRID }
      }
    }
  });
}

function loadDemoTwin() {
  document.getElementById("dtCustomName").value = "Ravi Kumar";
  document.getElementById("dtAge").value = 58;
  document.getElementById("dtGender").value = "Male";
  dtSelSyms = ["chest pain", "shortness of breath", "sweating"];
  buildDtPills();
  autofillVitals(dtSelSyms, 58);
  document.getElementById("dtScenario").value = "progression";
  runDigitalTwin();
}


// Overrides for testing
currentPatient = {
  name: "Pratik", age: 23, gender: "Male",
  symptoms: ["anxiety", "joint pain"],
  hr: 89, sbp: 143, smoking: false, symptom_duration_days: 7,
  prediction: {
    severity_score: 40.1,
    priority_category: "Medium",
    waiting_priority: "60 mins",
    initial_clinical_risk: "Significant",
    explanations: []
  }
};

addPatientFromPredictor();
console.log("Success! Queue length: " + patientQueue.length);
