export default function Hero() {
  return (
    <section style={{
      background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
      padding: "60px 0",
      borderBottom: "1px solid rgba(148, 163, 184, 0.1)",
      textAlign: "center"
    }}>
        <h2 style={{
          fontSize: "42px",
          fontWeight: "700",
          color: "#f1f5f9",
          marginBottom: "20px",
          letterSpacing: "-1px",
          background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text"
        }}>
          Simulez un Investissement Passif
        </h2>
        <p style={{
          fontSize: "18px",
          color: "#94a3b8",
          lineHeight: "1.8",
          margin: "0 auto",
          marginBottom: "16px",
          padding: "0 2%"
        }}>
          <strong style={{ color: "#cbd5e1" }}>PorteSim</strong> est un outil d'analyse financière qui vous permet de simuler 
          et d'optimiser vos investissements en portefeuille passif. Comparez les stratégies DCA (Dollar-Cost Averaging) 
          et Lump Sum, visualisez l'évolution de vos actifs avec des données historiques réelles, 
          et obtenez des prédictions basées sur la volatilité du marché.
        </p>
        <div style={{
          display: "flex",
          gap: "32px",
          justifyContent: "center",
          marginTop: "32px",
          flexWrap: "wrap"
        }}>
          <div style={{
            background: "rgba(59, 130, 246, 0.1)",
            padding: "16px 24px",
            borderRadius: "12px",
            border: "1px solid rgba(59, 130, 246, 0.2)"
          }}>
            <div style={{ fontSize: "28px", marginBottom: "8px" }}></div>
            <div style={{ color: "#cbd5e1", fontSize: "14px", fontWeight: "600" }}>Données Historiques</div>
          </div>
          <div style={{
            background: "rgba(139, 92, 246, 0.1)",
            padding: "16px 24px",
            borderRadius: "12px",
            border: "1px solid rgba(139, 92, 246, 0.2)"
          }}>
            <div style={{ fontSize: "28px", marginBottom: "8px" }}></div>
            <div style={{ color: "#cbd5e1", fontSize: "14px", fontWeight: "600" }}>Prédictions 5 ans</div>
          </div>
          <div style={{
            background: "rgba(16, 185, 129, 0.1)",
            padding: "16px 24px",
            borderRadius: "12px",
            border: "1px solid rgba(16, 185, 129, 0.2)"
          }}>
            <div style={{ fontSize: "28px", marginBottom: "8px" }}></div>
            <div style={{ color: "#cbd5e1", fontSize: "14px", fontWeight: "600" }}>Multi-Actifs</div>
          </div>
          <div style={{
            background: "rgba(245, 158, 11, 0.1)",
            padding: "16px 24px",
            borderRadius: "12px",
            border: "1px solid rgba(245, 158, 11, 0.2)"
          }}>
            <div style={{ fontSize: "28px", marginBottom: "8px" }}></div>
            <div style={{ color: "#cbd5e1", fontSize: "14px", fontWeight: "600" }}>Analyse Complète</div>
          </div>
        </div>
    </section>
  );
}
