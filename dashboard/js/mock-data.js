// Mock data for demo
const mockKassas = [
    {
        id: 1,
        kassa_id: '005',
        pc_name: 'KASSA_005_PC',
        ip_address: '192.168.1.45',
        viloyat: 'Sirdaryo',
        status: 'online',
        last_seen: new Date(Date.now() - 3000),
        uptime: 30840, // seconds
        cpu: 12,
        ram: 52,
        internet: true,
        alerts: 0
    },
    {
        id: 2,
        kassa_id: '012',
        pc_name: 'KASSA_012_PC',
        ip_address: '192.168.1.52',
        viloyat: 'Sirdaryo',
        status: 'idle',
        last_seen: new Date(Date.now() - 900000),
        uptime: 36000,
        cpu: 3,
        ram: 45,
        internet: true,
        alerts: 0
    },
    {
        id: 3,
        kassa_id: '023',
        pc_name: 'KASSA_023_PC',
        ip_address: '192.168.1.63',
        viloyat: 'Sirdaryo',
        status: 'alert',
        last_seen: new Date(Date.now() - 2000),
        uptime: 10800,
        cpu: 45,
        ram: 68,
        internet: true,
        alerts: 1,
        alert_reason: 'Telegram ochildi'
    },
    {
        id: 4,
        kassa_id: '034',
        pc_name: 'KASSA_034_PC',
        ip_address: '192.168.1.74',
        viloyat: 'Toshkent',
        status: 'online',
        last_seen: new Date(Date.now() - 5000),
        uptime: 28800,
        cpu: 8,
        ram: 42,
        internet: true,
        alerts: 0
    },
    {
        id: 5,
        kassa_id: '045',
        pc_name: 'KASSA_045_PC',
        ip_address: '192.168.1.85',
        viloyat: 'Toshkent',
        status: 'offline',
        last_seen: new Date(Date.now() - 86400000),
        uptime: 0,
        cpu: 0,
        ram: 0,
        internet: false,
        alerts: 1,
        alert_reason: 'Offline 1 kun'
    }
];

// Generate more mock data
for (let i = 6; i <= 100; i++) {
    const viloyatlar = ['Sirdaryo', 'Toshkent', 'Samarqand', 'Farg\'ona', 'Buxoro'];
    const statuses = ['online', 'online', 'online', 'idle', 'offline'];
    
    mockKassas.push({
        id: i,
        kassa_id: String(i).padStart(3, '0'),
        pc_name: `KASSA_${String(i).padStart(3, '0')}_PC`,
        ip_address: `192.168.1.${Math.floor(Math.random() * 254) + 1}`,
        viloyat: viloyatlar[Math.floor(Math.random() * viloyatlar.length)],
        status: statuses[Math.floor(Math.random() * statuses.length)],
        last_seen: new Date(Date.now() - Math.random() * 3600000),
        uptime: Math.floor(Math.random() * 86400),
        cpu: Math.floor(Math.random() * 100),
        ram: Math.floor(Math.random() * 100),
        internet: Math.random() > 0.1,
        alerts: Math.random() > 0.8 ? 1 : 0
    });
}