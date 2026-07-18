const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf8');
const js = html.split('<script>')[1].split('</script>')[0];

const scriptContext = `
let window = {};
let document = {
  getElementById: (id) => ({ 
    value: id === 'pName' ? 'Pratik' : (id === 'pAge' ? '23' : (id === 'pGender' ? 'Male' : '')), 
    textContent: '', 
    innerHTML: '',
    style: {},
    classList: { add: ()=>{}, remove: ()=>{} }
  }),
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

${js}

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
`;

fs.writeFileSync('pure_test.js', scriptContext);
