DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS udetails;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS edetails;
DROP TABLE IF EXISTS cart;

CREATE TABLE user (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  userlevel INT NOT NULL DEFAULT 0
);

CREATE TABLE udetails (
  udetailid INTEGER PRIMARY KEY AUTOINCREMENT,
  duserid INTEGER NOT NULL,
  gift FLOAT(4, 2) NOT NULL DEFAULT 0,
  creditcard INTEGER DEFAULT NULL,
  dateregistered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (duserid) REFERENCES user (userid)
);

CREATE TABLE events (
  eventid INTEGER PRIMARY KEY AUTOINCREMENT,
  eventtitle TEXT NOT NULL,
  eventdate DATETIME NOT NULL,
  eventlevel TEXT NOT NULL,
  eventprice FLOAT(4, 2) NOT NULL,
  eventfeature INTEGER DEFAULT NULL,
  
  authorid INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (authorid) REFERENCES user (userid)
);

CREATE TABLE edetails (
  detailid INTEGER PRIMARY KEY AUTOINCREMENT,
  deventid INTEGER NOT NULL,
  eventdesc TEXT DEFAULT NULL,
  eventhero TEXT DEFAULT NULL,
  eventvideo TEXT DEFAULT NULL,
  eventtags TEXT DEFAULT NULL,
  eventstream TEXT DEFAULT NULL,
  FOREIGN KEY (deventid) REFERENCES events (eventid)
 );

CREATE TABLE cart (
  cartid INTEGER PRIMARY KEY AUTOINCREMENT,
  ceventid INTEGER NOT NULL,
  cuserid INTEGER NOT NULL,
  purchased INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (cuserid) REFERENCES user (userid),
  FOREIGN KEY (ceventid) REFERENCES event (eventid)
);
