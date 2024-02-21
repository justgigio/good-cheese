import { FileUploader } from "@/components";
import { ReactElement } from "react";

import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const UploadBoleto = (): ReactElement => {

  const { t } = useTranslation();

  return (
    <>
      <section className="animate-in slide-in-from-top flex justify-between w-96">
        <Link to={'/boletos'} >
          <button className="rounded-md text-sm bg-zinc-600 text-white px-4 py-2 border-none font-semibold"> { t("links.main.back") } </button>
        </Link>
        <h1 className="text-2xl font-medium text-neutral-400"> { t("boletos.upload.title") } </h1>
      </section>
      <FileUploader />
    </>
  )

}

export { UploadBoleto };
