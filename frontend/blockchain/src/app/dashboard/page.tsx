import Link from "next/link";

export default function Dashboard() {
  const pages = [
    { href: "/blockchain", title: "Blockchain" },
    { href: "/NovaTransacao", title: "Nova Transação" },
    { href: "/Sincronizacao", title: "Sincronização" },
    { href: "/VerificarTransacao", title: "Verificar Transação" },
    { href: "/mineracao", title: "Minerar Bloco" },
    { href: "/carteira", title: "Carteira" },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="p-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {pages.map((page) => (
          <Link key={page.href} href={page.href}>
            <div className="p-4 border border-gray-300 rounded-lg hover:bg-gray-100 cursor-pointer text-center">
              <h2 className="text-lg font-semibold">{page.title}</h2>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
