const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3000;
const DATA_DIR = path.join(__dirname, 'data');
const SUBSCRIBERS_FILE = path.join(DATA_DIR, 'subscribers.json');

// Ensure data dir
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
if (!fs.existsSync(SUBSCRIBERS_FILE)) fs.writeFileSync(SUBSCRIBERS_FILE, '[]', 'utf-8');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg':  'image/svg+xml',
  '.webp': 'image/webp',
  '.ico':  'image/x-icon',
};

function serveStatic(req, res) {
  let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
  // Security: no directory traversal
  filePath = path.normalize(filePath);
  if (!filePath.startsWith(__dirname)) { res.writeHead(403); res.end('Forbidden'); return; }

  const ext = path.extname(filePath).toLowerCase();
  const mime = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') { res.writeHead(404); res.end('Not Found'); return; }
      res.writeHead(500); res.end('Server Error');
      return;
    }
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
}

function handleSubscribe(req, res) {
  let body = '';
  req.on('data', chunk => { body += chunk; });
  req.on('end', () => {
    try {
      const { contact, type } = JSON.parse(body);
      if (!contact || !type) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, msg: '请填写邮箱或手机号' }));
        return;
      }
      if (type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, msg: '邮箱格式不正确' }));
        return;
      }
      if (type === 'phone' && !/^[\d\-+() ]{7,18}$/.test(contact)) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, msg: '手机号格式不正确' }));
        return;
      }

      const subs = JSON.parse(fs.readFileSync(SUBSCRIBERS_FILE, 'utf-8'));
      // Dedup
      if (subs.find(s => s.contact === contact)) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, msg: '你已在降雨预报中 ☔' }));
        return;
      }

      subs.push({ contact, type, subscribedAt: new Date().toISOString() });
      fs.writeFileSync(SUBSCRIBERS_FILE, JSON.stringify(subs, null, 2), 'utf-8');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, msg: '订阅成功！下一场雨来临时，你会第一个知道。' }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, msg: '请求格式错误' }));
    }
  });
}

// Admin: serve subscriber data as JSON
function handleAdmin(req, res) {
  const subs = JSON.parse(fs.readFileSync(SUBSCRIBERS_FILE, 'utf-8'));
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(subs));
}

// Admin: login check (simple shared password)
function checkAdminAuth(req) {
  const parsed = url.parse(req.url, true);
  const key = parsed.query.key;
  return key === (process.env.ADMIN_KEY || 'rain2026');
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  if (req.method === 'POST' && parsed.pathname === '/api/subscribe') {
    handleSubscribe(req, res);
  } else if (parsed.pathname === '/api/admin') {
    if (!checkAdminAuth(req)) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Unauthorized. Add ?key=rain2026 to the URL' }));
      return;
    }
    handleAdmin(req, res);
  } else {
    serveStatic(req, res);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  const nets = require('os').networkInterfaces();
  let localIP = 'localhost';
  for (const iface of Object.values(nets)) {
    for (const addr of iface) {
      if (addr.family === 'IPv4' && !addr.internal) {
        localIP = addr.address;
      }
    }
  }
  console.log(`\n🌧️  RAIN · Perfume as Rain 服务器已启动`);
  console.log(`   本机: http://localhost:${PORT}`);
  console.log(`   手机: http://${localIP}:${PORT}`);
  console.log(`   订阅数据: ${SUBSCRIBERS_FILE}\n`);
});
