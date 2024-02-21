import { FileProvider } from "@/components";
import { ReactElement } from "react";

import { useTranslation } from "react-i18next";
import { Outlet } from "react-router-dom";

const Boletos = () : ReactElement => {
  const { t } = useTranslation();

  return (
    <>
      <h1 className="text-3xl font-medium text-white"> { t("boletos.main.title") } </h1>
      <hr className="border-white h-px w-full" />
      <FileProvider>
        <Outlet />
      </FileProvider>
    </>
  );

}

export { Boletos };
