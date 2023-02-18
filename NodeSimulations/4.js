const http = require("http"); //prendo modulo http

const server = http.createServer((req,res)=>{ //creo server
    if(req.url === "/"){ //richiedo un certo url
        res.end("Benvenuto"); //risponde questo
    } 
    
    if(req.url === "/pivaz"){
        res.end("Il profilo di Pivaz")
    } 
    
    res.end("Errore, pagina inesistente");
    
})

server.listen(3000); //localhost:3000 su inernet aspetta la mia richiesta