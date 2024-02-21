import { useTranslation } from 'react-i18next';

import BrasilFlag from '/flag-brazil.svg';
import EuaFlag from '/flag-united-states.svg';

const I18n = () => {
  const { i18n } = useTranslation();

  const handleChangeLanguage = (language: string) => {
    i18n.changeLanguage(language);
  };

  const selectedLanguage = i18n.language;
  return (
    <div className="absolute top-5 right-5 flex justify-between space-x-2">
      <img
        width={40}
        onClick={() => handleChangeLanguage('pt-BR')}
        alt="Bandeira do Brasil"
        src={BrasilFlag}
        className={selectedLanguage === 'pt-BR' ? 'drop-shadow-2xl' : 'grayscale cursor-pointer'}
      />
      <img
        width={40}
        onClick={() => handleChangeLanguage('en-US')}
        alt="United States Flag"
        src={EuaFlag}
        className={selectedLanguage === 'en-US' ? 'drop-shadow-2xl' : 'grayscale cursor-pointer'}
      />
    </div>
  )
}

export { I18n };
