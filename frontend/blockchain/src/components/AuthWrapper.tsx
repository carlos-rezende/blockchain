"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const AuthWrapper = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isAuthChecked, setIsAuthChecked] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
      router.push("/login"); // Redireciona para login se não autenticado
    }
    setIsAuthChecked(true);
  }, [router]);

  // const handleLogout = () => {
  //   localStorage.removeItem("token");
  //   setIsAuthenticated(false);
  //   router.push("/login");
  // };

  if (!isAuthChecked) {
    return <p>Carregando...</p>; // Enquanto a autenticação está sendo verificada
  }

  return (
    <>
      {isAuthenticated} {/* Renderiza o Header após o login */}
      {children} {/* Renderiza o conteúdo da página */}
    </>
  );
};

export default AuthWrapper;
