# Apollo IAM Engine — Event Log

| seq | uid | timestamp | event | actor | resource | resource_id | status | detail |
|-----|-----|-----------|-------|-------|----------|-------------|--------|--------|
| 1 | `6ccced82` | 2026-04-15T23:18:13.373060+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 2 | `6a43954c` | 2026-04-15T23:20:00.807191+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 3 | `b5b412dd` | 2026-04-15T23:23:17.983288+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 4 | `0f40e5c3` | 2026-04-15T23:23:18.560514+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 5 | `1114f9e1` | 2026-04-15T23:23:19.611845+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 6 | `8fb9c11c` | 2026-04-15T23:23:20.241011+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 7 | `fefa2d4f` | 2026-04-15T23:23:25.275338+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 8 | `9e66d4a0` | 2026-04-15T23:23:25.883883+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 9 | `04b59781` | 2026-04-15T23:23:30.725669+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 10 | `8eba7b32` | 2026-04-15T23:23:31.357704+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 11 | `f7c1f52f` | 2026-04-15T23:24:25.978702+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 12 | `5983a470` | 2026-04-15T23:24:28.006839+00:00 | `http.request` | 127.0.0.1 | /redocs | — | failure | {"method": "GET", "path": "/redocs", "query": "", "http_status": 404, "elapsed_m |
| 13 | `4b1a4616` | 2026-04-15T23:25:05.166218+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 14 | `9152724d` | 2026-04-15T23:25:08.889911+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 15 | `b418a34d` | 2026-04-15T23:29:14.329188+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 16 | `4439736f` | 2026-04-15T23:29:29.212102+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 17 | `e89ee14a` | 2026-04-15T23:29:29.225102+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 18 | `2b05ec22` | 2026-04-15T23:29:29.508636+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 19 | `381c2a1d` | 2026-04-15T23:29:29.538637+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 20 | `59c9299d` | 2026-04-15T23:29:29.571636+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 21 | `3ebed671` | 2026-04-15T23:29:29.598638+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 22 | `afd5edd1` | 2026-04-15T23:29:29.676647+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 23 | `f36dd279` | 2026-04-15T23:29:29.759170+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 24 | `3a675881` | 2026-04-15T23:29:29.791174+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 25 | `308c45ea` | 2026-04-15T23:29:29.819167+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 26 | `32d740c8` | 2026-04-15T23:29:29.853172+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 27 | `567b700a` | 2026-04-15T23:29:41.236584+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 28 | `d92ab00f` | 2026-04-15T23:29:45.479946+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 29 | `7141570f` | 2026-04-15T23:29:49.480271+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 30 | `b4a735b2` | 2026-04-15T23:29:53.786115+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 31 | `0a88f7bd` | 2026-04-15T23:29:57.562869+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 32 | `55045f32` | 2026-04-15T23:29:57.580385+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 33 | `edfb4c4e` | 2026-04-15T23:30:01.496149+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 34 | `eeb59b18` | 2026-04-15T23:30:05.479441+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 35 | `1dc6ef0f` | 2026-04-15T23:30:09.194206+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 36 | `288f1819` | 2026-04-15T23:30:13.053060+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 37 | `106b6d6e` | 2026-04-15T23:30:17.215845+00:00 | `settings.read` | admin | settings | — | success | {} |
| 38 | `9f62876d` | 2026-04-15T23:30:17.236846+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 39 | `80f21879` | 2026-04-15T23:30:21.111617+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 40 | `346a7efd` | 2026-04-15T23:30:21.128614+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 41 | `c5798e22` | 2026-04-15T23:30:21.147631+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 42 | `76964d7b` | 2026-04-15T23:30:21.170153+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 43 | `7eb81e93` | 2026-04-15T23:30:21.188153+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 44 | `992df5fd` | 2026-04-15T23:30:21.203152+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 45 | `5515ff4e` | 2026-04-15T23:30:21.221152+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 46 | `d51d33d5` | 2026-04-15T23:30:21.238151+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 47 | `125b9187` | 2026-04-15T23:30:21.255153+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 48 | `00d1d4f8` | 2026-04-15T23:30:35.888076+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 49 | `99d0df4f` | 2026-04-15T23:30:35.908075+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 50 | `61b95cdb` | 2026-04-15T23:30:52.154957+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 51 | `bd41f778` | 2026-04-15T23:30:55.861740+00:00 | `http.request` | 127.0.0.1 | /admin/users/2a33fa92-82a4-4535-8fe2-d07b1af98c1d | — | success | {"method": "GET", "path": "/admin/users/2a33fa92-82a4-4535-8fe2-d07b1af98c1d", " |
| 52 | `5980d8bc` | 2026-04-15T23:30:55.888740+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 53 | `a11d699e` | 2026-04-15T23:30:55.913736+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 54 | `6bfc3e1d` | 2026-04-15T23:30:55.946738+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 55 | `c4f6d6bd` | 2026-04-15T23:30:55.972739+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 56 | `1dfc938b` | 2026-04-15T23:30:56.001742+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 57 | `43a5a86e` | 2026-04-15T23:30:56.026739+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 58 | `efd5aabc` | 2026-04-15T23:30:56.048748+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/user/2a33fa92-82a4-4535-8fe2-d07b1af98c1d | — | success | {"method": "GET", "path": "/admin/custom-entities/user/2a33fa92-82a4-4535-8fe2-d |
| 59 | `5c5c5f34` | 2026-04-15T23:31:23.581409+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 60 | `ed7bf03c` | 2026-04-15T23:31:26.972627+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 61 | `c6c88e2a` | 2026-04-15T23:31:31.344381+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 62 | `8e0e10fc` | 2026-04-15T23:31:35.560111+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 63 | `0d6932db` | 2026-04-15T23:31:35.575111+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 64 | `5cf52826` | 2026-04-15T23:31:37.290730+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 65 | `2761cb1b` | 2026-04-15T23:31:46.022722+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 66 | `99a6f33f` | 2026-04-15T23:31:47.243293+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 67 | `55f33649` | 2026-04-15T23:31:55.060264+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 68 | `a5d73093` | 2026-04-15T23:32:00.330104+00:00 | `settings.read` | admin | settings | — | success | {} |
| 69 | `30a0c7c1` | 2026-04-15T23:32:00.341104+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 70 | `33ee0c14` | 2026-04-15T23:32:03.767808+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 71 | `3ae7cea9` | 2026-04-15T23:32:10.769226+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 72 | `d811c3ef` | 2026-04-15T23:33:12.195787+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 73 | `ac269336` | 2026-04-15T23:34:12.356166+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 74 | `bfeb1d0b` | 2026-04-15T23:34:26.777698+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 75 | `c60f289b` | 2026-04-15T23:34:28.954303+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 76 | `33444d18` | 2026-04-15T23:35:24.837036+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 77 | `024a281f` | 2026-04-15T23:35:25.477053+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 78 | `1c6d164d` | 2026-04-15T23:35:25.663571+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 79 | `56f19384` | 2026-04-15T23:35:26.424105+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 80 | `94aaf9ad` | 2026-04-15T23:36:13.516214+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 81 | `cec8b282` | 2026-04-15T23:36:38.395832+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 82 | `e0c1eabf` | 2026-04-15T23:36:38.838876+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 83 | `3fa31252` | 2026-04-15T23:36:39.974483+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 84 | `95aa9f4a` | 2026-04-15T23:36:40.274008+00:00 | `http.request` | 127.0.0.1 | /.well-known/appspecific/com.chrome.devtools.json | — | failure | {"method": "GET", "path": "/.well-known/appspecific/com.chrome.devtools.json", " |
| 85 | `f03ca1ca` | 2026-04-15T23:36:41.189115+00:00 | `http.request` | 127.0.0.1 | /cfb294d7f6536ffa8d42.worker.js.map | — | failure | {"method": "GET", "path": "/cfb294d7f6536ffa8d42.worker.js.map", "query": "", "h |
| 86 | `dd38b4c8` | 2026-04-15T23:56:35.082845+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 87 | `7d25323f` | 2026-04-15T23:57:00.262049+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 88 | `dbe8e452` | 2026-04-15T23:57:00.272569+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 89 | `afd3f13f` | 2026-04-15T23:57:00.543540+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 90 | `dfd02750` | 2026-04-15T23:57:00.562578+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 91 | `f663caf8` | 2026-04-15T23:57:00.586148+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 92 | `3cc53b71` | 2026-04-15T23:57:00.604180+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 93 | `88f8c87d` | 2026-04-15T23:57:00.626760+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 94 | `9fec5644` | 2026-04-15T23:57:00.647326+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 95 | `f125f2a9` | 2026-04-15T23:57:00.667372+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 96 | `0ae5b194` | 2026-04-15T23:57:00.692416+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 97 | `8c47fb5b` | 2026-04-15T23:57:00.710470+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 98 | `8326b64c` | 2026-04-15T23:57:03.977143+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 99 | `1cf8966b` | 2026-04-15T23:57:10.376741+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 100 | `980ccf86` | 2026-04-15T23:57:16.739269+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 101 | `558d5b41` | 2026-04-15T23:57:17.023849+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/logs | — | success | {"method": "GET", "path": "/admin/metrics/logs", "query": "skip=0&limit=200", "h |
| 102 | `a8dd043a` | 2026-04-15T23:57:34.732694+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 103 | `2b1ae35a` | 2026-04-15T23:57:39.654111+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 104 | `e6675c8e` | 2026-04-15T23:57:40.354721+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 105 | `3333d709` | 2026-04-15T23:57:45.728690+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 106 | `c15c3617` | 2026-04-15T23:57:50.729624+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 107 | `c120745e` | 2026-04-15T23:57:55.730068+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 108 | `45b2588d` | 2026-04-15T23:58:00.732147+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 109 | `1d556ad2` | 2026-04-15T23:58:05.728765+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 110 | `e04359a8` | 2026-04-15T23:58:09.478691+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 111 | `62d6f401` | 2026-04-15T23:58:17.807540+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 112 | `291b10a8` | 2026-04-15T23:58:17.825569+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 113 | `552fcc3f` | 2026-04-15T23:58:17.844620+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 114 | `78dd04ae` | 2026-04-15T23:58:17.863663+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 115 | `3c4e2b81` | 2026-04-15T23:58:17.881702+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 116 | `39c9446b` | 2026-04-15T23:58:17.905272+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 117 | `0b76553b` | 2026-04-15T23:58:17.972945+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 118 | `296687a1` | 2026-04-15T23:58:18.082739+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 119 | `c4772a35` | 2026-04-15T23:58:18.097784+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 120 | `32845ec0` | 2026-04-15T23:58:18.120841+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 121 | `cbbbf585` | 2026-04-15T23:58:19.395993+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 122 | `5c03f50b` | 2026-04-15T23:58:19.415022+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 123 | `2c8fc1a5` | 2026-04-15T23:58:19.438083+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 124 | `8277175e` | 2026-04-15T23:58:19.457121+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 125 | `23d6f06d` | 2026-04-15T23:58:19.475148+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 126 | `cb3c6193` | 2026-04-15T23:58:19.495201+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 127 | `f68c22d2` | 2026-04-15T23:58:19.514239+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 128 | `07a08ecb` | 2026-04-15T23:58:19.537825+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 129 | `346e0cc8` | 2026-04-15T23:58:19.558882+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 130 | `b87ff4f4` | 2026-04-15T23:58:21.476673+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 131 | `59262759` | 2026-04-15T23:58:22.838999+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 132 | `5593efe2` | 2026-04-15T23:58:24.730580+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 133 | `eba18326` | 2026-04-15T23:58:24.752631+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 134 | `d5f33f50` | 2026-04-15T23:58:26.270952+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 135 | `9c4a515d` | 2026-04-15T23:58:33.360259+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 136 | `a7b478a6` | 2026-04-15T23:58:38.653006+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 137 | `1bdd1626` | 2026-04-15T23:58:43.656069+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 138 | `f488a772` | 2026-04-15T23:58:44.149691+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 139 | `d0386a10` | 2026-04-15T23:58:46.185082+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 140 | `7dbb5db0` | 2026-04-15T23:58:48.687154+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 141 | `18526bb5` | 2026-04-15T23:58:52.540897+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 142 | `220a651d` | 2026-04-15T23:58:52.550413+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 143 | `60f222fc` | 2026-04-15T23:58:53.659938+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 144 | `e0a9fa22` | 2026-04-15T23:58:54.582579+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 145 | `34a9169e` | 2026-04-15T23:58:56.858475+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 146 | `db408bc4` | 2026-04-15T23:58:58.017768+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 147 | `f6b41d19` | 2026-04-15T23:58:58.910059+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 148 | `7ef84a9b` | 2026-04-15T23:59:00.958619+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 149 | `6cb9e818` | 2026-04-15T23:59:03.000575+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 150 | `d99c68d0` | 2026-04-15T23:59:03.026139+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 151 | `0b46f824` | 2026-04-15T23:59:05.078039+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 152 | `38d0b69d` | 2026-04-15T23:59:07.114083+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 153 | `8b52e8cf` | 2026-04-15T23:59:08.022377+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 154 | `1ee62bc0` | 2026-04-15T23:59:09.163597+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 155 | `0100d242` | 2026-04-15T23:59:10.713916+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/logs | — | success | {"method": "GET", "path": "/admin/metrics/logs", "query": "skip=0&limit=200", "h |
| 156 | `650a11da` | 2026-04-15T23:59:11.212783+00:00 | `settings.read` | admin | settings | — | success | {} |
| 157 | `ad44b9ea` | 2026-04-15T23:59:11.226843+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 158 | `3955d6c3` | 2026-04-15T23:59:12.989204+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 159 | `3df67bf7` | 2026-04-15T23:59:13.282122+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 160 | `20ca58ce` | 2026-04-15T23:59:15.330616+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 401, "ela |
| 161 | `710a8e53` | 2026-04-15T23:59:17.376387+00:00 | `permission.created` | admin | permissions | 869bd442-440a-42f0-a69a-18b131777836 | success | {"name": "cotacao:create"} |
| 162 | `7a306596` | 2026-04-15T23:59:17.386903+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 163 | `2e6d5feb` | 2026-04-15T23:59:17.997231+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 164 | `1996f327` | 2026-04-15T23:59:19.443903+00:00 | `permission.created` | admin | permissions | 4b81dec0-7dd1-47f2-95cf-4a42ac09dab3 | success | {"name": "cotacao:read"} |
| 165 | `5002f5e8` | 2026-04-15T23:59:19.456436+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 166 | `67cde836` | 2026-04-15T23:59:21.508980+00:00 | `permission.created` | admin | permissions | 2f64a534-f4f5-4b0a-9ea8-eb6a1cfd2ebf | success | {"name": "cotacao:update"} |
| 167 | `1571b3ab` | 2026-04-15T23:59:21.519496+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 168 | `7c15afdf` | 2026-04-15T23:59:23.151272+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 169 | `1105afae` | 2026-04-15T23:59:23.581931+00:00 | `permission.created` | admin | permissions | fd2b3347-cb2d-423c-99dd-4341b17863a3 | success | {"name": "cotacao:delete"} |
| 170 | `84600d24` | 2026-04-15T23:59:23.593958+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 171 | `59127547` | 2026-04-15T23:59:25.644561+00:00 | `permission.created` | admin | permissions | 82ab09af-0e5f-4065-abaf-5d8143e469cd | success | {"name": "cotacao:approve"} |
| 172 | `ec026c03` | 2026-04-15T23:59:25.656087+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 173 | `c782b4b7` | 2026-04-15T23:59:27.698396+00:00 | `role.created` | admin | roles | f6d9269c-b5cb-401d-b6b6-448603b35180 | success | {"name": "vendedor"} |
| 174 | `a4158069` | 2026-04-15T23:59:27.717445+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 175 | `6ba0b69b` | 2026-04-15T23:59:27.998512+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 176 | `ac652803` | 2026-04-15T23:59:29.756085+00:00 | `role.created` | admin | roles | aa5f615b-9006-4919-8e4a-03cd4dd7f788 | success | {"name": "aprovador"} |
| 177 | `23118991` | 2026-04-15T23:59:29.766600+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 178 | `95612f57` | 2026-04-15T23:59:31.809771+00:00 | `role.created` | admin | roles | b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | success | {"name": "gerente"} |
| 179 | `bf315390` | 2026-04-15T23:59:31.821290+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 180 | `30dae1bc` | 2026-04-15T23:59:33.671076+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 181 | `ce48c826` | 2026-04-15T23:59:33.875368+00:00 | `permission.assigned_to_role` | admin | permissions | 869bd442-440a-42f0-a69a-18b131777836 | success | {"role_id": "f6d9269c-b5cb-401d-b6b6-448603b35180"} |
| 182 | `fa065749` | 2026-04-15T23:59:33.887407+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/869bd442-440a-42f0-a69a-18b131777836/assign-role/f6d9269c-b5cb-401d-b6b6-448603b35180 | — | success | {"method": "POST", "path": "/admin/permissions/869bd442-440a-42f0-a69a-18b131777 |
| 183 | `9eef3c2a` | 2026-04-15T23:59:35.954740+00:00 | `permission.assigned_to_role` | admin | permissions | 4b81dec0-7dd1-47f2-95cf-4a42ac09dab3 | success | {"role_id": "aa5f615b-9006-4919-8e4a-03cd4dd7f788"} |
| 184 | `04009e41` | 2026-04-15T23:59:35.967262+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/4b81dec0-7dd1-47f2-95cf-4a42ac09dab3/assign-role/aa5f615b-9006-4919-8e4a-03cd4dd7f788 | — | success | {"method": "POST", "path": "/admin/permissions/4b81dec0-7dd1-47f2-95cf-4a42ac09d |
| 185 | `886c39b4` | 2026-04-15T23:59:38.036632+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 186 | `5fab4361` | 2026-04-15T23:59:38.060177+00:00 | `permission.assigned_to_role` | admin | permissions | 82ab09af-0e5f-4065-abaf-5d8143e469cd | success | {"role_id": "aa5f615b-9006-4919-8e4a-03cd4dd7f788"} |
| 187 | `38a03b79` | 2026-04-15T23:59:38.077228+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/82ab09af-0e5f-4065-abaf-5d8143e469cd/assign-role/aa5f615b-9006-4919-8e4a-03cd4dd7f788 | — | success | {"method": "POST", "path": "/admin/permissions/82ab09af-0e5f-4065-abaf-5d8143e46 |
| 188 | `57135b4e` | 2026-04-15T23:59:40.128373+00:00 | `permission.assigned_to_role` | admin | permissions | 869bd442-440a-42f0-a69a-18b131777836 | success | {"role_id": "b1c73493-0d09-4fba-95df-d3d2b0bc5f78"} |
| 189 | `4dcb9965` | 2026-04-15T23:59:40.141887+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/869bd442-440a-42f0-a69a-18b131777836/assign-role/b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | — | success | {"method": "POST", "path": "/admin/permissions/869bd442-440a-42f0-a69a-18b131777 |
| 190 | `ca48669d` | 2026-04-15T23:59:42.191549+00:00 | `permission.assigned_to_role` | admin | permissions | 4b81dec0-7dd1-47f2-95cf-4a42ac09dab3 | success | {"role_id": "b1c73493-0d09-4fba-95df-d3d2b0bc5f78"} |
| 191 | `cd79bed9` | 2026-04-15T23:59:42.204083+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/4b81dec0-7dd1-47f2-95cf-4a42ac09dab3/assign-role/b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | — | success | {"method": "POST", "path": "/admin/permissions/4b81dec0-7dd1-47f2-95cf-4a42ac09d |
| 192 | `9f1f5c8c` | 2026-04-15T23:59:43.004185+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 193 | `16e8c33b` | 2026-04-15T23:59:44.259089+00:00 | `permission.assigned_to_role` | admin | permissions | 2f64a534-f4f5-4b0a-9ea8-eb6a1cfd2ebf | success | {"role_id": "b1c73493-0d09-4fba-95df-d3d2b0bc5f78"} |
| 194 | `4c0b279b` | 2026-04-15T23:59:44.270606+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/2f64a534-f4f5-4b0a-9ea8-eb6a1cfd2ebf/assign-role/b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | — | success | {"method": "POST", "path": "/admin/permissions/2f64a534-f4f5-4b0a-9ea8-eb6a1cfd2 |
| 195 | `c081834c` | 2026-04-15T23:59:46.324522+00:00 | `permission.assigned_to_role` | admin | permissions | fd2b3347-cb2d-423c-99dd-4341b17863a3 | success | {"role_id": "b1c73493-0d09-4fba-95df-d3d2b0bc5f78"} |
| 196 | `f2e815bf` | 2026-04-15T23:59:46.334043+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/fd2b3347-cb2d-423c-99dd-4341b17863a3/assign-role/b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | — | success | {"method": "POST", "path": "/admin/permissions/fd2b3347-cb2d-423c-99dd-4341b1786 |
| 197 | `50377ce5` | 2026-04-15T23:59:47.540530+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 198 | `5af10917` | 2026-04-15T23:59:47.564596+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 199 | `b432e13d` | 2026-04-15T23:59:47.589645+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 200 | `5baa124b` | 2026-04-15T23:59:47.612189+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 201 | `e686eb37` | 2026-04-15T23:59:47.637759+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 202 | `aff8c3e5` | 2026-04-15T23:59:47.657797+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 203 | `674b3767` | 2026-04-15T23:59:47.677836+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 204 | `015e8a00` | 2026-04-15T23:59:47.696880+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 205 | `ec7ddbd1` | 2026-04-15T23:59:47.724941+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 206 | `a7e89e49` | 2026-04-15T23:59:48.417210+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 207 | `cea2d0e3` | 2026-04-15T23:59:48.437240+00:00 | `permission.assigned_to_role` | admin | permissions | 82ab09af-0e5f-4065-abaf-5d8143e469cd | success | {"role_id": "b1c73493-0d09-4fba-95df-d3d2b0bc5f78"} |
| 208 | `66ce6be1` | 2026-04-15T23:59:48.449757+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/82ab09af-0e5f-4065-abaf-5d8143e469cd/assign-role/b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | — | success | {"method": "POST", "path": "/admin/permissions/82ab09af-0e5f-4065-abaf-5d8143e46 |
| 209 | `299aa3a3` | 2026-04-15T23:59:50.497761+00:00 | `group.created` | admin | groups | f08f9722-b0bb-45ca-ae9a-968be73a0bea | success | {"name": "Vendas"} |
| 210 | `6d423187` | 2026-04-15T23:59:50.510275+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "POST", "path": "/admin/groups/", "query": "", "http_status": 201, "e |
| 211 | `59bf32d2` | 2026-04-15T23:59:52.528202+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 212 | `05d8e141` | 2026-04-15T23:59:52.597407+00:00 | `rbac.attribute_created` | admin | rbac_attributes | 351c4789-b68e-4224-8c04-45c979eae08b | success | {"key": "sistema"} |
| 213 | `78fab711` | 2026-04-15T23:59:52.611934+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "POST", "path": "/admin/rbac/", "query": "", "http_status": 201, "ela |
| 214 | `20cbf4b4` | 2026-04-15T23:59:54.859672+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=500", "http_st |
| 215 | `ff3352ea` | 2026-04-15T23:59:54.944918+00:00 | `user.created` | admin | users | 2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | success | {"username": "usuario1"} |
| 216 | `738dfdbc` | 2026-04-15T23:59:54.960445+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 217 | `ba01c136` | 2026-04-15T23:59:57.026709+00:00 | `role.assigned_to_user` | admin | roles | f6d9269c-b5cb-401d-b6b6-448603b35180 | success | {"user_id": "2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f"} |
| 218 | `a40502dc` | 2026-04-15T23:59:57.042231+00:00 | `http.request` | 127.0.0.1 | /admin/roles/f6d9269c-b5cb-401d-b6b6-448603b35180/assign-user/2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | — | success | {"method": "POST", "path": "/admin/roles/f6d9269c-b5cb-401d-b6b6-448603b35180/as |
| 219 | `2f9f233e` | 2026-04-15T23:59:57.812057+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=200", "http_st |
| 220 | `c7587a33` | 2026-04-15T23:59:59.090741+00:00 | `group.user_assigned` | admin | groups | f08f9722-b0bb-45ca-ae9a-968be73a0bea | success | {"user_id": "2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f"} |
| 221 | `2291edba` | 2026-04-15T23:59:59.102260+00:00 | `http.request` | 127.0.0.1 | /admin/groups/f08f9722-b0bb-45ca-ae9a-968be73a0bea/assign-user/2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | — | success | {"method": "POST", "path": "/admin/groups/f08f9722-b0bb-45ca-ae9a-968be73a0bea/a |
| 222 | `2c116b13` | 2026-04-16T00:00:01.155109+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | 2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | success | {"key": "sistema", "value": "cotacao"} |
| 223 | `bc825d48` | 2026-04-16T00:00:01.167123+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | — | success | {"method": "POST", "path": "/admin/rbac/assign/2abb2f50-c3e5-4a5c-b74d-e8c1bda18 |
| 224 | `bab742ec` | 2026-04-16T00:00:05.690730+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 225 | `85807ac8` | 2026-04-16T00:00:07.738250+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 226 | `c3f806b8` | 2026-04-16T00:00:09.782695+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | failure | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 401, "e |
| 227 | `75f46518` | 2026-04-16T00:00:11.822655+00:00 | `settings.read` | admin | settings | — | success | {} |
| 228 | `2024b706` | 2026-04-16T00:00:11.833683+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 229 | `2b76c649` | 2026-04-16T00:00:13.880911+00:00 | `settings.updated` | admin | settings | — | success | {"fields": {"access_token_expire_minutes": 90, "refresh_token_expire_days": 7, " |
| 230 | `8d438c95` | 2026-04-16T00:00:13.892429+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "PUT", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 231 | `29d083c4` | 2026-04-16T00:00:15.179999+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 232 | `7e443c12` | 2026-04-16T00:00:15.655403+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 233 | `fb817552` | 2026-04-16T00:00:15.937488+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 234 | `d8536485` | 2026-04-16T00:00:18.012180+00:00 | `entity.type_created` | admin | custom_entities | 67693ef2-8767-4788-a1ab-f185165fdbf6 | success | {"slug": "cargo"} |
| 235 | `c1d5d57e` | 2026-04-16T00:00:18.025207+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "POST", "path": "/admin/custom-entities/types", "query": "", "http_st |
| 236 | `fafee43e` | 2026-04-16T00:00:20.080340+00:00 | `entity.value_created` | admin | custom_entities | 185a71c3-c92e-45a4-adb1-0d7a11a5c496 | success | {"slug": "cargo", "name": "gerente"} |
| 237 | `73ea83fa` | 2026-04-16T00:00:20.093861+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 238 | `d67190fe` | 2026-04-16T00:00:22.144535+00:00 | `entity.value_created` | admin | custom_entities | e0ca7bd0-049c-4bc6-a4b1-9d139a393228 | success | {"slug": "cargo", "name": "vendedor"} |
| 239 | `2c1d33bc` | 2026-04-16T00:00:22.156064+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 240 | `63b86fa6` | 2026-04-16T00:00:24.431866+00:00 | `user.created` | admin | users | cbcb3603-9d12-47a4-bbdb-467e7bc04acb | success | {"username": "gerente1"} |
| 241 | `dd106ea3` | 2026-04-16T00:00:24.443887+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 242 | `63ac740e` | 2026-04-16T00:00:26.487113+00:00 | `role.assigned_to_user` | admin | roles | b1c73493-0d09-4fba-95df-d3d2b0bc5f78 | success | {"user_id": "cbcb3603-9d12-47a4-bbdb-467e7bc04acb"} |
| 243 | `7aca5824` | 2026-04-16T00:00:26.498623+00:00 | `http.request` | 127.0.0.1 | /admin/roles/b1c73493-0d09-4fba-95df-d3d2b0bc5f78/assign-user/cbcb3603-9d12-47a4-bbdb-467e7bc04acb | — | success | {"method": "POST", "path": "/admin/roles/b1c73493-0d09-4fba-95df-d3d2b0bc5f78/as |
| 244 | `e08f54d6` | 2026-04-16T00:00:28.552780+00:00 | `group.user_assigned` | admin | groups | f08f9722-b0bb-45ca-ae9a-968be73a0bea | success | {"user_id": "cbcb3603-9d12-47a4-bbdb-467e7bc04acb"} |
| 245 | `459350d7` | 2026-04-16T00:00:28.563801+00:00 | `http.request` | 127.0.0.1 | /admin/groups/f08f9722-b0bb-45ca-ae9a-968be73a0bea/assign-user/cbcb3603-9d12-47a4-bbdb-467e7bc04acb | — | success | {"method": "POST", "path": "/admin/groups/f08f9722-b0bb-45ca-ae9a-968be73a0bea/a |
| 246 | `c610ace9` | 2026-04-16T00:00:30.605318+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | cbcb3603-9d12-47a4-bbdb-467e7bc04acb | success | {"key": "sistema", "value": "cotacao"} |
| 247 | `8c7868e0` | 2026-04-16T00:00:30.617844+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/cbcb3603-9d12-47a4-bbdb-467e7bc04acb | — | success | {"method": "POST", "path": "/admin/rbac/assign/cbcb3603-9d12-47a4-bbdb-467e7bc04 |
| 248 | `ceb849ae` | 2026-04-16T00:00:32.677280+00:00 | `entity.assigned_to_user` | admin | custom_entities | cbcb3603-9d12-47a4-bbdb-467e7bc04acb | success | {"slug": "cargo", "value": "gerente"} |
| 249 | `b4ad718e` | 2026-04-16T00:00:32.688791+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/cbcb3603-9d12-47a4-bbdb-467e7bc04acb | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/cbcb3603-9d12-47a4-bbd |
| 250 | `73c8200d` | 2026-04-16T00:00:34.966138+00:00 | `user.created` | admin | users | a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | success | {"username": "aprovador1"} |
| 251 | `5374cdef` | 2026-04-16T00:00:34.980160+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 252 | `5db23124` | 2026-04-16T00:00:37.032307+00:00 | `role.assigned_to_user` | admin | roles | aa5f615b-9006-4919-8e4a-03cd4dd7f788 | success | {"user_id": "a3e75d18-985a-4cc1-9937-dc2eae8b68c4"} |
| 253 | `35078f7d` | 2026-04-16T00:00:37.044329+00:00 | `http.request` | 127.0.0.1 | /admin/roles/aa5f615b-9006-4919-8e4a-03cd4dd7f788/assign-user/a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | — | success | {"method": "POST", "path": "/admin/roles/aa5f615b-9006-4919-8e4a-03cd4dd7f788/as |
| 254 | `a15570fd` | 2026-04-16T00:00:39.098490+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | success | {"key": "sistema", "value": "cotacao"} |
| 255 | `2374abda` | 2026-04-16T00:00:39.110005+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | — | success | {"method": "POST", "path": "/admin/rbac/assign/a3e75d18-985a-4cc1-9937-dc2eae8b6 |
| 256 | `31e7ec20` | 2026-04-16T00:00:41.151531+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 257 | `e230cebd` | 2026-04-16T00:00:43.205949+00:00 | `entity.assigned_to_user` | admin | custom_entities | 2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | success | {"slug": "cargo", "value": "vendedor"} |
| 258 | `63afbd19` | 2026-04-16T00:00:43.218463+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/2abb2f50-c3e5-4a5c-b74d-e8c1bda18d9f | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/2abb2f50-c3e5-4a5c-b74 |
| 259 | `af11a455` | 2026-04-16T00:00:44.054127+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 260 | `e547aefb` | 2026-04-16T00:00:46.945141+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 261 | `d9c78999` | 2026-04-16T00:00:53.168449+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 262 | `504695dc` | 2026-04-16T00:00:53.354984+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 263 | `e73331fa` | 2026-04-16T00:00:55.592884+00:00 | `http.request` | 127.0.0.1 | /admin/users/a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | — | success | {"method": "GET", "path": "/admin/users/a3e75d18-985a-4cc1-9937-dc2eae8b68c4", " |
| 264 | `b9c0234e` | 2026-04-16T00:00:55.612921+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 265 | `8df426c1` | 2026-04-16T00:00:55.630973+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 266 | `c457acff` | 2026-04-16T00:00:55.648008+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 267 | `61eb524c` | 2026-04-16T00:00:55.666038+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 268 | `d52b139d` | 2026-04-16T00:00:55.685063+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 269 | `7380deb3` | 2026-04-16T00:00:55.705614+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 270 | `aefdd979` | 2026-04-16T00:00:55.728161+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/user/a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | — | success | {"method": "GET", "path": "/admin/custom-entities/user/a3e75d18-985a-4cc1-9937-d |
| 271 | `39bf9df5` | 2026-04-16T00:01:04.289509+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 272 | `0ca49fe8` | 2026-04-16T00:01:05.312409+00:00 | `user.status_toggled` | admin | users | a3e75d18-985a-4cc1-9937-dc2eae8b68c4 | success | {"is_active": false} |
| 273 | `554ebac3` | 2026-04-16T00:01:05.324948+00:00 | `http.request` | 127.0.0.1 | /admin/users/a3e75d18-985a-4cc1-9937-dc2eae8b68c4/toggle-status | — | success | {"method": "POST", "path": "/admin/users/a3e75d18-985a-4cc1-9937-dc2eae8b68c4/to |
| 274 | `8a59b199` | 2026-04-16T00:01:05.609873+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 275 | `16546470` | 2026-04-16T00:01:08.421018+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 276 | `5d6bc25f` | 2026-04-16T00:01:08.442055+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 277 | `72461dda` | 2026-04-16T00:01:08.461100+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 278 | `f066c0ba` | 2026-04-16T00:01:08.487658+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 279 | `0b18f2b9` | 2026-04-16T00:01:11.709990+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 280 | `cf22b91d` | 2026-04-16T00:01:20.661330+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 281 | `194a1cc9` | 2026-04-16T00:01:31.282512+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 282 | `41d28d24` | 2026-04-16T00:01:40.648688+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 283 | `27edb980` | 2026-04-16T00:01:51.280042+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 284 | `6c6a9748` | 2026-04-16T00:02:00.674130+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 285 | `ce63c2f7` | 2026-04-16T00:02:11.291607+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/ | — | success | {"method": "GET", "path": "/admin/metrics/", "query": "", "http_status": 200, "e |
| 286 | `f8940ae8` | 2026-04-16T00:14:17.703934+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 287 | `37d0b2fb` | 2026-04-16T00:14:44.129931+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 288 | `2a21cfca` | 2026-04-16T00:14:46.168298+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 289 | `af409433` | 2026-04-16T00:14:52.508192+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 290 | `1a5c2b29` | 2026-04-16T00:14:52.518712+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 291 | `398ead80` | 2026-04-16T00:14:54.569033+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 292 | `58d8453a` | 2026-04-16T00:14:56.850688+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 293 | `b4fcfb69` | 2026-04-16T00:14:58.898613+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 294 | `0b1775c3` | 2026-04-16T00:15:00.948190+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 295 | `df2c46cd` | 2026-04-16T00:15:02.996869+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 296 | `a988b732` | 2026-04-16T00:15:05.044533+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 297 | `d1878cf5` | 2026-04-16T00:15:07.094984+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 298 | `e95a0d4a` | 2026-04-16T00:15:09.145611+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 299 | `11078acd` | 2026-04-16T00:15:11.193335+00:00 | `settings.read` | admin | settings | — | success | {} |
| 300 | `38ab7354` | 2026-04-16T00:15:11.212875+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 301 | `a1252773` | 2026-04-16T00:15:13.267269+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 302 | `de01bf7e` | 2026-04-16T00:15:14.016458+00:00 | `http.request` | 127.0.0.1 | /admin | — | failure | {"method": "GET", "path": "/admin", "query": "", "http_status": 404, "elapsed_ms |
| 303 | `55d71a99` | 2026-04-16T00:15:15.311820+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 401, "ela |
| 304 | `cd3eebc4` | 2026-04-16T00:15:17.356007+00:00 | `permission.created` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"name": "cotacao:create"} |
| 305 | `3986e741` | 2026-04-16T00:15:17.368531+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 306 | `957878af` | 2026-04-16T00:15:19.424305+00:00 | `permission.created` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"name": "cotacao:read"} |
| 307 | `74128984` | 2026-04-16T00:15:19.435818+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 308 | `159911f5` | 2026-04-16T00:15:21.488986+00:00 | `permission.created` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"name": "cotacao:update"} |
| 309 | `00f10286` | 2026-04-16T00:15:21.503030+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 310 | `f9e34758` | 2026-04-16T00:15:23.554165+00:00 | `permission.created` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"name": "cotacao:delete"} |
| 311 | `f9cbcfc4` | 2026-04-16T00:15:23.568690+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 312 | `2f49cd39` | 2026-04-16T00:15:25.616695+00:00 | `permission.created` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"name": "cotacao:approve"} |
| 313 | `8db8c1ff` | 2026-04-16T00:15:25.631216+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 314 | `23f18b9f` | 2026-04-16T00:15:26.296297+00:00 | `http.request` | 127.0.0.1 | /admin | — | failure | {"method": "GET", "path": "/admin", "query": "", "http_status": 404, "elapsed_ms |
| 315 | `4de57c5c` | 2026-04-16T00:15:27.711562+00:00 | `role.created` | admin | roles | 788eb76d-ef55-48a7-8b1f-91c91cf3e362 | success | {"name": "vendedor"} |
| 316 | `02f8538f` | 2026-04-16T00:15:27.765228+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 317 | `a135bf88` | 2026-04-16T00:15:29.845324+00:00 | `role.created` | admin | roles | c111b914-7374-4178-8d1f-75eba14a1004 | success | {"name": "aprovador"} |
| 318 | `6a7e80a0` | 2026-04-16T00:15:29.864378+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 319 | `d34c6a35` | 2026-04-16T00:15:31.933008+00:00 | `role.created` | admin | roles | 73a8bc4f-adfc-4125-8b11-3bec07209ff0 | success | {"name": "gerente"} |
| 320 | `90a04c76` | 2026-04-16T00:15:31.943038+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 321 | `11b1a86d` | 2026-04-16T00:15:34.002224+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "788eb76d-ef55-48a7-8b1f-91c91cf3e362"} |
| 322 | `9ee7a949` | 2026-04-16T00:15:34.012744+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/788eb76d-ef55-48a7-8b1f-91c91cf3e362 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 323 | `cb000185` | 2026-04-16T00:15:36.081953+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 324 | `5589e134` | 2026-04-16T00:15:36.100998+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 325 | `0f37fb8f` | 2026-04-16T00:15:38.151351+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 326 | `09a76c72` | 2026-04-16T00:15:38.161868+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 327 | `5128b187` | 2026-04-16T00:15:40.217011+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 328 | `bb8e5b4e` | 2026-04-16T00:15:40.228534+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 329 | `560b6821` | 2026-04-16T00:15:42.282931+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 330 | `f39e740d` | 2026-04-16T00:15:42.292445+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 331 | `4620b980` | 2026-04-16T00:15:44.067718+00:00 | `http.request` | 127.0.0.1 | /admin | — | failure | {"method": "GET", "path": "/admin", "query": "", "http_status": 404, "elapsed_ms |
| 332 | `edda4339` | 2026-04-16T00:15:44.354388+00:00 | `permission.assigned_to_role` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 333 | `d2870910` | 2026-04-16T00:15:44.365418+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9ea6c/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9e |
| 334 | `65ba9d45` | 2026-04-16T00:15:46.416866+00:00 | `permission.assigned_to_role` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 335 | `10be02fc` | 2026-04-16T00:15:46.429888+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44222/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44 |
| 336 | `1e3960bb` | 2026-04-16T00:15:48.485326+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 337 | `f48baf7b` | 2026-04-16T00:15:48.498846+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 338 | `161cecb7` | 2026-04-16T00:15:50.564329+00:00 | `group.created` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"name": "Vendas"} |
| 339 | `f1650a3c` | 2026-04-16T00:15:50.596430+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "POST", "path": "/admin/groups/", "query": "", "http_status": 201, "e |
| 340 | `6ea06e5e` | 2026-04-16T00:15:52.648518+00:00 | `rbac.attribute_created` | admin | rbac_attributes | 29c0a137-413c-4099-ba20-26e65d6e115e | success | {"key": "sistema"} |
| 341 | `23ff8cba` | 2026-04-16T00:15:52.660539+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "POST", "path": "/admin/rbac/", "query": "", "http_status": 201, "ela |
| 342 | `549c5590` | 2026-04-16T00:17:38.699221+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 343 | `40a04275` | 2026-04-16T00:17:39.580233+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 344 | `4dbdf075` | 2026-04-16T00:17:39.605280+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 345 | `0e685f27` | 2026-04-16T00:17:39.628350+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 346 | `5077ff2a` | 2026-04-16T00:17:39.648406+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 347 | `0ec7cc81` | 2026-04-16T00:17:39.679017+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 348 | `5b6b8aaf` | 2026-04-16T00:17:39.708586+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 20 |
| 349 | `59c71808` | 2026-04-16T00:17:39.731156+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | success | {"method": "GET", "path": "/admin/user-types/", "query": "", "http_status": 200, |
| 350 | `24781cec` | 2026-04-16T00:17:39.760249+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | success | {"method": "GET", "path": "/admin/user-levels/", "query": "", "http_status": 200 |
| 351 | `b1341385` | 2026-04-16T00:17:39.784303+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "GET", "path": "/admin/custom-entities/types", "query": "", "http_sta |
| 352 | `6cbf3a0b` | 2026-04-16T00:17:42.843931+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/logs | — | success | {"method": "GET", "path": "/admin/metrics/logs", "query": "skip=0&limit=200", "h |
| 353 | `11fe3b4d` | 2026-04-16T00:17:43.421266+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "skip=0&limit=100", "http_st |
| 354 | `3ab07c19` | 2026-04-16T00:18:09.151610+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 355 | `95ba7cfe` | 2026-04-16T00:18:11.238620+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 356 | `ddba85d3` | 2026-04-16T00:18:17.604158+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 357 | `ded21cd8` | 2026-04-16T00:18:17.614671+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 358 | `e5042019` | 2026-04-16T00:18:19.654143+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 359 | `9be77b51` | 2026-04-16T00:18:22.114451+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 360 | `fd79675d` | 2026-04-16T00:18:24.161032+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 361 | `ec2b9f23` | 2026-04-16T00:18:26.204015+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 362 | `4fdf3533` | 2026-04-16T00:18:28.276897+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 363 | `b026f474` | 2026-04-16T00:18:30.337460+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 364 | `1b154200` | 2026-04-16T00:18:32.402044+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 365 | `dc0b2128` | 2026-04-16T00:18:34.457167+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 366 | `d3e26172` | 2026-04-16T00:18:35.432992+00:00 | `http.request` | 127.0.0.1 | /admin/metrics/logs | — | success | {"method": "GET", "path": "/admin/metrics/logs", "query": "skip=0&limit=200", "h |
| 367 | `ebb39081` | 2026-04-16T00:18:36.500673+00:00 | `settings.read` | admin | settings | — | success | {} |
| 368 | `9c88ec81` | 2026-04-16T00:18:36.516204+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 369 | `595d10e5` | 2026-04-16T00:18:38.572275+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 370 | `556ce1ea` | 2026-04-16T00:18:40.616962+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 401, "ela |
| 371 | `086986a5` | 2026-04-16T00:18:42.671092+00:00 | `permission.created` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"name": "cotacao:create"} |
| 372 | `96f913c5` | 2026-04-16T00:18:42.683614+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 373 | `08ab4e0a` | 2026-04-16T00:18:44.720761+00:00 | `permission.created` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"name": "cotacao:read"} |
| 374 | `cae6f52a` | 2026-04-16T00:18:44.732285+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 375 | `214247ae` | 2026-04-16T00:18:46.773674+00:00 | `permission.created` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"name": "cotacao:update"} |
| 376 | `541e1c3b` | 2026-04-16T00:18:46.785185+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 377 | `5fd0b588` | 2026-04-16T00:18:48.842984+00:00 | `permission.created` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"name": "cotacao:delete"} |
| 378 | `60e237c9` | 2026-04-16T00:18:48.858497+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 379 | `396a1e59` | 2026-04-16T00:18:50.919900+00:00 | `permission.created` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"name": "cotacao:approve"} |
| 380 | `ac33eece` | 2026-04-16T00:18:50.935952+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 381 | `f0e63b8f` | 2026-04-16T00:18:52.991130+00:00 | `role.created` | admin | roles | 788eb76d-ef55-48a7-8b1f-91c91cf3e362 | success | {"name": "vendedor"} |
| 382 | `501928d1` | 2026-04-16T00:18:53.003656+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 383 | `648d8c58` | 2026-04-16T00:18:55.059113+00:00 | `role.created` | admin | roles | c111b914-7374-4178-8d1f-75eba14a1004 | success | {"name": "aprovador"} |
| 384 | `15aef8f3` | 2026-04-16T00:18:55.113784+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 385 | `7f26a0b2` | 2026-04-16T00:18:57.186569+00:00 | `role.created` | admin | roles | 73a8bc4f-adfc-4125-8b11-3bec07209ff0 | success | {"name": "gerente"} |
| 386 | `f2d1221d` | 2026-04-16T00:18:57.201120+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 387 | `5514bcb3` | 2026-04-16T00:18:59.251427+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "788eb76d-ef55-48a7-8b1f-91c91cf3e362"} |
| 388 | `0435b7a7` | 2026-04-16T00:18:59.267953+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/788eb76d-ef55-48a7-8b1f-91c91cf3e362 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 389 | `41434ebf` | 2026-04-16T00:19:01.312559+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 390 | `40ebfde1` | 2026-04-16T00:19:01.326080+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 391 | `39866323` | 2026-04-16T00:19:03.378704+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 392 | `bddf747a` | 2026-04-16T00:19:03.393742+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 393 | `e434fd8a` | 2026-04-16T00:19:05.429735+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 394 | `d2ee21ec` | 2026-04-16T00:19:05.441258+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 395 | `f70a4b4e` | 2026-04-16T00:19:07.491988+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 396 | `3d94d5d2` | 2026-04-16T00:19:07.508022+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 397 | `f2a3b340` | 2026-04-16T00:19:09.555695+00:00 | `permission.assigned_to_role` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 398 | `5cb99ab5` | 2026-04-16T00:19:09.567207+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9ea6c/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9e |
| 399 | `f967146c` | 2026-04-16T00:19:11.605072+00:00 | `permission.assigned_to_role` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 400 | `1256936b` | 2026-04-16T00:19:11.620589+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44222/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44 |
| 401 | `6f72f0d3` | 2026-04-16T00:19:13.674394+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 402 | `de2892ac` | 2026-04-16T00:19:13.685909+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 403 | `6217e97f` | 2026-04-16T00:19:15.742865+00:00 | `group.created` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"name": "Vendas"} |
| 404 | `f7654707` | 2026-04-16T00:19:15.757383+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "POST", "path": "/admin/groups/", "query": "", "http_status": 201, "e |
| 405 | `d6778344` | 2026-04-16T00:19:17.808812+00:00 | `rbac.attribute_created` | admin | rbac_attributes | 29c0a137-413c-4099-ba20-26e65d6e115e | success | {"key": "sistema"} |
| 406 | `25557eaa` | 2026-04-16T00:19:17.821849+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "POST", "path": "/admin/rbac/", "query": "", "http_status": 201, "ela |
| 407 | `51d914ac` | 2026-04-16T00:19:20.107096+00:00 | `user.created` | admin | users | bfebd61e-8858-4201-bc40-b97a6afbe9eb | success | {"username": "usuario1"} |
| 408 | `1394f78a` | 2026-04-16T00:19:20.118608+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 409 | `dfe4a28f` | 2026-04-16T00:19:22.170092+00:00 | `role.assigned_to_user` | admin | roles | 788eb76d-ef55-48a7-8b1f-91c91cf3e362 | success | {"user_id": "bfebd61e-8858-4201-bc40-b97a6afbe9eb"} |
| 410 | `06d0bae9` | 2026-04-16T00:19:22.181120+00:00 | `http.request` | 127.0.0.1 | /admin/roles/788eb76d-ef55-48a7-8b1f-91c91cf3e362/assign-user/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/roles/788eb76d-ef55-48a7-8b1f-91c91cf3e362/as |
| 411 | `da97326c` | 2026-04-16T00:19:24.231571+00:00 | `group.user_assigned` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"user_id": "bfebd61e-8858-4201-bc40-b97a6afbe9eb"} |
| 412 | `f0139203` | 2026-04-16T00:19:24.243601+00:00 | `http.request` | 127.0.0.1 | /admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/assign-user/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/a |
| 413 | `a9aa3802` | 2026-04-16T00:19:26.309771+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | bfebd61e-8858-4201-bc40-b97a6afbe9eb | success | {"key": "sistema", "value": "cotacao"} |
| 414 | `e8703d34` | 2026-04-16T00:19:26.323305+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/rbac/assign/bfebd61e-8858-4201-bc40-b97a6afbe |
| 415 | `ce4ee3cc` | 2026-04-16T00:19:30.867236+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 416 | `e5886558` | 2026-04-16T00:19:32.913357+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 417 | `e4b42e68` | 2026-04-16T00:19:34.972859+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | failure | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 401, "e |
| 418 | `78472cd8` | 2026-04-16T00:19:37.011245+00:00 | `settings.read` | admin | settings | — | success | {} |
| 419 | `250084b3` | 2026-04-16T00:19:37.026772+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 420 | `aa83188a` | 2026-04-16T00:19:39.092934+00:00 | `settings.updated` | admin | settings | — | success | {"fields": {"access_token_expire_minutes": 90, "refresh_token_expire_days": 7, " |
| 421 | `65c17f6e` | 2026-04-16T00:19:39.108456+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "PUT", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 422 | `0e03621c` | 2026-04-16T00:19:41.184932+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 423 | `2c3dcb4b` | 2026-04-16T00:19:43.263190+00:00 | `entity.type_created` | admin | custom_entities | 55daef22-8add-4a8b-81b9-cade646ce1ca | success | {"slug": "cargo"} |
| 424 | `3564f0af` | 2026-04-16T00:19:43.274705+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | success | {"method": "POST", "path": "/admin/custom-entities/types", "query": "", "http_st |
| 425 | `17def5a4` | 2026-04-16T00:19:45.328901+00:00 | `entity.value_created` | admin | custom_entities | 3991e38f-83da-4e63-befd-b5381d779f5d | success | {"slug": "cargo", "name": "gerente"} |
| 426 | `cc7731f2` | 2026-04-16T00:19:45.340423+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 427 | `186b9baa` | 2026-04-16T00:19:47.389055+00:00 | `entity.value_created` | admin | custom_entities | d12216a2-6f31-457c-bfb0-4739320539e1 | success | {"slug": "cargo", "name": "vendedor"} |
| 428 | `558c778c` | 2026-04-16T00:19:47.400079+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 429 | `af17022f` | 2026-04-16T00:19:49.676194+00:00 | `user.created` | admin | users | 22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | success | {"username": "gerente1"} |
| 430 | `76eff35f` | 2026-04-16T00:19:49.687712+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 431 | `a999fff5` | 2026-04-16T00:19:51.745166+00:00 | `role.assigned_to_user` | admin | roles | 73a8bc4f-adfc-4125-8b11-3bec07209ff0 | success | {"user_id": "22bf38ad-cf9c-4052-a702-42ab05d3f7c7"} |
| 432 | `1656f637` | 2026-04-16T00:19:51.755678+00:00 | `http.request` | 127.0.0.1 | /admin/roles/73a8bc4f-adfc-4125-8b11-3bec07209ff0/assign-user/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/roles/73a8bc4f-adfc-4125-8b11-3bec07209ff0/as |
| 433 | `036e7232` | 2026-04-16T00:19:53.807715+00:00 | `group.user_assigned` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"user_id": "22bf38ad-cf9c-4052-a702-42ab05d3f7c7"} |
| 434 | `3e294f63` | 2026-04-16T00:19:53.819739+00:00 | `http.request` | 127.0.0.1 | /admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/assign-user/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/a |
| 435 | `c540db17` | 2026-04-16T00:19:55.877467+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | 22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | success | {"key": "sistema", "value": "cotacao"} |
| 436 | `2baffcc9` | 2026-04-16T00:19:55.888536+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/rbac/assign/22bf38ad-cf9c-4052-a702-42ab05d3f |
| 437 | `8842edc4` | 2026-04-16T00:19:57.948053+00:00 | `entity.assigned_to_user` | admin | custom_entities | 22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | success | {"slug": "cargo", "value": "gerente"} |
| 438 | `d8326794` | 2026-04-16T00:19:57.958566+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/22bf38ad-cf9c-4052-a70 |
| 439 | `2775cf52` | 2026-04-16T00:20:00.234985+00:00 | `user.created` | admin | users | c00f5e83-68f1-46ce-913f-ea1745ca2476 | success | {"username": "aprovador1"} |
| 440 | `77752ece` | 2026-04-16T00:20:00.247499+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 201, "el |
| 441 | `d2597b08` | 2026-04-16T00:20:02.298376+00:00 | `role.assigned_to_user` | admin | roles | c111b914-7374-4178-8d1f-75eba14a1004 | success | {"user_id": "c00f5e83-68f1-46ce-913f-ea1745ca2476"} |
| 442 | `fdd4303e` | 2026-04-16T00:20:02.311427+00:00 | `http.request` | 127.0.0.1 | /admin/roles/c111b914-7374-4178-8d1f-75eba14a1004/assign-user/c00f5e83-68f1-46ce-913f-ea1745ca2476 | — | success | {"method": "POST", "path": "/admin/roles/c111b914-7374-4178-8d1f-75eba14a1004/as |
| 443 | `5c374525` | 2026-04-16T00:20:04.367428+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | c00f5e83-68f1-46ce-913f-ea1745ca2476 | success | {"key": "sistema", "value": "cotacao"} |
| 444 | `e6cdaed1` | 2026-04-16T00:20:04.378947+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/c00f5e83-68f1-46ce-913f-ea1745ca2476 | — | success | {"method": "POST", "path": "/admin/rbac/assign/c00f5e83-68f1-46ce-913f-ea1745ca2 |
| 445 | `3d0d369e` | 2026-04-16T00:20:06.415445+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 446 | `821fbae0` | 2026-04-16T00:20:08.465534+00:00 | `entity.assigned_to_user` | admin | custom_entities | bfebd61e-8858-4201-bc40-b97a6afbe9eb | success | {"slug": "cargo", "value": "vendedor"} |
| 447 | `523cd071` | 2026-04-16T00:20:08.477053+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/bfebd61e-8858-4201-bc4 |
| 448 | `393beb0d` | 2026-04-16T00:37:01.097752+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 449 | `654230c2` | 2026-04-16T00:37:26.651414+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 450 | `37e60dee` | 2026-04-16T00:37:28.692240+00:00 | `http.request` | 127.0.0.1 | /health | — | success | {"method": "GET", "path": "/health", "query": "", "http_status": 200, "elapsed_m |
| 451 | `2319e2db` | 2026-04-16T00:37:35.073783+00:00 | `auth.login_success` | admin | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 452 | `6f800679` | 2026-04-16T00:37:35.084295+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 453 | `1cf4d4d2` | 2026-04-16T00:37:37.128919+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 454 | `b20bcedc` | 2026-04-16T00:37:39.430547+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 455 | `07d9c219` | 2026-04-16T00:37:41.484831+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 456 | `43dbc39b` | 2026-04-16T00:37:43.535592+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 457 | `a08bc452` | 2026-04-16T00:37:45.586321+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "GET", "path": "/admin/roles/", "query": "", "http_status": 200, "ela |
| 458 | `ed43f506` | 2026-04-16T00:37:47.632011+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "GET", "path": "/admin/permissions/", "query": "", "http_status": 200 |
| 459 | `23203b24` | 2026-04-16T00:37:49.681515+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "GET", "path": "/admin/groups/", "query": "", "http_status": 200, "el |
| 460 | `70f05b80` | 2026-04-16T00:37:51.738739+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "GET", "path": "/admin/rbac/", "query": "", "http_status": 200, "elap |
| 461 | `6f585f02` | 2026-04-16T00:37:53.787714+00:00 | `settings.read` | admin | settings | — | success | {} |
| 462 | `5911421c` | 2026-04-16T00:37:53.802753+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 463 | `6e5b88d3` | 2026-04-16T00:37:55.858053+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 464 | `a6709805` | 2026-04-16T00:37:57.904339+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 401, "ela |
| 465 | `861d256f` | 2026-04-16T00:37:59.962152+00:00 | `permission.created` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"name": "cotacao:create"} |
| 466 | `2f5d25d0` | 2026-04-16T00:37:59.973675+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 467 | `80e8edff` | 2026-04-16T00:38:02.028598+00:00 | `permission.created` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"name": "cotacao:read"} |
| 468 | `d04a191c` | 2026-04-16T00:38:02.043153+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 469 | `db1df2f1` | 2026-04-16T00:38:04.113717+00:00 | `permission.created` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"name": "cotacao:update"} |
| 470 | `467180c4` | 2026-04-16T00:38:04.126230+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 471 | `bb7a899a` | 2026-04-16T00:38:06.183632+00:00 | `permission.created` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"name": "cotacao:delete"} |
| 472 | `0e3ab931` | 2026-04-16T00:38:06.196150+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 473 | `e4aac86f` | 2026-04-16T00:38:08.251921+00:00 | `permission.created` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"name": "cotacao:approve"} |
| 474 | `784273c6` | 2026-04-16T00:38:08.268964+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | success | {"method": "POST", "path": "/admin/permissions/", "query": "", "http_status": 20 |
| 475 | `c3a34808` | 2026-04-16T00:38:10.334516+00:00 | `role.created` | admin | roles | 788eb76d-ef55-48a7-8b1f-91c91cf3e362 | success | {"name": "vendedor"} |
| 476 | `1e4884cc` | 2026-04-16T00:38:10.349031+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 477 | `6ae0070e` | 2026-04-16T00:38:12.402240+00:00 | `role.created` | admin | roles | c111b914-7374-4178-8d1f-75eba14a1004 | success | {"name": "aprovador"} |
| 478 | `949468f6` | 2026-04-16T00:38:12.413762+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 479 | `2ca3f5f1` | 2026-04-16T00:38:14.453374+00:00 | `role.created` | admin | roles | 73a8bc4f-adfc-4125-8b11-3bec07209ff0 | success | {"name": "gerente"} |
| 480 | `d8bcf1d8` | 2026-04-16T00:38:14.465397+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | success | {"method": "POST", "path": "/admin/roles/", "query": "", "http_status": 201, "el |
| 481 | `67ae5c7e` | 2026-04-16T00:38:16.522018+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "788eb76d-ef55-48a7-8b1f-91c91cf3e362"} |
| 482 | `498e379f` | 2026-04-16T00:38:16.534546+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/788eb76d-ef55-48a7-8b1f-91c91cf3e362 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 483 | `6e1011fb` | 2026-04-16T00:38:18.587896+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 484 | `fa42fdbc` | 2026-04-16T00:38:18.600431+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 485 | `641fcfc3` | 2026-04-16T00:38:20.640890+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "c111b914-7374-4178-8d1f-75eba14a1004"} |
| 486 | `a0467956` | 2026-04-16T00:38:20.657427+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/c111b914-7374-4178-8d1f-75eba14a1004 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 487 | `19058fe9` | 2026-04-16T00:38:22.704862+00:00 | `permission.assigned_to_role` | admin | permissions | b191b68d-8876-475b-ade4-4f346dae0e65 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 488 | `38d09c69` | 2026-04-16T00:38:22.717381+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/b191b68d-8876-475b-ade4-4f346dae0e65/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/b191b68d-8876-475b-ade4-4f346dae0 |
| 489 | `4c86cb5c` | 2026-04-16T00:38:24.770405+00:00 | `permission.assigned_to_role` | admin | permissions | 12b9f2b0-5071-4df8-94b7-5bf6ef4a4788 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 490 | `f2042a79` | 2026-04-16T00:38:24.782936+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4788/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/12b9f2b0-5071-4df8-94b7-5bf6ef4a4 |
| 491 | `8f2ebe38` | 2026-04-16T00:38:26.837283+00:00 | `permission.assigned_to_role` | admin | permissions | 30fe0ae0-3172-4b6d-8093-ef2004f9ea6c | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 492 | `56e8b064` | 2026-04-16T00:38:26.850306+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9ea6c/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/30fe0ae0-3172-4b6d-8093-ef2004f9e |
| 493 | `3cb3f515` | 2026-04-16T00:38:28.902933+00:00 | `permission.assigned_to_role` | admin | permissions | 360aa789-a54a-48a7-ab71-0c5ceec44222 | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 494 | `d963b101` | 2026-04-16T00:38:28.918449+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44222/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/360aa789-a54a-48a7-ab71-0c5ceec44 |
| 495 | `1fe1d1c6` | 2026-04-16T00:38:30.970479+00:00 | `permission.assigned_to_role` | admin | permissions | d90ab5cc-7bb3-4a43-9050-256e0fb45e9a | success | {"role_id": "73a8bc4f-adfc-4125-8b11-3bec07209ff0"} |
| 496 | `a730be9d` | 2026-04-16T00:38:30.983523+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45e9a/assign-role/73a8bc4f-adfc-4125-8b11-3bec07209ff0 | — | success | {"method": "POST", "path": "/admin/permissions/d90ab5cc-7bb3-4a43-9050-256e0fb45 |
| 497 | `095eb634` | 2026-04-16T00:38:33.042074+00:00 | `group.created` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"name": "Vendas"} |
| 498 | `a0c4bc55` | 2026-04-16T00:38:33.053590+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | success | {"method": "POST", "path": "/admin/groups/", "query": "", "http_status": 201, "e |
| 499 | `8de78d88` | 2026-04-16T00:38:35.123345+00:00 | `rbac.attribute_created` | admin | rbac_attributes | 29c0a137-413c-4099-ba20-26e65d6e115e | success | {"key": "sistema"} |
| 500 | `5e1004f7` | 2026-04-16T00:38:35.137874+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | success | {"method": "POST", "path": "/admin/rbac/", "query": "", "http_status": 201, "ela |
| 501 | `99e0bea7` | 2026-04-16T00:38:37.188111+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 409, "el |
| 502 | `e4b2f259` | 2026-04-16T00:38:39.241378+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 503 | `8a69d1c4` | 2026-04-16T00:38:41.290907+00:00 | `role.assigned_to_user` | admin | roles | 788eb76d-ef55-48a7-8b1f-91c91cf3e362 | success | {"user_id": "bfebd61e-8858-4201-bc40-b97a6afbe9eb"} |
| 504 | `2f343bbd` | 2026-04-16T00:38:41.305436+00:00 | `http.request` | 127.0.0.1 | /admin/roles/788eb76d-ef55-48a7-8b1f-91c91cf3e362/assign-user/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/roles/788eb76d-ef55-48a7-8b1f-91c91cf3e362/as |
| 505 | `876c6050` | 2026-04-16T00:38:43.352935+00:00 | `group.user_assigned` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"user_id": "bfebd61e-8858-4201-bc40-b97a6afbe9eb"} |
| 506 | `7b069988` | 2026-04-16T00:38:43.365456+00:00 | `http.request` | 127.0.0.1 | /admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/assign-user/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/a |
| 507 | `ce6c3478` | 2026-04-16T00:38:45.411838+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | bfebd61e-8858-4201-bc40-b97a6afbe9eb | success | {"key": "sistema", "value": "cotacao"} |
| 508 | `80725461` | 2026-04-16T00:38:45.424864+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/rbac/assign/bfebd61e-8858-4201-bc40-b97a6afbe |
| 509 | `e71864f8` | 2026-04-16T00:38:47.703486+00:00 | `auth.login_success` | usuario1 | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 510 | `64c6d795` | 2026-04-16T00:38:47.714000+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 511 | `8ef658c3` | 2026-04-16T00:38:49.762020+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 512 | `6c5cb3a6` | 2026-04-16T00:38:51.813251+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 403, "ela |
| 513 | `c6368e3d` | 2026-04-16T00:38:53.851203+00:00 | `http.request` | 127.0.0.1 | /auth/refresh | — | success | {"method": "POST", "path": "/auth/refresh", "query": "", "http_status": 200, "el |
| 514 | `df19f182` | 2026-04-16T00:38:55.902137+00:00 | `auth.logout` | token | auth | — | success | {"jti": "gN44YNdA"} |
| 515 | `a6995e4e` | 2026-04-16T00:38:55.913666+00:00 | `http.request` | 127.0.0.1 | /auth/logout | — | success | {"method": "POST", "path": "/auth/logout", "query": "", "http_status": 200, "ela |
| 516 | `9e681697` | 2026-04-16T00:38:57.965089+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | failure | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 401, "e |
| 517 | `7728f2b8` | 2026-04-16T00:39:00.234237+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 518 | `8da72457` | 2026-04-16T00:39:02.281710+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | failure | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 401, "elap |
| 519 | `5e5c3cec` | 2026-04-16T00:39:04.322609+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | failure | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 401, "e |
| 520 | `2c019c5b` | 2026-04-16T00:39:06.360058+00:00 | `settings.read` | admin | settings | — | success | {} |
| 521 | `bdf5d663` | 2026-04-16T00:39:06.372589+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "GET", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 522 | `562d56ca` | 2026-04-16T00:39:08.414939+00:00 | `settings.updated` | admin | settings | — | success | {"fields": {"access_token_expire_minutes": 90, "refresh_token_expire_days": 7, " |
| 523 | `a058acc1` | 2026-04-16T00:39:08.428454+00:00 | `http.request` | 127.0.0.1 | /admin/settings/ | — | success | {"method": "PUT", "path": "/admin/settings/", "query": "", "http_status": 200, " |
| 524 | `e8b2f991` | 2026-04-16T00:39:10.478904+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | success | {"method": "GET", "path": "/admin/audit/", "query": "", "http_status": 200, "ela |
| 525 | `5d71e25f` | 2026-04-16T00:39:12.533822+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | failure | {"method": "POST", "path": "/admin/custom-entities/types", "query": "", "http_st |
| 526 | `bfe1c727` | 2026-04-16T00:39:14.585214+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | failure | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 527 | `8adb4254` | 2026-04-16T00:39:16.633363+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "GET", "path": "/admin/custom-entities/cargo/values", "query": "", "h |
| 528 | `765ca2f4` | 2026-04-16T00:39:18.688675+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | failure | {"method": "POST", "path": "/admin/custom-entities/cargo/values", "query": "", " |
| 529 | `7c7fafae` | 2026-04-16T00:39:20.741936+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/cargo/values | — | success | {"method": "GET", "path": "/admin/custom-entities/cargo/values", "query": "", "h |
| 530 | `e81b8f1a` | 2026-04-16T00:39:22.807306+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 409, "el |
| 531 | `ac7f9a5c` | 2026-04-16T00:39:24.858526+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 532 | `169871a4` | 2026-04-16T00:39:26.908344+00:00 | `role.assigned_to_user` | admin | roles | 73a8bc4f-adfc-4125-8b11-3bec07209ff0 | success | {"user_id": "22bf38ad-cf9c-4052-a702-42ab05d3f7c7"} |
| 533 | `f77fea83` | 2026-04-16T00:39:26.919870+00:00 | `http.request` | 127.0.0.1 | /admin/roles/73a8bc4f-adfc-4125-8b11-3bec07209ff0/assign-user/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/roles/73a8bc4f-adfc-4125-8b11-3bec07209ff0/as |
| 534 | `43cb1edb` | 2026-04-16T00:39:28.962401+00:00 | `group.user_assigned` | admin | groups | dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8 | success | {"user_id": "22bf38ad-cf9c-4052-a702-42ab05d3f7c7"} |
| 535 | `f1c53a29` | 2026-04-16T00:39:28.977922+00:00 | `http.request` | 127.0.0.1 | /admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/assign-user/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/groups/dbcd13be-9ab9-48c1-91d6-c0aca4e7eac8/a |
| 536 | `0e7888fd` | 2026-04-16T00:39:31.034270+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | 22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | success | {"key": "sistema", "value": "cotacao"} |
| 537 | `a6da249e` | 2026-04-16T00:39:31.047785+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/rbac/assign/22bf38ad-cf9c-4052-a702-42ab05d3f |
| 538 | `35ab2a6f` | 2026-04-16T00:39:33.101573+00:00 | `entity.assigned_to_user` | admin | custom_entities | 22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | success | {"slug": "cargo", "value": "gerente"} |
| 539 | `5bcba734` | 2026-04-16T00:39:33.113094+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/22bf38ad-cf9c-4052-a702-42ab05d3f7c7 | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/22bf38ad-cf9c-4052-a70 |
| 540 | `208a2116` | 2026-04-16T00:39:35.165806+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | failure | {"method": "POST", "path": "/admin/users/", "query": "", "http_status": 409, "el |
| 541 | `29c48f60` | 2026-04-16T00:39:37.221173+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 542 | `55592551` | 2026-04-16T00:39:39.271775+00:00 | `role.assigned_to_user` | admin | roles | c111b914-7374-4178-8d1f-75eba14a1004 | success | {"user_id": "c00f5e83-68f1-46ce-913f-ea1745ca2476"} |
| 543 | `c620eaf6` | 2026-04-16T00:39:39.283296+00:00 | `http.request` | 127.0.0.1 | /admin/roles/c111b914-7374-4178-8d1f-75eba14a1004/assign-user/c00f5e83-68f1-46ce-913f-ea1745ca2476 | — | success | {"method": "POST", "path": "/admin/roles/c111b914-7374-4178-8d1f-75eba14a1004/as |
| 544 | `4ca43976` | 2026-04-16T00:39:41.326901+00:00 | `rbac.attribute_assigned_to_user` | admin | rbac_attributes | c00f5e83-68f1-46ce-913f-ea1745ca2476 | success | {"key": "sistema", "value": "cotacao"} |
| 545 | `b970ea9b` | 2026-04-16T00:39:41.338425+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/assign/c00f5e83-68f1-46ce-913f-ea1745ca2476 | — | success | {"method": "POST", "path": "/admin/rbac/assign/c00f5e83-68f1-46ce-913f-ea1745ca2 |
| 546 | `45a127d4` | 2026-04-16T00:39:43.394651+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | success | {"method": "GET", "path": "/admin/users/", "query": "", "http_status": 200, "ela |
| 547 | `6bd9d487` | 2026-04-16T00:39:45.444630+00:00 | `entity.assigned_to_user` | admin | custom_entities | bfebd61e-8858-4201-bc40-b97a6afbe9eb | success | {"slug": "cargo", "value": "vendedor"} |
| 548 | `97bc16a6` | 2026-04-16T00:39:45.456144+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/assign/bfebd61e-8858-4201-bc40-b97a6afbe9eb | — | success | {"method": "POST", "path": "/admin/custom-entities/assign/bfebd61e-8858-4201-bc4 |
| 549 | `f9c6aed1` | 2026-04-16T00:39:47.748990+00:00 | `auth.login_success` | usuario1 | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 550 | `b6680a88` | 2026-04-16T00:39:47.762016+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 551 | `59b5d1f7` | 2026-04-16T00:39:50.235756+00:00 | `auth.login_success` | gerente1 | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 552 | `01215b0c` | 2026-04-16T00:39:50.254827+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 553 | `8e1791ea` | 2026-04-16T00:39:52.550452+00:00 | `auth.login_success` | aprovador1 | auth | eyJhbGci | success | {"ip": "127.0.0.1"} |
| 554 | `b09193a0` | 2026-04-16T00:39:52.562989+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | success | {"method": "POST", "path": "/auth/token", "query": "", "http_status": 200, "elap |
| 555 | `ee894a48` | 2026-04-16T00:39:54.623001+00:00 | `auth.abac_check` | admin | auth/check | — | success | {"allowed": true, "reason": "superuser"} |
| 556 | `17108d56` | 2026-04-16T00:39:54.637517+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 557 | `5225508b` | 2026-04-16T00:39:56.684237+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 558 | `a421db3a` | 2026-04-16T00:39:56.697750+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 559 | `16471310` | 2026-04-16T00:39:58.752332+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 560 | `69620964` | 2026-04-16T00:40:00.795514+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 561 | `bca3a077` | 2026-04-16T00:40:00.811556+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 562 | `1e8dfd11` | 2026-04-16T00:40:02.859083+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 563 | `c8cab64e` | 2026-04-16T00:40:02.872623+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 564 | `a0543ed6` | 2026-04-16T00:40:04.925282+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 565 | `54793e8e` | 2026-04-16T00:40:06.977336+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 566 | `bc2dab87` | 2026-04-16T00:40:06.988848+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 567 | `6237a8a4` | 2026-04-16T00:40:09.043546+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 568 | `2b2a5846` | 2026-04-16T00:40:11.094530+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 569 | `7dece7ae` | 2026-04-16T00:40:11.106047+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 570 | `d59d6c5f` | 2026-04-16T00:40:13.147095+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 571 | `4ca9aa4f` | 2026-04-16T00:40:15.209364+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 572 | `b9dd8353` | 2026-04-16T00:40:15.221399+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 573 | `3b20ddca` | 2026-04-16T00:40:17.255138+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 574 | `ee5b3d94` | 2026-04-16T00:40:17.266654+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 575 | `98f0ba9d` | 2026-04-16T00:40:19.307547+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 576 | `ff637ed2` | 2026-04-16T00:40:21.356759+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 577 | `3bd42985` | 2026-04-16T00:40:21.370778+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 578 | `1fe256a1` | 2026-04-16T00:40:23.409935+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 579 | `7942f81d` | 2026-04-16T00:40:23.421467+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 580 | `e2c0dfe3` | 2026-04-16T00:40:25.480536+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 581 | `a3c23174` | 2026-04-16T00:40:27.549176+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 582 | `8a686843` | 2026-04-16T00:40:27.564211+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 583 | `cf228f56` | 2026-04-16T00:40:29.601422+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 584 | `108dcbaf` | 2026-04-16T00:40:29.613942+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 585 | `ecc7547a` | 2026-04-16T00:40:31.652660+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 586 | `2871acff` | 2026-04-16T00:40:33.706713+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 587 | `fb30ed03` | 2026-04-16T00:40:33.717232+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 588 | `19eaa6aa` | 2026-04-16T00:40:35.760409+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 589 | `177e7ce0` | 2026-04-16T00:40:37.810516+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 590 | `b2f6ba63` | 2026-04-16T00:40:37.822042+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 591 | `10f2c77c` | 2026-04-16T00:40:39.859076+00:00 | `auth.abac_check` | aprovador1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["aprovador"], "abac": {"sistema": "c |
| 592 | `c498199c` | 2026-04-16T00:40:39.870108+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 593 | `f86c8497` | 2026-04-16T00:40:41.913262+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 594 | `99c6283a` | 2026-04-16T00:40:43.960359+00:00 | `auth.abac_check` | anonymous | auth/check | — | failure | {"allowed": false, "reason": "Token invalido: "} |
| 595 | `8638c5be` | 2026-04-16T00:40:43.971384+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 596 | `1e117ff1` | 2026-04-16T00:40:46.017960+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 597 | `d302e4da` | 2026-04-16T00:40:48.068915+00:00 | `http.request` | 127.0.0.1 | /auth/validate | — | success | {"method": "POST", "path": "/auth/validate", "query": "", "http_status": 200, "e |
| 598 | `26abeab7` | 2026-04-16T00:40:50.106622+00:00 | `auth.abac_check` | usuario1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["vendedor"], "abac": {"sistema": "co |
| 599 | `49cb36b3` | 2026-04-16T00:40:50.117140+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 600 | `7a2e1b80` | 2026-04-16T00:40:52.156158+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 601 | `01716e01` | 2026-04-16T00:40:54.193737+00:00 | `auth.abac_check` | gerente1 | auth/check | — | success | {"allowed": true, "reason": "ok", "roles": ["gerente"], "abac": {"sistema": "cot |
| 602 | `a3e250fa` | 2026-04-16T00:40:54.209267+00:00 | `http.request` | 127.0.0.1 | /auth/check | — | success | {"method": "POST", "path": "/auth/check", "query": "", "http_status": 200, "elap |
| 603 | `e2c49bfb` | 2026-04-16T00:57:09.763397+00:00 | `system.startup` | system | api | — | success | {"version": "1.0.0"} |
| 604 | `15ad696e` | 2026-04-16T21:10:51.590475+00:00 | `system.startup` | system | api | — | — | success | — | {"version": "1.0.0"} |
| 605 | `cc44aaf1` | 2026-04-16T21:11:07.311164+00:00 | `auth.login_success` | admin | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 606 | `ab5f04ce` | 2026-04-16T21:11:07.321162+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 270.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 607 | `792dc92b` | 2026-04-16T21:11:07.632683+00:00 | `user.created` | admin | users | 882692bd-c05c-43bb-a5ec-c0adb378e0ef | — | success | — | {"username": "stress_bbf9db"} |
| 608 | `c8edb775` | 2026-04-16T21:11:07.644688+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | — | success | 305.9ms | {"method": "POST", "path": "/admin/users/", "query": null, "http_status": 201, " |
| 609 | `8dcb7da0` | 2026-04-16T21:11:07.896203+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 610 | `8b00e58c` | 2026-04-16T21:11:07.910715+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 248.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 611 | `a839f0ad` | 2026-04-16T21:11:07.947720+00:00 | `http.request` | 127.0.0.1 | /admin/policies/ | — | — | success | 20.0ms | {"method": "POST", "path": "/admin/policies/", "query": null, "http_status": 201 |
| 612 | `0c0d6ba8` | 2026-04-16T21:11:07.973717+00:00 | `http.request` | 127.0.0.1 | /admin/policies/reload | — | — | success | 8.3ms | {"method": "POST", "path": "/admin/policies/reload", "query": null, "http_status |
| 613 | `7032c624` | 2026-04-16T21:11:08.510758+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 614 | `cead4c32` | 2026-04-16T21:11:08.522756+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 261.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 615 | `c81f9338` | 2026-04-16T21:11:09.373299+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 616 | `9f4a6af3` | 2026-04-16T21:11:09.631812+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 617 | `2c0efe72` | 2026-04-16T21:11:09.645822+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 513.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 618 | `8e18b874` | 2026-04-16T21:11:09.656819+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 526.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 619 | `beacedf1` | 2026-04-16T21:11:09.918848+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 620 | `c3b0a6e7` | 2026-04-16T21:11:10.172359+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 621 | `d4c37bcc` | 2026-04-16T21:11:10.418873+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 622 | `b95fefbc` | 2026-04-16T21:11:10.431873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1297.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 623 | `fe4b412f` | 2026-04-16T21:11:10.443876+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1309.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 624 | `a09c0ed6` | 2026-04-16T21:11:10.456874+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1321.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 625 | `3b864283` | 2026-04-16T21:11:11.315408+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 626 | `845c59ad` | 2026-04-16T21:11:11.552926+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 627 | `47ca7424` | 2026-04-16T21:11:11.799438+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 628 | `5857ca61` | 2026-04-16T21:11:12.098960+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 629 | `b0cc20bf` | 2026-04-16T21:11:12.116958+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1042.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 630 | `19d25080` | 2026-04-16T21:11:12.133959+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1059.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 631 | `4cdb7e1b` | 2026-04-16T21:11:12.173485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1098.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 632 | `1fa2bd3b` | 2026-04-16T21:11:12.188485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1113.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 633 | `4ed086b4` | 2026-04-16T21:11:12.466003+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 634 | `c89d71ea` | 2026-04-16T21:11:12.720514+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 635 | `ad85fa0c` | 2026-04-16T21:11:12.991035+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 636 | `b3206bf1` | 2026-04-16T21:11:13.272556+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 637 | `a5edfc46` | 2026-04-16T21:11:13.522069+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 638 | `336d4577` | 2026-04-16T21:11:13.770577+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 639 | `ade2f163` | 2026-04-16T21:11:13.783579+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2703.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 640 | `e43e2cd3` | 2026-04-16T21:11:13.795579+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2714.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 641 | `395b839a` | 2026-04-16T21:11:13.806577+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2724.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 642 | `fbbdade1` | 2026-04-16T21:11:13.817577+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2734.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 643 | `6f3da8f9` | 2026-04-16T21:11:13.830575+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2747.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 644 | `f185c0ce` | 2026-04-16T21:11:13.846578+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 2762.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 645 | `d2dd069e` | 2026-04-16T21:11:14.682621+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 646 | `6be517cb` | 2026-04-16T21:11:14.724623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 275.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 647 | `5e092848` | 2026-04-16T21:11:14.974130+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 648 | `b25d8421` | 2026-04-16T21:11:14.998131+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 545.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 649 | `f1fc7917` | 2026-04-16T21:11:15.259640+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 650 | `eeb3ada7` | 2026-04-16T21:11:15.499148+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 651 | `6e5025e2` | 2026-04-16T21:11:15.735660+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 652 | `76a18bf8` | 2026-04-16T21:11:15.979177+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 653 | `8ac8018a` | 2026-04-16T21:11:16.257695+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 654 | `fb9e0d07` | 2026-04-16T21:11:16.499205+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 655 | `2ff4042d` | 2026-04-16T21:11:16.737715+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 656 | `e825490e` | 2026-04-16T21:11:16.977223+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 657 | `0c957caf` | 2026-04-16T21:11:17.216734+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 658 | `42a88d76` | 2026-04-16T21:11:17.459243+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 659 | `d17c4b6f` | 2026-04-16T21:11:17.696752+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 660 | `dfc6291d` | 2026-04-16T21:11:17.933755+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 661 | `d32e1a32` | 2026-04-16T21:11:18.171264+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 662 | `345d5fdf` | 2026-04-16T21:11:18.413786+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 663 | `980b978b` | 2026-04-16T21:11:18.660295+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 664 | `d39ae92f` | 2026-04-16T21:11:18.905814+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 665 | `e0838071` | 2026-04-16T21:11:19.168331+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 666 | `994c13df` | 2026-04-16T21:11:19.421846+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 667 | `413877b4` | 2026-04-16T21:11:19.667357+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 668 | `2e8bb0fd` | 2026-04-16T21:11:19.908874+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 669 | `1b718cd9` | 2026-04-16T21:11:20.149387+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 670 | `e5388170` | 2026-04-16T21:11:20.388894+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 671 | `48015682` | 2026-04-16T21:11:20.631402+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 672 | `876b0032` | 2026-04-16T21:11:20.642403+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5902.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 673 | `cb7fc561` | 2026-04-16T21:11:20.655404+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5915.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 674 | `70321f34` | 2026-04-16T21:11:20.665403+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5925.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 675 | `67808b48` | 2026-04-16T21:11:20.676402+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5935.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 676 | `f152eacb` | 2026-04-16T21:11:20.689407+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5949.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 677 | `96ef4e61` | 2026-04-16T21:11:20.701920+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5958.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 678 | `5a8ceb33` | 2026-04-16T21:11:20.711919+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5968.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 679 | `fe437e54` | 2026-04-16T21:11:20.721919+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5978.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 680 | `812becec` | 2026-04-16T21:11:20.730918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5987.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 681 | `20fb2a23` | 2026-04-16T21:11:20.740918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5997.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 682 | `85507a58` | 2026-04-16T21:11:20.752918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6009.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 683 | `ef7e09c4` | 2026-04-16T21:11:20.763921+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6019.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 684 | `8e3abf9f` | 2026-04-16T21:11:20.772918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6028.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 685 | `e3350771` | 2026-04-16T21:11:20.782921+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6039.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 686 | `1a3c63fe` | 2026-04-16T21:11:20.795922+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5807.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 687 | `7cb74664` | 2026-04-16T21:11:20.808918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5820.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 688 | `0e56a7eb` | 2026-04-16T21:11:20.819919+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5831.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 689 | `b70ffe28` | 2026-04-16T21:11:20.832918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5842.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 690 | `85c63bac` | 2026-04-16T21:11:20.843918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5853.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 691 | `9391ab34` | 2026-04-16T21:11:20.855919+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5863.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 692 | `da82cfd1` | 2026-04-16T21:11:20.868923+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5874.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 693 | `c9a4d420` | 2026-04-16T21:11:20.880921+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5886.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 694 | `61405b08` | 2026-04-16T21:11:20.892918+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5898.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 695 | `b4d97395` | 2026-04-16T21:11:21.927998+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 696 | `7d940e38` | 2026-04-16T21:11:22.190521+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 697 | `f69fb638` | 2026-04-16T21:11:22.464553+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 698 | `ff02f230` | 2026-04-16T21:11:22.713071+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 699 | `97d3cb80` | 2026-04-16T21:11:22.952582+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 700 | `bf6e7a06` | 2026-04-16T21:11:23.191584+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 701 | `ee3b92e0` | 2026-04-16T21:11:23.431096+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 702 | `3013c1e9` | 2026-04-16T21:11:23.666611+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 703 | `d677c527` | 2026-04-16T21:11:23.905120+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 704 | `250ffc75` | 2026-04-16T21:11:24.143634+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 705 | `a30d9297` | 2026-04-16T21:11:24.445154+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 706 | `2a32ea61` | 2026-04-16T21:11:24.682663+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 707 | `80613462` | 2026-04-16T21:11:24.920173+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 708 | `90f1512e` | 2026-04-16T21:11:25.199687+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 709 | `95d23d89` | 2026-04-16T21:11:25.440202+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 710 | `4787cc35` | 2026-04-16T21:11:25.679713+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 711 | `244f42d4` | 2026-04-16T21:11:25.918223+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 712 | `5479a48c` | 2026-04-16T21:11:26.162750+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 713 | `0dc78fe0` | 2026-04-16T21:11:26.401260+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 714 | `7ff74f6e` | 2026-04-16T21:11:26.638769+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 715 | `3e42274e` | 2026-04-16T21:11:26.877276+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 716 | `726bd449` | 2026-04-16T21:11:27.116790+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 717 | `4a008063` | 2026-04-16T21:11:27.137790+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5506.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 718 | `0778c70f` | 2026-04-16T21:11:27.148789+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5517.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 719 | `8f058d7d` | 2026-04-16T21:11:27.160796+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5529.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 720 | `d87b4ff1` | 2026-04-16T21:11:27.175790+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5541.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 721 | `e0687e77` | 2026-04-16T21:11:27.187791+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5553.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 722 | `22c4ee1b` | 2026-04-16T21:11:27.198797+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5564.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 723 | `89dbf53e` | 2026-04-16T21:11:27.212309+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5577.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 724 | `d4f650df` | 2026-04-16T21:11:27.223307+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5588.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 725 | `6a7a4d28` | 2026-04-16T21:11:27.234307+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5599.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 726 | `513e2d02` | 2026-04-16T21:11:27.245307+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5610.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 727 | `e8999d90` | 2026-04-16T21:11:27.256306+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5621.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 728 | `24dfc6d8` | 2026-04-16T21:11:27.267304+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5632.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 729 | `f2da6b3f` | 2026-04-16T21:11:27.280305+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5645.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 730 | `ea9bc750` | 2026-04-16T21:11:27.291304+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5656.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 731 | `62b22671` | 2026-04-16T21:11:27.301308+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5666.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 732 | `d7585322` | 2026-04-16T21:11:27.313305+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5677.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 733 | `c7d968e1` | 2026-04-16T21:11:27.324305+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5689.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 734 | `f8b322b8` | 2026-04-16T21:11:27.337305+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5696.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 735 | `ac02b9f6` | 2026-04-16T21:11:27.348306+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5707.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 736 | `94a4de22` | 2026-04-16T21:11:27.359305+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5718.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 737 | `448e3b25` | 2026-04-16T21:11:27.370304+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5729.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 738 | `7b2211a8` | 2026-04-16T21:11:27.383304+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 5742.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 739 | `f2eeea1b` | 2026-04-16T21:11:27.623812+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 740 | `1c82e0bd` | 2026-04-16T21:11:27.880329+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 741 | `31c0fb5a` | 2026-04-16T21:11:28.120839+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 742 | `35abe027` | 2026-04-16T21:11:28.362359+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 743 | `2be6723a` | 2026-04-16T21:11:28.605873+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 744 | `effe5273` | 2026-04-16T21:11:28.867388+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 745 | `24858eb1` | 2026-04-16T21:11:29.109897+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 746 | `45eccb80` | 2026-04-16T21:11:29.352407+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 747 | `824ac0e3` | 2026-04-16T21:11:29.594917+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 748 | `ec97cf6e` | 2026-04-16T21:11:29.837426+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 749 | `40f13df7` | 2026-04-16T21:11:30.082941+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 750 | `74b5feea` | 2026-04-16T21:11:30.329455+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 751 | `e4621467` | 2026-04-16T21:11:30.568966+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 752 | `0681c395` | 2026-04-16T21:11:30.810483+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 753 | `8f021493` | 2026-04-16T21:11:31.050998+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 754 | `1103a719` | 2026-04-16T21:11:31.292509+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 755 | `13cab8a4` | 2026-04-16T21:11:31.535019+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 756 | `fe78e667` | 2026-04-16T21:11:31.774528+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 757 | `e7329d1a` | 2026-04-16T21:11:32.017040+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 758 | `9eb54c39` | 2026-04-16T21:11:32.258546+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 759 | `2d017063` | 2026-04-16T21:11:32.513057+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 760 | `e4bb2a57` | 2026-04-16T21:11:32.753565+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 761 | `1a4d27cf` | 2026-04-16T21:11:32.993075+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 762 | `14df74d9` | 2026-04-16T21:11:33.230588+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 763 | `05368bb9` | 2026-04-16T21:11:33.470100+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 764 | `a650e0ea` | 2026-04-16T21:11:33.718103+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 765 | `71c6f6f1` | 2026-04-16T21:11:33.959616+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 766 | `8ee22910` | 2026-04-16T21:11:34.196127+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 767 | `74953400` | 2026-04-16T21:11:34.225656+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12562.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 768 | `9af4ade5` | 2026-04-16T21:11:34.241653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12577.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 769 | `07a8d4a8` | 2026-04-16T21:11:34.252653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12588.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 770 | `63e55a91` | 2026-04-16T21:11:34.264653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12600.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 771 | `f7911dcb` | 2026-04-16T21:11:34.274653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12610.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 772 | `45ebf72d` | 2026-04-16T21:11:34.285655+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12615.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 773 | `79297c89` | 2026-04-16T21:11:34.295655+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12625.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 774 | `25ed8b79` | 2026-04-16T21:11:34.307653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12643.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 775 | `2365b3d1` | 2026-04-16T21:11:34.323655+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12652.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 776 | `6faf47c8` | 2026-04-16T21:11:34.333653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12663.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 777 | `b2ef73f1` | 2026-04-16T21:11:34.343653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12672.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 778 | `86fddbe9` | 2026-04-16T21:11:34.353653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12683.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 779 | `352aef33` | 2026-04-16T21:11:34.365653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12695.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 780 | `3d5dd48f` | 2026-04-16T21:11:34.376655+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12706.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 781 | `4e6c3de7` | 2026-04-16T21:11:34.386653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12707.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 782 | `0e3be412` | 2026-04-16T21:11:34.397653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12717.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 783 | `9330bae4` | 2026-04-16T21:11:34.407653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12727.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 784 | `6ce0f091` | 2026-04-16T21:11:34.417653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12737.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 785 | `801923f7` | 2026-04-16T21:11:34.428656+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12747.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 786 | `e3a19e39` | 2026-04-16T21:11:34.438653+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12758.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 787 | `37613e26` | 2026-04-16T21:11:34.449654+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12768.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 788 | `52bd237e` | 2026-04-16T21:11:34.464656+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12794.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 789 | `0161c032` | 2026-04-16T21:11:34.475164+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12804.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 790 | `f5092762` | 2026-04-16T21:11:34.487166+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12816.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 791 | `5d1d0b41` | 2026-04-16T21:11:34.497164+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12826.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 792 | `43cda68f` | 2026-04-16T21:11:34.508165+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12837.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 793 | `29163df9` | 2026-04-16T21:11:34.518164+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12848.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 794 | `20e884dd` | 2026-04-16T21:11:34.528164+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12858.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 795 | `47697556` | 2026-04-16T21:11:35.730742+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 796 | `14b330dd` | 2026-04-16T21:11:35.974249+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 797 | `73abb0b6` | 2026-04-16T21:11:36.271777+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 798 | `bf1f73fc` | 2026-04-16T21:11:36.523288+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 799 | `2065eff1` | 2026-04-16T21:11:36.764798+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 800 | `3fdb52f8` | 2026-04-16T21:11:37.001306+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 801 | `22463d77` | 2026-04-16T21:11:37.240815+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 802 | `0546ff88` | 2026-04-16T21:11:37.482326+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 803 | `f428da12` | 2026-04-16T21:11:37.721333+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 804 | `b1f6ec00` | 2026-04-16T21:11:37.960837+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 805 | `fa0ae7bd` | 2026-04-16T21:11:38.201356+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 806 | `d9c4c6dd` | 2026-04-16T21:11:38.439873+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 807 | `df076233` | 2026-04-16T21:11:38.678384+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 808 | `3f955aa5` | 2026-04-16T21:11:38.917897+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 809 | `5715471b` | 2026-04-16T21:11:39.158417+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 810 | `1096af4f` | 2026-04-16T21:11:39.399925+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 811 | `daf763b9` | 2026-04-16T21:11:39.638438+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 812 | `338bc704` | 2026-04-16T21:11:39.874947+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 813 | `b08143b8` | 2026-04-16T21:11:40.113457+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 814 | `5023f7ed` | 2026-04-16T21:11:40.353967+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 815 | `6d4a7fd7` | 2026-04-16T21:11:40.591477+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 816 | `fb946db2` | 2026-04-16T21:11:40.830990+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 817 | `8607a961` | 2026-04-16T21:11:41.070502+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 818 | `5e6448b6` | 2026-04-16T21:11:41.310011+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 819 | `5e022c46` | 2026-04-16T21:11:41.547519+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 820 | `6fccefff` | 2026-04-16T21:11:41.791031+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 821 | `ab58343d` | 2026-04-16T21:11:42.040543+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 822 | `79fdc922` | 2026-04-16T21:11:42.280053+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 823 | `b586921f` | 2026-04-16T21:11:42.517558+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 824 | `65aa7b87` | 2026-04-16T21:11:42.756071+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 825 | `3affc911` | 2026-04-16T21:11:42.992584+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 826 | `a5fd9320` | 2026-04-16T21:11:43.234588+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 827 | `9fbeb030` | 2026-04-16T21:11:43.474094+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 828 | `a066f635` | 2026-04-16T21:11:43.712613+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 829 | `94cc357e` | 2026-04-16T21:11:43.949122+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 830 | `91f93a4a` | 2026-04-16T21:11:44.189632+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 831 | `aa806271` | 2026-04-16T21:11:44.433141+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 832 | `b50bdf1f` | 2026-04-16T21:11:44.669654+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 833 | `b5677e00` | 2026-04-16T21:11:44.909165+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 834 | `dca40456` | 2026-04-16T21:11:45.146675+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 835 | `af28b963` | 2026-04-16T21:11:45.391186+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 836 | `b7820e9a` | 2026-04-16T21:11:45.632698+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 837 | `fe4f65d1` | 2026-04-16T21:11:45.871211+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 838 | `0509fab3` | 2026-04-16T21:11:46.110725+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 839 | `b42e5fc4` | 2026-04-16T21:11:46.351237+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 840 | `a0cd5522` | 2026-04-16T21:11:46.593746+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 841 | `79b44cf5` | 2026-04-16T21:11:46.830257+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 842 | `41628be8` | 2026-04-16T21:11:47.069771+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 843 | `0c417ba6` | 2026-04-16T21:11:47.308284+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 844 | `6af1f296` | 2026-04-16T21:11:47.549795+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 845 | `fdf74b43` | 2026-04-16T21:11:47.562796+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12126.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 846 | `9155bfaf` | 2026-04-16T21:11:47.573795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12136.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 847 | `4429612f` | 2026-04-16T21:11:47.588796+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12151.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 848 | `5ed83a2b` | 2026-04-16T21:11:47.599795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12162.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 849 | `ff870495` | 2026-04-16T21:11:47.613796+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12177.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 850 | `440814a2` | 2026-04-16T21:11:47.629797+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12193.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 851 | `d3f9034c` | 2026-04-16T21:11:47.641796+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12200.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 852 | `32876b90` | 2026-04-16T21:11:47.651794+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12210.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 853 | `f01d750d` | 2026-04-16T21:11:47.663794+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12222.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 854 | `c1c5974a` | 2026-04-16T21:11:47.674795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12233.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 855 | `4b16e9b1` | 2026-04-16T21:11:47.689795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12247.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 856 | `7d1723d1` | 2026-04-16T21:11:47.700795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12259.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 857 | `8911ea41` | 2026-04-16T21:11:47.717795+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12275.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 858 | `a66f65c5` | 2026-04-16T21:11:47.733799+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12291.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 859 | `0e1192fe` | 2026-04-16T21:11:47.750314+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12308.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 860 | `efc60a3e` | 2026-04-16T21:11:47.762316+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12320.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 861 | `06dbe7ff` | 2026-04-16T21:11:47.773314+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12331.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 862 | `025e39ab` | 2026-04-16T21:11:47.784315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12342.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 863 | `cccb433a` | 2026-04-16T21:11:47.796315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12353.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 864 | `62ba8de5` | 2026-04-16T21:11:47.808314+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12365.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 865 | `04a3a8ab` | 2026-04-16T21:11:47.823315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12379.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 866 | `856468e5` | 2026-04-16T21:11:47.836315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12392.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 867 | `80c34e15` | 2026-04-16T21:11:47.848315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12404.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 868 | `43f66183` | 2026-04-16T21:11:47.860314+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12417.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 869 | `f2cfe020` | 2026-04-16T21:11:47.873314+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12430.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 870 | `df1b5d59` | 2026-04-16T21:11:47.885319+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12441.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 871 | `2997c56b` | 2026-04-16T21:11:47.903316+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12451.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 872 | `a8993f28` | 2026-04-16T21:11:47.916315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12464.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 873 | `f8905963` | 2026-04-16T21:11:47.932315+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12480.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 874 | `358c4903` | 2026-04-16T21:11:47.943313+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12490.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 875 | `ae7a72d8` | 2026-04-16T21:11:47.955313+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12503.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 876 | `cd1e19bb` | 2026-04-16T21:11:47.970313+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12517.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 877 | `e4869883` | 2026-04-16T21:11:47.984320+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12531.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 878 | `d419b335` | 2026-04-16T21:11:47.998828+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12547.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 879 | `92e12193` | 2026-04-16T21:11:48.009833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12557.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 880 | `617938f9` | 2026-04-16T21:11:48.023832+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12571.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 881 | `b1f053f0` | 2026-04-16T21:11:48.035833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12583.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 882 | `2611952b` | 2026-04-16T21:11:48.047833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12595.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 883 | `c2c41e11` | 2026-04-16T21:11:48.062834+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12604.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 884 | `4656c4be` | 2026-04-16T21:11:48.073833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12615.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 885 | `caa1bbd9` | 2026-04-16T21:11:48.090836+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12632.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 886 | `e1f2e1e7` | 2026-04-16T21:11:48.103836+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12644.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 887 | `edf1a349` | 2026-04-16T21:11:48.170836+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12712.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 888 | `b056fe42` | 2026-04-16T21:11:48.203833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12744.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 889 | `7483c66a` | 2026-04-16T21:11:48.215834+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12756.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 890 | `7268bfd2` | 2026-04-16T21:11:48.230833+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12771.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 891 | `18ba7306` | 2026-04-16T21:11:48.243840+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12783.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 892 | `c2b66b57` | 2026-04-16T21:11:48.255346+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12795.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 893 | `73dea92b` | 2026-04-16T21:11:48.280349+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12821.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 894 | `e3f4da3e` | 2026-04-16T21:11:48.292347+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 12833.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 895 | `e374cc15` | 2026-04-16T21:11:48.680856+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 896 | `d9e77224` | 2026-04-16T21:11:48.922370+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 897 | `77a8bcc4` | 2026-04-16T21:11:49.178885+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 898 | `c217f2e8` | 2026-04-16T21:11:49.432388+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 899 | `6f2b7122` | 2026-04-16T21:11:49.673900+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 900 | `a3992f44` | 2026-04-16T21:11:49.922414+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 901 | `069b63da` | 2026-04-16T21:11:50.175929+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 902 | `2f31aba1` | 2026-04-16T21:11:50.422440+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 903 | `ddf7bba3` | 2026-04-16T21:11:50.664954+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 904 | `579682dc` | 2026-04-16T21:11:50.902465+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 905 | `b7d62d9f` | 2026-04-16T21:11:51.142975+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 906 | `c03ee12b` | 2026-04-16T21:11:51.389487+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 907 | `75eda017` | 2026-04-16T21:11:51.642003+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 908 | `74ca5e39` | 2026-04-16T21:11:51.892517+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 909 | `f1f358ba` | 2026-04-16T21:11:52.139034+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 910 | `24bbb682` | 2026-04-16T21:11:52.389543+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 911 | `5ac0df03` | 2026-04-16T21:11:52.638062+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 912 | `dc0b3416` | 2026-04-16T21:11:52.879577+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 913 | `348374a7` | 2026-04-16T21:11:53.122090+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 914 | `bf3fe161` | 2026-04-16T21:11:53.370603+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 915 | `897487b9` | 2026-04-16T21:11:53.609114+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 916 | `24bf2baf` | 2026-04-16T21:11:53.851630+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 917 | `7c583664` | 2026-04-16T21:11:54.091145+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 918 | `b366b174` | 2026-04-16T21:11:54.334655+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 919 | `a5c47169` | 2026-04-16T21:11:54.575166+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 920 | `4d56cc82` | 2026-04-16T21:11:54.815677+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 921 | `09180e9a` | 2026-04-16T21:11:55.069193+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 922 | `95bcf6d9` | 2026-04-16T21:11:55.310704+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 923 | `62dbd97c` | 2026-04-16T21:11:55.555216+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 924 | `5dfa0e5f` | 2026-04-16T21:11:55.794723+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 925 | `4eed9c66` | 2026-04-16T21:11:56.035233+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 926 | `c53320ec` | 2026-04-16T21:11:56.275746+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 927 | `50991f22` | 2026-04-16T21:11:56.517261+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 928 | `9d9bf600` | 2026-04-16T21:11:56.760263+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 929 | `32e86ca0` | 2026-04-16T21:11:57.001773+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 930 | `da6aae78` | 2026-04-16T21:11:57.255298+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 931 | `4f976744` | 2026-04-16T21:11:57.515813+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 932 | `3d63942d` | 2026-04-16T21:11:57.777835+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 933 | `19ec4b28` | 2026-04-16T21:11:58.047361+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 934 | `296bebd2` | 2026-04-16T21:11:58.317872+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 935 | `44127b8e` | 2026-04-16T21:11:58.577380+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 936 | `42308640` | 2026-04-16T21:11:58.833890+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 937 | `fa7c7e16` | 2026-04-16T21:11:59.074399+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 938 | `4db1bbbb` | 2026-04-16T21:11:59.451923+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 939 | `d2e055f7` | 2026-04-16T21:11:59.700435+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 940 | `47238809` | 2026-04-16T21:11:59.945948+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 941 | `732a56eb` | 2026-04-16T21:11:59.958946+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11599.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 942 | `a212f075` | 2026-04-16T21:11:59.970945+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11620.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 943 | `e8e112dc` | 2026-04-16T21:11:59.984947+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11633.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 944 | `bccbbf75` | 2026-04-16T21:11:59.997947+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11646.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 945 | `cdf0a899` | 2026-04-16T21:12:00.009945+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11658.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 946 | `0c791798` | 2026-04-16T21:12:00.029949+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11678.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 947 | `629a42f0` | 2026-04-16T21:12:00.046957+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11687.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 948 | `b61f927b` | 2026-04-16T21:12:00.063472+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11704.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 949 | `8303ef7c` | 2026-04-16T21:12:00.083468+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11722.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 950 | `dd56eeff` | 2026-04-16T21:12:00.099469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11738.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 951 | `a9e87c91` | 2026-04-16T21:12:00.111469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11749.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 952 | `a68fd94c` | 2026-04-16T21:12:00.123470+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11761.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 953 | `9007a009` | 2026-04-16T21:12:00.135469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11772.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 954 | `bd43b905` | 2026-04-16T21:12:00.148469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11785.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 955 | `6d7e4e5c` | 2026-04-16T21:12:00.167472+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11805.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 956 | `54922f42` | 2026-04-16T21:12:00.183468+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11821.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 957 | `1821a94b` | 2026-04-16T21:12:00.197470+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11834.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 958 | `49d7ec69` | 2026-04-16T21:12:00.209468+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11847.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 959 | `13617e7b` | 2026-04-16T21:12:00.223469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11871.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 960 | `39a2fbdb` | 2026-04-16T21:12:00.235469+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11872.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 961 | `fd8e1624` | 2026-04-16T21:12:00.248474+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11885.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 962 | `dd042dc2` | 2026-04-16T21:12:00.260467+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11897.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 963 | `71633568` | 2026-04-16T21:12:00.273468+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11910.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 964 | `305629c8` | 2026-04-16T21:12:00.285468+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11921.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 965 | `75655425` | 2026-04-16T21:12:00.301473+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11937.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 966 | `7a74b821` | 2026-04-16T21:12:00.315983+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11956.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 967 | `3a3a2a83` | 2026-04-16T21:12:00.583499+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 968 | `9f317c34` | 2026-04-16T21:12:00.842012+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 969 | `0b33dbb5` | 2026-04-16T21:12:01.185533+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 970 | `b9301452` | 2026-04-16T21:12:01.452052+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 971 | `fe6de59a` | 2026-04-16T21:12:01.469053+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13081.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 972 | `51a7d28e` | 2026-04-16T21:12:01.481052+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13093.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 973 | `573ff82c` | 2026-04-16T21:12:01.493056+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13104.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 974 | `60a8998d` | 2026-04-16T21:12:01.505052+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13116.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 975 | `97b80ebe` | 2026-04-16T21:12:01.519053+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13130.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 976 | `a6e7e9a1` | 2026-04-16T21:12:01.534057+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13145.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 977 | `8919db13` | 2026-04-16T21:12:01.551058+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13162.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 978 | `949d310b` | 2026-04-16T21:12:01.562569+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13172.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 979 | `8ecec44d` | 2026-04-16T21:12:01.579570+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13188.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 980 | `e139f52f` | 2026-04-16T21:12:01.590566+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13200.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 981 | `223ccdcf` | 2026-04-16T21:12:01.603566+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13212.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 982 | `15bf94ed` | 2026-04-16T21:12:01.615569+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13225.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 983 | `6b87523d` | 2026-04-16T21:12:01.629566+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13227.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 984 | `5f6035d1` | 2026-04-16T21:12:01.645567+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13243.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 985 | `08b73683` | 2026-04-16T21:12:01.657567+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13250.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 986 | `dfa61a3e` | 2026-04-16T21:12:01.670568+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13263.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 987 | `6815cfab` | 2026-04-16T21:12:01.681565+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13274.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 988 | `a79c4a2d` | 2026-04-16T21:12:01.692566+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13286.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 989 | `d86700ec` | 2026-04-16T21:12:01.704566+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13297.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 990 | `692079ea` | 2026-04-16T21:12:01.715570+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13309.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 991 | `2d506f74` | 2026-04-16T21:12:01.746569+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13339.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 992 | `4c4f551f` | 2026-04-16T21:12:01.761568+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13352.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 993 | `e414db5b` | 2026-04-16T21:12:01.778570+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13371.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 994 | `eebc88a0` | 2026-04-16T21:12:01.793571+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 13384.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 995 | `f1533030` | 2026-04-16T21:12:03.453184+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 996 | `f330ad82` | 2026-04-16T21:12:03.713693+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 997 | `bdaddb30` | 2026-04-16T21:12:03.967210+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 998 | `97c80615` | 2026-04-16T21:12:04.216723+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 999 | `377b44a3` | 2026-04-16T21:12:04.462234+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1000 | `ea33880d` | 2026-04-16T21:12:04.706743+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1001 | `6431dd7c` | 2026-04-16T21:12:04.721744+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 1582.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1002 | `225b0a93` | 2026-04-16T21:12:04.964252+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1003 | `5ba10068` | 2026-04-16T21:12:05.205764+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1004 | `74fb3f26` | 2026-04-16T21:12:05.445275+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1005 | `15d276b2` | 2026-04-16T21:12:05.689784+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1006 | `cd27de81` | 2026-04-16T21:12:05.931299+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1007 | `e4e88b16` | 2026-04-16T21:12:06.176809+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1008 | `3333fe00` | 2026-04-16T21:12:06.198813+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 3054.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1009 | `1a2d65be` | 2026-04-16T21:12:06.440319+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1010 | `835db494` | 2026-04-16T21:12:06.683833+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1011 | `00e883c8` | 2026-04-16T21:12:06.923342+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1012 | `246fdf70` | 2026-04-16T21:12:07.168852+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1013 | `b0623cb9` | 2026-04-16T21:12:07.411367+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1014 | `d8f3dd9b` | 2026-04-16T21:12:07.422370+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4275.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1015 | `a07901eb` | 2026-04-16T21:12:07.442372+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4282.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1016 | `934d410b` | 2026-04-16T21:12:07.456367+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4309.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1017 | `745ffa27` | 2026-04-16T21:12:07.470370+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4310.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1018 | `6cd84bd2` | 2026-04-16T21:12:07.487371+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4327.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1019 | `6a0f3750` | 2026-04-16T21:12:07.500369+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4322.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1020 | `59814d3b` | 2026-04-16T21:12:07.515368+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4337.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1021 | `f5931224` | 2026-04-16T21:12:07.527368+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4349.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1022 | `1a25becc` | 2026-04-16T21:12:07.541367+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4362.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1023 | `bab5daed` | 2026-04-16T21:12:07.553367+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4375.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1024 | `05ec7e90` | 2026-04-16T21:12:07.569377+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4387.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1025 | `3563bc35` | 2026-04-16T21:12:07.581888+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4400.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1026 | `d61a3442` | 2026-04-16T21:12:07.593883+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4413.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1027 | `20eda2d0` | 2026-04-16T21:12:07.607882+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4426.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1028 | `37d3ebb1` | 2026-04-16T21:12:07.623886+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 4442.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1029 | `5191d382` | 2026-04-16T21:12:07.877397+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1030 | `eac39794` | 2026-04-16T21:12:08.124922+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1031 | `ce9e7eaa` | 2026-04-16T21:12:08.374435+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1032 | `8d32842b` | 2026-04-16T21:12:08.617945+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1033 | `90db6a41` | 2026-04-16T21:12:08.857452+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1034 | `3497b1a8` | 2026-04-16T21:12:09.100966+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1035 | `b4d9a43a` | 2026-04-16T21:12:09.359482+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1036 | `44556dd4` | 2026-04-16T21:12:09.604994+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1037 | `f82e8823` | 2026-04-16T21:12:09.847504+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1038 | `b7beb4ad` | 2026-04-16T21:12:09.965507+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6747.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1039 | `768c6a0c` | 2026-04-16T21:12:09.980504+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6762.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1040 | `c69309aa` | 2026-04-16T21:12:09.995507+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6777.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1041 | `06fe5546` | 2026-04-16T21:12:10.012506+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6793.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1042 | `039c6434` | 2026-04-16T21:12:10.022504+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6804.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1043 | `ae8c76c2` | 2026-04-16T21:12:10.040509+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6822.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1044 | `41dc22ee` | 2026-04-16T21:12:10.058510+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6591.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1045 | `21cc08ee` | 2026-04-16T21:12:10.069508+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6602.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1046 | `07dab5e8` | 2026-04-16T21:12:10.079508+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 6613.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1047 | `2e6a40d9` | 2026-04-16T21:12:10.326021+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1048 | `b10f156c` | 2026-04-16T21:12:10.568533+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1049 | `3668824a` | 2026-04-16T21:12:10.920577+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1050 | `caeb0e34` | 2026-04-16T21:12:11.182098+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1051 | `5e4ec335` | 2026-04-16T21:12:11.432614+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1052 | `1c3be843` | 2026-04-16T21:12:11.677124+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1053 | `f7420b3d` | 2026-04-16T21:12:11.925640+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1054 | `c96e18ac` | 2026-04-16T21:12:12.176147+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1055 | `17ba8c3e` | 2026-04-16T21:12:12.490668+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1056 | `b889fc39` | 2026-04-16T21:12:12.829187+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1057 | `eda93878` | 2026-04-16T21:12:13.073699+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1058 | `245db089` | 2026-04-16T21:12:13.321214+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1059 | `cec4e24c` | 2026-04-16T21:12:13.572728+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1060 | `48b25818` | 2026-04-16T21:12:13.822240+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1061 | `28d7b81d` | 2026-04-16T21:12:14.068758+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1062 | `4fe9c376` | 2026-04-16T21:12:14.314272+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1063 | `74476b95` | 2026-04-16T21:12:14.558786+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1064 | `86e1df8c` | 2026-04-16T21:12:14.801299+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1065 | `05ecfde0` | 2026-04-16T21:12:15.039809+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1066 | `363b63f6` | 2026-04-16T21:12:15.295322+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1067 | `0dad89d7` | 2026-04-16T21:12:15.533827+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1068 | `fe0c5887` | 2026-04-16T21:12:15.772338+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1069 | `28c86f55` | 2026-04-16T21:12:16.021847+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1070 | `2ecb531f` | 2026-04-16T21:12:16.264359+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1071 | `db05c28e` | 2026-04-16T21:12:16.323361+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10133.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1072 | `e8de77e3` | 2026-04-16T21:12:16.334363+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10144.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1073 | `80483fe3` | 2026-04-16T21:12:16.346366+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10156.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1074 | `cb70d53b` | 2026-04-16T21:12:16.357873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10167.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1075 | `ae9c55ee` | 2026-04-16T21:12:16.369875+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10179.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1076 | `9a03cf9a` | 2026-04-16T21:12:16.380875+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10190.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1077 | `8ab1bb3e` | 2026-04-16T21:12:16.391873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10200.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1078 | `29bd4d30` | 2026-04-16T21:12:16.402873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10212.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1079 | `cafcd5d9` | 2026-04-16T21:12:16.413873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10223.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1080 | `99aa58d8` | 2026-04-16T21:12:16.424873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10234.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1081 | `95d7d0c0` | 2026-04-16T21:12:16.435873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10246.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1082 | `8f9c586e` | 2026-04-16T21:12:16.452874+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10255.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1083 | `aad229b0` | 2026-04-16T21:12:16.463875+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10267.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1084 | `5ccbd383` | 2026-04-16T21:12:16.476876+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10279.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1085 | `182546c8` | 2026-04-16T21:12:16.488874+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10291.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1086 | `9940122f` | 2026-04-16T21:12:16.500873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10303.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1087 | `4e0f3e91` | 2026-04-16T21:12:16.512876+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10315.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1088 | `a99a8241` | 2026-04-16T21:12:16.523873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10326.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1089 | `509381a5` | 2026-04-16T21:12:16.536875+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10339.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1090 | `2fbdcfbf` | 2026-04-16T21:12:16.548874+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10350.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1091 | `9940bb79` | 2026-04-16T21:12:16.562876+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10364.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1092 | `33739920` | 2026-04-16T21:12:16.575873+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10377.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1093 | `fdc093ec` | 2026-04-16T21:12:16.589878+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10391.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1094 | `d60d68b7` | 2026-04-16T21:12:16.603389+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10405.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1095 | `21db8157` | 2026-04-16T21:12:16.867896+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1096 | `6da045b4` | 2026-04-16T21:12:17.135405+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1097 | `337c7c9f` | 2026-04-16T21:12:17.399914+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1098 | `51944533` | 2026-04-16T21:12:17.653426+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1099 | `4fe56053` | 2026-04-16T21:12:17.892934+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1100 | `77216565` | 2026-04-16T21:12:18.140446+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1101 | `51286b59` | 2026-04-16T21:12:18.386955+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1102 | `c990ad59` | 2026-04-16T21:12:18.398956+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 9283.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1103 | `6efe8e4f` | 2026-04-16T21:12:18.647473+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1104 | `617c0520` | 2026-04-16T21:12:18.886980+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1105 | `b0909240` | 2026-04-16T21:12:19.134494+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1106 | `340d9c2e` | 2026-04-16T21:12:19.428004+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1107 | `95c0a040` | 2026-04-16T21:12:19.671520+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1108 | `42baec6c` | 2026-04-16T21:12:19.692521+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 9826.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1109 | `e9fd32ad` | 2026-04-16T21:12:19.938026+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1110 | `b145831c` | 2026-04-16T21:12:20.199542+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1111 | `83f8ea1a` | 2026-04-16T21:12:20.537060+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1112 | `52ac0a97` | 2026-04-16T21:12:20.779582+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1113 | `45d42e23` | 2026-04-16T21:12:21.046098+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1114 | `0e446bb3` | 2026-04-16T21:12:21.081099+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11208.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1115 | `dc73784a` | 2026-04-16T21:12:21.115107+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11160.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1116 | `2a831e07` | 2026-04-16T21:12:21.127106+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11171.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1117 | `1f07cb94` | 2026-04-16T21:12:21.149623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11190.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1118 | `e770183c` | 2026-04-16T21:12:21.166623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11126.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1119 | `cea15404` | 2026-04-16T21:12:21.183623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11128.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1120 | `f3b450be` | 2026-04-16T21:12:21.202625+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11147.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1121 | `3fe3aae5` | 2026-04-16T21:12:21.218629+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11160.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1122 | `aa8be82e` | 2026-04-16T21:12:21.231622+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11173.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1123 | `19bc57c0` | 2026-04-16T21:12:21.248623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11190.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1124 | `e3091fe1` | 2026-04-16T21:12:21.272625+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11176.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1125 | `f9202bcb` | 2026-04-16T21:12:21.286622+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11189.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1126 | `9d038e7e` | 2026-04-16T21:12:21.299628+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11202.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1127 | `b436810e` | 2026-04-16T21:12:21.318626+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11221.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1128 | `e9145081` | 2026-04-16T21:12:21.343625+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11246.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1129 | `521424eb` | 2026-04-16T21:12:21.644664+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1130 | `fe599177` | 2026-04-16T21:12:21.896181+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1131 | `b4efdf1a` | 2026-04-16T21:12:22.157695+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1132 | `f5a61fe3` | 2026-04-16T21:12:22.409202+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1133 | `8ae4a988` | 2026-04-16T21:12:22.658709+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1134 | `d975a63b` | 2026-04-16T21:12:22.913231+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1135 | `93f54df5` | 2026-04-16T21:12:23.176738+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1136 | `74265cbb` | 2026-04-16T21:12:23.439248+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1137 | `1ee628cd` | 2026-04-16T21:12:23.738766+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1138 | `fce1102b` | 2026-04-16T21:12:23.780771+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7156.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1139 | `26489614` | 2026-04-16T21:12:23.796772+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7172.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1140 | `b1d7e521` | 2026-04-16T21:12:23.817774+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7192.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1141 | `5c0fb6fc` | 2026-04-16T21:12:23.841766+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7216.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1142 | `05eb5ec9` | 2026-04-16T21:12:23.865773+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7240.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1143 | `87e9190e` | 2026-04-16T21:12:23.886280+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7258.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1144 | `f8161836` | 2026-04-16T21:12:23.907289+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7276.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1145 | `7c2a1607` | 2026-04-16T21:12:23.921287+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7290.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1146 | `0a3b4de7` | 2026-04-16T21:12:23.938291+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7306.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1147 | `0763cae2` | 2026-04-16T21:12:24.353804+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1148 | `da1aa575` | 2026-04-16T21:12:24.597315+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1149 | `6d944b9b` | 2026-04-16T21:12:24.847823+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1150 | `beca1228` | 2026-04-16T21:12:25.097333+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1151 | `d592bfa5` | 2026-04-16T21:12:25.348852+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1152 | `26e8dded` | 2026-04-16T21:12:25.610360+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1153 | `294f30b9` | 2026-04-16T21:12:25.859880+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1154 | `caa2c577` | 2026-04-16T21:12:26.105387+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1155 | `e72e8ce9` | 2026-04-16T21:12:26.352898+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1156 | `38ac2020` | 2026-04-16T21:12:26.600413+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1157 | `3907c0ae` | 2026-04-16T21:12:26.846920+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1158 | `358e2fa5` | 2026-04-16T21:12:27.090429+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1159 | `79bd03d9` | 2026-04-16T21:12:27.371953+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1160 | `eabcb95a` | 2026-04-16T21:12:27.613464+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1161 | `785c0881` | 2026-04-16T21:12:27.856975+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1162 | `7f281ae5` | 2026-04-16T21:12:28.097485+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1163 | `cc94a0ab` | 2026-04-16T21:12:28.343995+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1164 | `2c1946f0` | 2026-04-16T21:12:28.588508+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1165 | `d85b0ae0` | 2026-04-16T21:12:28.835017+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1166 | `f550ceba` | 2026-04-16T21:12:29.083534+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1167 | `1b091f3d` | 2026-04-16T21:12:29.340040+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1168 | `31178d97` | 2026-04-16T21:12:29.590552+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1169 | `a46a9686` | 2026-04-16T21:12:29.844063+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1170 | `f62e461c` | 2026-04-16T21:12:30.087573+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1171 | `668d8f33` | 2026-04-16T21:12:30.154583+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10467.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1172 | `6dab31d6` | 2026-04-16T21:12:30.172098+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10484.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1173 | `06e77764` | 2026-04-16T21:12:30.185096+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10497.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1174 | `ac5d1711` | 2026-04-16T21:12:30.197097+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10508.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1175 | `be75280a` | 2026-04-16T21:12:30.208097+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10519.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1176 | `a556d3af` | 2026-04-16T21:12:30.219096+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10530.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1177 | `0725217d` | 2026-04-16T21:12:30.230097+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10541.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1178 | `cdf75749` | 2026-04-16T21:12:30.242096+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10553.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1179 | `519495d3` | 2026-04-16T21:12:30.255096+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10566.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1180 | `9d6406d2` | 2026-04-16T21:12:30.267097+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10578.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1181 | `52463769` | 2026-04-16T21:12:30.279100+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10590.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1182 | `cd0f7f67` | 2026-04-16T21:12:30.297104+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10605.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1183 | `83ea8f3e` | 2026-04-16T21:12:30.311097+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10619.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1184 | `73917b3b` | 2026-04-16T21:12:30.333098+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10641.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1185 | `c9b9d151` | 2026-04-16T21:12:30.353100+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10661.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1186 | `5670b2ff` | 2026-04-16T21:12:30.376099+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10684.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1187 | `e74a575d` | 2026-04-16T21:12:30.395101+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10702.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1188 | `75fd28e3` | 2026-04-16T21:12:30.412623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10720.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1189 | `a2e7ef2a` | 2026-04-16T21:12:30.431623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10739.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1190 | `17035c83` | 2026-04-16T21:12:30.507623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10814.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1191 | `311075ec` | 2026-04-16T21:12:30.535621+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10842.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1192 | `665cced8` | 2026-04-16T21:12:30.546621+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10854.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1193 | `27299d28` | 2026-04-16T21:12:30.558621+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10866.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1194 | `0e315c53` | 2026-04-16T21:12:30.572623+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10881.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1195 | `2156f54b` | 2026-04-16T21:12:30.841137+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1196 | `92bcca35` | 2026-04-16T21:12:31.130657+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1197 | `5b57cc27` | 2026-04-16T21:12:31.389182+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1198 | `a4aa3a94` | 2026-04-16T21:12:31.637700+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1199 | `58d56c86` | 2026-04-16T21:12:31.876213+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1200 | `b311e56c` | 2026-04-16T21:12:32.118722+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1201 | `ccef73b7` | 2026-04-16T21:12:32.362236+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1202 | `94dda083` | 2026-04-16T21:12:32.613745+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1203 | `ac9f4012` | 2026-04-16T21:12:32.627745+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 9698.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1204 | `c46b0bd8` | 2026-04-16T21:12:32.903257+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1205 | `7ded11a8` | 2026-04-16T21:12:33.157780+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1206 | `49f3cc40` | 2026-04-16T21:12:33.406292+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1207 | `87c98705` | 2026-04-16T21:12:33.649808+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1208 | `69fd6bda` | 2026-04-16T21:12:33.671322+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 9913.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1209 | `7dcd02ce` | 2026-04-16T21:12:33.925839+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1210 | `da7ac89a` | 2026-04-16T21:12:34.249357+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1211 | `7670b877` | 2026-04-16T21:12:34.501866+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1212 | `7a848b8c` | 2026-04-16T21:12:34.754381+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1213 | `43c69efb` | 2026-04-16T21:12:35.002898+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1214 | `e9171ac2` | 2026-04-16T21:12:35.018898+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11255.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1215 | `8c77cf41` | 2026-04-16T21:12:35.037897+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11265.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1216 | `2fe8a203` | 2026-04-16T21:12:35.049897+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11275.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1217 | `296617aa` | 2026-04-16T21:12:35.065899+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11289.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1218 | `9c80108c` | 2026-04-16T21:12:35.084898+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11222.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1219 | `114991a8` | 2026-04-16T21:12:35.102897+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11237.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1220 | `a97138fc` | 2026-04-16T21:12:35.115898+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11214.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1221 | `b5ce7926` | 2026-04-16T21:12:35.128904+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11221.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1222 | `e4faaccf` | 2026-04-16T21:12:35.141896+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11235.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1223 | `e20b8a4d` | 2026-04-16T21:12:35.178423+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11271.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1224 | `700df390` | 2026-04-16T21:12:35.193422+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 8335.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1225 | `bfd38c16` | 2026-04-16T21:12:35.205420+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 8346.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1226 | `341ffcf7` | 2026-04-16T21:12:35.218419+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 8361.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1227 | `47d2f58e` | 2026-04-16T21:12:35.230422+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 8372.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1228 | `7a588f60` | 2026-04-16T21:12:35.240419+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 8383.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1229 | `b7a1f74c` | 2026-04-16T21:12:35.503933+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1230 | `8afc2ae0` | 2026-04-16T21:12:35.743442+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1231 | `482bb788` | 2026-04-16T21:12:36.036957+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1232 | `cfb9cfa2` | 2026-04-16T21:12:36.280467+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1233 | `6cb3f208` | 2026-04-16T21:12:36.546980+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1234 | `c16cea6c` | 2026-04-16T21:12:37.003031+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1235 | `4be74a24` | 2026-04-16T21:12:37.260542+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1236 | `e463fa77` | 2026-04-16T21:12:37.508058+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1237 | `a8962fd6` | 2026-04-16T21:12:37.755580+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1238 | `f92b0b51` | 2026-04-16T21:12:37.811583+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7214.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1239 | `88b31690` | 2026-04-16T21:12:37.832581+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7234.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1240 | `b46a725e` | 2026-04-16T21:12:37.845581+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7247.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1241 | `7ced05ee` | 2026-04-16T21:12:37.863582+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7265.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1242 | `ce17968e` | 2026-04-16T21:12:37.889582+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7288.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1243 | `bbdb50a2` | 2026-04-16T21:12:37.905580+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7303.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1244 | `757dd170` | 2026-04-16T21:12:37.919589+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7311.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1245 | `8c5a4366` | 2026-04-16T21:12:37.931101+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7323.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1246 | `15467437` | 2026-04-16T21:12:37.942100+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 7334.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1247 | `9286b662` | 2026-04-16T21:12:38.320631+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1248 | `9e2bb1b5` | 2026-04-16T21:12:38.580154+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1249 | `fd858d97` | 2026-04-16T21:12:38.829661+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1250 | `6d9a7233` | 2026-04-16T21:12:39.074169+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1251 | `0384cc52` | 2026-04-16T21:12:39.327694+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1252 | `b489dc26` | 2026-04-16T21:12:39.750736+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1253 | `91fb81c5` | 2026-04-16T21:12:40.006251+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1254 | `547c4453` | 2026-04-16T21:12:40.272764+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1255 | `ff4c6d4b` | 2026-04-16T21:12:40.534281+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1256 | `0f90dbfb` | 2026-04-16T21:12:40.793791+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1257 | `1b22552f` | 2026-04-16T21:12:41.045306+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1258 | `0b36d6ba` | 2026-04-16T21:12:41.308817+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1259 | `36790948` | 2026-04-16T21:12:41.649334+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1260 | `8ddfaa75` | 2026-04-16T21:12:41.903845+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1261 | `0b46a426` | 2026-04-16T21:12:42.162368+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1262 | `0b14cd9d` | 2026-04-16T21:12:42.418881+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1263 | `36fd3b16` | 2026-04-16T21:12:42.671394+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1264 | `ac9b9f90` | 2026-04-16T21:12:42.915905+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1265 | `f1b879e1` | 2026-04-16T21:12:43.170415+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1266 | `586e6b5f` | 2026-04-16T21:12:43.414926+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1267 | `ff3e2652` | 2026-04-16T21:12:43.662439+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1268 | `002395cd` | 2026-04-16T21:12:43.901947+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1269 | `8bf08ab2` | 2026-04-16T21:12:44.146460+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1270 | `e6d3204d` | 2026-04-16T21:12:44.390968+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1271 | `091ea14d` | 2026-04-16T21:12:44.423969+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10757.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1272 | `9c812942` | 2026-04-16T21:12:44.438975+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10772.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1273 | `efc49364` | 2026-04-16T21:12:44.452491+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10785.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1274 | `08b8b01d` | 2026-04-16T21:12:44.465485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10798.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1275 | `ce3d0f69` | 2026-04-16T21:12:44.482485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10815.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1276 | `9fada409` | 2026-04-16T21:12:44.497484+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10830.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1277 | `51ce7149` | 2026-04-16T21:12:44.512485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10844.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1278 | `bafc1e5e` | 2026-04-16T21:12:44.524483+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10856.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1279 | `4d4a9636` | 2026-04-16T21:12:44.535483+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10866.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1280 | `e1ed74a9` | 2026-04-16T21:12:44.549483+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10882.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1281 | `7ca3daaf` | 2026-04-16T21:12:44.561489+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10894.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1282 | `7c270b84` | 2026-04-16T21:12:44.573484+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10904.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1283 | `e16d6d44` | 2026-04-16T21:12:44.585485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10915.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1284 | `d152345f` | 2026-04-16T21:12:44.596483+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10926.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1285 | `0d9a10d3` | 2026-04-16T21:12:44.613485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10943.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1286 | `f6ba196c` | 2026-04-16T21:12:44.628485+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10958.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1287 | `97d13584` | 2026-04-16T21:12:44.640484+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10970.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1288 | `1f558fd6` | 2026-04-16T21:12:44.658483+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10988.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1289 | `0cd1b594` | 2026-04-16T21:12:44.672487+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11002.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1290 | `5db9684b` | 2026-04-16T21:12:44.684491+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11014.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1291 | `9795387c` | 2026-04-16T21:12:44.697005+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11026.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1292 | `ea521c50` | 2026-04-16T21:12:44.715005+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11044.0ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1293 | `31972f6f` | 2026-04-16T21:12:44.732006+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11060.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1294 | `23b2fae3` | 2026-04-16T21:12:44.743003+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11071.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1295 | `de479a7e` | 2026-04-16T21:12:45.032531+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1296 | `c62acdb1` | 2026-04-16T21:12:45.298058+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1297 | `833f185d` | 2026-04-16T21:12:45.644578+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1298 | `d9d0617b` | 2026-04-16T21:12:45.938093+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1299 | `f864e7de` | 2026-04-16T21:12:46.215124+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1300 | `94894fe7` | 2026-04-16T21:12:46.465633+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1301 | `1bfa22d8` | 2026-04-16T21:12:46.478635+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 9460.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1302 | `f56c6e8f` | 2026-04-16T21:12:46.729151+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1303 | `1bf97f37` | 2026-04-16T21:12:46.997663+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1304 | `495c17c2` | 2026-04-16T21:12:47.263172+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1305 | `19c3d64b` | 2026-04-16T21:12:47.614679+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1306 | `03bed6d3` | 2026-04-16T21:12:47.886198+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1307 | `bbd7bb57` | 2026-04-16T21:12:48.135706+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1308 | `4b4cda2e` | 2026-04-16T21:12:48.147706+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10373.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1309 | `f40f76e9` | 2026-04-16T21:12:48.402219+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1310 | `ab548cf0` | 2026-04-16T21:12:48.653727+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1311 | `59e582de` | 2026-04-16T21:12:48.666730+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 10875.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1312 | `c64c6228` | 2026-04-16T21:12:48.910236+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1313 | `63853ae0` | 2026-04-16T21:12:49.153749+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1314 | `9c82d0fb` | 2026-04-16T21:12:49.410259+00:00 | `auth.login_success` | stress_bbf9db | auth | eyJhbGci | — | success | — | {"ip": "127.0.0.1"} |
| 1315 | `406283b0` | 2026-04-16T21:12:49.425262+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11624.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1316 | `cd52b1d4` | 2026-04-16T21:12:49.436262+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11633.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1317 | `82016876` | 2026-04-16T21:12:49.456265+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4686.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1318 | `0b6cec19` | 2026-04-16T21:12:49.468777+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4698.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1319 | `7b377139` | 2026-04-16T21:12:49.479776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4709.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1320 | `e0c84996` | 2026-04-16T21:12:49.496774+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4725.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1321 | `e21e0e1f` | 2026-04-16T21:12:49.507774+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11700.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1322 | `b91e4cd0` | 2026-04-16T21:12:49.521775+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4749.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1323 | `f88e7b20` | 2026-04-16T21:12:49.533776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4761.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1324 | `e0bb62b5` | 2026-04-16T21:12:49.552772+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11665.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1325 | `b4f40b2f` | 2026-04-16T21:12:49.573776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11686.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1326 | `ddb5e1d2` | 2026-04-16T21:12:49.587775+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11697.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1327 | `16b878af` | 2026-04-16T21:12:49.599777+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4824.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1328 | `bac83776` | 2026-04-16T21:12:49.611776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4836.6ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1329 | `cdb8e0aa` | 2026-04-16T21:12:49.621775+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 4846.5ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1330 | `230b8a1d` | 2026-04-16T21:12:49.637776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11718.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1331 | `d9b4eab0` | 2026-04-16T21:12:49.651773+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11732.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1332 | `29288d9e` | 2026-04-16T21:12:49.662775+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11743.8ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1333 | `e672fda8` | 2026-04-16T21:12:49.679776+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11710.9ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1334 | `bced00fa` | 2026-04-16T21:12:49.696782+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11727.4ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1335 | `6f17958c` | 2026-04-16T21:12:49.708782+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11739.3ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1336 | `361d814a` | 2026-04-16T21:12:49.720298+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11750.7ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1337 | `fb3a6ce2` | 2026-04-16T21:12:49.731295+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | success | 11762.1ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 200, "us |
| 1338 | `d8344d82` | 2026-04-16T21:12:49.752297+00:00 | `http.request` | 127.0.0.1 | /auth/token | — | — | failure | 2380.2ms | {"method": "POST", "path": "/auth/token", "query": null, "http_status": 400, "us |
| 1339 | `df9baa52` | 2026-04-16T21:12:55.804206+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | — | failure | 2.4ms | {"method": "GET", "path": "/admin/users/", "query": null, "http_status": 401, "u |
| 1340 | `c581b3cb` | 2026-04-16T21:12:55.834210+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | — | failure | 1.6ms | {"method": "GET", "path": "/admin/roles/", "query": null, "http_status": 401, "u |
| 1341 | `77f6ef96` | 2026-04-16T21:12:55.853719+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | — | failure | 1.9ms | {"method": "GET", "path": "/admin/groups/", "query": null, "http_status": 401, " |
| 1342 | `a5e45a40` | 2026-04-16T21:12:55.876717+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | — | failure | 1.7ms | {"method": "GET", "path": "/admin/permissions/", "query": null, "http_status": 4 |
| 1343 | `15737296` | 2026-04-16T21:12:55.900718+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | — | failure | 2.7ms | {"method": "GET", "path": "/admin/rbac/", "query": null, "http_status": 401, "us |
| 1344 | `5676ccf7` | 2026-04-16T21:12:55.919719+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | — | failure | 2.2ms | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 40 |
| 1345 | `6b37ac56` | 2026-04-16T21:12:55.939716+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | — | failure | 1.7ms | {"method": "GET", "path": "/admin/user-types/", "query": null, "http_status": 40 |
| 1346 | `e0b6e7c2` | 2026-04-16T21:12:55.968720+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | — | failure | 2.0ms | {"method": "GET", "path": "/admin/user-levels/", "query": null, "http_status": 4 |
| 1347 | `5c7b3ac8` | 2026-04-16T21:12:55.987717+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | — | failure | 2.1ms | {"method": "GET", "path": "/admin/custom-entities/types", "query": null, "http_s |
| 1348 | `d1796397` | 2026-04-16T21:13:04.138706+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | — | failure | 2.0ms | {"method": "GET", "path": "/admin/users/", "query": null, "http_status": 401, "u |
| 1349 | `7f7cdf18` | 2026-04-16T21:13:04.297707+00:00 | `http.request` | 127.0.0.1 | /admin/users/ | — | — | failure | 2.0ms | {"method": "GET", "path": "/admin/users/", "query": null, "http_status": 401, "u |
| 1350 | `83cdf3d2` | 2026-04-16T21:13:04.318704+00:00 | `http.request` | 127.0.0.1 | /admin/roles/ | — | — | failure | 1.7ms | {"method": "GET", "path": "/admin/roles/", "query": null, "http_status": 401, "u |
| 1351 | `a86ec191` | 2026-04-16T21:13:04.336705+00:00 | `http.request` | 127.0.0.1 | /admin/groups/ | — | — | failure | 1.7ms | {"method": "GET", "path": "/admin/groups/", "query": null, "http_status": 401, " |
| 1352 | `7e842dab` | 2026-04-16T21:13:04.358237+00:00 | `http.request` | 127.0.0.1 | /admin/permissions/ | — | — | failure | 1.9ms | {"method": "GET", "path": "/admin/permissions/", "query": null, "http_status": 4 |
| 1353 | `0d9f936d` | 2026-04-16T21:13:04.384238+00:00 | `http.request` | 127.0.0.1 | /admin/rbac/ | — | — | failure | 4.2ms | {"method": "GET", "path": "/admin/rbac/", "query": null, "http_status": 401, "us |
| 1354 | `898234cb` | 2026-04-16T21:13:04.406235+00:00 | `http.request` | 127.0.0.1 | /admin/audit/ | — | — | failure | 1.8ms | {"method": "GET", "path": "/admin/audit/", "query": "limit=5", "http_status": 40 |
| 1355 | `f63966d4` | 2026-04-16T21:13:04.424237+00:00 | `http.request` | 127.0.0.1 | /admin/user-types/ | — | — | failure | 1.6ms | {"method": "GET", "path": "/admin/user-types/", "query": null, "http_status": 40 |
| 1356 | `3b4a31bd` | 2026-04-16T21:13:04.445238+00:00 | `http.request` | 127.0.0.1 | /admin/user-levels/ | — | — | failure | 2.6ms | {"method": "GET", "path": "/admin/user-levels/", "query": null, "http_status": 4 |
| 1357 | `de94a7f2` | 2026-04-16T21:13:04.467235+00:00 | `http.request` | 127.0.0.1 | /admin/custom-entities/types | — | — | failure | 1.9ms | {"method": "GET", "path": "/admin/custom-entities/types", "query": null, "http_s |
| 1358 | `28f3ff0a` | 2026-04-17T22:34:43.305537+00:00 | `system.startup` | system | api | — | — | success | — | {"version": "1.0.0"} |
