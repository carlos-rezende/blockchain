"use client";
import Header from "@/components/header"; // Importando o Header
import axios from "axios";
import React, { useState } from "react";

const TransactionsPage: React.FC = () => {
  const [sender, setSender] = useState<string>("");
  const [recipient, setRecipient] = useState<string>("");
  const [amount, setAmount] = useState<number>(0);
  const [signature, setSignature] = useState<string>("");
  const [senderPublicKey, setSenderPublicKey] = useState<string>("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [verificationMessage, setVerificationMessage] = useState<string | null>(
    null
  );

  // Função para criar uma nova transação
  const handleCreateTransaction = async () => {
    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post(
        "http://localhost:5000/transactions/new",
        {
          sender,
          recipient,
          amount,
          signature,
          sender_public_key: senderPublicKey,
        }
      );
      setMessage(response.data.message);
    } catch {
      setMessage("Erro ao criar transação.");
    } finally {
      setLoading(false);
    }
  };

  // Função para verificar uma transação
  const handleVerifyTransaction = async () => {
    setLoading(true);
    setVerificationMessage(null);

    try {
      const response = await axios.post(
        "http://localhost:5000/transactions/verify",
        {
          sender,
          recipient,
          amount,
          signature,
          sender_public_key: senderPublicKey,
        }
      );
      setVerificationMessage(response.data.message);
    } catch {
      setVerificationMessage("Erro ao verificar transação.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-gray-200">
      {/* Adicionando o Header */}
      <Header
        onLogout={() => {
          localStorage.removeItem("token");
          window.location.href = "/login";
        }}
      />

      <div className="container mx-auto py-44 px-4">
        <h1 className="text-4xl font-extrabold text-teal-400 mb-8 text-center">
          Gerenciar Transações Blockchain
        </h1>

        {/* Formulário para criar e verificar transações */}
        <div className="bg-gray-800 bg-opacity-50 p-8 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg w-full max-w-md mx-auto">
          <h2 className="text-xl font-semibold text-teal-300 mb-4">
            Nova Transação
          </h2>

          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Remetente (Sender)
            </label>
            <input
              type="text"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={sender}
              onChange={(e) => setSender(e.target.value)}
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Destinatário (Recipient)
            </label>
            <input
              type="text"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Quantia (Amount)
            </label>
            <input
              type="number"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Assinatura (Signature)
            </label>
            <input
              type="text"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={signature}
              onChange={(e) => setSignature(e.target.value)}
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Chave Pública do Remetente (Sender Public Key)
            </label>
            <input
              type="text"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={senderPublicKey}
              onChange={(e) => setSenderPublicKey(e.target.value)}
            />
          </div>

          <button
            onClick={handleCreateTransaction}
            className={`w-full p-2 bg-teal-500 text-white font-bold rounded-lg hover:bg-teal-400 transition duration-300 ${
              loading ? "cursor-not-allowed opacity-50" : ""
            }`}
            disabled={loading}
          >
            {loading ? "Carregando..." : "Criar Transação"}
          </button>

          {message && <p className="mt-4 text-teal-300">{message}</p>}

          <hr className="my-6 border-gray-700" />

          <h2 className="text-xl font-semibold text-teal-300 mb-4">
            Verificar Transação
          </h2>
          <button
            onClick={handleVerifyTransaction}
            className={`w-full p-2 bg-teal-500 text-white font-bold rounded-lg hover:bg-teal-400 transition duration-300 ${
              loading ? "cursor-not-allowed opacity-50" : ""
            }`}
            disabled={loading}
          >
            {loading ? "Carregando..." : "Verificar Transação"}
          </button>

          {verificationMessage && (
            <p className="mt-4 text-teal-300">{verificationMessage}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TransactionsPage;
