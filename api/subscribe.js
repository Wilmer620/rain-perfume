const fs = require('fs');

const DATA_FILE = '/tmp/subscribers.json';

function ensure() {
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, '[]', 'utf-8');
}

module.exports = function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, msg: '仅支持 POST' });
  }
  try {
    const { contact, type } = req.body || {};
    if (!contact || !type) {
      return res.status(400).json({ ok: false, msg: '请填写邮箱或手机号' });
    }
    if (type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) {
      return res.status(400).json({ ok: false, msg: '邮箱格式不正确' });
    }
    if (type === 'phone' && !/^[\d\-+() ]{7,18}$/.test(contact)) {
      return res.status(400).json({ ok: false, msg: '手机号格式不正确' });
    }

    ensure();
    const subs = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
    if (subs.find(s => s.contact === contact)) {
      return res.status(200).json({ ok: true, msg: '你已在降雨预报中 ☔' });
    }
    subs.push({ contact, type, subscribedAt: new Date().toISOString() });
    fs.writeFileSync(DATA_FILE, JSON.stringify(subs), 'utf-8');
    return res.status(200).json({ ok: true, msg: '订阅成功！下一场雨来临时，你会第一个知道。' });
  } catch (e) {
    return res.status(500).json({ ok: false, msg: '服务器错误' });
  }
};
