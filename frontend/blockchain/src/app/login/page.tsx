"use client";
import Login from "@/components/login"; // Certifique-se de importar corretamente o componente Login
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  // Função chamada após o login bem-sucedido
  const handleLoginSuccess = () => {
    router.push("/dashboard"); // Redireciona para o dashboard após o login
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="mb-8 text-2xl font-bold">Seja bem vindo</h1>
      <Login onLoginSuccess={handleLoginSuccess} /> {/* Componente Login */}
    </div>
  );
}
