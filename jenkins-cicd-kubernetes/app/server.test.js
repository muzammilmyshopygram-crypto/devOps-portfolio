const test = require('node:test');
const assert = require('node:assert');
const { handler } = require('./server');

function call(url) {
  return new Promise((resolve) => {
    const res = {
      statusCode: 0, body: '',
      writeHead(code) { this.statusCode = code; },
      end(b) { this.body = b; resolve(this); },
    };
    handler({ url }, res);
  });
}

test('health endpoint returns ok', async () => {
  const r = await call('/health');
  assert.strictEqual(r.statusCode, 200);
  assert.deepStrictEqual(JSON.parse(r.body), { status: 'ok' });
});

test('root returns greeting', async () => {
  const r = await call('/');
  assert.match(r.body, /Hello/);
});
