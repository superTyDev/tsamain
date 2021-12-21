DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS details;
DROP TABLE IF EXISTS registrations;

CREATE TABLE user (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  userlevel INT NOT NULL DEFAULT 0
);

CREATE TABLE events (
  eventid INTEGER PRIMARY KEY AUTOINCREMENT,
  eventtitle TEXT NOT NULL,
  eventdate DATETIME NOT NULL,
  eventlevel TEXT NOT NULL,
  eventprice FLOAT(4, 2) NOT NULL,
  
  authorid INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (authorid) REFERENCES user (userid)
);

CREATE TABLE details (
  detailid INTEGER PRIMARY KEY AUTOINCREMENT,
  deventid INTEGER NOT NULL,
  eventdesc TEXT DEFAULT NULL,
  eventhero TEXT DEFAULT NULL,
  eventvideo TEXT DEFAULT NULL,
  eventstream TEXT DEFAULT NULL,
  FOREIGN KEY (deventid) REFERENCES events (eventid)
 );

CREATE TABLE registrations (
  reguser INTEGER,
  regevent INTEGER,
  regdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (reguser) REFERENCES user (userid),
  FOREIGN KEY (regevent) REFERENCES event (eventid)
);
