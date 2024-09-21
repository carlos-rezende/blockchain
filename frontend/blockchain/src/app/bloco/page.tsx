"use client";
import Header from "@/components/header";
import axios from "axios";
import { useState } from "react";

const BlocksPage: React.FC = () => {
  const [blocks, setBlocks] = useState<string[] | null>(null);
  const [block, setBlock] = useState<string | null>(null);
  const [blockIndex, setBlockIndex] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar todos os blocos da blockchain
  const fetchAllBlocks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get("http://localhost:5000/blocks");
      setBlocks(response.data); // Armazena a lista de blocos
    } catch {
      setError("Erro ao buscar blocos.");
    } finally {
      setLoading(false);
    }
  };

  // Função para buscar um bloco específico com base no índice
  const fetchBlockByIndex = async () => {
    if (!blockIndex) {
      setError("Por favor, forneça o índice do bloco.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(
        `http://localhost:5000/block/${blockIndex}`
      );
      setBlock(response.data); // Armazena o bloco específico
    } catch {
      setError("Erro ao buscar o bloco. Verifique o índice fornecido.");
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
        <h1 className="text-4xl font-extrabold text-teal-400 mb-8 text-center">
          Blocos da Blockchain
        </h1>

        {/* Botão para buscar todos os blocos */}
        <div className="text-center mb-8">
          <button
            onClick={fetchAllBlocks}
            className={`bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
              loading ? "cursor-not-allowed" : "hover:scale-105"
            }`}
            disabled={loading}
          >
            {loading ? "Carregando blocos..." : "Buscar Todos os Blocos"}
          </button>
        </div>

        {/* Exibe a lista completa de blocos */}
        {blocks && (
          <div className="bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg text-gray-200">
            <h2 className="text-2xl font-semibold text-teal-300 mb-4">
              Lista de Blocos
            </h2>
            <pre className="bg-gray-700 p-4 rounded-lg text-white overflow-x-auto">
              {JSON.stringify(blocks, null, 2)}
            </pre>
          </div>
        )}

        {/* Formulário para buscar um bloco específico */}
        <div className="bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg text-gray-200 mt-6">
          <h2 className="text-2xl font-semibold text-teal-300 mb-4">
            Buscar Bloco por Índice
          </h2>
          <div className="mb-4">
            <label className="block text-sm text-teal-300">
              Índice do Bloco
            </label>
            <input
              type="number"
              className="w-full p-2 mt-1 bg-gray-700 bg-opacity-80 text-white rounded-lg shadow-inner focus:outline-none focus:ring-2 focus:ring-teal-500"
              value={blockIndex}
              onChange={(e) => setBlockIndex(e.target.value)}
              placeholder="Digite o índice do bloco"
            />
          </div>
          <button
            onClick={fetchBlockByIndex}
            className={`bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
              loading ? "cursor-not-allowed" : "hover:scale-105"
            }`}
            disabled={loading}
          >
            {loading ? "Carregando bloco..." : "Buscar Bloco"}
          </button>
        </div>

        {/* Exibe o bloco específico, se encontrado */}
        {block && (
          <div className="bg-gray-800 bg-opacity-50 p-6 rounded-xl shadow-lg backdrop-filter backdrop-blur-lg text-gray-200 mt-6">
            <h2 className="text-2xl font-semibold text-teal-300 mb-4">
              Bloco {blockIndex}
            </h2>
            <pre className="bg-gray-700 p-4 rounded-lg text-white overflow-x-auto">
              {JSON.stringify(block, null, 2)}
            </pre>
          </div>
        )}

        {/* Exibe mensagem de erro, se houver */}
        {error && <p className="text-red-500 mt-4">{error}</p>}
      </div>
    </div>
  );
};

export default BlocksPage;
