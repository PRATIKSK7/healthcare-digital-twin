const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('frontend/index.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });

// Mock Chart to prevent errors
dom.window.Chart = class Chart { constructor() {} };

// Mock fetch
dom.window.fetch = async () => ({
  ok: true,
  json: async () => ({
    severity_score: 40.1,
    priority_category: "Medium",
    waiting_priority: "60 mins",
    initial_clinical_risk: "Significant Discomfort/Risk",
    explanations: []
  })
});

setTimeout(async () => {
  try {
    const win = dom.window;
    win.document.getElementById('pName').value = "Pratik";
    win.document.getElementById('pAge').value = "23";
    win.document.getElementById('pGender').value = "Male";
    
    win.toggleSym("anxiety");
    win.toggleSym("joint pain");
    win.toggleSym("muscle pain");
    
    await win.predict();
    console.log("Prediction complete. currentPatient:", win.currentPatient.name);
    console.log("Before click, queue length:", win.patientQueue.length);
    
    win.addPatientFromPredictor();
    console.log("After click, queue length:", win.patientQueue.length);
    
    // Check if it switched tab
    console.log("Active tab id:", win.document.querySelector('.tab-content.active').id);
    
  } catch(e) {
    console.error("Test failed:", e);
  }
}, 500);
