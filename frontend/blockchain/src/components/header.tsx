"use client";
import Link from "next/link";
import React from "react";

interface HeaderProps {
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  return (
    <header className="absolute top-0 left-0 w-full p-4 bg-gray-800 text-gray-100 z-10">
      <div className="container flex justify-between h-16 mx-auto">
        <a
          rel="noopener noreferrer"
          href="/"
          aria-label="Back to homepage"
          className="flex items-center p-2"
        >
          <span className="text-xl font-bold">Blockchain</span>
        </a>
        <ul className="items-stretch hidden space-x-3 lg:flex">
          <li className="flex">
            <Link
              href="/blockchain"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Blockchain
            </Link>
          </li>
          <li className="flex">
            <Link
              href="/NovaTransacao"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Nova Transação
            </Link>
          </li>
          <li className="flex">
            <Link
              href="/Sincronizacao"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Sincronização
            </Link>
          </li>
          <li className="flex">
            <Link
              href="/VerificarTransacao"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Verificar Transação
            </Link>
          </li>
          <li className="flex">
            <Link
              href="/mineracao"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Minerar Bloco
            </Link>
          </li>
          <li className="flex">
            <Link
              href="/carteira"
              className="flex items-center px-4 -mb-1 border-b-2 border-transparent hover:border-violet-600"
            >
              Carteira
            </Link>
          </li>
        </ul>
        <div className="items-center flex-shrink-0 hidden lg:flex">
          <button
            className="self-center px-8 py-3 font-semibold rounded bg-violet-600 text-gray-50"
            onClick={onLogout} // Chama a função de logout quando clicado
          >
            Sair
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
