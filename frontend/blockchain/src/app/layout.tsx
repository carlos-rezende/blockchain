"use client"; // Adiciona esta linha para transformar o componente em um Client Component
import Header from "@/components/header";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isAuthChecked, setIsAuthChecked] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
      router.push("/login");
    }
    setIsAuthChecked(true);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    router.push("/login"); // Redireciona para a página de login após logout
  };

  if (!isAuthChecked) {
    return <p>Carregando...</p>;
  }

  return (
    <html lang="pt-br">
      <body>
        {isAuthenticated && <Header onLogout={handleLogout} />}

        {children}
      </body>
    </html>
  );
}
