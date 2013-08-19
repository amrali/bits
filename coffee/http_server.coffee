sys = require 'sys'
http = require 'http'
path = require 'path'
url = require 'url'
filesys = require 'fs'

http.createServer((request, response) ->
    mypath = url.parse(request.url).pathname
    fullpath = path.join process.cwd(), mypath
    filesys.exists(fullpath, (exists) ->
        if !exists
            response.writeHeader 404, {"content-type": "text/plain"}
            response.write "404 Not Found\n"
            response.end()
        else
            filesys.readFile(fullpath, 'binary', (err, file) ->
                if err
                    response.writeHeader 500, {"content-type": "text/plain"}
                    response.write err + "\n"
                    response.end()
                else
                    response.writeHeader 200
                    response.write file, 'binary'
                    response.end()
            )
    )
).listen 8080

sys.puts 'Server running on 8080'
