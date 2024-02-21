import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const Home = () => {
  const { t } = useTranslation()

  return (<>
    <p className="text-2xl font-medium w-96 text-center"> { t("home.message") } </p>
    <Link to={"/boletos"} >
      <button className="rounded-md text-sm bg-zinc-600 text-white px-4 py-2 border-none font-semibold">
        { t("links.boletos.list") }
      </button>
    </Link>
  </>);

}

export { Home };
