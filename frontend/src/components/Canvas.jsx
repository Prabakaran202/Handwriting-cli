import React, { useRef, useState, useEffect } from "react";
import { terminalWS } from "../services/api";

export default function Canvas({ isConnected }) {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [strokes, setStrokes] = useState([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 4;

    // "clear-canvas" ஈவென்ட்டைக் கவனித்தல்
    const handleClear = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      setStrokes([]);
    };
    window.addEventListener("clear-canvas", handleClear);
    return () => window.removeEventListener("clear-canvas", handleClear);
  }, []);

  const startDrawing = (e) => {
    if (!isConnected) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    canvasRef.current.getContext("2d").beginPath();
    canvasRef.current.getContext("2d").moveTo(x, y);
    setIsDrawing(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const ctx = canvasRef.current.getContext("2d");
    ctx.lineTo(x, y);
    ctx.stroke();
    setStrokes((prev) => [...prev, { x, y }]);
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    if (strokes.length > 0) terminalWS.sendStroke(strokes);
  };

  return (
    <canvas
      ref={canvasRef}
      width={480}
      height={250}
      className="w-full bg-zinc-950 rounded border border-zinc-800 cursor-crosshair touch-none shadow-inner"
      onMouseDown={startDrawing}
      onMouseMove={draw}
      onMouseUp={stopDrawing}
      onMouseLeave={stopDrawing}
    />
  );
}
