import axios from "axios";
import React, { useState } from "react";

function Carteira() {
  const [walletId, setWalletId] = useState(null);
  const [publicKey, setPublicKey] = useState("");

  const createWallet = async () => {
    try {
      // Chama o endpoint correto sem o prefixo '/api'
      const response = await axios.post("http://localhost:5000/wallet/new");
      setWalletId(response.data.wallet_id);
      setPublicKey(response.data.public_key);
      alert("Carteira criada com sucesso!");
    } catch (error) {
      alert("Erro ao criar a carteira.");
      console.error("Erro ao criar a carteira:", error);
    }
  };

  return (
    <div>
      <h2>Criar Carteira</h2>
      <button onClick={createWallet}>Criar Nova Carteira</button>
      {walletId !== null && (
        <div>
          <h2>Detalhes da Carteira</h2>
          <p>
            <strong>Chave Pública:</strong>
          </p>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              backgroundColor: "#f4f4f4",
              padding: "10px",
              borderRadius: "5px",
              overflow: "auto",
            }}
          >
            {publicKey}
          </pre>
        </div>
      )}
    </div>
  );
}

export default Carteira;
