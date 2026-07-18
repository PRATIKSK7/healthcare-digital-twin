const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('frontend/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });

// Override fetch
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
    win.toggleSym("anxiety");
    win.toggleSym("joint pain");
    win.toggleSym("muscle pain");
    
    await win.predict();
    console.log("Prediction complete. currentPatient:", win.currentPatient);
    
    win.addPatientFromPredictor();
    console.log("Added to queue. Queue length:", win.patientQueue.length);
  } catch(e) {
    console.error("Test failed", e);
  }
}, 500);
