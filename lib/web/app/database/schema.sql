DROP TABLE IF EXISTS analyzes;
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS vulns;
DROP TABLE IF EXISTS process;
DROP TABLE IF EXISTS information;

create table analyzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status text NOT NULL DEFAULT 'pending',
    name text NOT NULL,
    message text DEFAULT NULL
);

CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    analyze_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    hash_name TEXT NOT NULL,
    results_id INTEGER NOT NULL DEFAULT 0
);


create table results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    analyze_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    run_time TEXT DEFAULT NULL
);

create table vulns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    results_id INTEGER NOT NULL,
    vuln_name TEXT NOT NULL,
    vuln_num TEXT NOT NULL
);

create table process (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vulns_id INTEGER NOT NULL,
    process text NOT NULL,
    vuln_func TEXT DEFAULT NULL
);

create table information (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    message TEXT DEFAULT NULL
);

INSERT into information (name, message) values ('StackOverFlow', '有關該漏洞的詳細資訊，請參考：https://cwe.mitre.org/data/definitions/121.html');
INSERT into information (name, message) values ('FormatStringBug', '有關該漏洞的詳細資訊，請參考：https://cwe.mitre.org/data/definitions/134.html');
INSERT into information (name, message) values ('HeapOverFlow', '有關該漏洞的詳細資訊，請參考：https://cwe.mitre.org/data/definitions/122.html');
INSERT into information (name, message) values ('UseAfterFree', '有關該漏洞的詳細資訊，請參考：https://cwe.mitre.org/data/definitions/416.html');
INSERT into information (name, message) values ('DoubleFree', '有關該漏洞的詳細資訊，請參考：https://cwe.mitre.org/data/definitions/415.html');