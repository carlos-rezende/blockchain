// src/components/NovaTransacao.js
import axios from "axios";
import React, { useState } from "react";

function NovaTransacao() {
  const [sender, setSender] = useState("");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState(0);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCreateTransaction = async () => {
    // Validações de entrada
    if (!sender || !recipient || amount <= 0) {
      setMessage("Por favor, preencha todos os campos corretamente.");
      return;
    }

    setLoading(true);
    setMessage(""); // Limpa a mensagem anterior

    try {
      await axios.post("http://127.0.0.1:5000/transaction", {
        sender,
        recipient,
        amount: parseFloat(amount), // Converte o valor para float
      });
      setMessage("Transação criada com sucesso!");
      setSender("");
      setRecipient("");
      setAmount(0);
    } catch (error) {
      setMessage("Erro ao criar transação.");
      console.error("Erro:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Criar Nova Transação</h2>
      {message && <p>{message}</p>}
      <input
        type="text"
        placeholder="Remetente"
        value={sender}
        onChange={(e) => setSender(e.target.value)}
      />
      <input
        type="text"
        placeholder="Destinatário"
        value={recipient}
        onChange={(e) => setRecipient(e.target.value)}
      />
      <input
        type="number"
        placeholder="Valor"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        min="0"
        step="0.01"
      />
      <button onClick={handleCreateTransaction} disabled={loading}>
        {loading ? "Processando..." : "Criar Transação"}
      </button>
    </div>
  );
}

export default NovaTransacao;
