import { Table, TableBody, TableCaption, TableCell, TableFooter, TableHead, TableHeader, TableRow, useFileContext } from "@/components";
import { FileActionType, UploadedFile } from "@/types";
import axios from "axios";
import { ReactElement, useDeferredValue, useEffect } from "react";

import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const ListBoletos = () : ReactElement => {
  const { t } = useTranslation();
  
  const context = useFileContext();

  const deferredFileList = useDeferredValue(context.state.fileList);

  // TODO: Move requests outside component
  useEffect(() => {
    context.dispatch({ type: FileActionType.FETCH_STARTED });
    const url = `http://localhost:8000/boletos/`;
    axios.get<UploadedFile[]>(url).then((response) => {
      const fileList = response.data;
      const payload = {fileList}
      context.dispatch({ type: FileActionType.FETCH_FINISHED, payload });
    }).catch(() => {
      context.dispatch({ type: FileActionType.FETCH_FINISHED, payload: { fileList: [] } });
    });
  }, []);

  return (
    <>
      <section className="animate-in slide-in-from-top flex justify-between w-full">
        <Link to={'/'} >
          <button className="text-sm rounded-md bg-zinc-600 text-white px-4 py-2 border-none font-semibold">
            { t("links.main.back") }
          </button>
        </Link>
        <h2 className="text-2xl font-medium text-neutral-400"> { t("boletos.list.title") } </h2>
        <Link to={"/boletos/upload"} >
          <button className="text-sm rounded-md bg-zinc-600 text-white px-4 py-2 border-none font-semibold">
            { t("links.boletos.upload") }
          </button>
        </Link>
      </section>
      <Table className="animate-in slide-in-from-top">
        <TableCaption>  { t("boletos.list.title") } </TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead> { t('boletos.list.header.id') } </TableHead>
            <TableHead> { t('boletos.list.header.name') } </TableHead>
            <TableHead> { t('boletos.list.header.size') } </TableHead>
            <TableHead> { t('boletos.list.header.uploaded_at') } </TableHead>
            <TableHead> { t('boletos.list.header.processed_at') } </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {deferredFileList.length > 0 ? 
            deferredFileList.map((file: UploadedFile) => {
              return (
                <TableRow key={file.id}>
                  <TableCell> {file.id} </TableCell>
                  <TableCell> {file.name} </TableCell>
                  <TableCell> {file.size} </TableCell>
                  <TableCell> {new Date(file.uploaded_at).toUTCString()} </TableCell>
                  <TableCell> {file.processed_at && new Date(file.processed_at).toISOString()} </TableCell>
                </TableRow>
              )
            }) :
            <TableRow>
              <TableCell colSpan={5} className="text-center">
                { t('boletos.list.empty') }
              </TableCell>
            </TableRow>
          }
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={5} className="text-center">
              {/* TODO: Pagination */}
              <a href={'#'}> 1 </a> | <a href={'#'}> 2 </a> | <a href={'#'}> 3 </a> ... <a href={'#'}> 12 </a>
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </>
  );

}

export { ListBoletos };
