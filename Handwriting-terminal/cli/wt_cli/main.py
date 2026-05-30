# cli/wt_cli/main.py
import click
import uvicorn
import webbrowser
from wt_cli.canvas_server import app

@click.group()
def cli():
    """Writing Terminal (WT) - Handwriting & Voice to Terminal Command Tool"""
    pass

@cli.command()
def start():
    """Handwriting ஸ்கிரீனை ஓபன் செய்ய"""
    click.echo("🚀 Writing Terminal சர்வர் துவங்குகிறது...")
    
    # பிரவுசரில் தானாக UI-ஐ ஓபன் செய்ய
    webbrowser.open("http://localhost:8000") 
    
    # FastAPI பேக்கெண்ட் சர்வரை லோக்கலில் ரன் செய்ய
    uvicorn.run(app, host="127.0.0.1", port=8000)

@cli.command()
@click.argument('tamil_text')
def run(tamil_text):
    """டெர்மினலிலேயே நேரடியாக தமிழ் கமாண்ட் ரன் செய்ய (எ.கா: wt run 'கோப்புறையை உருவாக்கு')"""
    # இங்கு உங்கள் AI Model-ஐ அழைத்து கமாண்டாக மாற்றி ரன் செய்ய வேண்டும்
    click.echo(f"Processing: {tamil_text}")

if __name__ == "__main__":
    cli()
