// src/components/Sincronizacao.js
import axios from "axios";
import React, { useState } from "react";

function Sincronizacao() {
  const [nodeAddress, setNodeAddress] = useState("");
  const [syncStatus, setSyncStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const sincronizarBlockchain = async () => {
    // Validação simples para o endereço do nó
    if (!nodeAddress || !nodeAddress.startsWith("http")) {
      setSyncStatus("Por favor, insira um endereço de nó válido.");
      return;
    }

    setLoading(true);
    setSyncStatus("Sincronizando...");

    try {
      // Chama a API do backend para sincronizar com outro nó
      const response = await axios.post("http://127.0.0.1:5000/sync", {
        nodeAddress,
      });

      // Verifica se a resposta contém a chave 'success'
      if (response.data && response.data.success) {
        setSyncStatus("Sincronização bem-sucedida!");
      } else {
        setSyncStatus("Falha na sincronização. Tente novamente.");
      }
    } catch (error) {
      setSyncStatus("Erro ao sincronizar com o nó.");
      console.error("Erro ao sincronizar blockchain:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Sincronizar Blockchain com Outro Nó</h2>
      <input
        type="text"
        placeholder="Endereço do nó (e.g., http://127.0.0.1:5000/)"
        value={nodeAddress}
        onChange={(e) => setNodeAddress(e.target.value)}
      />
      <button onClick={sincronizarBlockchain} disabled={loading}>
        {loading ? "Sincronizando..." : "Sincronizar"}
      </button>
      <p>Status: {syncStatus}</p>
    </div>
  );
}

export default Sincronizacao;
