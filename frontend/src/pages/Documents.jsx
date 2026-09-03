import FileUpload from "../components/FileUpload";


function Documents() {

  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-3xl font-bold text-white">
          Research Documents
        </h1>

        <p className="text-slate-400 mt-2">
          Upload papers and documents for RAG-based research.
        </p>

      </div>


      <FileUpload />


      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">

        <h2 className="text-white font-semibold">
          Uploaded Documents
        </h2>

        <p className="text-slate-500 mt-4">
          No documents uploaded yet.
        </p>

      </div>

    </div>
  );
}

export default Documents;