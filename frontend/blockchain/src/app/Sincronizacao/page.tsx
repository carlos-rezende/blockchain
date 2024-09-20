import React from "react";

// Definindo o componente App com TypeScript
const sincronizacao: React.FC = () => {
  return (
    <div className="App min-h-screen flex flex-col justify-center items-center bg-gray-100">
      {/* Cabeçalho */}
      <header className="App-header mb-8">
        <h1 className="text-4xl font-bold text-gray-800">Sincronização</h1>
      </header>

      {/* Corpo do conteúdo */}
      <main className="text-center">
        <div
          className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-lg"
          role="alert"
        >
          <p className="font-bold text-2xl">Página em Construção 🚧</p>
          <p>
            Esta página está em desenvolvimento. Por favor, volte mais tarde!
          </p>
        </div>
      </main>

      {/* Rodapé */}
      <footer className="mt-8">
        <p className="text-gray-600">© 2024 Todos os direitos reservados</p>
      </footer>
    </div>
  );
};

export default sincronizacao;
