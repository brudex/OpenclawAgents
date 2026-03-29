//Test which model
openclaw agent --agent main -m "Which model are you currently using?"

//restart gateway
openclaw gateway restart


openclaw agents list


openclaw agents list --verbose


openclaw agents set-identity code-reviewer


openclaw agents delete code-reviewer

//If you want to modify an agent's display name or other identity attributes, you can use the set-identity command:
openclaw agents set-identity code-reviewer


openclaw config set agents.ada.model.primary anthropic/claude-3-5-sonnet-latest


openclaw agent --agent ada  -m "Write a python script to get the weather in accra"


//to approve  a device
openclaw devices approve de42d3e3-f5c1-4e24-b128-77845122a8d1


Contabo Nginx Credentials
username:nana password: BOZt1tDF7BuOxM8fchOMFoWz
BOZt1tDF7BuOxM8fchOMFoWz

//Configure web Search
openclaw configure --section web

https://openclawskills.io/


//INstall skill
npx clawhub install gws-workflow
npx clawhub install gws-gmail
npx clawhub install gws-calendar
npx clawhub install swaylq/gws-workspace
gws-meet
gws-gmail-send
gws-tasks
gws-sheets
gws-calendar
gws-drive-upload
gws-docs-write
gws-workspace
gws-forms
gws-gmail-reply
gws-workflow


gws-workspace
swaylq/gws-workspace
recipe-organize-drive-folder
recipe-find-large-files
recipe-save-email-attachments
recipe-email-drive-link
recipe-create-shared-drive