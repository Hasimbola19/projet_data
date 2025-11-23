import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";

type Donnee = { annee: number; valeur: number };
type DashboardProps = { data: any };

export default function DashboardPortefeuille({ data }: DashboardProps) {
  if (!data) return <div>Simulation non effectuée</div>;

  const donneesPortefeuille: Donnee[] = data.simulation?.donnees_annuelles || [];
  const acwi: Donnee[] = data.acwi || [];

  // Fusionner les données pour le graphique de comparaison
  // On aligne les années pour que les deux lignes correspondent
  const annees = Array.from(new Set([
    ...donneesPortefeuille.map(d => d.annee),
    ...acwi.map(d => d.annee)
  ])).sort((a, b) => a - b);

  const donneesComparaison = annees.map(annee => {
    const port = donneesPortefeuille.find(d => d.annee === annee)?.valeur || null;
    const acwiVal = acwi.find(d => d.annee === annee)?.valeur || null;
    return { annee, portefeuille: port, acwi: acwiVal };
  });

  return (
    <div style={{ marginTop: "40px", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2 style={{ textAlign: "center" }}>Résultats du portefeuille</h2>

      <div style={{ marginBottom: "20px" }}>
        <h3>Ratios financiers</h3>
        <ul>
          <li>Rendement moyen annuel : {data.ratios_financiers.rendement_moyen_annuel}%</li>
          <li>Volatilité : {data.ratios_financiers.volatilite_annuelle}%</li>
          <li>Sharpe Ratio : {data.ratios_financiers.sharpe_ratio}</li>
          <li>CAGR : {data.ratios_financiers.cagr}%</li>
          <li>Rendement total : {data.ratios_financiers.rendement_total}%</li>
        </ul>
      </div>

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
            name={data.parametres.actifs[0].nom} // ETF choisi
            stroke="#8884d8"
          />
        </LineChart>
      </div>

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
            name={data.parametres.actifs[0].nom} // ETF choisi
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
