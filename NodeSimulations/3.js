const os = require("os");

console.log(os.userInfo());
console.log(os.uptime());
console.log(os.version());
console.log(os.arch());

const info = {
    nome: os.type(),
    release: os.release(),
    memoria: os.totalmem(),
    disponibile: os.freemem()
}

console.log(info);

const path = require("path");

console.log(path.sep);