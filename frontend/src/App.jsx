import React, { useState, useEffect } from "react";
import Home from "./pages/Home";
import StatusBar from "./components/StatusBar";
import { terminalWS } from "./services/api"; // நாம் அடுத்து எழுதப்போகும் வெப்சாக்கெட் சர்வீஸ்

export default function App() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // ஆப் லோட் ஆனவுடன் லோக்கல் பேக்கெண்ட் உடன் வெப்சாக்கெட் கனெக்ஷன் செய்கிறோம்
    terminalWS.connect(
      () => setIsConnected(true),
      () => setIsConnected(false)
    );

    return () => terminalWS.disconnect();
  }, []);

  return (
    <div className="flex flex-col h-screen bg-black text-zinc-100 font-mono overflow-hidden">
      <div className="flex-1 overflow-auto">
        <Home isConnected={isConnected} />
      </div>
      <StatusBar isConnected={isConnected} />
    </div>
  );
}
