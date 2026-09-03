function ReportViewer({ report }) {

  if (!report) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">

        <p className="text-slate-500">
          Your research report will appear here.
        </p>

      </div>
    );
  }


  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

      <div className="flex items-center justify-between mb-5">

        <h2 className="text-xl font-bold text-white">
          Research Report
        </h2>

        <span className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 text-xs">
          Completed
        </span>

      </div>


      <div className="text-slate-300 whitespace-pre-wrap leading-7">
        {typeof report === "string"
          ? report
          : JSON.stringify(report, null, 2)
        }
      </div>

    </div>
  );
}

export default ReportViewer;