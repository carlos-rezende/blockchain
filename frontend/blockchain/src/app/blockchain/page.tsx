"use client";
import Header from "@/components/header";
import { useEffect, useState } from "react";

// Definindo o tipo para um bloco da blockchain
interface Block {
  index: number;
  timestamp: string;
  data: string; // Dependendo da estrutura de dados de cada bloco, isso pode mudar
  previous_hash: string;
  hash: string;
}

export default function BlockchainPage() {
  const [blockchain, setBlockchain] = useState<Block[]>([]); // Estado para armazenar a blockchain
  const [loading, setLoading] = useState<boolean>(true); // Estado de carregamento
  const [error, setError] = useState<string | null>(null); // Estado para erros

  // Função para buscar a blockchain da API
  const fetchBlockchain = async () => {
    setLoading(true); // Inicia o carregamento
    setError(null); // Reseta o erro
    try {
      const response = await fetch("http://localhost:5000/blockchain"); // Chama a API
      if (!response.ok) {
        throw new Error("Erro ao buscar a blockchain");
      }
      const data = await response.json(); // Converte a resposta para JSON
      setBlockchain(data); // Atualiza o estado com a blockchain
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message); // Captura a mensagem de erro se for uma instância de Error
      } else {
        setError("Ocorreu um erro desconhecido."); // Mensagem genérica para erros desconhecidos
      }
    } finally {
      setLoading(false); // Desativa o carregamento após a requisição
    }
  };

  // Carrega a blockchain na primeira renderização
  useEffect(() => {
    fetchBlockchain();
  }, []); // O array vazio garante que a chamada será feita apenas uma vez

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-gray-200">
      {/* Renderiza o Header */}
      <Header
        onLogout={() => {
          localStorage.removeItem("token"); // Remove o token ao fazer logout
          window.location.href = "/login"; // Redireciona para login
        }}
      />

      <div className="container mx-auto py-44 px-4">
        <h1 className="text-4xl font-extrabold text-teal-400 mb-8 text-center">
          Blockchain
        </h1>

        {/* Botão de Atualizar */}
        <div className="text-center mb-8">
          <button
            onClick={fetchBlockchain} // Ação para recarregar a blockchain
            className={`bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-lg shadow-lg transition duration-300 ${
              loading ? "cursor-not-allowed" : "hover:scale-105"
            }`}
            disabled={loading}
          >
            {loading ? "Atualizando..." : "Atualizar Blockchain"}
          </button>
        </div>

        {/* Renderiza a blockchain ou mensagens de erro */}
        {loading && <p className="text-center">Carregando a blockchain...</p>}
        {error && <p className="text-red-500 text-center">Erro: {error}</p>}

        {/* Exibe os blocos da blockchain */}
        {!loading && !error && blockchain.length > 0 && (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {blockchain.map((block) => (
              <div
                key={block.hash} // Usar o hash como chave única
                className="p-6 border border-gray-300 rounded-xl shadow-md bg-opacity-50 bg-gray-800 backdrop-filter backdrop-blur-lg text-gray-200 hover:shadow-2xl transition duration-300 transform hover:scale-105"
              >
                <h2 className="text-xl font-bold text-teal-300">
                  Bloco {block.index}
                </h2>
                <p className="text-sm text-gray-400">
                  <strong>Timestamp:</strong> {block.timestamp}
                </p>
                <p className="text-sm text-gray-400">
                  <strong>Dados:</strong> {JSON.stringify(block.data)}
                </p>
                <p className="text-sm text-gray-400">
                  <strong>Hash Anterior:</strong> {block.previous_hash}
                </p>
                <p className="text-sm text-gray-400">
                  <strong>Hash:</strong> {block.hash}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Mensagem caso não haja blocos na blockchain */}
        {!loading && !error && blockchain.length === 0 && (
          <p className="text-center text-gray-400">
            Nenhum bloco disponível na blockchain.
          </p>
        )}
      </div>
    </div>
  );
}
