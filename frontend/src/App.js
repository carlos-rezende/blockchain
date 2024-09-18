import React, { useEffect, useState } from "react";
import Blockchain from "./components/Blockchain";
import Login from "./components/Login";
import NovaTransacao from "./components/NovaTransacao";
import Sincronizacao from "./components/Sincronizacao";
import VerificarTransacao from "./components/VerificarTransacao";
import Wallet from "./components/carteira";
import MinerarBloco from "./components/mineracao";

function App() {
  // Estado para rastrear se o usuário está autenticado
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // Estado para verificar se a checagem da autenticação foi concluída
  const [isAuthChecked, setIsAuthChecked] = useState(false);

  useEffect(() => {
    // Verifica se existe um token armazenado no localStorage
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    }
    // Define que a verificação foi concluída
    setIsAuthChecked(true);
  }, []);

  // Função para atualizar o estado de autenticação após o login
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  // Função de logout
  const handleLogout = () => {
    localStorage.removeItem("token"); // Remove o token do localStorage
    setIsAuthenticated(false); // Atualiza o estado para deslogado
  };

  // Se a verificação da autenticação não foi concluída, não renderiza nada
  if (!isAuthChecked) {
    return null; // Ou pode retornar um loader/spinner para indicar que está carregando
  }

  // Se não estiver autenticado, renderiza apenas o componente de Login
  if (!isAuthenticated) {
    return (
      <div className="App">
        <h1>Seja Bem vindo a Blockchain</h1>
        <Login onLoginSuccess={handleLoginSuccess} />
      </div>
    );
  }

  // Se estiver autenticado, renderiza os componentes da aplicação
  return (
    <div className="App">
      <h1>Blockchain</h1>
      <button onClick={handleLogout}>Sair</button> {/* Botão de logout */}
      <Blockchain />
      <NovaTransacao />
      <Sincronizacao />
      <VerificarTransacao />
      <MinerarBloco />
      <Wallet />
    </div>
  );
}

export default App;
