import React from "react";

export default function Toolbar({ onClear }) {
  const triggerClear = () => {
    window.dispatchEvent(new Event("clear-canvas"));
    onClear();
  };

  return (
    <div className="flex justify-between items-center bg-zinc-900 p-2 rounded border border-zinc-800 text-sm">
      <span className="text-zinc-400 font-medium px-2">✏️ Input Panel</span>
      <div className="space-x-2">
        <button 
          onClick={() => alert("Voice feature coming soon!")}
          className="bg-zinc-800 text-zinc-300 px-3 py-1 rounded border border-zinc-700 hover:bg-zinc-700 transition"
        >
          🎙️ Voice
        </button>
        <button 
          onClick={triggerClear}
          className="bg-red-950/40 text-red-400 px-3 py-1 rounded border border-red-900/60 hover:bg-red-900/40 transition"
        >
          Clear
        </button>
      </div>
    </div>
  );
}
