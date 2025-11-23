import { useState } from "react";
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

    console.log("Réponse API :", data); // <--- vérifie que les données arrivent
 

    // Ici, on peut aussi récupérer un indice ACWI IMI simulé ou depuis Yahoo Finance
    // Exemple : l'API Django renvoie un tableau "acwi" déjà présent dans la réponse
    setResultat(data);
  } catch (err) {
    console.error("Erreur lors de la simulation :", err);
  }
};


  return (
    <div>
      <h1>Simulation Portefeuille Passif</h1>
      <FormulairePortefeuille onSubmit={handleSimuler} />
      <DashboardPortefeuille data={resultat} />
    </div>
  );
}

export default App;
