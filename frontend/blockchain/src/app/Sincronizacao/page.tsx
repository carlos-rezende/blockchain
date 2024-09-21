"use client";
import Header from "@/components/header";
import { useState } from "react";

export default function SyncPage() {
  const [nodes, setNodes] = useState<string>(""); // Armazena os nós fornecidos pelo usuário
  const [message, setMessage] = useState<string | null>(null); // Armazena mensagens de sucesso ou erro
  const [error, setError] = useState<string | null>(null); // Armazena erros
  const [loading, setLoading] = useState<boolean>(false); // Armazena o estado de carregamento

  // Função para sincronizar a blockchain com os nós fornecidos
  const syncBlockchain = async () => {
    if (!nodes) {
      setError("Por favor, forneça um ou mais nós para sincronizar.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/sync", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nodes: nodes.split(",") }), // Divide os nós em uma lista
      });

      if (!response.ok) {
        throw new Error("Erro ao sincronizar a blockchain");
      }

      const data = await response.json();
      setMessage(data.message); // Armazena a mensagem de sucesso
      setError(null); // Limpa os erros
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError("Erro ao sincronizar a blockchain: " + err.message);
      } else {
        setError("Erro desconhecido ao sincronizar a blockchain");
      }
    } finally {
      setLoading(false); // Termina o estado de carregamento
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
          Sincronizar Blockchain
        </h1>

        {/* Formulário para fornecer os nós e sincronizar */}
        <div className="mt-6 bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg max-w-md mx-auto">
          <h2 className="text-xl font-semibold mb-4 text-teal-300">
            Forneça os Nós
          </h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              syncBlockchain();
            }}
            className="grid grid-cols-1 gap-4"
          >
            <input
              type="text"
              placeholder="Digite os nós separados por vírgula"
              value={nodes}
              onChange={(e) => setNodes(e.target.value)}
              className="border border-gray-600 rounded-lg p-2 bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            <button
              type="submit"
              className={`bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
                loading ? "cursor-not-allowed opacity-50" : "hover:scale-105"
              }`}
              disabled={loading}
            >
              {loading ? "Sincronizando..." : "Sincronizar Blockchain"}
            </button>
          </form>

          {/* Exibe mensagem de sucesso ou erro */}
          {message && <p className="text-green-400 mt-4">{message}</p>}
          {error && <p className="text-red-500 mt-4">{error}</p>}
        </div>
      </div>
    </div>
  );
}
