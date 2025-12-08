export default function Navbar() {
  return (
    <nav style={{
      background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
      padding: "20px 40px",
      boxShadow: "0 4px 20px rgba(0, 0, 0, 0.5)",
      borderBottom: "1px solid rgba(148, 163, 184, 0.2)",
      position: "sticky",
      top: 0,
      zIndex: 1000,
      backdropFilter: "blur(10px)"
    }}>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
      }}>
        {/* Logo et titre */}
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{
            width: "48px",
            height: "48px",
            background: "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
            borderRadius: "12px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "24px",
            fontWeight: "700",
            color: "white",
            boxShadow: "0 4px 12px rgba(59, 130, 246, 0.4)"
          }}>
            PS
          </div>
          <div>
            <h1 style={{
              margin: 0,
              fontSize: "24px",
              fontWeight: "700",
              color: "#f1f5f9",
              letterSpacing: "-0.5px"
            }}>
              PorteSim
            </h1>
            <p style={{
              margin: 0,
              fontSize: "13px",
              color: "#94a3b8",
              fontWeight: "500"
            }}>
              Simulateur d'Investissement Passif
            </p>
          </div>
        </div>

        {/* Menu de navigation */}
        <div style={{ display: "flex", gap: "24px", alignItems: "center" }}>
          <a
            href="#simulation"
            style={{
              color: "#cbd5e1",
              textDecoration: "none",
              fontSize: "15px",
              fontWeight: "600",
              transition: "color 0.2s",
              cursor: "pointer"
            }}
            onMouseOver={(e) => e.currentTarget.style.color = "#3b82f6"}
            onMouseOut={(e) => e.currentTarget.style.color = "#cbd5e1"}
          >
            Simulation
          </a>
          <a
            href="#resultats"
            style={{
              color: "#cbd5e1",
              textDecoration: "none",
              fontSize: "15px",
              fontWeight: "600",
              transition: "color 0.2s",
              cursor: "pointer"
            }}
            onMouseOver={(e) => e.currentTarget.style.color = "#3b82f6"}
            onMouseOut={(e) => e.currentTarget.style.color = "#cbd5e1"}
          >
            Résultats
          </a>
        </div>
      </div>
    </nav>
  );
}
