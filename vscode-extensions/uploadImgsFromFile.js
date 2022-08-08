const path = require('path');

module.exports = async function (filePath, savePath, markdownPath) {
    // Return a picture access link
    const targetPath = path.relative(path.dirname(markdownPath), filePath) + "-test-path";
    console.log(JSON.stringify({filePath, savePath, markdownPath, targetPath}, null, 2));
    return targetPath
}