const fs = require('fs');
const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
files.forEach(f => {
    const html = fs.readFileSync(f, 'utf-8');
    const links = html.match(/<link[^>]*rel=["']stylesheet["'][^>]*>/gi) || [];
    console.log(f + ':');
    links.forEach(l => console.log('  ' + l.trim()));
});
