import React from "react";

export default function CommandPreview({ text, setText, onExecute, isExecuting }) {
  return (
    <div className="bg-zinc-900 p-4 rounded border border-zinc-800 space-y-3">
      <div className="text-xs text-zinc-400">🤖 AI Predicted Command (Editable):</div>
      <div className="flex gap-2">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="flex-1 bg-black border border-zinc-700 rounded px-3 py-2 text-sky-400 focus:outline-none focus:border-sky-500 font-mono"
          placeholder="Draw something or type command here..."
        />
        <button
          onClick={onExecute}
          disabled={isExecuting || !text}
          className="bg-sky-600 hover:bg-sky-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-bold px-4 py-2 rounded transition"
        >
          {isExecuting ? "Running..." : "Run"}
        </button>
      </div>
    </div>
  );
}
