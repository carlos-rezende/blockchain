"use client";
import Header from "@/components/header";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function AuthWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isAuthChecked, setIsAuthChecked] = useState<boolean>(false);
  const router = useRouter();

  // Verifica o token no localStorage assim que o componente carrega
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem("token");
      if (token) {
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
        router.push("/login"); // Redireciona para login se não estiver autenticado
      }
      setIsAuthChecked(true);
    };

    checkAuth();

    // Escuta mudanças no localStorage para refletir logout ou login em outras abas
    window.addEventListener("storage", checkAuth);

    return () => {
      window.removeEventListener("storage", checkAuth);
    };
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    router.push("/login"); // Redireciona após logout
  };

  if (!isAuthChecked) {
    return <p>Carregando...</p>;
  }

  return (
    <>
      {isAuthenticated && <Header onLogout={handleLogout} />}
      {children}
    </>
  );
}
