import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('error_rate');

export const options = {
    stages: [
        { duration: '30s', target: 20 },
        { duration: '1m30s', target: 50 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<200'],
        http_req_failed: ['rate<0.01'],
        error_rate: ['rate<0.01'],
    },
};

const BASE_URL = 'http://TiendaGO.somee.com';

export default function () {
    const resCat = http.get(`${BASE_URL}/api/categorias`);
    const catOk = check(resCat, {
        'Categorias responde 200': (r) => r.status === 200,
        'Latencia categorias < 200ms': (r) => r.timings.duration < 200,
    });

    if (!catOk) {
        errorRate.add(1);
    }

    const resProd = http.get(`${BASE_URL}/api/productos`);
    const prodOk = check(resProd, {
        'Productos responde 200': (r) => r.status === 200,
        'Latencia productos < 200ms': (r) => r.timings.duration < 200,
    });

    if (!prodOk) {
        errorRate.add(1);
    }

    sleep(1);
}