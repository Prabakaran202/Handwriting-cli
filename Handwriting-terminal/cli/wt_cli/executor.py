# cli/wt_cli/executor.py
import subprocess

def execute_command(command_str):
    # மிக முக்கியமான பாதுகாப்பு செக்
    forbidden = ["rm -rf /", "sudo ", "mkfs"]
    if any(danger in command_str for danger in forbidden):
        return "❌ பிழை: இந்த கமாண்டை இயக்க அனுமதி இல்லை (Security Restriction)!"

    try:
        # கமாண்டை சிஸ்டம் ஷெல்லில் இயக்குகிறோம்
        result = subprocess.run(command_str, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Error:\n{result.stderr}"
            
    except Exception as e:
        return f"An error occurred: {str(e)}"
