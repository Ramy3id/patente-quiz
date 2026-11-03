/**
 * Patente B Pro - Robust Static Server
 * Full UTF-8 support for Arabic & Italian, clean URLs, and directory index
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = parseInt(process.argv[2], 10) || 8080;
const ROOT_DIR = path.resolve(__dirname, '..');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
  '.md': 'text/markdown; charset=utf-8'
};

const server = http.createServer((req, res) => {
  let decodedUrl = '';
  try {
    decodedUrl = decodeURIComponent(req.url.split('?')[0]);
  } catch (_) {
    try {
      decodedUrl = decodeURI(req.url.split('?')[0]);
    } catch (__) {
      decodedUrl = req.url.split('?')[0];
    }
  }

  if (decodedUrl === '/' || decodedUrl === '') {
    decodedUrl = '/Capitoli_Divisi/index.html';
  }

  // Remove leading slash for safe join
  let relativePath = decodedUrl.replace(/^[/\\]+/, '');
  let filePath = path.join(ROOT_DIR, relativePath);

  // 1. Check exact file or directory index
  let finalPath = null;
  if (fs.existsSync(filePath)) {
    const stat = fs.statSync(filePath);
    if (stat.isFile()) {
      finalPath = filePath;
    } else if (stat.isDirectory()) {
      const idx = path.join(filePath, 'index.html');
      if (fs.existsSync(idx) && fs.statSync(idx).isFile()) {
        finalPath = idx;
      }
    }
  }

  // 2. Check with .html appended if not found
  if (!finalPath) {
    const withHtml = filePath + '.html';
    if (fs.existsSync(withHtml) && fs.statSync(withHtml).isFile()) {
      finalPath = withHtml;
    }
  }

  // 3. Check within Capitoli_Divisi or interactive_pages (file or directory index)
  if (!finalPath) {
    const inCap = path.join(ROOT_DIR, 'Capitoli_Divisi', relativePath);
    if (fs.existsSync(inCap)) {
      if (fs.statSync(inCap).isFile()) {
        finalPath = inCap;
      } else if (fs.statSync(inCap).isDirectory()) {
        const idx = path.join(inCap, 'index.html');
        if (fs.existsSync(idx) && fs.statSync(idx).isFile()) {
          finalPath = idx;
        }
      }
    }
  }
  if (!finalPath) {
    const inInt = path.join(ROOT_DIR, 'interactive_pages', relativePath);
    if (fs.existsSync(inInt)) {
      if (fs.statSync(inInt).isFile()) {
        finalPath = inInt;
      } else if (fs.statSync(inInt).isDirectory()) {
        const idx = path.join(inInt, 'index.html');
        if (fs.existsSync(idx) && fs.statSync(idx).isFile()) {
          finalPath = idx;
        }
      }
    }
  }

  if (finalPath) {
    const ext = path.extname(finalPath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
      'Pragma': 'no-cache',
      'Expires': '0',
      'Access-Control-Allow-Origin': '*'
    });
    console.log(`[200] ${req.method} ${req.url} -> ${path.relative(ROOT_DIR, finalPath)}`);
    fs.createReadStream(finalPath).pipe(res);
  } else {
    console.warn(`[404] ${req.method} ${req.url}`);
    // Return 404.html if exists
    const notFoundHtml = path.join(ROOT_DIR, '404.html');
    if (fs.existsSync(notFoundHtml)) {
      res.writeHead(404, { 
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
      });
      fs.createReadStream(notFoundHtml).pipe(res);
    } else {
      res.writeHead(404, { 
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
      });
      res.end(`<!DOCTYPE html><html dir="rtl"><body><h2>404 - لم يتم العثور على الصفحة</h2></body></html>`);
    }
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`====================================================`);
  console.log(`🚦 Patente B Pro Server is running on port ${PORT}!`);
  console.log(`📱 Local URL: http://localhost:${PORT}/Capitoli_Divisi/index.html`);
  console.log(`====================================================`);
});
