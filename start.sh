#!/bin/bash
osascript -e 'tell application "Terminal"
	activate
    do script "cd ~/side/Pactify_API" in selected tab of the front window
    do script "source venv/bin/activate" in selected tab of the front window
    do script "export FLASK_APP=start.py" in selected tab of the front window
    do script "export FLASK_DEBUG=true" in selected tab of the front window
    do script "export PACTIFY_API_CONFIG_SETTINGS='config_app.DevelopmentConfig'" in selected tab of the front window
    do script "export SQLALCHEMY_DATABASE_URI='postgresql:///pactifydb'" in selected tab of the front window
    do script "export DATABASE_URL='postgresql:///pactifydb'" in selected tab of the front window
    do script "flask run" in selected tab of the front window
    
    delay 1
    tell application "System Events"
        keystroke "t" using {command down}
    end tell
    do script "cd ~/side/Pactify_API" in selected tab of the front window
    do script "psql" in selected tab of the front window
    do script "\\c pactifydb" in selected tab of the front window

    delay 1
    tell application "System Events"
        keystroke "t" using {command down}
    end tell
    do script "cd ~/side/Pactify_API" in selected tab of the front window
    do script "git status" in selected tab of the front window
end tell'
