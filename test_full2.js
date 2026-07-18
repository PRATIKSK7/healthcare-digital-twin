const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('frontend/index.html', 'utf8');

let cleanedHtml = html.replace(/new Chart\(/g, '// new Chart(');
const dom = new JSDOM(cleanedHtml, { runScripts: "dangerously" });
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
    // Call Predict manually as if form was filled
    win.selSyms = ["anxiety", "joint pain"];
    win.document.getElementById('pName').value = "Pratik";
    await win.predict();
    
    // Check if add to queue throws any error
    win.addPatientFromPredictor();
    console.log("Success! Queue length:", win.patientQueue.length);
  } catch(e) {
    console.error("Test failed:", e);
  }
}, 500);
