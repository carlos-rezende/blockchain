import axios from "axios";
import React, { useState } from "react";

function Blockchain() {
  // Estado para armazenar os blocos da blockchain
  const [blocks, setBlocks] = useState([]);
  const [error, setError] = useState(null); // Novo estado para armazenar erros

  // Função para buscar os blocos da API
  const fetchBlocks = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/blockchain");

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
    <div>
      <h1>Blockchain</h1>
      <button onClick={fetchBlocks}>Carregar Blocos</button>{" "}
      {/* Botão para carregar os blocos */}
      <ul>
        {blocks.map((block, index) => (
          <li key={index}>
            <strong>Bloco {block.index}</strong>: Hash - {block.hash}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Blockchain;
