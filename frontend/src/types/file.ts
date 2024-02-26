import { ReactNode } from "react";

export enum FileActionType {
  INPUT_CHANGE = "INPUT_CHANGE",
  UPLOAD_STARTED = "UPLOAD_STARTED",
  UPLOAD_FINISHED = "UPLOAD_FINISHED",
  UPLOAD_ERROR = "UPLOAD_ERROR",
  FETCH_STARTED = "FETCH_STARTED",
  FETCH_FINISHED = "FETCH_FINISHED",
}

type ReducerAction<T, P> = {
  type: T;
  payload?: Partial<P>;
};

type FileContextState = {
  isLoading: boolean;
  file: File | null;
  fileList: UploadedFile[]; // & {} You can add more information about the challenge inside this type
  uploadedFile: UploadedFile | null;
};

type FileAction = ReducerAction<FileActionType, Partial<FileContextState>>;

type FileDispatch = ({ type, payload }: FileAction) => void;

type FileContextType = {
  state: FileContextState;
  dispatch: FileDispatch;
};

type FileProviderProps = { children: ReactNode };

type FileStatus = {
  id: number;
  size: number;
  inserted: number;
  completed: boolean;
  percent: number;
};

type UploadedFile = {
  id: number;
  name: string;
  checksum: string;
  size: number;
  uploaded_at: Date;
  processed_at: Date;
};

export type {
  FileContextState,
  FileAction,
  FileDispatch,
  FileContextType,
  FileProviderProps,
  FileStatus,
  UploadedFile,
};
