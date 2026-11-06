
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('error_rate');

export const options = {
    stages: [
        { duration: '30s', target: 50 },
        { duration: '1m', target: 150 },
        { duration: '1m', target: 300 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.05'],
    },
};

const BASE_URL = 'http://TiendaGO.somee.com';

export default function () {
    const res = http.get(`${BASE_URL}/api/productos`);
    const ok = check(res, {
        'Respuesta status 200 en productos bajo estres': (r) => r.status === 200,
    });

    if (!ok) {
        errorRate.add(1);
    }

    sleep(0.5);
}
