import { useState } from "react";

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

  const [actif, setActif] = useState<Actif>({ type: "ETF", ticker: "SPY", ponderation: 100 });

  // Listes d'actifs
  const ETF_LIST = [
    { ticker: "SPY", nom: "S&P 500 ETF" },
    { ticker: "VTI", nom: "Total Stock Market ETF" },
    { ticker: "AGG", nom: "Bond Aggregate ETF" },
    { ticker: "EFA", nom: "MSCI EAFE ETF" },
  ];

  const ACTIONS_LIST = [
    { ticker: "AAPL", nom: "Apple" },
    { ticker: "MSFT", nom: "Microsoft" },
    { ticker: "GOOGL", nom: "Alphabet" },
  ];

  const OBLIGATIONS_LIST = [
    { ticker: "BND", nom: "Vanguard Total Bond Market" },
    { ticker: "TLT", nom: "iShares 20+ Year Treasury" },
  ];

  const ALL_ASSETS = [
    { type: "ETF", list: ETF_LIST },
    { type: "Action", list: ACTIONS_LIST },
    { type: "Obligation", list: OBLIGATIONS_LIST },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      montant_initial: montantInitial,
      montant_contribution: contribution,
      frequence_contribution: frequence,
      duree_investissement: duree,
      frais_gestion_annuels: frais,
      actifs: [actif], // toujours sous forme de liste
      risques: 0.02,
      periode_historique: "5y",
      strategie: strategie,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="formulaire">
      <div className="form-row">
        <div className="form-group">
          <label>Montant initial (€) :</label>
          <input type="number" value={montantInitial} onChange={(e) => setMontantInitial(+e.target.value)} />
        </div>
        <div className="form-group">
          <label>Contribution (€) :</label>
          <input type="number" value={contribution} onChange={(e) => setContribution(+e.target.value)} />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Fréquence :</label>
          <select value={frequence} onChange={(e) => setFrequence(+e.target.value)}>
            <option value={1}>Mensuel</option>
            <option value={2}>Trimestriel</option>
            <option value={4}>Semestriel</option>
            <option value={12}>Annuel</option>
          </select>
        </div>
        <div className="form-group">
          <label>Durée (années) :</label>
          <input type="number" value={duree} onChange={(e) => setDuree(+e.target.value)} />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Frais annuels (%) :</label>
          <input type="number" step="0.01" value={frais} onChange={(e) => setFrais(+e.target.value)} />
        </div>
        <div className="form-group">
          <label>Stratégie :</label>
          <select value={strategie} onChange={(e) => setStrategie(e.target.value as "DCA" | "LumpSum")}>
            <option value="DCA">DCA</option>
            <option value="LumpSum">Lump Sum</option>
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Type d'actif :</label>
          <select
            value={actif.type}
            onChange={(e) => setActif({ ...actif, type: e.target.value, ticker: "" })}
          >
            <option value="ETF">ETF</option>
            <option value="Action">Action</option>
            <option value="Obligation">Obligation</option>
          </select>
        </div>
        <div className="form-group">
          <label>Actif :</label>
          <select
            value={actif.ticker}
            onChange={(e) => setActif({ ...actif, ticker: e.target.value })}
          >
            <option value="">Sélectionner un actif</option>
            {ALL_ASSETS.find((a) => a.type === actif.type)?.list.map((e) => (
              <option key={e.ticker} value={e.ticker}>{e.nom}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Pondération (%) :</label>
          <input
            type="number"
            value={actif.ponderation}
            onChange={(e) => setActif({ ...actif, ponderation: +e.target.value })}
          />
        </div>
      </div>

      <button type="submit">Simuler</button>
    </form>
  );
}
