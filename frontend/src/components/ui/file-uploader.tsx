import { FileActionType, FileStatus, UploadedFile } from "@/types";
import { useFileContext } from "./file";
import { ChangeEvent, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const FileUploader = () => {
  const context = useFileContext();

  const file = context.state.file;
  const isLoading = context.state.isLoading;
  const [loadingPercentage, setLoadingPercentage] = useState(0);

  const navigate = useNavigate();

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.currentTarget.files && event.currentTarget.files.length > 0) {
      const file = event.currentTarget.files[0];
      const payload = { file };
      context.dispatch({ type: FileActionType.INPUT_CHANGE, payload });
    }
  };

  // TODO: Move requests outside component
  const handleSubmit = () => {
    if (file) {
      const url = "http://localhost:8000/boletos/upload";
      const formData = new FormData();
      formData.append("file", file);
      formData.append("fileName", file.name);
      const config = {
        headers: {
          "content-type": "multipart/form-data",
        },
      };

      context.dispatch({ type: FileActionType.UPLOAD_STARTED });
      axios.post<UploadedFile>(url, formData, config).then((response) => {
        checkUpload(response.data);
      });
    }
  };

  // TODO: Move requests outside component
  const checkUpload = (file: UploadedFile) => {
    const url = `http://localhost:8000/boletos/upload/${file.id}`;
    axios
      .get<FileStatus>(url)
      .then((response) => {
        const status = response.data;

        setLoadingPercentage(status.percent);
        if (status.completed) {
          const payload = { uploadedFile: file };
          context.dispatch({ type: FileActionType.UPLOAD_FINISHED, payload });
          navigate("/boletos", { replace: true });
        } else {
          setTimeout(() => checkUpload(file), 500);
        }
      })
      .catch(() => {
        context.dispatch({ type: FileActionType.UPLOAD_ERROR });
      });
  };

  const humanByteSize = (bytesize: number): string => {
    if (bytesize > 1024 * 1024) {
      return `${(bytesize / (1024 * 1024)).toFixed(2)} MB`;
    }

    if (bytesize > 1024) {
      return `${(bytesize / 1024).toFixed(2)} KB`;
    }

    return `${bytesize} bytes`;
  };

  return (
    <div className="flex flex-col gap-6 w-full">
      {!isLoading && (
        <div>
          <label htmlFor="file" className="sr-only">
            Choose a file
          </label>
          <input
            id="file"
            type="file"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,text/csv"
            onChange={handleChange}
          />
        </div>
      )}
      {file && !isLoading && (
        <section className="animate-in slide-in-from-top flex flex-col">
          <p className="pb-6">File details:</p>
          <ul>
            <li>Name: {file.name}</li>
            <li>Type: {file.type}</li>
            <li>Size: {humanByteSize(file.size)}</li>
          </ul>
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="rounded-lg bg-green-800 text-white px-4 py-2 border-none font-semibold"
          >
            Upload the file
          </button>
        </section>
      )}
      {isLoading && (
        <section className="animate-in slide-in-from-top flex flex-col w-full">
          <p className="pb-6">Uploading...</p>
          <div className="w-full h-2 bg-green-800 rounded-full">
            <div
              style={{ width: `${loadingPercentage}%` }}
              className="h-full text-center text-xs text-white bg-green-600 rounded-full transition-all"
            ></div>
          </div>
        </section>
      )}
    </div>
  );
};

export { FileUploader };
