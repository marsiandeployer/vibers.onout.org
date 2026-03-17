module.exports = {
  apps: [{
    name: 'vibers-invite-checker',
    script: '/root/vibers.onout.org/scripts/check-invites.py',
    interpreter: 'python3',
    autorestart: false,
    cron_restart: '*/1 * * * *',
    env: {
      TELEGRAM_SESSION_STRING: process.env.TELEGRAM_SESSION_STRING || '',
      TELEGRAM_API_HASH: process.env.TELEGRAM_API_HASH || '',
      TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID || '-5058393445',
    }
  }, {
    name: 'vibers-feedback',
    script: '/root/vibers.onout.org/scripts/feedback-server.py',
    interpreter: 'python3',
    autorestart: true,
    env: {
      TELEGRAM_SESSION_STRING: process.env.TELEGRAM_SESSION_STRING || '',
      TELEGRAM_API_HASH: process.env.TELEGRAM_API_HASH || '',
      TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID || '-5058393445',
      FEEDBACK_PORT: '3847',
    }
  }]
};
