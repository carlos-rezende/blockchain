"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { FaBars, FaTimes } from "react-icons/fa"; // Ícones para o menu responsivo

interface HeaderProps {
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const router = useRouter(); // Hook para navegação programática

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    onLogout(); // Chama a função de logout do pai
    router.push("/login"); // Navegação rápida para login sem recarregar a página
  };

  return (
    <header className="absolute top-0 left-0 w-full p-4 bg-gradient-to-r from-gray-900 via-purple-900 to-black text-gray-100 z-20 shadow-lg">
      <div className="container flex justify-between items-center mx-auto">
        {/* Usando Link ao invés de <a> para navegação rápida */}
        <Link
          href="/"
          className="flex items-center space-x-2 text-2xl font-bold tracking-wider text-teal-400"
        >
          <span>Blockchain</span>
        </Link>

        {/* Menu para telas grandes */}
        <ul className="hidden space-x-6 lg:flex">
          <li>
            <Link
              href="/blockchain"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Blockchain
            </Link>
          </li>
          <li>
            <Link
              href="/NovaTransacao"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Transações
            </Link>
          </li>
          <li>
            <Link
              href="/Sincronizacao"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Sincronização
            </Link>
          </li>
          <li>
            <Link
              href="/bloco"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Bloco
            </Link>
          </li>
          <li>
            <Link
              href="/mineracao"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Minerar Bloco
            </Link>
          </li>
          <li>
            <Link
              href="/carteira"
              className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
            >
              Carteira
            </Link>
          </li>
        </ul>

        {/* Botão de logout para telas grandes */}
        <div className="hidden lg:flex items-center space-x-4">
          <button
            className="px-4 py-2 bg-red-600 rounded-lg text-white font-semibold hover:bg-red-500 transition duration-300"
            onClick={handleLogout} // Usa a função de logout otimizada
          >
            Sair
          </button>
        </div>

        {/* Menu Mobile - Ícone de hambúrguer */}
        <div className="lg:hidden">
          <button onClick={toggleMenu} className="text-gray-200">
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>
      </div>

      {/* Menu Mobile */}
      {isMenuOpen && (
        <div className="lg:hidden mt-4">
          <ul className="flex flex-col space-y-4 items-center">
            <li>
              <Link
                href="/blockchain"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu} // Fecha o menu ao clicar no link
              >
                Blockchain
              </Link>
            </li>
            <li>
              <Link
                href="/NovaTransacao"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu}
              >
                Transações
              </Link>
            </li>
            <li>
              <Link
                href="/Sincronizacao"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu}
              >
                Sincronização
              </Link>
            </li>
            <li>
              <Link
                href="/bloco"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu}
              >
                Bloco
              </Link>
            </li>
            <li>
              <Link
                href="/mineracao"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu}
              >
                Minerar Bloco
              </Link>
            </li>
            <li>
              <Link
                href="/carteira"
                className="text-gray-200 hover:text-teal-400 transition-colors duration-300"
                onClick={toggleMenu}
              >
                Carteira
              </Link>
            </li>
            <li>
              <button
                className="px-4 py-2 bg-red-600 rounded-lg text-white font-semibold hover:bg-red-500 transition duration-300"
                onClick={handleLogout} // Usa a função de logout otimizada
              >
                Sair
              </button>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
};

export default Header;
