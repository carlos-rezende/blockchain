import axios from "axios";
import React, { useState } from "react";

// Define a estrutura esperada para os blocos
interface Block {
  index: number;
  hash: string;
}

const Blockchain: React.FC = () => {
  // Estado para armazenar os blocos da blockchain
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [error, setError] = useState<string | null>(null); // Estado para armazenar erros

  // Função para buscar os blocos da API
  const fetchBlocks = async () => {
    try {
      const response = await axios.get<Block[]>(
        "http://127.0.0.1:5000/blockchain"
      );

      // Agora deve receber diretamente um array
      console.log("Resposta da API:", response.data);

      // Verifica se a resposta é um array
      if (Array.isArray(response.data)) {
        setBlocks(response.data);
      } else {
        throw new Error("Resposta da API não é um array.");
      }
    } catch (error) {
      console.error("Erro ao buscar a blockchain:", error);
      setError("Erro ao buscar a blockchain.");
    }
  };

  // Renderiza uma mensagem de erro, se houver
  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="pt-24 p-4 relative z-0">
      <h1 className="text-center mb-4">Blockchain</h1>
      <button
        onClick={fetchBlocks}
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Carregar Blocos
      </button>
      {/* Botão para carregar os blocos */}
      <ul className="list-disc pl-5">
        {blocks.map((block, index) => (
          <li key={index} className="mb-2">
            <strong>Bloco {block.index}</strong>: Hash - {block.hash}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Blockchain;
