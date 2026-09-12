const fs = require('fs');
const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
files.forEach(f => {
    const html = fs.readFileSync(f, 'utf-8');
    const scripts = html.match(/<script[^>]*src=["'][^"']*["'][^>]*>/gi) || [];
    console.log(f + ':');
    scripts.forEach(s => console.log('  ' + s));
});
