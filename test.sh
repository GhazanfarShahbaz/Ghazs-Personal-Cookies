#/bin/sh 

PROJECT_DIR=/home/ghaz/flask_gateway/apps/tool_repository/tools/

for FILE in ${PROJECT_DIR}/*
do
    git add ${FILE}
    git commit -m "Updated: Pylint ${FILE}"
    git push origin HEAD
done