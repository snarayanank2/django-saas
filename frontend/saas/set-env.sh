#!/bin/sh

TARGET_DIR=$1
echo "Target directory is ${TARGET_DIR}"

mkdir -p ${TARGET_DIR}
(cat <<EOF
(function (window) {
    window.__env = window.__env || {};  
    window.__env.apiBaseUrl = '${API_BASE_URL}';
    window.__env.appBaseUrl = '${APP_BASE_URL}';
    window.__env.enableDebug = '${ENABLE_DEBUG}';
}(this));
EOF
) > ${TARGET_DIR}/env.js
