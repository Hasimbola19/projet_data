import { useState } from "react";
import Navbar from "./Navbar";
import Hero from "./Hero";
import FormulairePortefeuille from "./FormulairePortefeuille";
import DashboardPortefeuille from "./DashboardPortefeuille";

function App() {
  const [resultat, setResultat] = useState<any>(null);

  const handleSimuler = async (params: any) => {
  try {
    const response = await fetch("http://localhost:8000/api/simuler/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    const data = await response.json();

    console.log("Réponse API :", data); 
 

    setResultat(data);
  } catch (err) {
    console.error("Erreur lors de la simulation :", err);
  }
};


  return (
    <div style={{ backgroundColor: "#0f172a", minHeight: "100vh" }}>
      <Navbar />
      <Hero />
      <div id="simulation">
        <FormulairePortefeuille onSubmit={handleSimuler} />
      </div>
      <div id="resultats">
        <DashboardPortefeuille data={resultat} />
      </div>
    </div>
  );
}

export default App;
