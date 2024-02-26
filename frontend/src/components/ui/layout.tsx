import { ReactElement } from "react";
import { Link, Outlet } from "react-router-dom";
import { I18n } from ".";

function Layout(): ReactElement {
  return (
    <>
      <div className="h-screen w-screen bg-zinc-800 text-white gap-6 flex flex-1 flex-col items-center justify-center">
        <header className="w-full h-20 text-center justify-center align-middle flex">
          <I18n />
          <h1 className="text-4xl text-green-700 leading-loose">
            <Link to={"/"} className="inline-block h-full">
              Fullstack Kanastra's Challenge
            </Link>
          </h1>
        </header>
        <main className="gap-6 flex flex-1 flex-col items-center">
          <Outlet />
        </main>
      </div>
    </>
  );
}

export { Layout };
