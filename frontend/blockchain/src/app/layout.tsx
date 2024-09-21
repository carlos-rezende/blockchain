import AuthWrapper from "@/components/AuthWrapper"; // Um novo componente que usará hooks
import { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "Blockchain",
  description: "App de blockchain com Next.js",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-br">
      <head>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body>
        {/* Envolva o conteúdo em um Client Component */}
        <AuthWrapper>{children}</AuthWrapper>
      </body>
    </html>
  );
}
