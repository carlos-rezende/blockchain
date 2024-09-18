import axios from "axios";
import React, { useState } from "react";

function VerificarTransacao() {
  const [transactionId, setTransactionId] = useState("");
  const [transactionDetails, setTransactionDetails] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const verificarTransacao = async () => {
    if (!transactionId) {
      setStatus("Por favor, insira um ID de transação.");
      return;
    }

    try {
      setStatus("Verificando transação...");
      setLoading(true);

      // Chama a API do backend para obter os detalhes da transação
      const response = await axios.get(
        `http://127.0.0.1:5000/transaction/${transactionId}`
      );

      if (response.data && response.data.transaction) {
        setTransactionDetails(response.data.transaction);
        setStatus("Transação encontrada.");
      } else {
        setStatus("Transação não encontrada.");
        setTransactionDetails(null);
      }
    } catch (error) {
      setStatus("Erro ao verificar transação.");
      console.error("Erro ao verificar transação:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Verificar Transação</h2>
      <input
        type="text"
        placeholder="ID da Transação"
        value={transactionId}
        onChange={(e) => setTransactionId(e.target.value)}
      />
      <button onClick={verificarTransacao} disabled={loading}>
        {loading ? "Verificando..." : "Verificar"}
      </button>
      <p>Status: {status}</p>
      {transactionDetails && (
        <div>
          <h3>Detalhes da Transação:</h3>
          <p>Remetente: {transactionDetails.sender}</p>
          <p>Destinatário: {transactionDetails.recipient}</p>
          <p>Quantidade: {transactionDetails.amount}</p>
          <p>Assinatura: {transactionDetails.signature}</p>
        </div>
      )}
    </div>
  );
}

export default VerificarTransacao;
