"use client";
import Header from "@/components/header";
import { useState } from "react";

export default function MinePage() {
  const [minerAddress, setMinerAddress] = useState<string>("");
  const [message, setMessage] = useState<string | null>(null);
  const [blockData, setBlockData] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Função para minerar um bloco pendente sem fornecer endereço
  const minePendingTransactions = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/mine", {
        method: "GET",
      });

      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (err) {
      if (err instanceof Error) {
        setError("Erro ao minerar transações pendentes: " + err.message);
      } else {
        setError("Erro desconhecido ao minerar transações pendentes");
      }
    } finally {
      setLoading(false);
    }
  };

  // Função para minerar um novo bloco fornecendo o endereço do minerador
  const mineBlock = async () => {
    if (!minerAddress) {
      setError("O endereço do minerador é obrigatório.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/mine_block", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ miner_address: minerAddress }),
      });

      if (!response.ok) {
        throw new Error("Erro ao minerar o bloco");
      }

      const data = await response.json();
      setMessage(data.message);
      setBlockData(data.block); // Armazena os dados do bloco minerado
      setError(null);
    } catch (err) {
      if (err instanceof Error) {
        setError("Erro ao minerar o bloco: " + err.message);
      } else {
        setError("Erro desconhecido ao minerar o bloco");
      }
    } finally {
      setLoading(false);
    }
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
          Mineração de Blocos
        </h1>

        {/* Botão para minerar transações pendentes */}
        <div className="text-center mb-6">
          <button
            onClick={minePendingTransactions}
            className={`bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
              loading ? "cursor-not-allowed" : "hover:scale-105"
            }`}
            disabled={loading}
          >
            {loading ? "Minerando..." : "Minerar Transações Pendentes"}
          </button>
        </div>

        {/* Exibe mensagem de sucesso ou erro */}
        {message && (
          <p className="text-green-400 mt-4 text-center">{message}</p>
        )}
        {error && <p className="text-red-500 mt-4 text-center">{error}</p>}

        {/* Formulário para minerar um bloco fornecendo o endereço do minerador */}
        <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg">
          <h2 className="text-xl font-semibold mb-4 text-teal-300">
            Minerar Novo Bloco
          </h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              mineBlock();
            }}
            className="grid grid-cols-1 gap-4"
          >
            <input
              type="text"
              placeholder="Endereço do Minerador"
              value={minerAddress}
              onChange={(e) => setMinerAddress(e.target.value)}
              className="border border-gray-600 rounded-lg p-2 bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            <button
              type="submit"
              className={`bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
                loading ? "cursor-not-allowed" : "hover:scale-105"
              }`}
              disabled={loading}
            >
              {loading ? "Minerando Bloco..." : "Minerar Bloco"}
            </button>
          </form>
        </div>

        {/* Exibe os dados do bloco minerado, se disponível */}
        {blockData && (
          <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg">
            <h2 className="text-xl font-semibold mb-4 text-teal-300">
              Bloco Minerado
            </h2>
            <pre className="bg-gray-700 p-4 rounded-lg text-white overflow-x-auto">
              {JSON.stringify(blockData, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
