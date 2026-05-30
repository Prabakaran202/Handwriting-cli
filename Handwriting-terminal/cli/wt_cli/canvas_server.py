import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from wt_cli.executor import execute_command

# AI Services இறக்குமதி (இப்போதைக்கு placeholders ஆக இருக்கும்)
# from app.services.ink_recognition import recognize_ink
# from app.services.command_parser import parse_tamil_command
# from app.services.ai_fixer import fix_command

app = FastAPI(title="Writing Terminal (WT) Backend Server")

# Frontend (React) உடன் தடையின்றி இணைய CORS அனுமதி
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production-ல் இதை குறிப்பிட்ட போர்ட்டிற்கு மட்டும் மாற்றலாம்
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Writing Terminal API is running locally!"}


@app.websocket("/ws/terminal")
async def websocket_endpoint(websocket: WebSocket):
    """
    React Canvas மற்றும் Terminal Output Panel-ஐ இணைக்கும் 
    முக்கியமான ரியல்-டைம் வெப்சாக்கெட் சேனல்.
    """
    await websocket.accept()
    print("🔌 UI Connection Established!")
    
    try:
        while True:
            # Frontend-லிருந்து டேட்டாவை வாங்குதல் (JSON வடிவில்)
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            data_type = payload.get("type") # 'stroke', 'execute', 'voice'
            
            # 1. பயனர் கேன்வாஸில் எழுதும்போது (Real-time Stroke Tracking)
            if data_type == "stroke":
                coordinates = payload.get("data")
                # TODO: இங்கு உங்கள் AI மாடலை இணைக்க வேண்டும் (ai/handwriting_model)
                # predicted_text = recognize_ink(coordinates)
                predicted_text = "git status" # இப்போதைக்கு ஒரு டெஸ்ட் ஸ்ட்ரிங்
                
                # கண்டுபிடித்த டெக்ஸ்டை உடனுக்குடன் UI-க்கு அனுப்புதல்
                await websocket.send_json({
                    "type": "prediction",
                    "text": predicted_text
                })
                
            # 2. பயனர் கமாண்டை இயக்கச் சொல்லும்போது (Command Execution)
            elif data_type == "execute":
                raw_text = payload.get("text")
                print(f"📥 Received Text to Process: {raw_text}")
                
                # TODO: தமிழ் கமாண்டாக இருந்தால் லினக்ஸ் கமாண்டாக மாற்றும் லேயர்
                # if is_tamil(raw_text):
                #     final_command = parse_tamil_command(raw_text)
                # else:
                #     final_command = raw_text
                
                final_command = raw_text # இப்போதைக்கு டைரக்ட் கமாண்ட்
                
                # கமாண்டை பாதுகாப்பாக சிஸ்டமில் இயக்குதல்
                await websocket.send_json({"type": "status", "message": f"Running: {final_command}..."})
                output = execute_command(final_command)
                
                # அவுட்புட்டை UI-ன் OutputPanel-க்கு அனுப்புதல்
                await websocket.send_json({
                    "type": "terminal_output",
                    "output": output
                })

    except WebSocketDisconnect:
        print("❌ UI Connection Disconnected.")
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        await websocket.send_json({"type": "error", "message": str(e)})
