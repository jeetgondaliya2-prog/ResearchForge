import { useState } from "react";
import { Upload } from "lucide-react";
import { uploadDocument } from "../services/api";


function FileUpload() {

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const handleUpload = async () => {

    if (!file) {
      setMessage("Please select a file.");
      return;
    }


    setLoading(true);
    setMessage("");


    try {

      const result = await uploadDocument(file);

      setMessage(
        result.message ||
        "Document uploaded successfully."
      );

    } catch (error) {

      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        "Document upload failed."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

      <div className="flex items-center gap-3 mb-4">

        <Upload className="text-purple-400" />

        <h2 className="text-white font-semibold">
          Upload Research Documents
        </h2>

      </div>


      <input
        type="file"
        accept=".pdf,.txt,.doc,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        className="w-full text-sm text-slate-400"
      />


      {file && (
        <p className="text-slate-400 text-sm mt-3">
          Selected: {file.name}
        </p>
      )}


      <button
        onClick={handleUpload}
        disabled={loading}
        className="mt-4 bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 text-white px-5 py-2 rounded-lg"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>


      {message && (
        <p className="text-sm text-slate-300 mt-4">
          {message}
        </p>
      )}

    </div>
  );
}

export default FileUpload;