import { useState } from "react";
import "./App.css";

type Actif = { type: string; ticker: string; ponderation: number };

type FormulaireProps = {
  onSubmit: (params: any) => void;
};

export default function FormulairePortefeuille({ onSubmit }: FormulaireProps) {
  const [montantInitial, setMontantInitial] = useState<number>(10000);
  const [contribution, setContribution] = useState<number>(500);
  const [frequence, setFrequence] = useState<number>(1);
  const [duree, setDuree] = useState<number>(10);
  const [frais, setFrais] = useState<number>(0.2);
  const [strategie, setStrategie] = useState<"DCA" | "LumpSum">("DCA");
  const [dateDebut, setDateDebut] = useState<string>("");
  const [dateFin, setDateFin] = useState<string>("");

  // Gestion du portefeuille multi-actifs
  const [portefeuille, setPortefeuille] = useState<Actif[]>([]);
  const [actifEnCours, setActifEnCours] = useState<Actif>({ type: "ETF", ticker: "", ponderation: 0 });

  const ETF_LIST = [
    { ticker: "SPY", nom: "S&P 500 ETF" },
    { ticker: "VTI", nom: "Total Stock Market ETF" },
    { ticker: "AGG", nom: "Bond Aggregate ETF" },
    { ticker: "EFA", nom: "MSCI EAFE ETF" },
    { ticker: "VT", nom: "Vanguard Total World Stock" },
    { ticker: "QQQ", nom: "Nasdaq-100 ETF" },
  ];

  const ACTIONS_LIST = [
    { ticker: "AAPL", nom: "Apple" },
    { ticker: "MSFT", nom: "Microsoft" },
    { ticker: "GOOGL", nom: "Alphabet" },
    { ticker: "AMZN", nom: "Amazon" },
    { ticker: "NVDA", nom: "NVIDIA" },
    { ticker: "TSLA", nom: "Tesla" },
  ];

  const OBLIGATIONS_LIST = [
    { ticker: "BND", nom: "Vanguard Total Bond Market" },
    { ticker: "TLT", nom: "iShares 20+ Year Treasury" },
    { ticker: "AGG", nom: "iShares Core U.S. Aggregate Bond" },
    { ticker: "LQD", nom: "iShares Investment Grade Corporate" },
  ];

  const ALL_ASSETS = [
    { type: "ETF", list: ETF_LIST },
    { type: "Action", list: ACTIONS_LIST },
    { type: "Obligation", list: OBLIGATIONS_LIST },
  ];

  // Calculer la pondération totale du portefeuille
  const ponderationTotale = portefeuille.reduce((sum, a) => sum + a.ponderation, 0);
  const ponderationRestante = 100 - ponderationTotale;

  // Ajouter un actif au portefeuille
  const ajouterActif = () => {
    if (!actifEnCours.ticker) {
      alert("Veuillez sélectionner un actif");
      return;
    }
    if (actifEnCours.ponderation <= 0) {
      alert("La pondération doit être supérieure à 0");
      return;
    }
    if (ponderationTotale + actifEnCours.ponderation > 100) {
      alert(`La pondération totale ne peut pas dépasser 100% (restant: ${ponderationRestante}%)`);
      return;
    }
    
    setPortefeuille([...portefeuille, { ...actifEnCours }]);
    setActifEnCours({ type: "ETF", ticker: "", ponderation: 0 });
  };

  // Retirer un actif du portefeuille
  const retirerActif = (index: number) => {
    setPortefeuille(portefeuille.filter((_, i) => i !== index));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (portefeuille.length === 0) {
      alert("Veuillez ajouter au moins un actif au portefeuille");
      return;
    }
    
    const ponderationTotale = portefeuille.reduce((sum, a) => sum + a.ponderation, 0);
    if (Math.abs(ponderationTotale - 100) > 0.01) {
      alert(`La pondération totale doit être égale à 100% (actuellement: ${ponderationTotale}%)`);
      return;
    }
    
    const params: any = {
      montant_initial: montantInitial,
      montant_contribution: contribution,
      frequence_contribution: frequence,
      duree_investissement: duree,
      frais_gestion_annuels: frais,
      actifs: portefeuille, 
      risques: 0.02,
      periode_historique: "5y",
      strategie: strategie,
    };
    
    // Ajouter les dates si elles sont définies
    if (dateDebut) params.date_debut = dateDebut;
    if (dateFin) params.date_fin = dateFin;
    
    onSubmit(params);
  };

  return (
    <form onSubmit={handleSubmit} className="modern-grid">
      <div className="grid-container">
        <div className="field-card">
          <label>Montant initial (€)</label>
          <input type="number" value={montantInitial} onChange={(e) => setMontantInitial(+e.target.value)} />
        </div>

        <div className="field-card">
          <label>Contribution (€)</label>
          <input type="number" value={contribution} onChange={(e) => setContribution(+e.target.value)} />
        </div>

        <div className="field-card">
          <label>Fréquence</label>
          <select value={frequence} onChange={(e) => setFrequence(+e.target.value)}>
            <option value={1}>Mensuel</option>
            <option value={2}>Trimestriel</option>
            <option value={4}>Semestriel</option>
            <option value={12}>Annuel</option>
          </select>
        </div>

        <div className="field-card">
          <label>Durée (années)</label>
          <input type="number" value={duree} onChange={(e) => setDuree(+e.target.value)} />
        </div>

        <div className="field-card">
          <label>Frais annuels (%)</label>
          <input type="number" step="0.01" value={frais} onChange={(e) => setFrais(+e.target.value)} />
        </div>

        <div className="field-card">
          <label>Stratégie</label>
          <select value={strategie} onChange={(e) => setStrategie(e.target.value as "DCA" | "LumpSum")}>
            <option value="DCA">DCA</option>
            <option value="LumpSum">Lump Sum</option>
          </select>
        </div>

        <div className="field-card">
          <label>Date de début (optionnel)</label>
          <input 
            type="date" 
            value={dateDebut} 
            onChange={(e) => setDateDebut(e.target.value)}
            placeholder="YYYY-MM-DD" 
          />
        </div>

        <div className="field-card">
          <label>Date de fin (optionnel)</label>
          <input 
            type="date" 
            value={dateFin} 
            onChange={(e) => setDateFin(e.target.value)}
            placeholder="YYYY-MM-DD" 
          />
        </div>

      </div>

      {/* Section Composition du Portefeuille */}
      <div style={{ marginTop: "30px", marginBottom: "20px", padding: "24px", background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", borderRadius: "16px", border: "1px solid rgba(148, 163, 184, 0.15)" }}>
        <h3 style={{ marginBottom: "20px", color: "#f1f5f9", fontSize: "22px", fontWeight: "700", borderBottom: "3px solid #3b82f6", paddingBottom: "12px" }}>Composition du Portefeuille</h3>
        
        {/* Affichage du portefeuille actuel */}
        {portefeuille.length > 0 && (
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "16px", padding: "12px", background: "rgba(59, 130, 246, 0.1)", borderRadius: "8px", border: "1px solid rgba(59, 130, 246, 0.2)" }}>
              <strong style={{ color: "#cbd5e1" }}>Portefeuille actuel:</strong>
              <strong style={{ color: ponderationTotale === 100 ? "#4ade80" : "#fb923c", fontSize: "18px" }}>
                Total: {ponderationTotale.toFixed(1)}%
              </strong>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {portefeuille.map((actif, index) => (
                <div key={index} style={{ 
                  display: "flex", 
                  justifyContent: "space-between", 
                  alignItems: "center",
                  padding: "14px 18px",
                  background: "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
                  borderRadius: "10px",
                  border: "1px solid rgba(148, 163, 184, 0.2)",
                  transition: "all 0.2s"
                }}>
                  <span style={{ color: "#e4e4e7", fontSize: "15px" }}>
                    <strong style={{ color: "#60a5fa" }}>{actif.type}</strong>: <strong style={{ color: "#f1f5f9" }}>{actif.ticker}</strong> <span style={{ color: "#94a3b8" }}>({actif.ponderation}%)</span>
                  </span>
                  <button 
                    type="button"
                    onClick={() => retirerActif(index)}
                    style={{
                      padding: "8px 16px",
                      background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                      color: "white",
                      border: "none",
                      borderRadius: "8px",
                      cursor: "pointer",
                      fontWeight: "600",
                      fontSize: "13px",
                      transition: "all 0.2s",
                      boxShadow: "0 2px 8px rgba(239, 68, 68, 0.3)"
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.transform = "translateY(-2px)";
                      e.currentTarget.style.boxShadow = "0 4px 12px rgba(239, 68, 68, 0.4)";
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.transform = "translateY(0)";
                      e.currentTarget.style.boxShadow = "0 2px 8px rgba(239, 68, 68, 0.3)";
                    }}
                  >
                    Retirer
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Formulaire d'ajout d'actif */}
        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(3, 1fr)", 
          gap: "16px",
          padding: "24px",
          background: "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
          borderRadius: "12px",
          marginBottom: "15px",
          border: "1px solid rgba(148, 163, 184, 0.2)"
        }}>
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "600", color: "#cbd5e1", fontSize: "13px", textTransform: "uppercase", letterSpacing: "0.5px" }}>ETF</label>
            <select 
              value={actifEnCours.type === "ETF" ? actifEnCours.ticker : ""}
              onChange={(e) => setActifEnCours({ type: "ETF", ticker: e.target.value, ponderation: actifEnCours.ponderation })}
              style={{ width: "100%", padding: "10px 12px", borderRadius: "8px", border: "2px solid rgba(148, 163, 184, 0.2)", backgroundColor: "#0f172a", color: "#e4e4e7", fontSize: "14px" }}
            >
              <option value="">Sélectionner un ETF</option>
              {ETF_LIST.map((etf) => (
                <option key={etf.ticker} value={etf.ticker}>{etf.nom}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "600", color: "#cbd5e1", fontSize: "13px", textTransform: "uppercase", letterSpacing: "0.5px" }}>Actions</label>
            <select 
              value={actifEnCours.type === "Action" ? actifEnCours.ticker : ""}
              onChange={(e) => setActifEnCours({ type: "Action", ticker: e.target.value, ponderation: actifEnCours.ponderation })}
              style={{ width: "100%", padding: "10px 12px", borderRadius: "8px", border: "2px solid rgba(148, 163, 184, 0.2)", backgroundColor: "#0f172a", color: "#e4e4e7", fontSize: "14px" }}
            >
              <option value="">Sélectionner une action</option>
              {ACTIONS_LIST.map((action) => (
                <option key={action.ticker} value={action.ticker}>{action.nom}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "600", color: "#cbd5e1", fontSize: "13px", textTransform: "uppercase", letterSpacing: "0.5px" }}>Obligations</label>
            <select 
              value={actifEnCours.type === "Obligation" ? actifEnCours.ticker : ""}
              onChange={(e) => setActifEnCours({ type: "Obligation", ticker: e.target.value, ponderation: actifEnCours.ponderation })}
              style={{ width: "100%", padding: "10px 12px", borderRadius: "8px", border: "2px solid rgba(148, 163, 184, 0.2)", backgroundColor: "#0f172a", color: "#e4e4e7", fontSize: "14px" }}
            >
              <option value="">Sélectionner une obligation</option>
              {OBLIGATIONS_LIST.map((obligation) => (
                <option key={obligation.ticker} value={obligation.ticker}>{obligation.nom}</option>
              ))}
            </select>
          </div>

          <div style={{ gridColumn: "span 3" }}>
            <label style={{ display: "block", marginBottom: "10px", fontWeight: "600", color: "#cbd5e1", fontSize: "13px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
              Pondération (%) - <span style={{ color: ponderationRestante > 0 ? "#4ade80" : "#ef4444" }}>Restant: {ponderationRestante}%</span>
            </label>
            <div style={{ display: "flex", gap: "12px" }}>
              <input 
                type="number" 
                min="0"
                max={ponderationRestante}
                step="0.1"
                value={actifEnCours.ponderation || ""}
                onChange={(e) => setActifEnCours({ ...actifEnCours, ponderation: +e.target.value })}
                style={{ flex: 1, padding: "12px 16px", borderRadius: "8px", border: "2px solid rgba(148, 163, 184, 0.2)", backgroundColor: "#0f172a", color: "#e4e4e7", fontSize: "15px", fontWeight: "600" }}
                placeholder="Ex: 30"
              />
              <button 
                type="button"
                onClick={ajouterActif}
                style={{
                  padding: "12px 28px",
                  background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
                  color: "white",
                  border: "none",
                  borderRadius: "10px",
                  cursor: "pointer",
                  fontWeight: "700",
                  fontSize: "14px",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  boxShadow: "0 4px 12px rgba(59, 130, 246, 0.3)",
                  transition: "all 0.2s"
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.background = "linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)";
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 6px 20px rgba(59, 130, 246, 0.4)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.background = "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)";
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(59, 130, 246, 0.3)";
                }}
              >
                + Ajouter au portefeuille
              </button>
            </div>
          </div>
        </div>
      </div>

      <button type="submit" className="submit-btn">Simuler</button>
    </form>
  );
}
