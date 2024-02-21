import { FileAction, FileActionType, FileContextState, FileContextType, FileProviderProps, UploadedFile } from "@/types";
import { createContext, useContext, useReducer } from "react";

const FileContextInitialValues: FileContextState = {
  file: null,
  isLoading: false,
  fileList: [],
  uploadedFile: null
};

const FileContext = createContext({} as FileContextType);

const FileReducer = (
  state: FileContextState,
  action: FileAction,
): FileContextState => {
  switch (action.type) {
    case FileActionType.INPUT_CHANGE:
      if (action.payload?.file !== undefined) {
        return {
          ...state,
          file: action.payload.file
        }
      };
      return {
        ...state,
        file: null
      };
    case FileActionType.UPLOAD_STARTED:
      return {
        ...state,
        isLoading: true
      };
    case FileActionType.UPLOAD_FINISHED:
      return {
        ...state,
        file: null,
        isLoading: false,
        fileList: [...state.fileList, action.payload?.uploadedFile as UploadedFile]
      };
    case FileActionType.UPLOAD_ERROR:
      return {
        ...FileContextInitialValues,
        fileList: state.fileList
      };
    case FileActionType.FETCH_STARTED:
      return {
        ...state,
        isLoading: true
      };
    case FileActionType.FETCH_FINISHED:
      return {
        ...state,
        isLoading: false,
        fileList: action.payload?.fileList || []
      };
    default: {
      throw new Error(`Unhandled action type: ${action.type}`);
    }
  }
};

export const FileProvider = ({ children }: FileProviderProps) => {
  const [state, dispatch] = useReducer(
    FileReducer,
    FileContextInitialValues,
  );

  return (
    <FileContext.Provider value={{ state, dispatch }}>
      {children}
    </FileContext.Provider>
  );
};

export const useFileContext = () => {
  const context = useContext(FileContext);

  if (context === undefined)
    throw new Error("useFileContext must be used within a FileProvider");

  return context;
};
