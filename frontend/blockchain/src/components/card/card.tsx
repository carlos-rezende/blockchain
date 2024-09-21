import Link from "next/link";
import { ReactNode } from "react";

// Define o tipo das props para o componente Card
interface CardProps {
  name: string;
  subTitle: string;
  linkRoutes: string;
  icon?: ReactNode;
}

// Componente reutilizável que cria um card com um link.
const Card: React.FC<CardProps> = ({ name, subTitle, linkRoutes, icon }) => {
  return (
    <Link
      href={linkRoutes}
      className="relative block p-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl shadow-lg transform transition hover:scale-105 hover:shadow-2xl hover:bg-opacity-90"
    >
      {/* LinkComponent para renderizar o conteúdo */}
      <LinkComponent name={name} subTitle={subTitle} icon={icon} />
      <div className="absolute inset-0 z-[-1] bg-white bg-opacity-10 blur-md rounded-xl"></div>
    </Link>
  );
};

// Define o tipo das props para o componente LinkComponent
interface LinkComponentProps {
  name: string;
  subTitle: string;
  icon?: ReactNode;
}

// Componente que renderiza o conteúdo dentro do card.
const LinkComponent: React.FC<LinkComponentProps> = ({
  name,
  subTitle,
  icon,
}) => {
  return (
    <div className="text-center space-y-2">
      <div className="flex items-center justify-center h-16 w-16 rounded-full bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-inner">
        {icon && <span className="text-4xl">{icon}</span>}
      </div>
      <h4 className="text-2xl font-bold text-white">{name}</h4>
      <p className="text-sm font-medium text-gray-300">{subTitle}</p>
    </div>
  );
};

export default Card;
