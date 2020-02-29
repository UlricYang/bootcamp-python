SELECT a.sid
FROM
    (SELECT sid,
            score
     FROM sc
     WHERE cid="01") a,

    (SELECT sid,
            score
     FROM sc
     WHERE cid="02") b
WHERE a.score>b.score
    AND a.sid=b.sid;

