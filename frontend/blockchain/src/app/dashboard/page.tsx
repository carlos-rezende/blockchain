"use client";
import dynamic from "next/dynamic";
import { Suspense } from "react";
import { BsWallet2 } from "react-icons/bs";
import { FaMoneyBillTransfer } from "react-icons/fa6";
import { GiMiner } from "react-icons/gi";
import { GrTransaction, GrUpdate } from "react-icons/gr";
import { SiHiveBlockchain } from "react-icons/si";

// Lazy load Header
const Header = dynamic(() => import("@/components/header"), {
  ssr: false, // O Header será carregado no cliente apenas
});

const LinkComponentCard = dynamic(() => import("@/components/card/card"), {
  ssr: false, // Carrega o card dinamicamente no cliente
});

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
      <Suspense fallback={<p>Carregando...</p>}>
        {/* Renderiza o Header */}
        <Header
          onLogout={() => {
            localStorage.removeItem("token");
            window.location.href = "/login"; // Redireciona para login
          }}
        />
      </Suspense>

      {/* Conteúdo do dashboard */}
      <div className="container mx-auto py-44 px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold tracking-wide">
            Painel de Controle Blockchain
          </h1>
          <p className="text-lg text-gray-300 mt-4">
            Gerencie suas operações e interações com a blockchain de forma
            intuitiva.
          </p>
        </div>

        {/* Cards de funcionalidades */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <LinkComponentCard
            name="Blockchain"
            subTitle="Gerencie sua blockchain"
            linkRoutes="/blockchain"
            icon={<SiHiveBlockchain size={30} />}
          />
          <LinkComponentCard
            name="Nova Transação"
            subTitle="Realize uma transação"
            linkRoutes="/NovaTransacao"
            icon={<FaMoneyBillTransfer size={30} />}
          />
          <LinkComponentCard
            name="Sincronização"
            subTitle="Sincronize a blockchain"
            linkRoutes="/Sincronizacao"
            icon={<GrUpdate size={30} />}
          />
          <LinkComponentCard
            name="Verificar Transação"
            subTitle="Verifique uma transação"
            linkRoutes="/VerificarTransacao"
            icon={<GrTransaction size={30} />}
          />
          <LinkComponentCard
            name="Minerar Bloco"
            subTitle="Minere um novo bloco"
            linkRoutes="/mineracao"
            icon={<GiMiner size={40} />}
          />
          <LinkComponentCard
            name="Carteira"
            subTitle="Consulte sua carteira"
            linkRoutes="/carteira"
            icon={<BsWallet2 size={24} />}
          />
        </div>
      </div>
    </div>
  );
}
