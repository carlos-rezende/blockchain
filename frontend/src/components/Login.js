import axios from "axios";
import React, { useState } from "react";

function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    try {
      // Envia os dados de login usando os valores de email e senha
      const response = await axios.post("http://localhost:5000/login", {
        username: email, // Usa o estado de email como username
        password: password, // Usa o estado de password
      });

      const token = response.data.access_token;
      localStorage.setItem("token", token); // Armazena o token no localStorage
      setError(null); // Reseta o estado de erro
      alert("Login realizado com sucesso!");
      onLoginSuccess(); // Notifica o App que o login foi bem-sucedido
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      setError("Usuário ou senha incorretos.");
    }
  };

  return (
    <div className="flex flex-col max-w-md p-6 rounded-md sm:p-10 dark:bg-gray-50 dark:text-gray-800">
      <div className="mb-8 text-center">
        <h1 className="my-3 text-4xl font-bold">Sign in</h1>
        <p className="text-sm dark:text-gray-600">
          Sign in to access your account
        </p>
      </div>
      <form noValidate="" action="" className="space-y-12">
        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block mb-2 text-sm">
              Email address
            </label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder="leroy@jenkins.com"
              className="w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800"
            />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <label htmlFor="password" className="text-sm">
                Password
              </label>
              <a
                rel="noopener noreferrer"
                href="#"
                className="text-xs hover:underline dark:text-gray-600"
              >
                Forgot password?
              </a>
            </div>
            <input
              type="password"
              name="password"
              id="password"
              placeholder="*****"
              className="w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800"
            />
          </div>
        </div>
        <div className="space-y-2">
          <div>
            <button
              type="button"
              className="w-full px-8 py-3 font-semibold rounded-md dark:bg-violet-600 dark:text-gray-50"
            >
              Sign in
            </button>
          </div>
          <p className="px-6 text-sm text-center dark:text-gray-600">
            Don't have an account yet?
            <a
              rel="noopener noreferrer"
              href="#"
              className="hover:underline dark:text-violet-600"
            >
              Sign up
            </a>
            .
          </p>
        </div>
      </form>
    </div>
  );
}

export default Login;
