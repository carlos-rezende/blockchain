"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isAuthChecked, setIsAuthChecked] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      router.push("/dashboard"); // Redireciona imediatamente se estiver autenticado
    } else {
      setIsAuthChecked(true);
    }
  }, [router]);

  if (!isAuthChecked) {
    return <p>Carregando...</p>;
  }

  if (!isAuthenticated) {
    // Redireciona o usuário para a página de login se não estiver autenticado
    router.push("/login");
    return <p>Redirecionando para a página de login...</p>;
  }

  return <p>Redirecionando para o dashboard...</p>;
}
