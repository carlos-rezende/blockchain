import axios from "axios";
import React, { useState } from "react";

function MinerarBloco() {
  const [minerAddress, setMinerAddress] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const minerarBloco = async () => {
    if (!minerAddress) {
      setStatus("Por favor, insira o endereço do minerador.");
      return;
    }

    try {
      setStatus("Iniciando mineração...");
      setLoading(true);

      // Chama a API do backend para minerar um novo bloco
      const response = await axios.post("http://127.0.0.1:5000/mine", {
        miner_address: minerAddress,
      });

      if (response.data && response.data.message) {
        setStatus(response.data.message);
      } else {
        setStatus("Erro desconhecido durante a mineração.");
      }
    } catch (error) {
      setStatus("Erro ao minerar bloco.");
      console.error("Erro ao minerar bloco:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Minerar Novo Bloco</h2>
      <input
        type="text"
        placeholder="Endereço do Minerador"
        value={minerAddress}
        onChange={(e) => setMinerAddress(e.target.value)}
      />
      <button onClick={minerarBloco} disabled={loading}>
        {loading ? "Minerando..." : "Minerar Bloco"}
      </button>
      <p>Status: {status}</p>
    </div>
  );
}

export default MinerarBloco;
