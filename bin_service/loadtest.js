import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 1000 },
    { duration: '5m', target: 1000 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'],
  },
};

export default function () {
  let res = http.get('http://localhost:8000/bin/860006/');
  check(res, { 'status was 200': (r) => r.status === 200 });
  sleep(1);
}
