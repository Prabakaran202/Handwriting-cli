
import click
import uvicorn
import webbrowser
import threading
import time
from wt_cli.canvas_server import app
from wt_cli.executor import execute_command

@click.group()
def cli():
    """
    🖋️ Writing Terminal (WT) - CLI Tool
    Handwriting & Voice commands translated directly into Linux Terminal actions.
    """
    pass

def open_browser():
    """சர்வர் ஆன் ஆனவுடன் பிரவுசரை ஓபன் செய்ய சிறிய delay-உடன் இயங்கும் பங்க்ஷன்"""
    time.sleep(1.5)  # சர்வர் முழுமையாகத் துவங்க காத்திருக்கிறோம்
    click.echo("🌐 Opening Writing Terminal UI in your browser...")
    webbrowser.open("http://localhost:8000")

@cli.command()
def start():
    """Handwriting Canvas மற்றும் சர்வரை லோக்கலில் துவக்க"""
    click.echo("🚀 Writing Terminal (WT) Engine Starting up...")
    
    # பிரவுசரைத் தனியாக ஒரு Thread-ல் ஓபன் செய்கிறோம் (Blocking-ஐ தவிர்க்க)
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # FastAPI சர்வரை லோக்கல் போர்ட் 8000-ல் இயக்குகிறோம்
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        click.echo("\n🛑 Writing Terminal சர்வர் நிறுத்தப்பட்டது. மீண்டும் சந்திப்போம்!")

@cli.command()
@click.argument('tamil_text')
def run(tamil_text):
    """டெர்மினலிலேயே நேரடியாக தமிழ் கமாண்ட் ரன் செய்ய (எ.கா: wt run 'கோப்புறையை உருவாக்கு')"""
    click.echo(f"📥 ஆய்ந்தறியப்படுகிறது: '{tamil_text}'...")
    
    # TODO: இங்கு உங்களுடைய ai/command_mapper மாடலை இணைக்க வேண்டும்.
    # இப்போதைக்கு ஒரு எளிய ஹார்ட்கோடட் மேப்பிங் டெஸ்டிங்கிற்காக:
    command_map = {
        "கோப்புறையை உருவாக்கு": "mkdir புதிய_கோப்பு",
        "பட்டியலிடு": "ls -la",
        "தற்போதைய பாதை": "pwd"
    }
    
    final_command = command_map.get(tamil_text.strip())
    
    if final_command:
        click.echo(f"⚙️ Executing Linux Command: {final_command}")
        output = execute_command(final_command)
        click.echo(output)
    else:
        click.echo(f"❌ பிழை: '{tamil_text}' என்பதற்கான லினக்ஸ் கமாண்ட் கண்டறியப்படவில்லை!")

if __name__ == "__main__":
    cli()
