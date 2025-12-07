import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, BarChart, Bar, Cell, ResponsiveContainer } from "recharts";
import "./App.css";

// Types des données
type Donnee = { annee: number; valeur: number; date?: string };
type DonneeMensuelle = { date: string; valeur: number };
type ComparaisonData = { date: string; portefeuille: number; indice: number };
type PredictionData = { 
  date: string;
  valeur_predite: number; 
  sigma_plus_1: number; 
  sigma_plus_2: number; 
  sigma_moins_1: number; 
  sigma_moins_2: number; 
};
type RendementAnnuel = {
  annee: number;
  rendement: number;
};
type HistogrammeData = {
  rendements_annuels: RendementAnnuel[];
  meilleures_annees: RendementAnnuel[];
  pires_annees: RendementAnnuel[];
};
type SimulationLumpSum = {
  donnees_mensuelles: DonneeMensuelle[];
  valeur_finale: number;
  cagr: number;
  rendement_total: number;
};
type RatiosFinanciers = {
  rendement_moyen_annuel: number;
  volatilite_annuelle: number;
  sharpe_ratio: number;
  cagr: number;
  rendement_total: number;
};
type Actif = { ticker: string; ponderation: number };
type Parametres = { actifs: Actif[] };

// Type complet du prop data
type SimulationData = {
  simulation?: { donnees_annuelles: Donnee[]; donnees_mensuelles?: DonneeMensuelle[] };
  comparaison_indice?: { 
    donnees_comparaison: ComparaisonData[];
    indice?: { nom: string };
  };
  ratios_financiers: RatiosFinanciers;
  parametres: Parametres;
  predictions_futures?: PredictionData[];
  histogramme_rendements?: HistogrammeData;
  simulation_lump_sum?: SimulationLumpSum;
};

type DashboardProps = { data: SimulationData };

export default function DashboardPortefeuille({ data }: DashboardProps) {
  if (!data) return <div>Simulation non effectuée</div>;

  // Données du portefeuille - utiliser les données mensuelles si disponibles pour plus de détails
  const donneesMensuelles: DonneeMensuelle[] = data.simulation?.donnees_mensuelles || [];
  const donneesPortefeuille: Donnee[] = data.simulation?.donnees_annuelles || [];

  // Ajouter l'année calendaire aux données mensuelles
  const donneesMensuellesAvecAnnee = donneesMensuelles.map((d) => {
    const date = new Date(d.date);
    // Calculer l'année fractionnaire (ex: 2005.5 pour juin 2005)
    const anneeCalendaire = date.getFullYear() + (date.getMonth() / 12);
    return {
      ...d,
      anneeCalendaire: Math.round(anneeCalendaire * 100) / 100 // Précision à 2 décimales
    };
  });

  // Données de comparaison avec l'indice
  const donneesComparaison = data.comparaison_indice?.donnees_comparaison || [];
  const nomIndice = data.comparaison_indice?.indice?.nom || "Indice Mondial";

  // Transformer pour le graphique avec année calendaire
  const donneesGraphiqueComparaison = donneesComparaison.map((d) => {
    const date = new Date(d.date);
    const anneeCalendaire = date.getFullYear() + (date.getMonth() / 12);
    return {
      anneeCalendaire: Math.round(anneeCalendaire * 100) / 100,
      portefeuille: d.portefeuille,
      indice: d.indice
    };
  });
  
  // Données de prédiction futures
  const predictionsFutures = data.predictions_futures || [];

  return (
    <div style={{ marginTop: "20px", fontFamily: "'Inter', 'Segoe UI', sans-serif", backgroundColor: "#0f172a", padding: "20px", minHeight: "100vh", backgroundImage: "radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.05) 0%, transparent 50%)" }}>
      <div style={{ maxWidth: "1400px", margin: "0 auto", width: "100%" }}>
      <h1 style={{ textAlign: "center", color: "#f1f5f9", marginBottom: "48px", fontSize: "36px", fontWeight: "700", letterSpacing: "-1px" }}>Analyse du Portefeuille</h1>

      {/* Composition du portefeuille */}
      <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
        <h2 style={{ color: "#f1f5f9", marginBottom: "24px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #3b82f6", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Composition du Portefeuille</h2>
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "space-between", gap: "16px" }}>
          {data.parametres.actifs.map((actif: any, index: number) => (
            <div 
              key={index} 
              style={{ 
                flex: "1 1 calc(33.333% - 16px)",
                minWidth: "200px",
                padding: "24px 32px", 
                background: "linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)",
                borderRadius: "12px",
                border: "1px solid rgba(59, 130, 246, 0.3)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "8px",
                transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                cursor: "default"
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = "translateY(-4px)";
                e.currentTarget.style.borderColor = "rgba(59, 130, 246, 0.6)";
                e.currentTarget.style.boxShadow = "0 8px 20px rgba(59, 130, 246, 0.3)";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.borderColor = "rgba(59, 130, 246, 0.3)";
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              <span style={{ fontSize: "16px", color: "#60a5fa", fontWeight: "700", letterSpacing: "0.5px" }}>
                {actif.ticker}
              </span>
              <span style={{ fontSize: "24px", color: "#f1f5f9", fontWeight: "700" }}>
                {actif.ponderation}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Ratios financiers */}
      <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
        <h2 style={{ color: "#f1f5f9", marginBottom: "24px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #10b981", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Indicateurs Financiers</h2>
        <div className="grid-container">
          {[
            { label: "Rendement moyen annuel", value: data.ratios_financiers.rendement_moyen_annuel + "%" },
            { label: "Volatilité", value: data.ratios_financiers.volatilite_annuelle + "%" },
            { label: "Sharpe Ratio", value: data.ratios_financiers.sharpe_ratio },
            { label: "CAGR", value: data.ratios_financiers.cagr + "%" },
            { label: "Rendement total", value: data.ratios_financiers.rendement_total + "%" },
          ].map((ratio) => (
            <div key={ratio.label} className="field-card" style={{ borderLeft: "4px solid #3b82f6", background: "linear-gradient(135deg, #334155 0%, #1e293b 100%)" }}>
              <label style={{ color: "#94a3b8", fontSize: "13px", textTransform: "uppercase", letterSpacing: "0.5px" }}>{ratio.label}</label>
              <span style={{ fontSize: "28px", color: "#f1f5f9", fontWeight: "700", display: "block", marginTop: "10px" }}>{ratio.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Graphique du portefeuille */}
      <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
        <h2 style={{ color: "#f1f5f9", marginBottom: "12px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #8b5cf6", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Évolution du Portefeuille</h2>
        <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "24px" }}>
          Axe X : Années calendaires | Axe Y : Valeur du portefeuille (€) | Valeurs journalières affichées
        </p>
        <ResponsiveContainer width="100%" height={400}>
        <LineChart data={donneesMensuellesAvecAnnee.length > 0 ? donneesMensuellesAvecAnnee : donneesPortefeuille}>
          <XAxis 
            dataKey={donneesMensuellesAvecAnnee.length > 0 ? "anneeCalendaire" : "annee"}
            label={{ value: 'Année', position: 'insideBottom', offset: -5 }}
            height={60}
            tickFormatter={(value) => Math.floor(value).toString()}
            domain={['dataMin', 'dataMax']}
            ticks={donneesMensuellesAvecAnnee.length > 0 ? 
              Array.from(new Set(donneesMensuellesAvecAnnee.map(d => Math.floor(d.anneeCalendaire))))
              : undefined}
          />
          <YAxis label={{ value: 'Valeur (€)', angle: -90, position: 'insideLeft' }} />
          <Tooltip 
            labelFormatter={(value) => {
              const annee = Math.floor(value);
              const mois = Math.round((value - annee) * 12);
              const moisNoms = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
              return `${moisNoms[mois]} ${annee}`;
            }}
            formatter={(value: number) => [`${value.toLocaleString('fr-FR')} €`, 'Valeur']}
          />
          <Legend />
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <Line
            type="linear"
            dataKey="valeur"
            name="Mon Portefeuille"
            stroke="#8884d8"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Graphique comparaison portefeuille vs ACWI */}
      {donneesGraphiqueComparaison.length > 0 ? (
      <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
        <h2 style={{ color: "#f1f5f9", marginBottom: "12px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #f59e0b", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Comparaison avec {nomIndice}</h2>
        <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "24px" }}>
          Axe X : Années calendaires | Axe Y : Valeur du portefeuille (€) | Valeurs journalières affichées
        </p>
        <ResponsiveContainer width="100%" height={400}>
        <LineChart data={donneesGraphiqueComparaison}>
          <XAxis 
            dataKey="anneeCalendaire"
            label={{ value: 'Année', position: 'insideBottom', offset: -5 }}
            height={60}
            tickFormatter={(value) => Math.floor(value).toString()}
            domain={['dataMin', 'dataMax']}
            ticks={donneesGraphiqueComparaison.length > 0 ? 
              Array.from(new Set(donneesGraphiqueComparaison.map(d => Math.floor(d.anneeCalendaire))))
              : undefined}
          />
          <YAxis label={{ value: 'Valeur (€)', angle: -90, position: 'insideLeft' }} />
          <Tooltip 
            formatter={(value: number) => `${value.toLocaleString('fr-FR')} €`}
            labelFormatter={(value) => {
              const annee = Math.floor(value);
              const mois = Math.round((value - annee) * 12);
              const moisNoms = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
              return `${moisNoms[mois]} ${annee}`;
            }}
          />
          <Legend />
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <Line
            type="linear"
            dataKey="portefeuille"
            name="Mon Portefeuille"
            stroke="#8884d8"
            dot={false}
            strokeWidth={2}
          />
          <Line
            type="linear"
            dataKey="indice"
            name={nomIndice}
            stroke="#ff7300"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
        </ResponsiveContainer>
      </div>
      ) : (
        <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(251, 191, 36, 0.3)" }}>
          <p style={{ margin: 0, color: "#fbbf24", fontSize: "14px" }}>
            Aucune donnée de comparaison avec l'indice de référence disponible pour cette période.
          </p>
        </div>
      )}

      {/* Graphique de prédiction avec bandes de volatilité */}
      {predictionsFutures.length > 0 && (
        <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
          <h2 style={{ color: "#f1f5f9", marginBottom: "12px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #ec4899", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Prédictions sur 5 ans</h2>
          <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "24px" }}>
            Les bandes représentent les intervalles de confiance : σ±1 (68% de probabilité) et σ±2 (95% de probabilité)
            <br />
            Axe X : Années calendaires futures | Axe Y : Valeur prédite (€) | Données journalières affichées
          </p>
          <ResponsiveContainer width="100%" height={400}>
          <LineChart data={predictionsFutures.map((p) => {
            const date = new Date(p.date);
            const anneeCalendaire = date.getFullYear() + (date.getMonth() / 12);
            return {
              ...p,
              anneeCalendaire: Math.round(anneeCalendaire * 100) / 100
            };
          })}>
            <XAxis 
              dataKey="anneeCalendaire"
              label={{ value: 'Année', position: 'insideBottom', offset: -5 }}
              height={60}
              tickFormatter={(value) => Math.floor(value).toString()}
              domain={['dataMin', 'dataMax']}
              ticks={predictionsFutures.length > 0 ? 
                Array.from(new Set(predictionsFutures.map(p => {
                  const date = new Date(p.date);
                  return date.getFullYear();
                })))
                : undefined}
            />
            <YAxis label={{ value: 'Valeur (€)', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              labelFormatter={(value) => {
                const annee = Math.floor(value);
                const mois = Math.round((value - annee) * 12);
                const moisNoms = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
                return `${moisNoms[mois]} ${annee}`;
              }}
              formatter={(value: number) => `${value.toLocaleString('fr-FR')} €`}
            />
            <Legend />
            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
            
            {/* Bande σ+2 */}
            <Line
              type="linear"
              dataKey="sigma_plus_2"
              name="σ +2 (95%)"
              stroke="#ffcccc"
              strokeDasharray="5 5"
              dot={false}
              strokeWidth={1}
            />
            
            {/* Bande σ+1 */}
            <Line
              type="linear"
              dataKey="sigma_plus_1"
              name="σ +1 (68%)"
              stroke="#ff9999"
              strokeDasharray="3 3"
              dot={false}
              strokeWidth={1.5}
            />
            
            {/* Prédiction centrale */}
            <Line
              type="linear"
              dataKey="valeur_predite"
              name="Prédiction"
              stroke="#8884d8"
              dot={false}
              strokeWidth={2}
            />
            
            {/* Bande σ-1 */}
            <Line
              type="linear"
              dataKey="sigma_moins_1"
              name="σ -1 (68%)"
              stroke="#ff9999"
              strokeDasharray="3 3"
              dot={false}
              strokeWidth={1.5}
            />
            
            {/* Bande σ-2 */}
            <Line
              type="linear"
              dataKey="sigma_moins_2"
              name="σ -2 (95%)"
              stroke="#ffcccc"
              strokeDasharray="5 5"
              dot={false}
              strokeWidth={1}
            />
          </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Histogramme des rendements annuels */}
      {data.histogramme_rendements && data.histogramme_rendements.rendements_annuels && data.histogramme_rendements.rendements_annuels.length > 0 && (
        <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
          <h2 style={{ color: "#f1f5f9", marginBottom: "12px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #06b6d4", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Distribution des Rendements Annuels</h2>
          <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "24px" }}>
            Rendements annuels de votre portefeuille (valeurs positives en haut, négatives en bas)
          </p>
          <ResponsiveContainer width="100%" height={450}>
          <BarChart data={data.histogramme_rendements.rendements_annuels}>
            <XAxis 
              dataKey="annee"
              label={{ value: 'Année', position: 'insideBottom', offset: -5 }}
              height={60}
            />
            <YAxis 
              label={{ value: 'Rendement (%)', angle: -90, position: 'insideLeft' }}
              domain={['auto', 'auto']}
            />
            <Tooltip 
              formatter={(value: number) => `${value.toFixed(2)}%`}
              labelFormatter={(label) => `Année ${label}`}
            />
            <Legend />
            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
            <Bar
              dataKey="rendement"
              name="Rendement annuel"
            >
              {data.histogramme_rendements.rendements_annuels.map((entry: RendementAnnuel, index: number) => (
                <Cell key={`cell-${index}`} fill={entry.rendement >= 0 ? "#4CAF50" : "#f44336"} />
              ))}
            </Bar>
          </BarChart>
          </ResponsiveContainer>
          
          {/* Meilleures et pires années */}
          <div style={{ display: "flex", justifyContent: "space-around", marginTop: "24px", gap: "20px" }}>
            <div style={{ flex: 1, background: "linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%)", padding: "24px", borderRadius: "12px", border: "1px solid rgba(34, 197, 94, 0.3)" }}>
              <h3 style={{ color: "#4ade80", marginBottom: "20px", fontSize: "20px", fontWeight: "700" }}>🏆 Meilleures Années</h3>
              {data.histogramme_rendements.meilleures_annees.map((annee: RendementAnnuel, index: number) => (
                <div key={index} style={{ padding: "14px 0", borderBottom: index < data.histogramme_rendements!.meilleures_annees.length - 1 ? "1px solid rgba(34, 197, 94, 0.2)" : "none", color: "#e4e4e7" }}>
                  <strong>{annee.annee}</strong>: +{annee.rendement.toFixed(2)}%
                </div>
              ))}
            </div>
            <div style={{ flex: 1, background: "linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%)", padding: "24px", borderRadius: "12px", border: "1px solid rgba(239, 68, 68, 0.3)" }}>
              <h3 style={{ color: "#f87171", marginBottom: "20px", fontSize: "20px", fontWeight: "700" }}>📉 Pires Années</h3>
              {data.histogramme_rendements.pires_annees.map((annee: RendementAnnuel, index: number) => (
                <div key={index} style={{ padding: "14px 0", borderBottom: index < data.histogramme_rendements!.pires_annees.length - 1 ? "1px solid rgba(239, 68, 68, 0.2)" : "none", color: "#e4e4e7" }}>
                  <strong>{annee.annee}</strong>: {annee.rendement.toFixed(2)}%
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Comparaison DCA vs Lump Sum */}
      {data.simulation_lump_sum && donneesMensuelles.length > 0 && (
        <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)" }}>
          <h2 style={{ color: "#f1f5f9", marginBottom: "12px", fontSize: "24px", fontWeight: "700", borderBottom: "3px solid #14b8a6", paddingBottom: "12px", letterSpacing: "-0.5px" }}>Comparaison DCA vs Lump Sum</h2>
          <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "24px" }}>
            DCA: {data.simulation?.donnees_mensuelles?.[data.simulation.donnees_mensuelles.length - 1]?.valeur.toLocaleString('fr-FR')} € 
            (CAGR: {data.ratios_financiers.cagr}%)
            <br />
            Lump Sum: {data.simulation_lump_sum.valeur_finale.toLocaleString('fr-FR')} € 
            (CAGR: {data.simulation_lump_sum.cagr}%)
            <br />
            Axe X : Années calendaires | Axe Y : Valeur du portefeuille (€) | Valeurs journalières affichées
          </p>
          <ResponsiveContainer width="100%" height={400}>
          <LineChart 
            data={donneesMensuellesAvecAnnee.map((dca, index) => ({
              anneeCalendaire: dca.anneeCalendaire,
              DCA: dca.valeur,
              LumpSum: data.simulation_lump_sum?.donnees_mensuelles?.[index]?.valeur || 0
            }))}
          >
            <XAxis 
              dataKey="anneeCalendaire"
              label={{ value: 'Année', position: 'insideBottom', offset: -5 }}
              height={60}
              tickFormatter={(value) => Math.floor(value).toString()}
              domain={['dataMin', 'dataMax']}
              ticks={donneesMensuellesAvecAnnee.length > 0 ? 
                Array.from(new Set(donneesMensuellesAvecAnnee.map(d => Math.floor(d.anneeCalendaire))))
                : undefined}
            />
            <YAxis label={{ value: 'Valeur (€)', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              labelFormatter={(value) => {
                const annee = Math.floor(value);
                const mois = Math.round((value - annee) * 12);
                const moisNoms = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
                return `${moisNoms[mois]} ${annee}`;
              }}
              formatter={(value: number) => `${value.toLocaleString('fr-FR')} €`}
            />
            <Legend />
            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
            <Line
              type="linear"
              dataKey="DCA"
              name="DCA (Dollar-Cost Averaging)"
              stroke="#8884d8"
              dot={false}
              strokeWidth={2}
            />
            <Line
              type="linear"
              dataKey="LumpSum"
              name="Lump Sum (Investissement unique)"
              stroke="#82ca9d"
              dot={false}
              strokeWidth={2}
            />
          </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Bouton d'export */}
      <div style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", padding: "32px", borderRadius: "16px", marginBottom: "24px", boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(148, 163, 184, 0.1)", textAlign: "center" }}>
        <button
          onClick={() => window.print()}
          style={{
            padding: "18px 48px",
            fontSize: "17px",
            fontWeight: "700",
            background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
            color: "white",
            border: "none",
            borderRadius: "12px",
            cursor: "pointer",
            boxShadow: "0 8px 20px rgba(59, 130, 246, 0.4)",
            transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            textTransform: "uppercase",
            letterSpacing: "1.2px"
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.background = "linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)";
            e.currentTarget.style.transform = "translateY(-4px)";
            e.currentTarget.style.boxShadow = "0 12px 32px rgba(59, 130, 246, 0.5)";
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.background = "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)";
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "0 8px 20px rgba(59, 130, 246, 0.4)";
          }}
        >
          📄 Exporter en PDF
        </button>
      </div>
      </div>
    </div>
  );
}
