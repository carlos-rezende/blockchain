import axios from "axios";
import { useState } from "react";

interface LoginProps {
  onLoginSuccess: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Função para processar o login
  const handleLogin = async () => {
    if (!email || !password) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    // Verifica se as credenciais são do administrador
    if (email === "admin@admin" && password === "admin1234") {
      // Login master bem-sucedido
      localStorage.setItem("token", "admin-token"); // Você pode usar um token fictício
      setError(null);
      onLoginSuccess(); // Chama a função de sucesso para redirecionar
      return;
    }

    // Processa login normal com a API
    try {
      setLoading(true);
      const response = await axios.post("/login", {
        username: email,
        password,
      });

      const token = response.data.access_token;
      localStorage.setItem("token", token);
      setError(null);
      onLoginSuccess(); // Chama a função de sucesso para redirecionar
    } catch (err: unknown) {
      // Exibe detalhes do erro no console para depuração
      console.error("Erro ao fazer login:", err);
      setError("Erro ao fazer login. Verifique suas credenciais.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 shadow-lg rounded-lg p-8 w-full max-w-md mx-auto">
      <h2 className="text-3xl text-center text-teal-400 font-semibold mb-6">
        Login Blockchain
      </h2>
      <form
        onSubmit={(e) => e.preventDefault()}
        className="space-y-6"
        noValidate
      >
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-teal-300"
          >
            Email
          </label>
          <input
            type="email"
            id="email"
            placeholder="example@email.com"
            className="mt-1 block w-full px-4 py-2 bg-gray-800 text-white border border-gray-700 rounded-lg shadow-sm focus:ring-teal-400 focus:border-teal-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-teal-300"
          >
            Senha
          </label>
          <input
            type="password"
            id="password"
            placeholder="******"
            className="mt-1 block w-full px-4 py-2 bg-gray-800 text-white border border-gray-700 rounded-lg shadow-sm focus:ring-teal-400 focus:border-teal-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button
          type="button"
          className="w-full py-2 bg-teal-500 hover:bg-teal-400 text-white font-semibold rounded-lg shadow-lg transition duration-300"
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? "Carregando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
};

export default Login;
