const http = require('http');

function handler(req, res) {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'ok' }));
  }
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end(`Hello from ${process.env.APP_VERSION || 'dev'}\n`);
}

if (require.main === module) {
  http.createServer(handler).listen(3000, () => console.log('listening on 3000'));
}

module.exports = { handler };
