import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import "./App.css";

// Types des données
type Donnee = { annee: number; valeur: number };
type AcwiData = { annee: number; indice: number };
type RatiosFinanciers = {
  rendement_moyen_annuel: number;
  volatilite_annuelle: number;
  sharpe_ratio: number;
  cagr: number;
  rendement_total: number;
};
type Actif = { nom: string };
type Parametres = { actifs: Actif[] };

// Type complet du prop data
type SimulationData = {
  simulation?: { donnees_annuelles: Donnee[] };
  comparaison_indice?: { donnees_comparaison: AcwiData[] };
  ratios_financiers: RatiosFinanciers;
  parametres: Parametres;
};

type DashboardProps = { data: SimulationData };

export default function DashboardPortefeuille({ data }: DashboardProps) {
  if (!data) return <div>Simulation non effectuée</div>;

  // Données du portefeuille
  const donneesPortefeuille: Donnee[] = data.simulation?.donnees_annuelles || [];

  // Données ACWI
  const acwi: AcwiData[] = data.comparaison_indice?.donnees_comparaison || [];
  console.log("Données ACWI reçues :", acwi);

  // Fusionner portefeuille et ACWI par année
  const donneesComparaison = donneesPortefeuille.map((d) => ({
    annee: d.annee,
    portefeuille: d.valeur,
    acwi: acwi.find(a => a.annee === d.annee)?.indice ?? 0
  }));

  return (
    <div style={{ marginTop: "40px", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2 style={{ textAlign: "center" }}>Résultats du portefeuille</h2>

      {/* Ratios financiers */}
      <div style={{ marginBottom: "20px" }}>
        <h3>Ratios financiers</h3>
        <div className="grid-container">
          {[
            { label: "Rendement moyen annuel", value: data.ratios_financiers.rendement_moyen_annuel + "%" },
            { label: "Volatilité", value: data.ratios_financiers.volatilite_annuelle + "%" },
            { label: "Sharpe Ratio", value: data.ratios_financiers.sharpe_ratio },
            { label: "CAGR", value: data.ratios_financiers.cagr + "%" },
            { label: "Rendement total", value: data.ratios_financiers.rendement_total + "%" },
          ].map((ratio) => (
            <div key={ratio.label} className="field-card">
              <label>{ratio.label}</label>
              <span style={{ fontSize: "18px", color: "#222" }}>{ratio.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Graphique du portefeuille */}
      <div style={{ overflowX: "auto", marginBottom: "40px" }}>
        <h3>Évolution du portefeuille</h3>
        <LineChart width={700} height={300} data={donneesPortefeuille}>
          <XAxis dataKey="annee" />
          <YAxis />
          <Tooltip />
          <Legend />
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <Line
            type="monotone"
            dataKey="valeur"
            name={data.parametres.actifs[0].nom} 
            stroke="#8884d8"
          />
        </LineChart>
      </div>

      {/* Graphique comparaison portefeuille vs ACWI */}
      <div style={{ overflowX: "auto" }}>
        <h3>Comparaison avec l'indice ACWI IMI</h3>
        <LineChart width={700} height={300} data={donneesComparaison}>
          <XAxis dataKey="annee" />
          <YAxis />
          <Tooltip />
          <Legend />
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <Line
            type="monotone"
            dataKey="portefeuille"
            name={data.parametres.actifs[0].nom} 
            stroke="#8884d8"
          />
          <Line
            type="monotone"
            dataKey="acwi"
            name="ACWI IMI"
            stroke="#ff7300"
          />
        </LineChart>
      </div>
    </div>
  );
}
