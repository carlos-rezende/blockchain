"use client";
import Header from "@/components/header";
import { useState } from "react";

export default function WalletPage() {
  const [walletId, setWalletId] = useState<number | null>(null);
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [transactionData, setTransactionData] = useState({
    sender: "",
    recipient: "",
    amount: "",
  });
  const [signature, setSignature] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Função para criar uma nova carteira
  const createWallet = async () => {
    try {
      const response = await fetch("http://localhost:5000/wallet/new", {
        method: "POST",
      });
      const data = await response.json();
      setWalletId(data.wallet_id);
      setPublicKey(data.public_key);
      setSuccessMessage("Carteira criada com sucesso!");
      setError(null); // Limpa mensagens de erro
    } catch (err) {
      if (err instanceof Error) {
        setError("Erro ao criar carteira: " + err.message);
      } else {
        setError("Erro desconhecido ao criar carteira");
      }
    }
  };

  // Função para assinar uma transação
  const signTransaction = async () => {
    if (walletId === null) {
      setError("Carteira não encontrada. Crie uma carteira primeiro.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000/wallet/${walletId}/sign`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(transactionData),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao assinar a transação");
      }

      const data = await response.json();
      setSignature(data.signature);
      setSuccessMessage("Transação assinada com sucesso!");
      setError(null);
    } catch (err) {
      if (err instanceof Error) {
        setError("Erro ao assinar a transação: " + err.message);
      } else {
        setError("Erro desconhecido ao assinar a transação");
      }
    }
  };

  // Função para lidar com os dados da transação
  const handleTransactionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTransactionData({
      ...transactionData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-gray-200">
      {/* Renderiza o Header */}
      <Header
        onLogout={() => {
          localStorage.removeItem("token");
          window.location.href = "/login";
        }}
      />
      <div className="container mx-auto py-44 px-4">
        <h1 className="text-4xl font-extrabold mb-6 text-teal-400 text-center">
          Carteira Blockchain
        </h1>

        {/* Botão para criar uma nova carteira */}
        <div className="text-center mb-6">
          <button
            onClick={createWallet}
            className={`bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
              walletId !== null ? "cursor-not-allowed opacity-50" : ""
            }`}
            disabled={walletId !== null}
          >
            Criar Nova Carteira
          </button>
        </div>

        {successMessage && (
          <p className="text-green-400 mt-4 text-center">{successMessage}</p>
        )}
        {error && <p className="text-red-500 mt-4 text-center">{error}</p>}

        {/* Exibe as informações da carteira criada */}
        {walletId !== null && (
          <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg">
            <h2 className="text-xl font-semibold mb-4 text-teal-300">
              Carteira Criada
            </h2>
            <p>
              <strong>ID da Carteira:</strong> {walletId}
            </p>
            <p className="break-all">
              <strong>Chave Pública:</strong> {publicKey}
            </p>
          </div>
        )}

        {/* Formulário para assinar uma transação */}
        {walletId !== null && (
          <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg">
            <h2 className="text-xl font-semibold mb-4 text-teal-300">
              Assinar Transação
            </h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                signTransaction();
              }}
              className="grid grid-cols-1 gap-4"
            >
              <input
                type="text"
                name="sender"
                placeholder="Endereço do Remetente"
                value={transactionData.sender}
                onChange={handleTransactionChange}
                className="border border-gray-600 rounded-lg p-2 bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <input
                type="text"
                name="recipient"
                placeholder="Endereço do Destinatário"
                value={transactionData.recipient}
                onChange={handleTransactionChange}
                className="border border-gray-600 rounded-lg p-2 bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <input
                type="number"
                name="amount"
                placeholder="Valor da Transação"
                value={transactionData.amount}
                onChange={handleTransactionChange}
                className="border border-gray-600 rounded-lg p-2 bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button
                type="submit"
                className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300"
              >
                Assinar Transação
              </button>
            </form>
          </div>
        )}

        {/* Exibe a assinatura da transação */}
        {signature && (
          <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg">
            <h2 className="text-xl font-semibold mb-4 text-teal-300">
              Assinatura da Transação
            </h2>
            <p className="break-all bg-gray-700 p-4 rounded-lg text-white">
              {signature}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
