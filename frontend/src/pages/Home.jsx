import React, { useState, useEffect } from "react";
import Canvas from "../components/Canvas";
import Toolbar from "../components/Toolbar";
import CommandPreview from "../components/CommandPreview";
import OutputPanel from "../components/OutputPanel";
import { terminalWS } from "../services/api";

export default function Home({ isConnected }) {
  const [predictedText, setPredictedText] = useState("");
  const [terminalLogs, setTerminalLogs] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    // பேக்கெண்டில் இருந்து வரும் அவுட்புட்டைக் கவனித்தல்
    const unsubscribe = terminalWS.subscribe((message) => {
      if (message.type === "prediction") {
        setPredictedText(message.text);
      } else if (message.type === "status") {
        setIsExecuting(true);
        setTerminalLogs((prev) => [...prev, `> ${message.message}`]);
      } else if (message.type === "terminal_output") {
        setIsExecuting(false);
        setTerminalLogs((prev) => [...prev, message.output]);
      } else if (message.type === "error") {
        setIsExecuting(false);
        setTerminalLogs((prev) => [...prev, `❌ Error: ${message.message}`]);
      }
    });

    return () => unsubscribe();
  }, []);

  const handleExecute = () => {
    if (!predictedText) return;
    terminalWS.executeCommand(predictedText);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <header className="border-b border-zinc-800 pb-4">
        <h1 className="text-2xl font-bold text-sky-400">Writing Terminal (WT)</h1>
        <p className="text-xs text-zinc-500">Handwriting & Voice Developer Productivity Tool</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <Toolbar onClear={() => setPredictedText("")} />
          <Canvas isConnected={isConnected} />
          <CommandPreview 
            text={predictedText} 
            setText={setPredictedText} 
            onExecute={handleExecute}
            isExecuting={isExecuting}
          />
        </div>
        <div>
          <OutputPanel logs={terminalLogs} setLogs={setTerminalLogs} />
        </div>
      </div>
    </div>
  );
}
