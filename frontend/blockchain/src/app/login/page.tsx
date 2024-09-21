"use client";
import Login from "@/components/Login"; // Certifique-se de importar corretamente o componente Login
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function LoginPage() {
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const router = useRouter();

  // Função chamada após o login bem-sucedido
  const handleLoginSuccess = () => {
    setShowSuccessMessage(true); // Exibe a mensagem de sucesso
  };

  // Efeito para redirecionar após a mensagem de sucesso ser exibida
  useEffect(() => {
    if (showSuccessMessage) {
      const timer = setTimeout(() => {
        router.push("/dashboard"); // Redireciona após 3 segundos
      }, 3000);

      return () => clearTimeout(timer); // Limpa o timeout quando o componente desmonta
    }
  }, [showSuccessMessage, router]);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-gray-900 to-gray-700">
      <h1 className="mb-8 text-4xl font-bold text-teal-400">Seja bem-vindo</h1>

      {/* Componente Login */}
      <Login onLoginSuccess={handleLoginSuccess} />

      {/* Mensagem de sucesso exibida após o login */}
      {showSuccessMessage && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg text-lg transition-opacity duration-300 ease-in-out">
          🎉 Login realizado com sucesso! Redirecionando...
        </div>
      )}

      <div className="absolute bottom-4 text-teal-500 text-sm">
        Created by Carlos Rezende
      </div>
    </div>
  );
}
