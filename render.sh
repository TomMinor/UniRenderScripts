echo Agent pid 11699;
ssh-add

~/fixRmanCl.sh
export MAYA_RENDER_DESC_PATH=/opt/pixar/RenderManStudio-19.0-maya2014/etc

~/render.py $@
eval SSH_AUTH_SOCK=/tmp/ssh-kVnKV11697/agent.11697; export SSH_AUTH_SOCK;
SSH_AGENT_PID=11699; export SSH_AGENT_PID;
