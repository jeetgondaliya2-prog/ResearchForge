function SourceCard({ source }) {

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">

      <h3 className="text-white font-medium">
        {source.title || "Research Source"}
      </h3>

      {source.url && (
        <a
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-purple-400 text-sm mt-2 inline-block hover:underline"
        >
          Open Source
        </a>
      )}

      {source.abstract && (
        <p className="text-slate-400 text-sm mt-3 line-clamp-4">
          {source.abstract}
        </p>
      )}

    </div>
  );
}

export default SourceCard;