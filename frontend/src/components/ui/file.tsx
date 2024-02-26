import { FileContextType } from "@/types";
import { useContext } from "react";
import { FileContext } from "./file-provider";

export const useFileContext = (): FileContextType => {
  const context = useContext(FileContext);

  if (context === undefined)
    throw new Error("useFileContext must be used within a FileProvider");

  return context;
};
